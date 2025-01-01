import streamlit as st
from repsponse_chatbot import get_response
from recommendation import get_recomendation


# ===============SETUP===============
st.set_page_config(
    page_title="Carbot",
    page_icon="🚗"
)
# st.markdown(hide_st_style, unsafe_allow_html=True)

# Inisialisasi variabel st.session_state.messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Pesan awal dari chatbot
if "tensibot_greeted" not in st.session_state:
    greeting_chat = "Ha, Carbot disini. ada yang bisa saya bantu?"
    st.session_state.messages.append({"role": "🚗" , "content": greeting_chat})
    st.session_state.tensibot_greeted = True

# Main App
st.title("CarBot-Sitem Rekomendasi Mobil Bekas")
st.write("---")
st.sidebar.success("Pilih Halaman Di Atas")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# ==================CHATBOT SYSTEM==========
# input pesan
if prompt := st.chat_input("Ketik pesan.."):
    # msg user
    with st.chat_message("user"):
        st.markdown(prompt)
    # add to history msg
    st.session_state.messages.append({"role": "user", "content": prompt})

    # msg chatbot
    with st.chat_message("🚗"):
        response = ""
        if "#rekomendasi" in prompt:
            response = get_recomendation(prompt)
        else:
            response = f"{get_response(prompt)}"
        st.markdown(response)
    st.session_state.messages.append({"role": "🚗", "content": response})