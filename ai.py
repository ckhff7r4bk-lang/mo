import streamlit as st
import numpy as np
import pickle
import os
import time
import threading
import random
from datetime import datetime
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from duckduckgo_search import DDGS

# إعداد ملفات الذاكرة الدائمة على الهارد ديسك
BRAIN_FILE = "infinite_brain.pkl"
TRANSFORMER_FILE = "infinite_transformer.pkl"
DATA_FILE = "infinite_memory_data.pkl"

st.set_page_config(page_title="ذكاء دائم التطور 24/7 مع السجلات", page_icon="⏳", layout="centered")

st.title("⏳ منظومة الذكاء الاصطناعي دائمة التطور والتعلم")
st.write("هذا النظام يحتوي على محرك خلفي يعمل على مدار الساعة؛ يبحر في الإنترنت ويطور شبكته العصبية ويخزن الذاكرة في كل الأوقات دون توقف!")

# --- 📚 قائمة المواضيع الموسعة والشاملة لتعليم النظام في غيابك ---
AUTO_TOPICS = [
    "الذكاء الاصطناعي وتعلم الآلة", "استكشاف الفضاء والمجرات", "البرمجة الحيثية وتطوير النظم", 
    "الطب النانوي والهندسة الحيوية", "الطاقة المتجددة والمستدامة", "الحوسبة الكمومية والتشفير", 
    "تاريخ العلوم والاكتشافات", "الأمن السيبراني وحماية البيانات", "علم النفس السلوكي", 
    "الهندسة الوراثية وتعديل الجينات", "اقتصاد المستقبل والعملات الرقمية", "علم الروبوتات والأتمتة الفائقة"
]

# --- محرك إدارة الذاكرة والتطوير في الخلفية ---
def load_memory():
    if os.path.exists(BRAIN_FILE) and os.path.exists(TRANSFORMER_FILE) and os.path.exists(DATA_FILE):
        with open(BRAIN_FILE, "rb") as f: brain = pickle.load(f)
        with open(TRANSFORMER_FILE, "rb") as f: transformer = pickle.load(f)
        with open(DATA_FILE, "rb") as f: data = pickle.load(f)
        return brain, transformer, data["texts"], data["labels"], data.get("logs", [])
    else:
        brain = MLPClassifier(hidden_layer_sizes=(50, 25), learning_rate_init=0.01, warm_start=True)
        transformer = TfidfVectorizer(max_features=100)
        return brain, transformer, [], [], []

def save_memory(brain, transformer, texts, labels, logs):
    with open(BRAIN_FILE, "wb") as f: pickle.dump(brain, f)
    with open(TRANSFORMER_FILE, "wb") as f: pickle.dump(transformer, f)
    with open(DATA_FILE, "wb") as f: pickle.dump({"texts": texts, "labels": labels, "logs": logs}, f)

# دالة محرك الخلفية المستقل (تشتغل كخيط منفصل تماماً عن الشاشة)
def background_learning_loop():
    while True:
        topic = random.choice(AUTO_TOPICS)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            b, t, texts, labels, logs = load_memory()
            
            # الإبحار في الإنترنت حياً عبر DuckDuckGo
            scraped_articles = []
            links_visited = []
            with DDGS() as ddgs:
                results = list(ddgs.text(topic, max_results=3))
                for res in results:
                    body = res.get('body', '')
                    href = res.get('href', '')
                    if body: 
                        scraped_articles.append(body)
                        if href: links_visited.append(href)
            
            if scraped_articles:
                # دمج المقالات وتلقين الخلايا العصبية
                for article in scraped_articles:
                    texts.append(article)
                    labels.append(1 if any(keyword in article for keyword in ["تكنولوجيا", "علم", "ذكاء", "تقنية"]) else 0)
                
                if len(texts) > 1000:
                    texts = texts[-1000:]
                    labels = labels[-1000:]

                # تدريب وتحديث الأوزان الرياضية للشبكة العصبية
                X_trans = t.fit_transform(texts).toarray()
                b.fit(X_trans, np.array(labels))
                
                # إضافة سجل جديد يوضح نجاح العملية
                log_entry = f"⏱️ [{current_time}] تم دراسة موضوع: '{topic}' بنجاح عبر جلب وتدريب {len(scraped_articles)} مصادر جديدة."
                logs.append(log_entry)
                if len(logs) > 20: logs = logs[-20:] # الاحتفاظ بآخر 20 سجل فقط لحفظ المساحة
                
                save_memory(b, t, texts, labels, logs)
                
        except Exception as e:
            # تسجيل أخطاء الإنترنت في حال انقطاع الشبكة لضمان استقرار الدورة
            try:
                b, t, texts, labels, logs = load_memory()
                logs.append(f"⚠️ [{current_time}] فشل الإبحار مؤقتاً في موضوع: '{topic}' بسبب مشكلة اتصال.")
                save_memory(b, t, texts, labels, logs)
            except:
                pass
        
        # أخذ استراحة لمدة 15 ثانية ثم تكرار العملية إلى الأبد
        time.sleep(15)

# تفعيل محرك الخلفية المستمر لمرة واحدة فقط عند تشغيل التطبيق لأول مرة
if "background_thread_started" not in st.session_state:
    thread = threading.Thread(target=background_learning_loop, daemon=True)
    thread.start()
    st.session_state.background_thread_started = True

# استدعاء الذاكرة الحالية لعرضها على الشاشة أمام المستخدم
brain, transformer, saved_texts, saved_labels, saved_logs = load_memory()

# --- واجهة المستخدم الرسومية ---
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="⚙️ حالة محرك التطوير الخلفي", value="يعمل بنشاط 🟢")
with col2:
    st.metric(label="📚 حجم وعي النظام الممتص حالياً", value=f"{len(saved_texts)} مقال")

st.caption("💡 نصيحة: انتظر بضع ثوانٍ ثم قم بتحديث الصفحة (Refresh)، وستلاحظ أن العداد والسجلات تتحدث تلقائياً!")

st.divider()

# 🔮 استجواب واختبار وعي ذكائك الاصطناعي في أي وقت
st.subheader("🔮 اختبر ما تعلمه نظامك حتى هذه اللحظة")
user_input = st.text_input("اكتب جملة عشوائية لنرى كيف سيحللها عقل نظامك المطور تلقائياً:")

if st.button("🔮 استجواب الخلايا العصبية المحدثة"):
    if len(saved_texts) > 0 and user_input:
        try:
            test_vector = transformer.transform([user_input]).toarray()
            prediction = brain.predict(test_vector)
            confidence = np.max(brain.predict_proba(test_vector)) * 100
            
            st.markdown("### 👑 القرار الصادر من العقل المتطور:")
            if prediction == 1:
                st.info(f"🧠 عقل نظامك يرى أن هذا النص يحمل طابعاً: **[ علمي / تكنولوجي ]** بنسبة يقين {confidence:.1f}%")
            else:
                st.info(f"🧠 عقل نظامك يرى أن هذا نص يحمل طابعاً: **[ عام / محايد ]** بنسبة يقين {confidence:.1f}%")
        except Exception as e:
            st.error(f"⚠️ النظام مشغول حالياً بتحديث خلاياه العصبية، اضغط مرة أخرى. ({str(e)})")
    else:
        st.warning("⚠️ انتظر بضع ثوانٍ حتى يمتص المحرك الخلفي أول درس له من الإنترنت!")

st.divider()

# 📊 📜 لوحة السجلات الحية لعرض ما يفعله النظام في غيابك
st.subheader("📊 📜 لوحة السجلات الحية لعمليات التطوير")
if saved_logs:
    for log in reversed(saved_logs): # عرض الأحدث أولاً
        if "بنجاح" in log:
            st.success(log)
        else:
            st.warning(log)
else:
    st.info("📂 لا توجد سجلات بعد، جاري بدء أول عملية دراسة مستقلة الآن...")
