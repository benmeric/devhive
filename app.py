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
body, [data-testid="stAppViewContainer"] {
    background-color: #0a0a0a;
    color: white;
}
.sidebar-footer {
    position: absolute;
    bottom: 20px;
    font-size: 13px;
    color: #aaa;
}
.sidebar-footer a {
    color: #1f77b4;
    text-decoration: none;
}
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
    
    # Footer (sidebar en alt)
    st.markdown("""
    <div class="sidebar-footer">
        <strong>Geliştirici:</strong> Meriç Yüzaklı<br>
        📸 <a href="https://www.instagram.com/benmericig/" target="_blank">Instagram</a><br>
        ▶️ <a href="https://www.youtube.com/benmericyt" target="_blank">YouTube</a><br>
        📧 benmericinfo@gmail.com<br>
        🔄 Versiyon: 1.0.0
    </div>
    """, unsafe_allow_html=True)

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Programlama ile ilgili nasıl yardımcı olabilirim? 😊"}]

# Mesajları Göster
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

    previous_chat = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    final_prompt = f"""You are a programming teaching assistant named DevHive (Developer Hive), created by Meriç Yüzaklı.
Answer only programming and code-related questions.
previous_chat:
{previous_chat}
Human: {prompt}
Chatbot:"""

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
