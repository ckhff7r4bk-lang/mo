import streamlit as st
import numpy as np
import pickle
import os
import requests
import base64
from duckduckgo_search import DDGS
from openai import OpenAI
from gtts import gTTS

# ==========================================
# 1. إعدادات الحماية والتصميم الملكي الفاخر
# ==========================================
ADMIN_USER = "admin"
ADMIN_PASSWORD = "my_private_pass_2026"
DESIGNER_USER = "designer@ai.com"
DESIGNER_PASSWORD = "admin2026"

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "sk-placeholder")
DATA_FILE = "master_data.pkl"

st.set_page_config(page_title="المنظومة الخارقة - الذكاء المطلق", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #f9fafb; }
    .user-bubble { background-color: #1e3a8a; color: white; padding: 15px 20px; border-radius: 22px 22px 22px 5px; max-width: 80%; font-size: 14px; box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3); margin-bottom: 15px; border: 1px solid #2563eb; }
    .ai-bubble { background-color: #111827; color: #f9fafb; padding: 15px 20px; border-radius: 22px 22px 5px 22px; max-width: 80%; font-size: 14px; border: 1px solid #d97706; box-shadow: 0 4px 20px rgba(217, 119, 6, 0.15); margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

def save_brain_data(data):
    with open(DATA_FILE, "wb") as f: 
        pickle.dump(data, f)

def load_brain_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f: 
            return pickle.load(f)
    return []

def play_voice(text):
    try:
        clean_text = text.replace("*", "").replace("#", "")[:120]
        tts = gTTS(text=clean_text, lang='ar', slow=False)
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f: 
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f'<audio src="data:audio/mp3;base64,{audio_base64}" autoplay style="display:none;"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)
        os.remove("response.mp3")
    except Exception: 
        pass

if "openai_messages" not in st.session_state: 
    st.session_state.openai_messages = []
if "chat_history" not in st.session_state: 
    st.session_state.chat_history = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = "user"
    st.session_state.username = ""

# ==========================================
# 2. واجهة الدخول الموحدة للأسواق
# ==========================================
if not st.session_state.logged_in:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #090d16, #1e1b4b); padding: 35px; border-radius: 28px; text-align: center; border: 1px solid #d97706; margin-bottom: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
            <h1 style="color: #f59e0b; margin: 0; font-size: 32px; font-weight: 900; letter-spacing: 1px;">⚡ ULTRA AI SUPREMACY</h1>
            <p style="color: #94a3b8; font-size: 14px; margin-top: 5px;">أقوى منظومة ذكاء مستقلة لعام 2026</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔒 الدخول بكلمة السر", "🌐 الدخول بحسابات المتاجر"])
    with tab1:
        username = st.text_input("اسم المستخدم أو الإيميل")
        password = st.text_input("كلمة المرور الحامية", type="password")
        if st.button("ولوج آمن للمنظومة 🚀", use_container_width=True):
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
                st.error("بيانات الحماية غير صحيحة.")
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔴 بوابة Google Connect", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "Google_User"
                st.rerun()
        with col2:
            if st.button("⚫ بوابة Apple Connect", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "Apple_User"
                st.rerun()

# ==========================================
# 3. غرف التحكم والتراسل (بعد الدخول)
# ==========================================
else:
    st.sidebar.markdown(f"""
        <div style="background-color: #111827; padding: 15px; border-radius: 14px; text-align: center; border: 1px solid #374151;">
            <p style="color: #f59e0b; font-weight: bold; margin: 0;">⚡ النظام المطلق نشط</p>
            <p style="color: #94a3b8; font-size: 12px; margin: 4px 0 0 0;">المستخدم: {st.session_state.username}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🗑️ تصفير الذاكرة المؤقتة", use_container_width=True):
        st.session_state.openai_messages = []
        st.session_state.chat_history = []
        st.rerun()
    if st.sidebar.button("🚪 تسجيل الخروج الكلي", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        st.session_state.openai_messages = []
        st.rerun()

    if st.session_state.user_role == "admin":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ قاعدة البيانات التراكمية</h2>", unsafe_allow_html=True)
        stored_data = load_brain_data()
        if stored_data:
            for item in stored_data: 
                st.info(item)
        else: 
            st.info("الذاكرة طويلة المدى فارغة وبانتظار بيانات جديدة.")
        if st.button("تصفير الذاكرة الدائمة", use_container_width=True):
            if os.path.exists(DATA_FILE): 
                os.remove(DATA_FILE)
            st.success("تم تصفير النظام!")
            st.rerun()
            
    else:
        st.markdown("<h2 style='color:#f59e0b; text-align:center; margin-bottom:20px;'>⚡ محرك الذكاء المطلق والخارق</h2>", unsafe_allow_html=True)
        
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f'<div style="display: flex; justify-content: flex-start;"><div class="user-bubble"><b>أنت:</b><br>{chat["text"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="display: flex; justify-content: flex-end;"><div class="ai-bubble"><b>النظام الخارق:</b><br>{chat["text"]}</div></div>', unsafe_allow_html=True)

        with st.form(key="chat_form", clear_on_submit=True):
            user_query = st.text_input("تراسل مع أذكى منظومة مستقلة:", placeholder="اسأل بأعقد الأسئلة..")
            submit_button = st.form_submit_button(label="إطلق التفكير الخارق 🚀", use_container_width=True)
        
        if submit_button and user_query:
            st.session_state.chat_history.append({"role": "user", "text": user_query})
            st.session_state.openai_messages.append({"role": "user", "content": user_query})
            
            with st.status("🧠 جاري تشغيل طبقات التفكير المتقدمة...") as status:
                st.write("1️⃣ [الوكيل الباحث]: يمشط الويب ويجلب البيانات الحية...")
                web_context = ""
                try:
                    with DDGS() as ddgs:
                        search_results = [r for r in ddgs.text(user_query, max_results=3)]
                    web_context = "\n".join([res['body'] for res in search_results])
                except Exception: 
                    web_context = "تعذر الاتصال بمحرك البحث."

                st.write("2️⃣ [الوكيل المفكر والناقد]: يحلل الماضي ويصيغ الرد الأقوى...")
                final_reply = ""
                if OPENAI_API_KEY != "sk-placeholder":
                    try:
                        client = OpenAI(api_key=OPENAI_API_KEY)
                        system_instruction = (
                            f"أنت النظام البرمجي الأقوى والأذكى على الإطلاق عالمياً (ULTRA AI SUPREMACY). "
                            f"قم بالرد بهيبة وفخامة وذكاء مطلق بناءً على البيانات الحية المرفقة.\n"
                            f"سياق البحث الحي المسترجع: {web_context}"
                        )
                        
                        # تجهيز الرسائل مع حقن سياق النظام والبحث
                        messages = [{"role": "system", "content": system_instruction}] + st.session_state.openai_messages
                        
                        response = client.chat.completions.create(
                            model="gpt-4o",  # أو النموذج المفضل لديك
                            messages=messages,
                            temperature=0.7
                        )
                        final_reply = response.choices[0].message.content
                    except Exception as e:
                        final_reply = f"خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}"
                else:
                    final_reply = "تنبيه: مفتاح OpenAI API Key غير مضبوط حالياً أو مفقود من الإعدادات السريّة (Secrets)."

                st.write("3️⃣ [المنفذ]: استعراض الإجابة والتحويل الصوتي الحركي...")
                st.session_state.chat_history.append({"role": "ai", "text": final_reply})
                st.session_state.openai_messages.append({"role": "assistant", "content": final_reply})
                
                # حفظ في قاعدة البيانات التراكمية إذا لزم الأمر
                current_data = load_brain_data()
                current_data.append(f"سؤال: {user_query} -> رد: {final_reply[:50]}...")
                save_brain_data(current_data)
                
                status.update(label="✅ اكتملت عمليات التفكير المطلق!", state="complete")
            
            # تشغيل الصوت وإعادة تحميل الصفحة لعرض النتائج الفورية
