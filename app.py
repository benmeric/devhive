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
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# CSS Stilleri
st.markdown("""
<style>
/* Uygulama arka plan ve yazı rengi */
body, [data-testid="stAppViewContainer"] {
    background-color: #0a0a0a;
    color: white;
}
/* Chat mesajları */
[data-testid="stChatMessage"].user {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    margin-left: auto;
    border: 1px solid #333333 !important;
    padding: 12px 16px;
    border-radius: 8px;
}
[data-testid="stChatMessage"].assistant {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
    margin-right: auto;
    border: 1px solid #333333 !important;
    padding: 12px 16px;
    border-radius: 8px;
}
/* Butonlar */
.stButton>button {
    background-color: #2a2a2a !important;
    color: white !important;
    border: 1px solid #444444 !important;
    border-radius: 8px !important;
}
.stButton>button:hover {
    background-color: #333333 !important;
}
/* Download butonu */
.stDownloadButton>button {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
}
/* Sidebar */
[data-testid="stSidebar"] {
    background: #121212 !important;
    border-right: 1px solid #333333 !important;
}
/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #333333;
    border-radius: 4px;
}
/* Footer sola sabit */
.footer {
    text-align: left;
    padding: 16px;
    color: #aaaaaa !important;
    font-size: 14px;
    position: fixed;
    bottom: 0;
    left: 0;
    background: #0a0a0a !important;
    border-top: 1px solid #333333 !important;
    width: 100%;
}
#MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Başlık
st.title("DevHive")
st.caption("Profesyonel Programlama Asistanı")

# Sidebar
with st.sidebar:
    st.header(" </> ")
    st.markdown("### Kullanım Kılavuzu")
    st.markdown("Sadece programlama ve kodlama ile ilgili sorular sorun.")
    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    st.markdown("**Geliştirici:** Meriç Yüzaklı")
    st.markdown("**📸 İnstagram:** [benmericig](https://www.instagram.com/benmericig/)")
    st.markdown("**▶️ Youtube:** [benmericyt](https://www.youtube.com/benmericyt)")
    st.markdown("**📧 İletişim:** benmericinfo@gmail.com")
    st.markdown("**🔄 Versiyon:** 1.0.0")
    st.markdown("</div>", unsafe_allow_html=True)

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Programlama ile ilgili nasıl yardımcı olabilirim? 😊"}]

# Mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"], unsafe_allow_html=True)

# Action Butonları
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Yeni Sohbet", use_container_width=True, help="Sohbet geçmişini temizler"):
        st.session_state.clear()
        st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Programlama ile ilgili nasıl yardımcı olabilirim? 😊"}]
        st.rerun()

with col2:
    if len(st.session_state.messages) > 1:
        chat_content = "\n\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        st.download_button(
            "📥 Sohbeti İndir",
            chat_content,
            file_name=f"devhive_sohbet_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            use_container_width=True,
            help="Sohbet geçmişini txt olarak indir"
        )

# Kullanıcı Girişi
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt, unsafe_allow_html=True)

    # Prompt'u oluştur
    previous_chat = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    final_prompt = f"""You are a programming teaching assistant named DevHive (Developer Hive), created by Meriç Yüzaklı.
Answer only programming and code-related questions.
previous_chat:
{previous_chat}
Human: {prompt}
Chatbot:"""

    # Gemini yanıtı al
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤖 Cevap oluşturuluyor..."):
            response = model.generate_content(
                final_prompt,
                generation_config=GenerationConfig(
                    max_output_tokens=4096,
                    temperature=0.7
                )
            )
            st.markdown(response.text, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response.text})

# Footer - SOL ALTA SABİTLENMİŞ
st.markdown("""
<div class="footer">
    <div>© 2025 DevHive - Tüm hakları saklıdır</div>
</div>
""", unsafe_allow_html=True)
