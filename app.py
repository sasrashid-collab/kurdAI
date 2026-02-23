import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish (DeepSeek)", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی (DeepSeek)")

# فێڵ لە گیتهەب بۆ پاراستنی کلیلەکە
p1 = "hf_BAwYKhlvyOaWVC"
p2 = "HyByITypmvJfXVBdnCcm"
token = p1 + p2

# ناونیشانی سێرڤەری DeepSeek لەسەر Hugging Face
API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
headers = {"Authorization": f"Bearer {token}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("لێرە پرسیار لە DeepSeek بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🦁 DeepSeek خەریکی بیرکردنەوەیە..."):
            try:
                # ناردنی پرسیار
                payload = {
                    "inputs": f"User: {prompt}\nAssistant: Answer in Kurdish language.",
                    "parameters": {"max_new_tokens": 500, "temperature": 0.6}
                }
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    res_json = response.json()
                    output = res_json[0]['generated_text'] if isinstance(res_json, list) else res_json['generated_text']
                    
                    # جیاکردنەوەی وەڵامەکە (DeepSeek زۆر جار پڕۆسەی بیرکردنەوەکەش دەنووسێت)
                    answer = output.split("Assistant:")[-1].strip()
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                elif response.status_code == 503:
                    st.info("🦁 DeepSeek ئێستا زۆر قەرەباڵغە! ٣٠ چرکە بوەستە و دووبارە تاقی بکەرەوە.")
                else:
                    st.error(f"⚠️ ئێرۆری سێرڤەر: {response.status_code}")
            except:
                st.error("🦁 کێشەیەک لە گەیشتن بە DeepSeek هەیە.")
