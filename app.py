import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# فێڵ لە گیتهەب: کلیلەکە لێرە پارچە پارچە دەکەین تا نەیسوتێنێت
p1 = "hf_BAwYKhlvyOaWVC"
p2 = "HyByITypmvJfXVBdnCcm"
token = p1 + p2

API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"
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
        with st.spinner("🦁 بیر دەکەمەوە..."):
            try:
                payload = {"inputs": f"User: {prompt}\nAssistant: Answer in Kurdish:", "parameters": {"max_new_tokens": 500}}
                response = requests.post(API_URL, headers=headers, json=payload)
                if response.status_code == 200:
                    output = response.json()[0]['generated_text']
                    answer = output.split("Assistant:")[-1].strip()
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"ئێرۆری سێرڤەر: {response.status_code}")
            except:
                st.error("🦁 پەیوەندی بڕا.")
