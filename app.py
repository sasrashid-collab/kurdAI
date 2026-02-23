import streamlit as st
from groq import Groq
from PIL import Image
import io
import base64
import requests

# ڕێکخستنی سەرەتایی سایتەکە
st.set_page_config(page_title="🦁 Kurdish AI Assistant", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")

# وەرگرتنی کلیلەکان لە Secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    XAI_API_KEY = st.secrets["XAI_API_KEY"]
except:
    st.error("⚠️ کلیلەکان لە بەشی Secrets نەدۆزرانەوە!")
    st.stop()

# ناساندنی کلاینتی Groq
groq_client = Groq(api_key=GROQ_API_KEY)

tab1, tab2 = st.tabs(["📸 شیکارکردنی وێنە (Groq)", "💬 چاتی Grok (xAI)"])

with tab1:
    st.header("شیکارکردنی وێنە بە Llama 3.2")
    uploaded_file = st.file_uploader("وێنەیەک هەڵبژێرە...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='وێنەکە ئامادەیە', use_container_width=True)
        
        if st.button("🔍 شیکار بکە"):
            with st.spinner("خەریکە Groq وێنەکە دەخوێنێتەوە..."):
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

                response = groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{"role": "user", "content": [{"type": "text", "text": "ئەم وێنەیە بە وردی بە کوردی شیکار بکە."}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}]
                )
                st.success("ئەنجامی Groq:")
                st.write(response.choices[0].message.content)

with tab2:
    st.header("چات لەگەڵ Grok")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("لێرە پرسیار لە Grok بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # بانگکردنی Grok بە شێوەی ڕاستەوخۆ (بەبێ OpenAI library)
            headers = {"Authorization": f"Bearer {XAI_API_KEY}", "Content-Type": "application/json"}
            payload = {"model": "grok-beta", "messages": st.session_state.messages}
            
            response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
            if response.status_code == 200:
                answer = response.json()['choices'][0]['message']['content']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("کێشەیەک لە پەیوەندی بە Grok دروست بوو.")
