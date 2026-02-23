import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# هێنانی کلیلەکە لە سندوقی نهێنی ستریملیت
try:
    hf_token = st.secrets["MY_TOKEN"]
except:
    st.error("❌ تکایە کلیلەکە لە بەشی Secrets دابنێ بە ناوی MY_TOKEN")
    st.stop()

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {hf_token}"}

if prompt := st.chat_input("لێرە شتێک بنووسە..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": f"Answer in Kurdish: {prompt}"})
            if response.status_code == 200:
                res = response.json()
                answer = res[0]['generated_text'] if isinstance(res, list) else res['generated_text']
                st.write(answer.replace(f"Answer in Kurdish: {prompt}", "").strip())
            elif response.status_code == 503:
                st.info("🦁 مۆدێلەکە خەریکە گەرم دەبێت... کەمێکی تر دووبارە بنووسەوە.")
            else:
                st.error(f"⚠️ کێشەی سێرڤەر: {response.status_code}")
        except:
            st.error("🦁 پەیوەندی بڕا.")
