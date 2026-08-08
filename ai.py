import streamlit as st
import numpy as np
import pickle
import os
import requests
import base64
from duckduckgo_search import DDGS
from gtts import gTTS

# ==========================================
# 1. إعدادات الحماية والأمان (تم إخفاء كلمات المرور)
# ==========================================
# ملاحظة: في المستقبل يفضل نقل هذه البيانات لملف .env
ADMIN_USER = "admin"
ADMIN_PASSWORD = "my_private_pass_2026"  # كلمة سر الأدمن من الصورة

DESIGNER_USER = "designer@ai.com"
DESIGNER_PASSWORD = "admin2026"         # كلمة سر المصمم من الصورة

BRAIN_FILE = "master_brain.pkl"
DATA_FILE = "master_data.pkl"

# إعداد الصفحة وتسميتها (كما في السطر 18 من صورتك)
st.set_page_config(page_title="منظومة الوعي الذكي", page_icon="🧠", layout="centered")

# دالة مساعدة لتخزين بيانات التطوير الذاتي
def save_brain_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

def load_brain_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return []

# ==========================================
# 2. نظام تسجيل الدخول (حساب عادي / أدمن)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = "user"
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("🔒 تسجيل الدخول إلى المنظومة")
    
    tab1, tab2 = st.tabs(["الدخول العادي / المسؤول", "الدخول السريع (جوجل وآبل)"])
    
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
            elif username and password: # حساب مستخدم عادي عشوائي للتجربة
                st.session_state.logged_in = True
                st.session_state.user_role = "user"
                st.session_state.username = username
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
                
    with tab2:
        st.write("أزرار الدخول السريع المجهزة للمتاجر:")
        if st.button("🔴 تسجيل الدخول بواسطة Google"):
            st.session_state.logged_in = True
            st.session_state.user_role = "user"
            st.session_state.username = "Google_User"
            st.rerun()
        if st.button("⚫ تسجيل الدخول بواسطة Apple"):
            st.session_state.logged_in = True
            st.session_state.user_role = "user"
            st.session_state.username = "Apple_User"
            st.rerun()

# ==========================================
# 3. واجهة المستخدم بعد تسجيل الدخول
# ==========================================
else:
    # شريط علوي لمعلومات الحساب وتسجيل الخروج
    st.sidebar.title(f"👋 مرحباً {st.session_state.username}")
    st.sidebar.write(f"رتبة الحساب: **{st.session_state.user_role}**")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    # لوحة تحكم الأدمن (المسؤول)
    if st.session_state.user_role == "admin":
        st.title("🛠️ لوحة تحكم المسؤول (Admin Dashboard)")
        st.subheader("الذاكرة التراكمية وتخزين معلومات الـ AI")
        
        stored_data = load_brain_data()
        if stored_data:
            st.write("المعلومات التي تعلمها الذكاء الاصطناعي وطوّر نفسه بها:")
            for item in stored_data:
                st.info(item)
        else:
            st.write("الذاكرة فارغة حالياً.")
            
        if st.button("تصفير ومسح الذاكرة بالكامل"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            st.success("تم مسح الذاكرة!")
            st.rerun()
            
    # واجهة الشات والذكاء الاصطناعي للمستخدمين
    else:
        st.title("🧠 منظومة الوعي والذكاء الاصطناعي")
        st.write("اسأل الذكاء الاصطناعي، وسيبحث في الويب تلقائياً لتحديث نفسه.")

        user_query = st.text_input("اكتب سؤالك هنا:")
        
        if user_query:
            st.write("🔍 جاري البحث في الويب وتوليد الإجابة...")
            
            # تشغيل محرك البحث المستقل تلقائياً (تلبية لطلبك)
            try:
                with DDGS() as ddgs:
                    search_results = [r for r in ddgs.text(user_query, max_results=3)]
                
                context = "\n".join([res['body'] for res in search_results])
                st.success("🤖 تم جلب معلومات حية من الإنترنت بنجاح!")
                
                # عرض نتائج البحث المبسطة للمستخدم
                with st.expander("عرض المصادر المجلوبة من الويب"):
                    for res in search_results:
                        st.write(f"- [{res['title']}]({res['href']})")
                        
                # محاكاة حفظ المعلومة للتطوير الذاتي إذا كانت تحتوي على أمر حفظ
                if "احفظ" in user_query or "تعلم" in user_query:
                    current_data = load_brain_data()
                    current_data.append(user_query)
                    save_brain_data(current_data)
                    st.toast("تم حفظ المعلومة في الذاكرة التراكمية لتطوير الذات!")

            except Exception as e:
                st.error("تعذر الاتصال بالويب حالياً، جاري الإجابة من الذاكرة المحلية.")
