import streamlit as st
import requests

# ناوی سایتەکە
st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# بانگکردنی کلیلە نوێیەکە
if "HF_TOKEN" not in st.secrets:
    st.error("⚠️ مامە گیان، کلیلە نوێیەکە لە Secrets نییە!")
    st.stop()

token = st.secrets["HF_TOKEN"]
# بەکارهێنانی مۆدێلی Mistral کە زۆر خێرا و باشە
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {token}"}

# سیستەمی چات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("لێرە پرسیار بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # ناردنی پرسیار بۆ Hugging Face
        res = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        if res.status_code == 200:
            # وەرگرتنی وەڵام بەبێ تێکچوون
            output = res.json()[0]['generated_text'].split(prompt)[-1].strip()
            st.write(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
        else:
            st.error("⚠️ سێرڤەر وەڵامی نەبوو، کەمێکی تر تاقی بکەرەوە.")
