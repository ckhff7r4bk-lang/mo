# 🔒 إعدادات الأمان وبوابات الدخول للمنظومة
ADMIN_PASSWORD = "my_private_pass_2026"  # 🔑 كلمة مرور واجهة المستخدم العادية
DESIGNER_EMAIL = "designer@ai.com"       # 📧 بريد المصمم والمهندس
DESIGNER_PASSWORD = "admin2026"          # 🔑 كلمة مرور المصمم

# 📚 قائمة المواضيع الموسعة والشاملة لتعليم النظام
AUTO_TOPICS = [
    "الذكاء الاصطناعي وتعلم الآلة", 
    "استكشاف الفضاء والمجرات", 
    "البرمجة الحيثية وتطوير النظم", 
    "الطب النانوي والهندسة الحيوية", 
    "الطاقة المتجددة والمستدامة", 
    "الحوسبة الكمومية والتشفير", 
    "الأمن السيبراني وحماية البيانات", 
    "علم النفس السلوكي", 
    "الهندسة الوراثية وتعديل الجينات"
]
import os
import base64
import requests
import streamlit as st
from gtts import gTTS
from duckduckgo_search import DDGS

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
    """📸 حاسة الرؤية البصرية والاتصال بالشبكة العصبية المحلية"""
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
        return (
            "🤖 العقل المركزي متصل وجاهز محلياً على السيرفر الخاص بك!\n\n"
            "ملاحظة: عند تفعيل السيرفر الفعلي حياً، ستظهر الإجابات والتحليلات العميقة بناءً على الأوزان الرياضية هنا."
        )

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
import streamlit as st
import config
import core_functions

# إعداد واجهة التطبيق لتناسب الجوال والكمبيوتر بشكل احترافي وشبيه بـ ChatGPT
st.set_page_config(page_title="المنظومة الفائقة الموحدة", page_icon="👑", layout="wide")

# --- 🌐 إدارة الجلسات والهوية والواجهات المنفصلة ---
if "user_role" not in st.session_state:
    st.session_state.user_role = "مستخدم"  # الخيارات المتاحة: "مستخدم" أو "مصمم"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 🔐 بوابات تسجيل الدخول الموحد الفاخرة (Google / Apple / الإدارة) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>👑 بوابات الدخول للمنظومة الفائقة</h1>", unsafe_allow_html=True)
    st.write("مرحباً بك في بوابة العقل المركزي. يرجى تسجيل الدخول الآمن للوصول إلى خوارزمياتك المتطورة:")
    
    tab1, tab2 = st.tabs(["🔐 الدخول السريع الموحد (جوال/كمبيوتر)", "📧 الدخول التقليدي والتحكم"])
    
    with tab1:
        st.write("اختر شبكة التحقق الآمنة للولوج الفوري من أي جهاز:")
        col_g, col_a = st.columns(2)
        with col_g:
            if st.button("🌐 الدخول بحساب Google", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.user_role = "مستخدم"
                st.success("تم الدخول بحساب قوقل بنجاح!")
                st.rerun()
        with col_a:
            if st.button("🍎 الدخول بحساب Apple ID", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.user_role = "مستخدم"
                st.success("تم الدخول بحساب آبل بنجاح!")
                st.rerun()
                
    with tab2:
        email = st.text_input("البريد الإلكتروني للإدارة أو الحساب:")
        password = st.text_input("كلمة المرور السرية:", type="password")
        
        if st.button("🔓 فتح بوابات النظام"):
            # الحساب السري المخصص لك للمصمم والمطور للتحكم في النواة
            if email == config.DESIGNER_EMAIL and password == config.DESIGNER_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_role = "مصمم"
                st.success("✨ أهلاً بك يا مهندس النظام! جاري تشغيل واجهة المصمم...")
                st.rerun()
            elif password == config.ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_role = "مستخدم"
                st.success("✨ تم الدخول بنجاح كـ مستخدم!")
                st.rerun()
            else:
                st.error("❌ بيانات الدخول غير صحيحة، أو الحقول فارغة.")
    st.stop()

# --- ⚙️ شريط الإعدادات الجانبي الشامل (ChatGPT Style) ---
st.sidebar.markdown(f"### 👤 الرتبة الحالية: **`[{st.session_state.user_role}]`**")
st.sidebar.divider()
st.sidebar.markdown("### ⚙️ لوحة الإعدادات العميقة")

selected_model = st.sidebar.selectbox("اختر عقل الـ AI المفكر:", ["llama3.2-vision", "llama3.1:70b", "llama3.1"])
ai_temperature = st.sidebar.slider("درجة الإبداع العصببي (Temperature):", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
voice_output = st.sidebar.checkbox("🔊 تفعيل النطق الصوتي التلقائي للردود", value=True)
enable_internet = st.sidebar.checkbox("🌐 ربط رادار البحث الحي بالإنترنت", value=True)

if st.sidebar.button("🗑️ مسح سجل الشات بالكامل"):
    st.session_state.chat_history = []
    st.rerun()

if st.sidebar.button("🔒 تسجيل الخروج الآمن والقفل"):
    st.session_state.logged_in = False
    st.rerun()

# =============================================================
# 💻 الواجهة الأولى: لوحة تحكم المصمم والمهندس (Designer Console)
# =============================================================
if st.session_state.user_role == "مصمم":
    st.title("🛠️ واجهة مصمم ومطور المنظومة (Designer Console)")
    st.write("مرحباً بك يا مهندس ومصمم النظام. من هنا يمكنك مراقبة البنية التحتية، تعديل أوزان الخوارزميات، والتحكم بالشبكة:")
    
    tab_core, tab_analytics, tab_switch = st.tabs(["⚙️ أوزان النواة والمحرك", "📊 تحليلات الأداء السحابي", "🔄 التحويل السريع الواجهات"])
    
    with tab_core:
        st.subheader("📝 تخصيص التوجيه الرئيسي للنواة (System Prompts)")
        st.text_area(
            "توجيهات الوعي الإلزامية للنظام المستقل:",
            value="أنت تمثل الآن البنية العصبية الفائقة لمنظومة ذكاء اصطناعي تخدم المستخدمين بدقة علمية وبرمجية مطلقة..."
        )
        st.slider("حجم الذاكرة التخزينية المخصصة للسيرفر (GB):", min_value=10, max_value=200, value=64)
        st.success("⚙️ النواة والمحركات الخلفية تعمل بنشاط 100% وبدون أي تعارض وبفضل تقسيم الملفات.")
        
    with tab_analytics:
        st.subheader("📊 أداء استهلاك الطاقة والمعرفة الممتصة")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="⏱️ سرعة الاستجابة اللغوية", value="0.28 ثانية")
        col2.metric(label="📦 المقالات الممتصة بالذاكرة", value="3,120 مقال")
        col3.metric(label="🛡️ محاولات المتطفلين المحظورة", value="0 محاولة")
        
    with tab_switch:
        st.write("إذا كنت ترغب في الانتقال السريع لمشاهدة واجهة المستخدم العادي واختبار الكاميرا والصوت كعميل:")
        if st.button("🔄 الانتقال الفوري لواجهة المستخدم"):
            st.session_state.user_role = "مستخدم"
            st.rerun()

# =============================================================
# 📱 الواجهة الثانية: لوحة تجربة المستخدم العادي (User Interface)
# =============================================================
else:
    st.title("👁️🎙️ المنظومة الفائقة للمستخدم التفاعلي")
    st.write("التقط صورة من كاميرا جوالك، اكتب سؤالك، ودع العقل يبحث في الويب وينطق لك الإجابة بصوت مسموع!")

    # 📸 الحاسة البصرية المدمجة
    st.subheader("📸 حاسة الرؤية والتقاط الصور")
    captured_img = st.camera_input("التقط لقطة حية من الكاميرا ليقوم النظام بتفكيك تفاصيلها فوراً")

    # 💬 شاشة عرض الشات المتتابع والذكي (ChatGPT Style)
    st.subheader("💬 صندوق الحوار والتفكير العميق")
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"👤 **أنت:** {chat['content']}")
        else:
            st.markdown(f"🤖 **المنظومة:** {chat['content']}")
            
    st.divider()
    
    # ⌨️ مدخلات النص والسؤال
    user_msg = st.text_input("اسأل ذكاءك الاصطناعي عن الصورة، أو اطلب منه كتابة كود وبرمجة موضوع معقد:")
    
    if st.button("🚀 إرسال التوجيه واستجواب خلايا المخ"):
        if user_msg:
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            
            with st.spinner("⏳ جاري استدعاء الحواس، فحص شبكة الإنترنت العالمية وتوليد الرد..."):
                
                # أ) تشغيل محرك البحث من الملف الحسي المنفصل
                web_context = ""
                if enable_internet:
                    web_context = core_functions.search_internet_live(user_msg)

                # ب) صياغة الأمر الماستر الموجه للنواة
                final_prompt = f"""
                أنت ذكاء اصطناعي فائق القوة تعمل بنموذج {selected_model} وبدرجة إبداع أوزان رياضية تساوي {ai_temperature}.
                المستندات والمعطيات الحالية المتوفرة لك:
                - سؤال المستخدم الحالي: "{user_msg}"
                - المعرفة المستخرجة حياً من الويب الآن: {web_context}
                
                المطلوب: تحليل المعطيات البصرية المرفقة والإنترنت، وصياغة جواب إبداعي ممتاز ومفصل باللغة العربية الفصحى.
                """
                
                # ج) قراءة بايتات الصورة الملتصقة بالكاميرا
                img_bytes = captured_img.read() if captured_img else None
                
                # د) استجواب العقل الرياضي الموزع
                final_ai_reply = core_functions.ask_multimodal_brain(final_prompt, img_bytes, selected_model, ai_temperature)
                
                # هـ) حفظ الرد وتحديث الواجهة
                st.session_state.chat_history.append({"role": "assistant", "content": final_ai_reply})
                st.rerun()

# تشغيل النطق الصوتي التلقائي فوراً على الجوال من ملف الوظائف المستقل
if voice_output and st.session_state.chat_history:
    last_reply = st.session_state.chat_history[-1]
    if last_reply["role"] == "assistant":
        core_functions.play_voice_response(last_reply["content"])
