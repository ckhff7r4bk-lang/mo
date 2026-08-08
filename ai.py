import streamlit as st
import numpy as np
import pickle
import os
import requests
from duckduckgo_search import DDGS
from openai import OpenAI

# ==========================================
# 1. إعدادات الحماية المباشرة (حل مشكلة الخطأ الفوري)
# ==========================================
ADMIN_USER = "admin"
ADMIN_PASSWORD = "my_private_pass_2026"  # تم التعديل ليعمل مباشرة بدون سيكرتس

DESIGNER_USER = "designer@ai.com"
DESIGNER_PASSWORD = "admin2026"

# جلب مفتاح الذكاء الاصطناعي (إذا لم يتوفر، سيعمل كود البحث في الويب)
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "sk-placeholder")

DATA_FILE = "master_data.pkl"

st.set_page_config(page_title="منظومة الوعي الذكي", page_icon="🧠", layout="centered")

def save_brain_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

def load_brain_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return []

# ==========================================
# 2. نظام تسجيل الدخول الآمن
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = "user"
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("🔒 تسجيل الدخول إلى المنظومة")
    tab1, tab2 = st.tabs(["تسجيل الدخول اليدوي", "الدخول السريع (جوجل وآبل)"])
    
    with tab1:
        username = st.text_input("اسم المستخدم أو البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول آمن"):
            if username == ADMIN_USER and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
                st.session_state.username = username
                st.rerun()
            elif username == DESIGNER_USER and password == DESIGNER_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_role = "designer"
                st.session_state.username = username
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    with tab2:
        if st.button("🔴 الدخول بواسطة Google"):
            st.session_state.logged_in = True
            st.session_state.user_role = "user"
            st.session_state.username = "Google_User"
            st.rerun()
        if st.button("⚫ الدخول بواسطة Apple"):
            st.session_state.logged_in = True
            st.session_state.user_role = "user"
            st.session_state.username = "Apple_User"
            st.rerun()
else:
    st.sidebar.title(f"👋 مرحباً {st.session_state.username}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.user_role == "admin":
        st.title("🛠️ لوحة تحكم المسؤول (Admin Dashboard)")
        stored_data = load_brain_data()
        if stored_data:
            for item in stored_data:
                st.info(item)
        else:
            st.write("الذاكرة فارغة حالياً.")
    else:
        # 3. نظام التراسل والبحث التلقائي في الويب
        st.title("🧠 منظومة الوعي والذكاء الاصطناعي")
        user_query = st.text_input("تراسل معي واكتب سؤالك هنا:")
        
        if user_query:
            st.write("🔍 جاري البحث الذاتي في الويب والتفكير لإجابة دقيقة...")
            
            web_context = ""
            try:
                with DDGS() as ddgs:
                    search_results = [r for r in ddgs.text(user_query, max_results=2)]
                web_context = "\n".join([res['body'] for res in search_results])
            except Exception:
                web_context = "تعذر جلب بيانات حية من الويب حالياً."

            # محاولة التشغيل عبر OpenAI، وإذا لم يوضع المفتاح تجيب المنظومة عبر نتائج الويب مباشرة
            if OPENAI_API_KEY != "sk-placeholder":
                try:
                    client = OpenAI(api_key=OPENAI_API_KEY)
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": f"أنت ذكاء اصطناعي متطور. إليك سياق الويب: {web_context}"},
                            {"role": "user", "content": user_query}
                        ]
                    )
                    ai_reply = response.choices.message.content
                    st.success("🤖 رد الذكاء الاصطناعي:")
                    st.write(ai_reply)
                except Exception:
                    st.warning("تعذر الاتصال بـ OpenAI، إليك البيانات المجلوبة من الإنترنت:")
                    st.write(web_context)
            else:
                st.info("🤖 تم جلب النتائج مباشرة من محرك البحث لعدم ربط مفتاح الحساب:")
                st.write(web_context)
                
            if "احفظ" in user_query or "تعلم" in user_query:
                current_data = load_brain_data()
                current_data.append(user_query)
                save_brain_data(current_data)
                st.toast("تم حفظ البيانات بنجاح!")
