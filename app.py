import streamlit as st
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from datetime import datetime

# API Ayarları
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Sayfa Ayarları
st.set_page_config(
    page_title="DevHive - Programlama Asistanı",
    page_icon="🤖",
    layout="centered",
    menu_items={}
)

# Dil Ayarları
languages = {
    "Türkçe": {
        "title": "DevHive",
        "caption": "Profesyonel Programlama Asistanı",
        "guide_header": "Kullanım Kılavuzu",
        "guide_text": "Sadece programlama ve kodlama ile ilgili sorular sorun.",
        "new_chat": "🔄 Yeni Sohbet",
        "download_chat": "📥 Sohbeti İndir",
        "input_placeholder": "Mesajınızı yazın...",
        "download_help": "Sohbet geçmişini txt olarak indir",
        "initial_message": "Merhaba! Programlama ile ilgili nasıl yardımcı olabilirim? 😊",
        "generating": "🤖 Cevap oluşturuluyor...",
        "version": "Versiyon",
        "developer": "Geliştirici"
    },
    "English": {
        "title": "DevHive",
        "caption": "Professional Programming Assistant",
        "guide_header": "User Guide",
        "guide_text": "Only ask programming and coding related questions.",
        "new_chat": "🔄 New Chat",
        "download_chat": "📥 Download Chat",
        "input_placeholder": "Type your message...",
        "download_help": "Download chat history as a .txt file",
        "initial_message": "Hi there! How can I assist you with programming? 😊",
        "generating": "🤖 Generating response...",
        "version": "Version",
        "developer": "Developer"
    }
}

# Varsayılan dil ayarı
if "language" not in st.session_state:
    st.session_state.language = "Türkçe"
language = st.session_state.language
lang = languages[language]

# Sidebar - Dar bayrak butonları
with st.sidebar:
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)

    # Daha dar kolonlar: 0.48 oranı, arada küçük boşluk kalır
    col1, col2 = st.columns([0.48, 0.48])
    with col1:
        if st.button("🇹🇷", use_container_width=True):
            st.session_state.language = "Türkçe"
            st.rerun()
    with col2:
        if st.button("🇺🇸", use_container_width=True):
            st.session_state.language = "English"
            st.rerun()

    st.header(" </> ")
    st.markdown(f"### {lang['guide_header']}")
    st.markdown(lang['guide_text'])

    st.markdown(f"""
    <div class="sidebar-footer">
        📸 <a href="https://www.instagram.com/benmericig/" target="_blank">Instagram</a><br>
        ▶️ <a href="https://www.youtube.com/benmericyt" target="_blank">YouTube</a><br>
        😺 <a href="https://github.com/benmeric" target="_blank">GitHub</a><br>
        👤 <strong>{lang['developer']}:</strong> Meriç Yüzaklı<br>
        📧 benmericinfo@gmail.com<br>
        🔄 {lang['version']}: 1.0.0
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# CSS
st.markdown("""
<style>
body, [data-testid="stAppViewContainer"] {
    background-color: #0a0a0a;
    color: white;
}
.sidebar-container {
    display: flex;
    flex-direction: column;
    height: 100%;
}
.sidebar-footer {
    margin-top: auto;
    font-size: 13px;
    color: #aaa;
    padding-top: 10px;
    border-top: 1px solid #333;
}
.sidebar-footer a {
    color: #1f77b4;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# Başlık ve Açıklama
st.title(lang["title"])
st.caption(lang["caption"])

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": lang["initial_message"]}]

# Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"], unsafe_allow_html=True)

# Butonlar
col1, col2 = st.columns(2)
with col1:
    if st.button(lang["new_chat"], use_container_width=True):
        st.session_state.clear()
        st.session_state.language = language  # Dil değişmesin diye tekrar ayarla
        st.session_state.messages = [{"role": "assistant", "content": lang["initial_message"]}]
        st.rerun()

with col2:
    if len(st.session_state.messages) > 1:
        chat_content = "\n\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        st.download_button(
            label=lang["download_chat"],
            data=chat_content,
            file_name=f"devhive_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            help=lang["download_help"],
            use_container_width=True
        )

# Kullanıcı Mesajı
if prompt := st.chat_input(lang["input_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt, unsafe_allow_html=True)

    previous_chat = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

    if language == "English":
        final_prompt = f"""You are a programming teaching assistant named DevHive (Developer Hive), created by Meriç Yüzaklı.
Only answer programming and code-related questions.
previous_chat:
{previous_chat}
Human: {prompt}
Chatbot:"""
    else:
        final_prompt = f"""Sen Meriç Yüzaklı tarafından geliştirilmiş bir programlama öğretmenisin. Adın DevHive (Developer Hive).
Sadece programlama ve kodlama ile ilgili sorulara cevap ver.
Önceki sohbet:
{previous_chat}
İnsan: {prompt}
Asistan:"""

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner(lang["generating"]):
            response = model.generate_content(
                final_prompt,
                generation_config=GenerationConfig(
                    max_output_tokens=4096,
                    temperature=0.7
                )
            )
            st.markdown(response.text, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
