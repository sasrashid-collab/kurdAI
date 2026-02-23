import streamlit as st
from groq import Groq

# ناوی سایتەکە
st.title("🦁 زیرەکی دەستکردی کوردی")

# پشکنینی ئەوەی ئایا کلیلەکە لە سەکریت دانراوە یان نا
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ مامە گیان، سیمکارتەکە (کلیلەکە) لە ناو سەکریت نییە.")
    st.stop()

# دەستپێکردنی ئیشەکە
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# دروستکردنی شوێنی نووسین
prompt = st.chat_input("لێرە هەر پرسیارێکت هەیە یان کۆدێکت دەوێت بنووسە...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    try:
        # ناردنی پرسیارەکە بۆ زیرەکی دەستکرد
        res = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        with st.chat_message("assistant"):
            st.write(res.choices[0].message.content)
    except Exception as e:
        st.error(f"کێشەیەک هەیە: {e}")
