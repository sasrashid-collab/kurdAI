import streamlit as st
from groq import Groq
from PIL import Image
import io, base64

st.set_page_config(page_title="🦁 Kurdish AI & Coding", layout="wide")
st.title("🦁 یاریدەدەری زیرەکی کوردی (وێنە + چات + کۆدینگ)")

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ تکایە کلیلی GROQ_API_KEY لە بەشی Secrets دابنێ")
    st.stop()

client = Groq(api_key=API_KEY)

# دروستکردنی ٣ بەش
tab1, tab2, tab3 = st.tabs(["📸 وێنە", "💬 چات", "💻 کۆدینگ"])

# بەشی وێنە (وەک پێشتر)
with tab1:
    st.header("شیکاری وێنە")
    file = st.file_uploader("وێنەیەک ئەپلۆد بکە", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, width=300)
        if st.button("🔍 پشکنین"):
            with st.spinner("..."):
                buf = io.BytesIO(); img.save(buf, format="JPEG")
                img_b64 = base64.b64encode(buf.getvalue()).decode()
                res = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{"role": "user", "content": [{"type": "text", "text": "ئەم وێنەیە شیکار بکە."}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}]}]
                )
                st.write(res.choices[0].message.content)

# بەشی چاتی گشتی
with tab2:
    st.header("قسەکردنی ئاسایی")
    if "m1" not in st.session_state: st.session_state.m1 = []
    for m in st.session_state.m1:
        with st.chat_message(m["role"]): st.write(m["content"])
    if p := st.chat_input("چی دەپرسی؟", key="chat"):
        st.session_state.m1.append({"role": "user", "content": p})
        res = client.chat.completions.create(model="llama3-70b-8192", messages=st.session_state.m1)
        ans = res.choices[0].message.content
        st.session_state.m1.append({"role": "assistant", "content": ans})
        st.rerun()

# بەشی تایبەت بە کۆدینگ
with tab3:
    st.header("💻 پڕۆگرامسازی و کۆدینگ")
    st.info("لێرە داوای هەر جۆرە کۆدێک بکە یان کۆدێک بنێرە بۆ چاککردن")
    if "m2" not in st.session_state: st.session_state.m2 = []
    for m in st.session_state.m2:
        with st.chat_message(m["role"]): st.code(m["content"]) # کۆدەکان بە جوانی پیشان دەدات
    if p_code := st.chat_input("کۆدەکەت لێرە داوا بکە...", key="coding"):
        st.session_state.m2.append({"role": "user", "content": p_code})
        # لێرە فەرمان بە AI دەکەین کە وەک پڕۆگرامسازێک جواب بداتەوە
        res = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": "You are an expert programmer. Write clean code and explain it in Kurdish."}] + st.session_state.m2
        )
        ans = res.choices[0].message.content
        st.session_state.m2.append({"role": "assistant", "content": ans})
        st.rerun()
