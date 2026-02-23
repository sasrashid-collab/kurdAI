import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# مامە گیان، کلیلەکەم ڕاستەوخۆ لێرە بۆ داناویت تا ئێرۆر نەمێنێت
token = "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"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {token}"}

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
        with st.spinner("خەریکە بیر دەکاتەوە..."):
            res = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            if res.status_code == 200:
                output = res.json()[0]['generated_text'].replace(prompt, "").strip()
                st.write(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
            else:
                st.error("سێرڤەر وەڵامی نەبوو.")
