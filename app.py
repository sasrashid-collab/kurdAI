import streamlit as st
from groq import Groq
from PIL import Image
import io
import base64
import requests

# دیزاینی سایتەکە
st.set_page_config(page_title="🦁 Kurdish AI Assistant", layout="wide")
st.title("🦁 یاریدەدەری زیرەکی کوردی")
st.markdown("---")

# بانگکردنی کلیلەکان لە Secrets (ئەوانەی ئێستا داتنان)
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    G_KEY = st.secrets["XAI_API_KEY"]
except Exception as e:
    st.error("⚠️ کێشەیەک لە کلیلەکاندا هەیە، تکایە دڵنیابە لە بەشی Secrets بە ڕاستی نووسیوتن.")
    st.stop()

# دروستکردنی کلاینتی Groq
groq_client = Groq(api_key=GROQ_KEY)

# دروستکردنی دوو بەش (Tabs)
tab1, tab2 = st.tabs(["📸 شیکارکردنی پسوڵە و وێنە", "💬 چات لەگەڵ Grok"])

# --- بەشی یەکەم: وێنە ---
with tab1:
    st.header("پشکنینی وێنە")
    img_file = st.file_uploader("وێنەی پسوڵە یان هەر شتێک ئەپلۆد بکە", type=["jpg", "png", "jpeg"])
    
    if img_file:
        image = Image.open(img_file)
        st.image(image, width=400)
        
        if st.button("🔍 شیکاری بکە"):
            with st.spinner("خەریکە Groq وێنەکە دەخوێنێتەوە..."):
                # ئامادەکردنی وێنەکە
                buf = io.BytesIO()
                image.save(buf, format="JPEG")
                img_b64 = base64.b64encode(buf.getvalue()).decode()

                # ناردنی بۆ مۆدێلی وێنەیی Groq
                res = groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "تکایە ئەم وێنەیە بە وردی بە زمانی کوردی شیکار بکە."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                        ]
                    }]
                )
                st.success("ئەنجام:")
                st.write(res.choices[0].message.content)

# --- بەشی دووەم: چات ---
with tab2:
    st.header("چاتی زیرەکی کوردی (Grok)")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # پیشاندانی نامە کۆنەکان
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # وەرگرتنی نامەی نوێ
    user_input = st.chat_input("لێرە شتێک بنووسە...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            # بانگکردنی Grok بە شێوەی ڕاستەوخۆ
            h = {"Authorization": f"Bearer {G_KEY}", "Content-Type": "application/json"}
            p = {"model": "grok-beta", "messages": st.session_state.chat_history}
            
            r = requests.post("https://api.x.ai/v1/chat/completions", headers=h, json=p)
            
            if r.status_code == 200:
                reply = r.json()['choices'][0]['message']['content']
                st.write(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            else:
                st.error("کێشەیەک لە پەیوەندی بە Grok هەبوو. دڵنیابە کلیلەکەت ڕاستە.")
