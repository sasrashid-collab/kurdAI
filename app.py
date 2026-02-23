import streamlit as st
from groq import Groq

st.title("🦁 پشکنینی سندوقی Secrets")

# ١. لێرە سەیری ناوەکان دەکەین
all_keys = list(st.secrets.keys())

if len(all_keys) == 0:
    st.warning("⚠️ مامە گیان، سندوقی Secrets بەتاڵ دەردەکەوێت! ستریملیت هیچی تێدا نابینێت.")
else:
    st.success(f"✅ ئەمانەم دۆزییەوە: {all_keys}")
    
    # ٢. ئەگەر کلیلەکە هەبوو، هەوڵی پەیوەندی دەدەین
    try:
        # لێرە ناوی یەکەم کلیل وەردەگرین چی بێت گرنگ نییە
        my_key = st.secrets[all_keys[0]]
        client = Groq(api_key=my_key)
        
        if st.button("تاقیکردنەوەی چات"):
            res = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": "سڵاو"}]
            )
            st.info("وەڵامی زیرەکی دەستکرد: " + res.choices[0].message.content)
    except Exception as e:
        st.error(f"❌ کێشەیەک لە کلیلەکەدا هەیە: {e}")

st.divider()
st.write("ئەگەر لیستەکە بەتاڵ بوو، واتە دەبێت لە لاپەڕەی ستریملیت Reboot App بکەیت.")
