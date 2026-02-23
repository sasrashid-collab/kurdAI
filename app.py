import streamlit as st
import requests

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# وەرگرتنی کلیلەکە لە Secrets (بەبێ ئەوەی کلیلەکە لێرە بنووسین)
try:
    token = st.secrets["HF_TOKEN"]
except KeyError:
    st.error("⚠️ ئاگاداری: کلیلەکە لە بەشی Secrets نەدۆزرایەوە. تکایە لە Streamlit دایبنێ.")
    st.stop()

# ناونیشانی سێرڤەری مۆدێل (وەشانی Qwen یان Llama 3)
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"
headers = {"Authorization": f"Bearer {token}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

# پیشاندانی چاتەکان
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# وەرگرتنی پرسیار
if prompt := st.chat_input("لێرە پرسیار بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🦁 خەریکم بیر دەکەمەوە..."):
            try:
                # ناردنی داواکاری بۆ سێرڤەر
                payload = {
                    "inputs": f"User: {prompt}\nAssistant: Answer in Kurdish language.",
                    "parameters": {"max_new_tokens": 500}
                }
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    res_json = response.json()
                    # هەندێک جار سێرڤەر لیست دەنێرێت
                    if isinstance(res_json, list):
                        output = res_json[0]['generated_text']
                    else:
                        output = res_json['generated_text']
                    
                    # پاککردنەوەی وەڵامەکە
                    answer = output.split("Assistant:")[-1].strip()
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                elif response.status_code == 503:
                    st.warning("🦁 سێرڤەر کەمێک کاتی دەوێت بۆ خەبەربوونەوە، تکایە بوەستە و دووبارە بنووسە.")
                elif response.status_code == 401:
                    st.error("❌ کلیلەکەت (Token) لە Hugging Face سووتاوە. یەکێکی نوێ دروست بکە و بیخە Secrets.")
                else:
                    st.error(f"⚠️ کێشەی سێرڤەر: {response.status_code}")
            except Exception as e:
                st.error(f"🦁 کێشەیەکی تەکنیکی: {e}")
