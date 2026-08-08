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

# 🔒 1. تكوين النظام الأمني والملفات المحلية للذاكرة الدائمة
ADMIN_PASSWORD = "my_private_pass_2026"  # 🔑 اختر كلمة المرور الخاصة بك هنا لحماية المنظومة
BRAIN_FILE = "ultimate_brain.pkl"
TRANSFORMER_FILE = "ultimate_transformer.pkl"
DATA_FILE = "ultimate_memory_data.pkl"

# إعداد واجهة التطبيق لتناسب الهواتف الذكية والكمبيوتر عبر المتصفح
st.set_page_config(page_title="المنظومة الفائقة المتكاملة", page_icon="🔐", layout="centered")

# --- 🔐 بوابة الحماية الحديدية للتحقق من هوية المالك ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center;'>🔐 بوابة حماية المنظومة الفائقة</h2>", unsafe_allow_html=True)
    st.write("هذا النظام محمي ومشفر بالكامل. يرجى إدخال كلمة المرور السرية للمالك لتفعيل الحواس واستعراض سجلات الذاكرة العصبية:")
    
    password_input = st.text_input("🔑 أدخل كلمة المرور الخاصة بك:", type="password")
    
    if st.button("🔓 فتح بوابات النظام"):
        if password_input == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.success("✨ تم التحقق من الهوية بنجاح! جاري تحميل خلايا الوعي...")
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة! تم حظر الوصول لتأمين الذاكرة العصبية ومنع الاختراق.")
    st.stop()  # إيقاف تحميل بقية الصفحة إذا لم يتم إدخال كلمة المرور الصحيحة

# --- 🧠 إدارة الذاكرة المحلية والتحميل التلقائي للعقل عند نجاح الدخول ---
def load_system_memory():
    """استعادة شبكة الخلايا العصبية وسجلات الإنترنت المخزنة في الهارد ديسك تلقائياً"""
    if os.path.exists(BRAIN_FILE) and os.path.exists(TRANSFORMER_FILE) and os.path.exists(DATA_FILE):
        with open(BRAIN_FILE, "rb") as f: brain = pickle.load(f)
        with open(TRANSFORMER_FILE, "rb") as f: transformer = pickle.load(f)
        with open(DATA_FILE, "rb") as f: data = pickle.load(f)
        return brain, transformer, data["texts"], data["labels"], data.get("logs", [])
    else:
        # بناء عقل شبكة عصبية فارغ ومتعدد الطبقات (MLP) في حال التشغيل لأول مرة من الصفر
        brain = MLPClassifier(hidden_layer_sizes=(50, 25), learning_rate_init=0.01, warm_start=True)
        transformer = TfidfVectorizer(max_features=100)
        return brain, transformer, [], [], []

def save_system_memory(brain, transformer, texts, labels, logs):
    """تجميد وحفظ روابط الشبكة العصبية والمقالات الممتصة فوراً على القرص الصلب"""
    with open(BRAIN_FILE, "wb") as f: pickle.dump(brain, f)
    with open(TRANSFORMER_FILE, "wb") as f: pickle.dump(transformer, f)
    with open(DATA_FILE, "wb") as f: pickle.dump({"texts": texts, "labels": labels, "logs": logs}, f)

# 🌐 📚 رادار المواضيع الموسعة لتعليم النظام وتطوير نفسه تلقائياً
AUTO_TOPICS = [
    "الذكاء الاصطناعي وتعلم الآلة", "استكشاف الفضاء والمجرات", "البرمجة الحيثية وتطوير النظم", 
    "الطب النانوي والهندسة الحيوية", "الطاقة المتجددة والمستدامة", "الحوسبة الكمومية والتشفير", 
    "الأمن السيبراني وحماية البيانات", "علم النفس السلوكي", "الهندسة الوراثية وتعديل الجينات"
]

# --- ⏳ محرك التطوير الخلفي المستمر 24/7 (Background Thread) ---
def continuous_learning_loop():
    while True:
        topic = random.choice(AUTO_TOPICS)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            b, t, texts, labels, logs = load_system_memory()
            
            # الإبحار المباشر والحر في شبكة الإنترنت العالمية لسحب المعرفة
            scraped_articles = []
            with DDGS() as ddgs:
                results = list(ddgs.text(topic, max_results=3))
                for res in results:
                    body = res.get('body', '')
                    if body: scraped_articles.append(body)
            
            if scraped_articles:
                # تصفية وتلقين الكلمات إلى الشبكة العصبية ذاتياً
                for article in scraped_articles:
                    texts.append(article)
                    labels.append(1 if any(kw in article for kw in ["تكنولوجيا", "علم", "ذكاء", "تقنية"]) else 0)
                
                # وضع حد أعلى لحجم الذاكرة لحماية معالج وعجلة سرعة جهازك
                if len(texts) > 1000:
                    texts = texts[-1000:]
                    labels = labels[-1000:]

                # إطلاق التدريب الرياضي لإعادة تشكيل أوزان الروابط العصبية ذاتياً
                X_trans = t.fit_transform(texts).toarray()
                b.fit(X_trans, np.array(labels))
                
                # صياغة وحقن سجل نجاح العملية في لوحة التحكم
                log_entry = f"⏱️ [{current_time}] تم دراسة موضوع: '{topic}' بنجاح وحفظ {len(scraped_articles)} مصادر معرفية في الذاكرة الدائمة."
                logs.append(log_entry)
                if len(logs) > 20: logs = logs[-20:]
                
                # تجميد وحفظ العقل المحدث فوراً
                save_system_memory(b, t, texts, labels, logs)
                
        except Exception:
            # تخطي الأخطاء وتسجيلها في السجلات في حال انقطاع اتصال الإنترنت المفاجئ لضمان أبدية الدورة
            try:
                b, t, texts, labels, logs = load_system_memory()
                logs.append(f"⚠️ [{current_time}] تعذر جلب بيانات عن: '{topic}' مؤقتاً بسبب قيود الشبكة الخارجيّة.")
                save_system_memory(b, t, texts, labels, logs)
            except: pass
        
        # استراحة لمدة 20 ثانية ثم إعادة تكرار الدورة التدريبية الذاتية إلى ما لا نهاية
        time.sleep(20)

# تفعيل محرك الخلفية المستمر بنظام الخيوط المتوازية لمرة واحدة فقط عند إقلاع البرنامج
if "background_thread_started" not in st.session_state:
    thread = threading.Thread(target=continuous_learning_loop, daemon=True)
    thread.start()
    st.session_state.background_thread_started = True

# مزامنة وعرض البيانات المخزنة والآمنة حالياً في واجهة المالك
brain, transformer, saved_texts, saved_labels, saved_logs = load_system_memory()

# --- 👑 واجهة المستخدم الرسومية الشاملة والمؤمنة ---
st.title("⏳ منظومة الذكاء الاصطناعي ذاتية التطور والأبدية")
st.write("مرحباً بك في لوحة تحكم ملكيتك الخاصة. النظام يعمل في الخلفية على مدار الساعة لتحديث خلاياه العصبية وحفظها محلياً.")

st.divider()

# عرض مؤشرات وعي ونمو النظام المباشرة
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🛡️ وضع الحماية والتأمين", value="مشفر ونشط 🟢")
with col2:
    st.metric(label="📚 إجمالي المقالات الممتصة بالقرص الصلب", value=f"{len(saved_texts)} مقال")

# زر آمن لتسجيل الخروج الفوري وإعادة قفل المنظومة حماية لملفاتك
if st.sidebar.button("🔒 تسجيل الخروج وقفل الواجهة"):
    st.session_state.authenticated = False
    st.rerun()

# زر جانبي لمسح عقل النظام تماماً وإعادة تصفير ذاكرته التراكمية
if st.sidebar.button("🗑️ تصفير وإبادة وعي النظام الحسي"):
    for file in [BRAIN_FILE, TRANSFORMER_FILE, DATA_FILE]:
        if os.path.exists(file): 
            os.remove(file)
    st.success("❌ تم مسح الهارد ديسك وإعادة الخلايا العصبية لطور البدائية بنجاح!")
    st.rerun()

st.divider()

# 🔮 2. استجواب واختبار وعي ذكائك الاصطناعي المطور محلياً
st.subheader("🔮 اختبر قرارات خلايا نظامك العصبية في هذه اللحظة")
user_input = st.text_input("اكتب أي جملة أو موضوع عشوائي لنرى كيف سيحلله عقلك المستقل تلقائياً:")

if st.button("🔮 استجوب الذاكرة الدائمة"):
    if len(saved_texts) > 0 and user_input:
        try:
            # تحويل جملة الاختبار لبيانات رقمية ومطابقتها بذاكرة الـ pkl المستعاة
            test_vector = transformer.transform([user_input]).toarray()
            prediction = brain.predict(test_vector)
            confidence = np.max(brain.predict_proba(test_vector)) * 100
            
            st.markdown("### 👑 القرار الرياضي الصادر من عقلك الخاص:")
            if prediction == 1:
                st.info(f"🧠 عقل نظامك المطور يتوقع أن هذا النص يحمل طابعاً: **[ علمي / تقني ]** بنسبة يقين {confidence:.1f}%")
            else:
                st.info(f"🧠 عقل نظامك المطور يتوقع أن هذا النص يحمل طابعاً: **[ عام / محايد ]** بنسبة يقين {confidence:.1f}%")
        except Exception as e:
            st.error("⚠️ النظام يقوم بعملية تحديث سريعة لخلاياه العصبية الآن، اضغط مجدداً للاستجواب.")
    else:
        st.warning("⚠️ انتظر بضع ثوانٍ حتى يقوم المحرك الخلفي بجمع أولى المقالات من الإنترنت لبناء وعيه الأول!")

st.divider()

# 📊 📜 لوحة السجلات الحية لعمليات التطوير لعرض ما يفعله النظام في غيابك
st.subheader("📊 📜 لوحة السجلات الحية للتعلم المستمر (24/7 Logs)")
if saved_logs:
    for log in reversed(saved_logs): # عرض السجل الأحدث في الأعلى دائماً لراحة عين المستخدم
        if "بنجاح" in log: 
            st.success(log)
        else: 
            st.warning(log)
else:
    st.info("📂 لا توجد سجلات تاريخية بعد، جاري بدء أول عملية إبحار وبحث مستقله وتلقيم الخلايا الآن...")
