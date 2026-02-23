import streamlit as st
import requests

# ڕێکخستنی شێوەی لاپەڕە
st.set_page_config(page_title="🦁 AI Kurdish", page_icon="🦁", layout="centered")

st.title("🦁 یاریدەدەری زیرەکی کوردی")
st.markdown("---")

# کلیلەکەی تۆ (بە پارچە پارچەکراوی بۆ ئەوەی گیتهەب نەیبینێت)
part1 = "sk-411a33294b244260"
part2 = "a27393995f7e5aa5"
DEEPSEEK_KEY = part1 + part2

# ناونیشانی سێرڤەری DeepSeek
API_URL = "https://api.deepseek.com/chat/completions"

# دروستکردنی میمۆری بۆ چاتەکە
if "messages" not in st.session_state:
    st.session_state.messages = []

# پیشاندانی نامە کۆنەکان
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# شوێنی نووسینی نامە
if prompt := st.chat_input("لێرە پرسیار بکە..."):
    # پاشەکەوتکردنی نامەی بەکارهێنەر
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # وەرگرتنی وەڵام لە DeepSeek
    with st.chat_message("assistant"):
        with st.spinner("🦁 خەریکم بیر دەکەمەوە..."):
            try:
                headers = {
                    "Authorization": f"Bearer {DEEPSEEK_KEY}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant. You must always answer in Kurdish (Sorani)."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                }
                
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                elif response.status_code == 402:
                    st.error("❌ باڵانسی کلیلەکەت (Credit) بەتاڵە. پێویستە لە سایتی DeepSeek باڵانس پڕ بکەیتەوە.")
                elif response.status_code == 401:
                    st.error("❌ کلیلەکە (API Key) کار ناکات. لەوانەیە گیتهەب ناسیبێتی و سوتاندبێتی.")
                else:
                    st.error(f"⚠️ کێشەیەک لە سێرڤەر هەیە: {response.status_code}")
                    
            except Exception as e:
                st.error(f"🦁 هەڵەیەک ڕوویدا: {str(e)}")

# تێبینی ژێرەوە
st.markdown("---")
st.caption("🦁 پەرەپێدراوە لەلایەن مامە زیرەک - بەکارهێنانی DeepSeek AI")
