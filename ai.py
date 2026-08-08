import streamlit as st
import numpy as np
import pickle
import os
import requests
from duckduckgo_search import DDGS
from openai import OpenAI

# 1. إعدادات الحماية وجلب البيانات السرية بأمان من السحابة
ADMIN_USER = "admin"
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
DESIGNER_USER = "designer@ai.com"
DESIGNER_PASSWORD = st.secrets["DESIGNER_PASSWORD"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

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

# 2. نظام تسجيل الدخول الآمن والموحد للمتاجر
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
        # 3. نظام التراسل الحي والبحث التلقائي بالإنترنت
        st.title("🧠 منظومة الوعي والذكاء الاصطناعي")
        user_query = st.text_input("تراسل معي واكتب سؤالك هنا:")
        
        if user_query:
            st.write("🔍 جاري البحث الذاتي في الويب والتفكير للإجابة عليك...")
            
            web_context = ""
            try:
                with DDGS() as ddgs:
                    search_results = [r for r in ddgs.text(user_query, max_results=2)]
                web_context = "\n".join([res['body'] for res in search_results])
            except Exception:
                web_context = "تعذر الحصول على معلومات حية من الويب، سأعتمد على معرفتي الأساسية."

            try:
                client = OpenAI(api_key=OPENAI_API_KEY)
                system_instruction = (
                    "أنت ذكاء اصطناعي متطور وخارق تتحدث بثقة وعروبة مطلقة وتساعد المستخدم في كافة المجالات وتتعلم منه.\n"
                    f"إليك بيانات حية من الويب للتوثيق والاستعانة بها: \n{web_context}"
                )
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_query}
                    ]
                )
                
                ai_reply = response.choices.message.content
                st.success("🤖 رد الذكاء الاصطناعي:")
                st.write(ai_reply)
                
                if "احفظ" in user_query or "تعلم" in user_query:
                    current_data = load_brain_data()
                    current_data.append(f"سؤال المستخدم: {user_query} -> الرد: {ai_reply}")
                    save_brain_data(current_data)
                    st.toast("تم حفظ البيانات في الذاكرة التراكمية لتطوير الذات!")
            except Exception as e:
                st.error("الرجاء التأكد من إضافة مفتاح الذكاء الاصطناعي بنجاح في الإعدادات لتفعيل التراسل الحقيقي.")
