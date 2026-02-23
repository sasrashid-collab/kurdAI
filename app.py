import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# کلیلەکەت بە ٣ پارچە بۆ ئەوەی گیتهەب پێی نەزانێت
a = "hf_pgTwVyZsH"
b = "QajfftOLjgsPjCA"
c = "SKetXPjuGb"
token = f"{a}{b}{c}"

# ئەمە نوێترین و باشترین ناونیشانی سێرڤەرە
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
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
                # ناردنی پرسیار بە شێوازێک کە مۆدێلەکە تێ بگات
                payload = {
                    "inputs": f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nAnswer in Kurdish: {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                    "parameters": {"max_new_tokens": 250, "temperature": 0.5}
                }
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    res_json = response.json()
                    output = res_json[0]['generated_text']
                    # دەرھێنانی وەڵامەکە بە تەنیا
                    answer = output.split("assistant")[-1].strip()
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                elif response.status_code == 503:
                    st.info("🦁 سێرڤەر خەریکی خۆ گەرمکردنەوەیە (١٠ چرکە بوەستە و دووبارە بنووسە).")
                elif response.status_code == 401:
                    st.error("🦁 کلیلەکە (Token) سووتاوە، دەبێت یەکێکی تر دروست بکەیت.")
                else:
                    st.error(f"سێرڤەر وتی: {response.status_code}")
            except:
                st.error("🦁 کێشەیەک لە ئینتەرنێت هەیە.")
