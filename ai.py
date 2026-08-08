import streamlit as st
from duckduckgo_search import DDGS
import g4f
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
import urllib.parse
import hashlib
from pypdf import PdfReader

# 1. إعداد الصفحة وتحسين الواجهة لتناسب الجوال والآيفون
st.set_page_config(page_title="منصة AuraAI الذكية", page_icon="🧠", layout="centered")

# 🎨 إضافة لمسة الـ CSS الفخمة والوضع المظلم (Premium Cyberpunk Dark Mode)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d0e15 0%, #161925 100%);
        color: #e2e8f0;
    }
    h1, h2, h3, h4, h5 {
        color: #00f2fe !important;
        text-shadow: 0px 0px 10px rgba(0, 242, 254, 0.3);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stChatMessage {
        background-color: #1e2235 !important;
        border-radius: 15px !important;
        border: 1px solid #2d3250 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        margin-bottom: 12px !important;
    }
    hr {
        border-top: 1px solid #00f2fe !important;
        opacity: 0.2;
    }
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(45deg, #00f2fe, #4facfe) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 8px 20px !important;
        font-weight: bold !important;
        box-shadow: 0px 4px 10px rgba(0, 242, 254, 0.4) !important;
        width: 100%;
    }
    .stTextInput > div > div > input, .stFileUploader > div {
        background-color: #1e2235 !important;
        color: #ffffff !important;
        border: 1px solid #2d3250 !important;
        border-radius: 10px !important;
    }
    audio {
        width: 100%;
        margin-top: 10px;
        border-radius: 10px;
    }
    .stImage > img {
        border-radius: 15px !important;
        border: 2px solid #00f2fe !important;
        box-shadow: 0px 0px 15px rgba(0, 242, 254, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 🔐 إدارة نظام الحسابات وتشفير كلمات المرور في الجلسة
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "mohammed": hashlib.sha256("123456".encode()).hexdigest()
    }

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

def تشفير_كلمة_المرور(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- واجهة تسجيل الدخول والاشتراك ---
if not st.session_state.authenticated:
    st.title("🔐 بوابة حماية AuraAI")
    st.markdown("##### يرجى تسجيل الدخول أو إنشاء حساب جديد للوصول للمنظومة الذكية")
    
    tab1, tab2 = st.tabs(["تسجيل الدخول 🔑", "إنشاء حساب جديد ✨"])
    
    with tab1:
        login_user = st.text_input("اسم المستخدم", key="login_user")
        login_pass = st.text_input("كلمة المرور", type="password", key="login_pass")
        if st.button("دخول المنصة 🚀"):
            hashed_pass = تشفير_كلمة_المرور(login_pass)
            if login_user in st.session_state.users_db and st.session_state.users_db[login_user] == hashed_pass:
                st.session_state.authenticated = True
                st.session_state.username = login_user
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة!")
                
    with tab2:
        new_user = st.text_input("اختر اسم مستخدم جديد", key="new_user")
        new_pass = st.text_input("اختر كلمة مرور قوية", type="password", key="new_pass")
        if st.button("تسجيل الحساب بنجاح 🎉"):
            if new_user.strip() == "" or new_pass.strip() == "":
                st.warning("⚠️ الحقول لا يمكن أن تكون فارغة!")
            elif new_user in st.session_state.users_db:
                st.error("❌ اسم المستخدم هذا مسجّل مسبقاً!")
            else:
                st.session_state.users_db[new_user] = تشفير_كلمة_المرور(new_pass)
                st.success("✅ تم إنشاء حسابك بنجاح! يمكنك الآن الانتقال لتبويب تسجيل الدخول.")

# --- واجهة التطبيق الذكي الرئيسية بعد تسجيل الدخول ---
else:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("🧠 مساعد AuraAI")
    with col2:
        # تجهيز نص المحادثة للتحميل
        chat_text = ""
        for msg in st.session_state.messages:
            chat_text += f"{msg['role'].upper()}: {msg['content']}\n\n"
        
        st.download_button(
            label="حفظ الشات 💾",
            data=chat_text,
            file_name=f"AuraAI_Chat_{st.session_state.username}.txt",
            mime="text/plain"
        )
    with col3:
        if st.button("خروج 🚪"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.messages = []
            st.rerun()
            
    st.markdown(f"<p style='color: #00f2fe;'>مرحباً بك يا <b>{st.session_state.username}</b> | نظام معالجة الملفات والويب والرسوم نشط الآن الحين.</p>", unsafe_allow_html=True)
    st.write("---")

    # 📁 إضافة قسم رفع وتحليل ملفات المستندات (PDF / TXT)
    st.markdown("##### 📁 مركز تحليل المستندات والملفات:")
    uploaded_file = st.file_uploader("ارفع ملف PDF أو TXT ليقوم AuraAI بقراءته وفهمه فوراً", type=["pdf", "txt"])
    
    file_context = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            try:
                pdf_reader = PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        file_context += text + "\n"
                st.info(f"📁 تم ربط مستند PDF بنجاح: {uploaded_file.name}")
            except Exception:
                st.error("❌ حدث خطأ أثناء معالجة ملف الـ PDF.")
        elif uploaded_file.name.endswith(".txt"):
            file_context = uploaded_file.read().decode("utf-8")
            st.info(f"📁 تم ربط ملف النص بنجاح: {uploaded_file.name}")

    # الترحيب الافتراضي إذا كانت الذاكرة فارغة
    if not st.session_state.messages:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"أهلاً بك يا {st.session_state.username}! أنا جاهز الآن بكامل قواي الذكية. يمكنك التحدث معي، أو رفع ملفات لتحليلها، أو طلبي برسم أي صورة تتخيلها فوراً! 🦾"
        })

    # عرض المحادثات السابقة المخزنة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "image" in msg:
                st.image(msg["image"])
            if "audio" in msg:
                st.audio(msg["audio"], format="audio/mp3")

    def توليد_رد_الذكاء_الاصطناعي(السؤال, السياق_الخارجه, نوع_السياق="ويب"):
        if نوع_السياق == "ملف":
            الطلب = f"المستند المرفوع يحتوي على النص التالي:\n{السياق_الخارجه}\n\nبناءً على محتوى المستند أعلاه، أجب بدقة على سؤال المستخدم: '{السؤال}'."
        else:
            الطلب = f"المستخدم يسأل: '{السؤال}'. المعلومات الحية المجلوبة من الويب هي:\n{السياق_الخارجه}\n\nفضلاً صغ إجابة ذكية، منسقة ومفصلة باللغة العربية بناءً على هذه المعلومات والتحية إن وجدت."
        try:
            response = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": الطلب}])
            return response
        except Exception:
            return f"🤖 إليك البيانات المتاحة حول سؤالك:\n\n{السياق_الخارجه[:500]}..."

    def تحويل_النص_الى_صوت(text_to_speak):
        try:
            clean_text = text_to_speak.split("🔗")[0].strip()
            tts = gTTS(text=clean_text, lang='ar', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp
        except Exception:
            return None

    # 🎤 وحدة المايكروفون الذكية
    st.markdown("##### 🎙️ اطلب بالصوت أو ارسم بالذكاء:")
    voice_text = speech_to_text(start_prompt="اضغط للتحدث 🎤", stop_prompt="توقف وجاري التحويل ⏳", language='ar', use_container_width=True, key='microphone')

    # التقاط المدخلات
    user_input = ""
    if voice_text:
        user_input = voice_text
    else:
        chat_box = st.chat_input("تحدث مع الذكاء أو اسأل عن الملف المرفوع...")
        if chat_box:
            user_input = chat_box

    # معالجة الطلب الحين
    if user_input:
        # حفظ وعرض سؤال المستخدم فوراً
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        نص_تنظيف = user_input.strip().lower()
        current_msg_data = {"role": "assistant", "content": ""}

        with st.chat_message("assistant"):
            with st.spinner("🧠 جاري المعالجة الإبداعية وصناعة الرد..."):
                
                # 🔥 [تثبيت الهوية]
                if any(كلمة in نص_تنظيف for كلمة in ["صنعك", "طورك", "مبرمجك", "سواك", "المطور", "الصانع", "creator", "developer"]):
                    reply = "👑 صانعي ومطوري هو المبرمج العبقري **محمد عطية المعلوي**، من **المملكة العربية السعودية** 🇸🇦. لقد قام بهندستي وبرمجتي بالكامل من الجوال ليتحدى الصعاب التقنية ويصنع هذا النظام الذكي!"
                    st.write(reply)
                    current_msg_data["content"] = reply
                    
                # 🎨 [محرك توليد الصور]
                elif any(كلمة in نص_تنظيف for كلمة in ["ارسم", "رسم", "صورة", "صوره", "تخيل", "draw", "image", "picture"]):
                    encoded_prompt = urllib.parse.quote(user_input)
                    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&nologo=true"
                    reply = f"🎨 لقد قمت بتوليد ورسم الصورة بناءً على خيالك وطلبك: **'{user_input}'**"
                    st.write(reply)
                    st.image(image_url)
                    current_msg_data["content"] = reply
                    current_msg_data["image"] = image_url
                
