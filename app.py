import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# هێنانی کلیلەکە بە پیتە گەورەکان وەک ئەوەی لە Secrets دامانناوە
try:
    token = st.secrets["HF_TOKEN"]
except:
    st.error("❌ کلیلەکە نەدۆزرایەوە! دڵنیابە لە Secrets بە ناوی HF_TOKEN نووسیوتە.")
    st.stop()

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {token}"}

if prompt := st.chat_input("لێرە شتێک بنووسە..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            # ناردنی داواکاری بۆ مۆدێلەکە
            response = requests.post(API_URL, headers=headers, json={"inputs": f"Answer in Kurdish: {prompt}"})
            
            if response.status_code == 200:
                res = response.json()
                answer = res[0]['generated_text'] if isinstance(res, list) else res['generated_text']
                # سڕینەوەی بەشی پرسیارەکە لە وەڵامەکەدا
                final_answer = answer.replace(f"Answer in Kurdish: {prompt}", "").strip()
                st.write(final_answer)
            elif response.status_code == 503:
                st.info("🦁 مۆدێلەکە خەریکە گەرم دەبێت... ٣٠ چرکە بوەستە و دووبارە بنووسەوە.")
            else:
                st.error(f"⚠️ ئێرۆری سێرڤەر: {response.status_code}")
        except:
            st.error("🦁 کێشەیەک لە پەیوەندی هەیە.")
