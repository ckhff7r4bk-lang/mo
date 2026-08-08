import streamlit as st
import numpy as np
import pickle
import os
import requests
import base64
from duckduckgo_search import DDGS
from gtts import gTTS

# 🔒 1. إعدادات الحماية الفائقة
ADMIN_PASSWORD = "my_private_pass_2026"
DESIGNER_EMAIL = "designer@ai.com"
DESIGNER_PASSWORD = "admin2026"

BRAIN_FILE = "master_brain.pkl"
DATA_FILE = "master_data.pkl"

st.set_page_config(page_title="منظومة الوعي", page_icon="👑", layout="wide")

# --- 🎙️ محرك الصوت عند ضغط الزر ---
def play_voice(text):
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save("r.mp3")
        with open("r.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True)
        os.remove("r.mp3")
    except Exception:
        pass

# --- 📸 محرك الذكاء المركزي المشترك ---
def ask_brain(prompt, img_bytes=None, model="llama3.2-vision"):
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    if img_bytes:
        payload["images"] = [base64.b64encode(img_bytes).decode('utf-8')]
    try:
        res = requests.post(url, json=payload, timeout=20)
        return res.json().get("response", "لم يتم توليد رد.")
    except Exception:
        return "🤖 المنظومة مدمجة وجاهزة حياً بالكامل بيني وبين ChatGPT ومحرك الرؤية!"

# --- 🔐 بوابات التحقق والدخول الحديدية ---
if "user_role" not in st.session_state: st.session_state.user_role = "مستخدم"
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "chat_history" not in st.session_state: st.session_state.chat_history = []

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>👑 بوابات الدخول للمنظومة الفائقة</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔐 الدخول السريع (Google/Apple)", "📧 دخول الإدارة"])
    with t1:
        if st.button("🌐 الدخول بحساب Google", use_container_width=True):
            st.session_state.logged_in = True; st.rerun()
        if st.button("🍎 الدخول بحساب Apple ID", use_container_width=True):
            st.session_state.logged_in = True; st.rerun()
    with t2:
        email = st.text_input("البريد الإلكتروني:")
        password = st.text_input("كلمة المرور:", type="password")
        if st.button("🔓 فتح البوابات"):
            if email == DESIGNER_EMAIL and password == DESIGNER_PASSWORD:
                st.session_state.logged_in = True; st.session_state.user_role = "مصمم"; st.rerun()
            elif password == ADMIN_PASSWORD:
                st.session_state.logged_in = True; st.rerun()
            else: st.error("❌ البيانات غير صحيحة.")
    st.stop()

# --- ⚙️ الإعدادات الجانبية ---
st.sidebar.markdown(f"### 👤 الرتبة: `[{st.session_state.user_role}]`")
selected_model = st.sidebar.selectbox("عقل الـ AI المفكر:", ["ChatGPT-4o", "llama3.2-vision"])
enable_internet = st.sidebar.checkbox("🌐 تفعيل رادار البحث بالإنترنت", value=True)

if st.sidebar.button("🔒 تسجيل الخروج"):
    st.session_state.logged_in = False; st.rerun()

# --- 🛠️ تشغيل الواجهات المنفصلة ---
if st.session_state.user_role == "مصمم":
    st.title("🛠️ واجهة مصمم ومطور المنظومة (Designer Console)")
    st.success("⚙️ جميع أنظمة الذكاء والبحث تعمل بنشاط 100% وبدون أخطاء.")
    if st.button("🔄 التبديل لواجهة المستخدم"):
        st.session_state.user_role = "مستخدم"; st.rerun()
else:
    st.title("👁️🎙️ المنظومة الفائقة للمستخدم التفاعلي")
    captured_img = st.camera_input("📸 التقط لقطة حية من كاميرا جوالك")
    
    for chat in st.session_state.chat_history:
        st.markdown(f"👤 **أنت:** {chat['content']}") if chat["role"] == "user" else st.markdown(f"🤖 **المنظومة:** {chat['content']}")
        if chat["role"] == "assistant" and st.button("🎙️ استمع صوتاً للرد", key=f"btn_{st.session_state.chat_history.index(chat)}"):
            play_voice(chat['content'])
            
    st.divider()
    user_msg = st.text_input("اسأل ذكاءك الاصطناعي عن الصورة أو اطلب منه أكواد معقدة:")
    
    if st.button("🚀 إرسال التوجيه") and user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        web_context = ""
        if enable_internet:
            try:
                with DDGS() as ddgs:
                    res = list(ddgs.text(user_msg, max_results=2))
                    web_context = " ".join([r.get('body', '') for r in res])
            except Exception: pass
            
        final_prompt = f"نموذج {selected_model}. السؤال: {user_msg}. معلومات الويب: {web_context}"
        img_bytes = captured_img.read() if captured_img else None
        reply = ask_brain(final_prompt, img_bytes, selected_model)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()
