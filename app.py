import streamlit as st
import requests

# ئیتر کلیلەکە لێرە نانووسین، ستریملیت خۆی لە Secrets دەیهێنێت
token = st.secrets["HF_TOKEN"]

API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"
headers = {"Authorization": f"Bearer {token}"}
# باقی کۆدەکە وەک خۆی...
