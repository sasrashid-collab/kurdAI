import streamlit as st
from groq import Groq
import io, base64
from PIL import Image

# ١. دیزاینی سادە
st.set_page_config(page_title="🦁 Kurdish AI", layout="wide")
st.title("🦁 زیرەکی دەستکردی کوردی")

# ٢. بانگکردنی کلیلەکە (دڵنیابە لە Secrets هەر ئەم ناوەیە: GROQ_API_KEY)
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ مامە گیان، کلیلەکە لە Secrets نییە! ناوی بنێ: GROQ_API_KEY")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ٣. دروستکردنی بەشەکان
tab1, tab2 = st.tabs(["💬 چات و کۆدینگ", "📸 پشکنینی وێنە"])

# --- بەشی چات و کۆدینگ (هەردووکی لە یەک شوێن) ---
with tab1:
    st.header("چات و پڕۆگرامسازی")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("چی دەپرسی؟ (کۆد یان چات)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # بەکارهێنانی بەهێزترین مۆدێل بۆ چات و کۆدینگ
            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer in Kurdish. If the user asks for code, provide it clearly."},
                    *st.session_state.messages
                ]
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- بەشی وێنە ---
with tab2:
    st.header("خوێندنەوەی وێنە و پسوڵە")
    uploaded_file = st.file_uploader("وێنەیەک لێرە دابنێ", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=300)
        if st.button("🔍 شیکاری بکە"):
            with st.spinner("خەریکە دەیخوێنێتەوە..."):
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG")
                base64_image = base64.b64encode(buffered.getvalue()).decode()
                
                vision_res = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{"role": "user", "content": [
                        {"type": "text", "text": "ئەم وێنەیە بە کوردی شیکار بکە."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}]
                )
                st.info(vision_res.choices[0].message.content)
