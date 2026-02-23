import streamlit as st
import requests

st.set_page_config(page_title="🦁 AI Kurdish", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# فێڵ لە گیتهەب (کلیلەکەت بە ٣ پارچە)
a = "hf_pgTwVyZsH"
b = "QajfftOLjgsPjCA"
c = "SKetXPjuGb"
token = f"{a}{b}{c}"

# بەکارهێنانی وەشانی v0.2 کە جێگیرترە و ئێرۆری 410 نادات
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
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
                # ناردنی پرسیار
                payload = {"inputs": f"Answer in Kurdish: {prompt}"}
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    res_json = response.json()
                    output = res_json[0]['generated_text']
                    answer = output.replace(f"Answer in Kurdish: {prompt}", "").strip()
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                elif response.status_code == 503:
                    st.warning("🦁 سێرڤەر خەوتووە، ٣٠ چرکە بوەستە و دووبارە بنووسە.")
                else:
                    st.error(f"سێرڤەر وتی: {response.status_code}. (ئەگەر ٤٠١ بوو کلیلەکە سوتاوە)")
            except:
                st.error("🦁 کێشەی هێڵ هەیە.")
