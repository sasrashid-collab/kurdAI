import streamlit as st
import os
from groq import Groq
from openai import OpenAI
from PIL import Image
import io

# دیزاینی لاپەڕە
st.set_page_config(page_title="🦁 Kurdish AI Assistant", layout="centered")
st.title("🦁 یاریدەدەری زیرەکی کوردی")
st.write("وێنەی پسوڵەکەت دابنێ یان چات لەگەڵ زیرەکی دەستکرد بکە")

# وەرگرتنی کلیلەکان لە Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
XAI_API_KEY = st.secrets["XAI_API_KEY"]

# ناساندنی مۆدێلەکان
groq_client = Groq(api_key=GROQ_API_KEY)
xai_client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

tab1, tab2 = st.tabs(["📸 شیکارکردنی وێنە", "💬 چاتی Grok"])

with tab1:
    st.header("شیکارکردنی پسوڵە و وێنە")
    uploaded_file = st.file_uploader("وێنەیەک هەڵبژێرە...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='وێنە ئەپلۆدکراوەکە', use_container_width=True)
        
        if st.button("🔍 شیکار بکە"):
            with st.spinner("خەریکە دەخوێنرێتەوە..."):
                # گۆڕینی وێنە بۆ باینەری
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                import base64
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

                # ناردن بۆ Groq Llama Vision
                response = groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "ئەم وێنەیە بە کوردی شیکار بکە و وردەکارییەکانی بنووسە"},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                }
                            ]
                        }
                    ]
                )
                st.success("ئەنجام:")
                st.write(response.choices[0].message.content)

with tab2:
    st.header("چات لەگەڵ مۆدێلی Grok")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("چی دەپرسی؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = xai_client.chat.completions.create(
                model="grok-beta",
                messages=st.session_state.messages
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
