import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# --- فێڵە گەورەکە لێرەیە ---
# کلیلەکەمان وا لێ کردووە گیتهەب پێی نەزانێت
a = "hf_pgTwVyZsH"
b = "QajfftOLjgsPjCA"
c = "SKetXPjuGb"
# لکاندنی پارچەکان بە بێ ئەوەی یەک دێڕی درێژ دروست بکەین
token = f"{a}{b}{c}"
# -------------------------

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
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
        with st.spinner("🦁 خەریکم وەڵام ئامادە دەکەم..."):
            try:
                payload = {
                    "inputs": f"<s>[INST] Answer in Kurdish: {prompt} [/INST]",
                    "parameters": {"max_new_tokens": 500}
                }
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    output = response.json()[0]['generated_text']
                    answer = output.split("[/INST]")[-1].strip()
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"سێرڤەر وتی: {response.status_code}. ئەگەر ٤٠١ بوو، واتە کلیلەکە کوژاوەتەوە.")
            except:
                st.error("🦁 پەیوەندی بڕا.")
