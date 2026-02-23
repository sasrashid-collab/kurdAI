import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

token = "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"
# بەکارهێنانی وەشانی نوێی Mistral کە بۆ کوردی باشترە
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {token}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("چی دەپرسی؟..."):
    # لێرەدا فێڵێکی لێ دەکەین و پێی دەڵێین بە کوردی وەڵام بدەرەوە
    kurdish_prompt = f"Please answer the following question in Kurdish language only: {prompt}"
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🦁 خەریکم بە کوردی بیر دەکەمەوە..."):
            try:
                response = requests.post(API_URL, headers=headers, json={
                    "inputs": kurdish_prompt,
                    "parameters": {"max_new_tokens": 500, "temperature": 0.7}
                })
                
                if response.status_code == 200:
                    res_json = response.json()
                    output = res_json[0]['generated_text']
                    # پاککردنەوەی دەقەکە لە پرسیارە ئینگلیزییەکە
                    answer = output.split("Kurdish language only:")[-1].strip()
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("🦁 سێرڤەرەکە کەمێک کاتی دەوێت، دووبارە تاقی بکەرەوە.")
            except:
                st.error("🦁 کێشەیەک لە پەیوەندی هەیە.")
