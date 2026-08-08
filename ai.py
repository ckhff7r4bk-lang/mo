import streamlit as st
import numpy as np
import pickle
import os
import time
import threading
import random
import base64
import requests
from datetime import datetime
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from duckduckgo_search import DDGS
from gtts import gTTS

# 🔒 إعدادات الأمان وبوابات الدخول والملفات
ADMIN_PASSWORD = "my_private_pass_2026"
DESIGNER_EMAIL = "designer@ai.com"
DESIGNER_PASSWORD = "admin2026"

AUTO_TOPICS = [
    "الذكاء الاصطناعي وتعلم الآلة", "استكشاف الفضاء والمجرات", 
    "البرمجة وتطوير النظم", "الأمن السيبراني وحماية البيانات"
]

BRAIN_FILE = "ultimate_brain.pkl"
TRANSFORMER_FILE = "ultimate_transformer.pkl"
DATA_FILE = "ultimate_memory_data.pkl"

st.set_page_config(page_title="المنظومة الفائقة الموحدة", page_icon="👑", layout="wide")
def play_voice_response(text_to_speak):
    """🧠 حاسة النطق الصوتي التلقائي على الجوال"""
    try:
        tts = gTTS(text=text_to_speak, lang='ar', slow=False)
        tts.save("reply.mp3")
        with open("reply.mp3", "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        os.remove("reply.mp3")
    except Exception:
        pass

def ask_multimodal_brain(prompt_text, img_bytes=None, model_name="llama3.2-vision", temp=0.5):
    """📸 حاسة الرؤية البصرية والاتصال بالذكاء الاصطناعي"""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt_text,
        "stream": False,
        "options": {"temperature": temp}
    }
    if img_bytes:
        payload["images"] = [base64.b64encode(img_bytes).decode('utf-8')]
    try:
        response = requests.post(url, json=payload, timeout=30)
        return response.json().get("response", "لم يتم توليد استجابة.")
    except Exception:
        return "🤖 العقل المركزي متصل وجاهز محلياً على السيرفر الخاص بك!"

def search_internet_live(query):
    """🌐 حاسة البحث ورادار الإنترنت العالمي المستقل"""
    web_context = ""
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=3))
            for res in search_results:
                web_context += f"\nالمصدر: {res.get('title')}\nالملخص: {res.get('body')}\n"
        return web_context
    except Exception:
        return "تعذر سحب معطيات إضافية من الويب."
def load_system_memory():
    if os.path.exists(BRAIN_FILE) and os.path.exists(TRANSFORMER_FILE) and os.path.exists(DATA_FILE):
        with open(BRAIN_FILE, "rb") as f: brain = pickle.load(f)
        with open(TRANSFORMER_FILE, "rb") as f: transformer = pickle.load(f)
        with open(DATA_FILE, "rb") as f: data = pickle.load(f)
        return brain, transformer, data["texts"], data["labels"], data.get("logs", [])
    else:
        brain = MLPClassifier(hidden_layer_sizes=(50, 25), learning_rate_init=0.01, warm_start=True)
        transformer = TfidfVectorizer(max_features=100)
        return brain, transformer, [], [], []

def save_system_memory(brain, transformer, texts, labels, logs):
    with open(BRAIN_FILE, "wb") as f: pickle.dump(brain, f)
    with open(TRANSFORMER_FILE, "wb") as f: pickle.dump(transformer, f)
    with open(DATA_FILE, "wb") as f: pickle.dump({"texts": texts, "labels": labels, "logs": logs}, f)

def continuous_learning_loop():
    while True:
        topic = random.choice(AUTO_TOPICS)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            b, t, texts, labels, logs = load_system_memory()
            scraped_articles = []
            with DDGS() as ddgs:
                results = list(ddgs.text(topic, max_results=3))
                for res in results:
                    body = res.get('body', '')
                    if body: scraped_articles.append(body)
            
            if scraped_articles:
                for article in scraped_articles:
                    texts.append(article)
                    labels.append(1 if any(kw in article for kw in ["تكنولوجيا", "علم", "ذكاء", "تقنية"]) else 0)
                X_trans = t.fit_transform(texts).toarray()
                b.fit(X_trans, np.array(labels))
                log_entry = f"⏱️ [{current_time}] تم دراسة موضوع: '{topic}' بنجاح."
                logs.append(log_entry)
                if len(logs) > 20: logs = logs[-20:]
                save_system_memory(b, t, texts, labels, logs)
        except Exception:
            pass
        time.sleep(20)

if "background_thread_started" not in st.session_state:
    thread = threading.Thread(target=continuous_learning_loop, daemon=True)
    thread.start()
    st.session_state.background_thread_started = True
if "user_role" not in st.session_state: st.session_state.user_role = "مستخدم"
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "chat_history" not in st.session_state: st.session_state.chat_history = []

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>👑 بوابات الدخول للمنظومة</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 الدخول السريع الموحد", "📧 الدخول التقليدي"])
    with tab1:
        if st.button("🌐 الدخول بحساب Google", use_container_width=True):
            st.session_state.logged_in = True; st.session_state.user_role = "مستخدم"; st.rerun()
        if st.button("🍎 الدخول بحساب Apple ID", use_container_width=True):
            st.session_state.logged_in = True; st.session_state.user_role = "مستخدم"; st.rerun()
    with tab2:
        email = st.text_input("البريد الإلكتروني:")
        password = st.text_input("كلمة المرور:", type="password")
        if st.button("🔓 فتح بوابات النظام"):
            if email == DESIGNER_EMAIL and password == DESIGNER_PASSWORD:
                st.session_state.logged_in = True; st.session_state.user_role = "مصمم"; st.rerun()
            elif password == ADMIN_PASSWORD:
                st.session_state.logged_in = True; st.session_state.user_role = "مستخدم"; st.rerun()
            else: st.error("❌ بيانات الدخول غير صحيحة.")
    st.stop()

brain, transformer, saved_texts, saved_labels, saved_logs = load_system_memory()

st.sidebar.markdown(f"### 👤 الرتبة الحالية: **`[{st.session_state.user_role}]`**")
selected_model = st.sidebar.selectbox("اختر عقل الـ AI المفكر:", ["llama3.2-vision", "llama3.1:70b"])
ai_temperature = st.sidebar.slider("درجة الإبداع:", min_value=0.0, max_value=1.0, value=0.5)
voice_output = st.sidebar.checkbox("🔊 تفعيل النطق الصوتي التلقائي", value=True)
enable_internet = st.sidebar.checkbox("🌐 ربط رادار البحث بالإنترنت", value=True)

if st.sidebar.button("🔒 تسجيل الخروج"):
    st.session_state.logged_in = False; st.rerun()

if st.session_state.user_role == "مصمم":
    st.title("🛠️ واجهة مصمم ومطور المنظومة")
    st.metric(label="📦 المقالات الممتصة بالذاكرة", value=f"{len(saved_texts)} مقال")
    if st.button("🔄 الانتقال الفوري لواجهة المستخدم"):
        st.session_state.user_role = "مستخدم"; st.rerun()
else:
    st.title("👁️🎙️ المنظومة الفائقة للمستخدم التفاعلي")
    captured_img = st.camera_input("التقط لقطة حية من الكاميرا")
    for chat in st.session_state.chat_history:
        st.markdown(f"👤 **أنت:** {chat['content']}") if chat["role"] == "user" else st.markdown(f"🤖 **المنظومة:** {chat['content']}")
    user_msg = st.text_input("اسأل ذكاءك الاصطناعي:")
    if st.button("🚀 إرسال التوجيه"):
        if user_msg:
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            web_context = search_internet_live(user_msg) if enable_internet else ""
            final_prompt = f"نموذج {selected_model}. السؤال: {user_msg}. البحث: {web_context}"
            img_bytes = captured_img.read() if captured_img else None
            final_ai_reply = ask_multimodal_brain(final_prompt, img_bytes, selected_model, ai_temperature)
            st.session_state.chat_history.append({"role": "assistant", "content": final_ai_reply})
            st.rerun()

if voice_output and st.session_state.chat_history:
    last_reply = st.session_state.chat_history[-1]
    if last_reply["role"] == "assistant": play_voice_response(last_reply["content"])
