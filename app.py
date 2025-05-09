import streamlit as st
import google.generativeai as genai
from datetime import datetime

# API Ayarları
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Tasarım Ayarları
st.set_page_config(
    page_title="DevHive - Programlama Asistanı",
    page_icon="??",
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
/* Ana stiller */
[data-testid="stAppViewContainer"] {
    background-color: #0a0a0a !important;
    color: #ffffff !important;
}
[data-testid="stHeader"] {
    background-color: #000000 !important;
    border-bottom: 1px solid #333333 !important;
}
[data-testid="stToolbar"] {
    color: white !important;
}
[data-testid="stChatMessage"] {
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    max-width: 80%;
    word-wrap: break-word;
}
[data-testid="stChatMessage"].user {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    margin-left: auto;
    border-bottom-right-radius: 2px;
    border: 1px solid #333333 !important;
}
[data-testid="stChatMessage"].assistant {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
    margin-right: auto;
    border-bottom-left-radius: 2px;
    border: 1px solid #333333 !important;
}
.stButton>button {
    background-color: #2a2a2a !important;
    color: white !important;
    border-radius: 8px !important;
    margin: 4px !important;
    border: 1px solid #444444 !important;
}
.stButton>button:hover {
    background-color: #333333 !important;
}
.stDownloadButton>button {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
    margin: 4px !important;
}
.footer {
    text-align: center;
    padding: 16px;
    color: #aaaaaa !important;
    font-size: 14px;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #0a0a0a !important;
    border-top: 1px solid #333333 !important;
}
.action-buttons {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin: 16px 0;
}
/* Ba?lık stilleri */
h1 {
    color: #4dabf7 !important;
}
h2, h3, h4, h5, h6 {
    color: #adb5bd !important;
}
/* Yazı giri? kutusu */
[data-testid="stChatInput"] {
    background: #1a1a1a !important;
    border: 1px solid #333333 !important;
    color: white !important;
}
/* Sidebar */
[data-testid="stSidebar"] {
    background: #121212 !important;
    border-right: 1px solid #333333 !important;
    display: flex;
    flex-direction: column;
}
.sidebar-footer {
    margin-top: auto;
    padding-top: 20px;
    border-top: 1px solid #333333;
}
/* Di?er metinler */
p, .stMarkdown, .caption {
    color: #e9ecef !important;
}
/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #1a1a1a;
}
::-webkit-scrollbar-thumb {
    background: #333333;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #444444;
}
/* Sa? üst menüyü gizle */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Ba?lık
st.title("DevHive")
st.caption("Profesyonel Programlama Asistanı")

# Sidebar
with st.sidebar:
    st.header(" </> ")
    
    # Sidebar içeri?i
    st.markdown("### Kullanım Kılavuzu")
    st.markdown("Sadece programlama ve kodlama ile ilgili sorular sorun.")
    
    # Sidebar footer (en alta yerle?tirildi)
    with st.container():
        st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
        st.markdown("**?��?��??Geli?tirici:** Meriç Yüzaklı")  
        st.markdown("**?�� İnstagram:** [benmericig](https://www.instagram.com/benmericig/)")
        st.markdown("**?��? Youtube:** [benmericyt](https://www.youtube.com/benmericyt)")
        st.markdown("**?�� İleti?im:** benmericinfo@gmail.com")
        st.markdown("**?? Versiyon:** 1.0.0")
        st.markdown("</div>", unsafe_allow_html=True)

# Sohbet Geçmi?i
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Programlama ile ilgili nasıl yardımcı olabilirim? ??"}]

# Mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"], unsafe_allow_html=True)

# Action Butonları
col1, col2 = st.columns(2)
with col1:
    if st.button("?? Yeni Sohbet", use_container_width=True, help="Sohbet geçmi?ini temizler"):
        st.session_state.clear()
        st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Programlama ile ilgili nasıl yardımcı olabilirim? ??"}]
        st.rerun()

with col2:
    if len(st.session_state.messages) > 1:
        chat_content = "\n\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        st.download_button(
            "?�� Sohbeti İndir",
            chat_content,
            file_name=f"devhive_sohbet_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            use_container_width=True,
            help="Sohbet geçmi?ini txt dosyası olarak indir"
        )

# Kullanıcı Giri?i ve Prompt Güncellemesi
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt, unsafe_allow_html=True)

    # Prompt'u Güncelleme
    previous_chat = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    final_prompt = f"""You are a programming teaching assistant named DevHive ( Developer Hive ), created by Meriç Yüzaklı an AI Specialist. Answer only the programming, error-fixing and code-related question that being asked. 
    Important note, If Question non-related to coding or programming means, you have to say: 'Please ask only coding-related questions.' except greeting and those kind of questions "who are you", "who created you".
    previous_chat:  
    {previous_chat}
    Human: {prompt}
    Chatbot:"""

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("?? Cevap olu?turuluyor..."):
            response = model.generate_content(final_prompt)
            st.markdown(response.text, unsafe_allow_html=True)
        
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# Footer
st.markdown("""
<div class="footer">
    <div>© 2025 DevHive - Tüm hakları saklıdır</div>
</div>
""", unsafe_allow_html=True)
