import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی (DeepSeek)")

# هێنانی کلیلەکە لە سندوقی نهێنی (Secrets)
try:
    deepseek_key = st.secrets["DEEPSEEK_KEY"]
except:
    st.error("⚠️ کلیلەکە لە Secrets نەدۆزرایەوە!")
    st.stop()

API_URL = "https://api.deepseek.com/chat/completions"

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
        with st.spinner("🦁 DeepSeek بیر دەکەمەوە..."):
            try:
                headers = {
                    "Authorization": f"Bearer {deepseek_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant. Answer in Kurdish Sorani."},
                        {"role": "user", "content": prompt}
                    ]
                }
                response = requests.post(API_URL, headers=headers, json=data)
                
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                elif response.status_code == 402:
                    st.error("❌ باڵانسی ئەم کلیلە بەتاڵە (Credit Zero).")
                else:
                    st.error(f"⚠️ ئێرۆری سێرڤەر: {response.status_code}")
            except Exception as e:
                st.error(f"🦁 هەڵەیەک: {e}")
