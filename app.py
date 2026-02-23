import streamlit as st
import requests

# 1. ڕێکخستنی لاپەڕە
st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# 2. وەرگرتنی کلیلەکە بە شێوەی پارێزراو
try:
    token = st.secrets["HF_TOKEN"]
except:
    st.error("❌ کلیلەکە لە Secrets نەدۆزرایەوە!")
    st.stop()

# 3. بەکارهێنانی مۆدێلی بەلاش و بەهێز
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {token}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("لێرە شتێک بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🦁 چاوەڕوان بە..."):
            try:
                payload = {
                    "inputs": f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nAnswer in Kurdish: {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                    "parameters": {"max_new_tokens": 500, "temperature": 0.7}
                }
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    output = response.json()[0]['generated_text']
                    answer = output.split("assistant")[-1].strip()
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"⚠️ سێرڤەر کەمێک ماندووە، دووبارە هەوڵ بدەرەوە.")
            except:
                st.error("🦁 کێشەیەک ڕوویدا.")
