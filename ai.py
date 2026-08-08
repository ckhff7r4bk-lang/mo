import streamlit as st
from duckduckgo_search import DDGS
import g4f
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
import urllib.parse
import hashlib
from pypdf import PdfReader

# 1. إعداد الصفحة وتأمين الواجهة لتناسب الجوال والآيفون
st.set_page_config(page_title="منصة AuraAI الذكية", page_icon="🧠", layout="centered")

# 🎨 🛠️ تصميم الخلفية السديمية الفخمة مع الأيقونات المدمجة (Premium Cyberpunk Theme)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a102f 0%, #0b0c10 100%);
        background-attachment: fixed;
        color: #e2e8f0;
    }
    
    h1, h2, h3, h4, h5 {
        color: #00f2fe !important;
        text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.4);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: right;
    }
    
    .stChatMessage {
        background: rgba(30, 34, 53, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 15px !important;
    }
    
    /* شريط معالجة المدخلات والأيقونات السفلي الموحد */
    .input-container {
        background: rgba(20, 24, 40, 0.85) !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 30px !important;
        padding: 10px 15px !important;
        margin-bottom: 20px;
    }
    
    hr {
        border-top: 1px solid rgba(0, 242, 254, 0.2) !important;
    }
    
    /* أزرار علوية فخمة دائرية */
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(45deg, #7b2ff7, #00f2fe) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 6px 16px !important;
        font-weight: bold !important;
        box-shadow: 0px 4px 12px rgba(123, 47, 247, 0.3) !important;
        width: 100%;
    }
    
    audio {
        width: 100%;
        margin-top: 10px;
        border-radius: 12px;
    }
    
    .stImage > img {
        border-radius: 16px !important;
        border: 1px solid rgba(0, 242, 254, 0.4) !important;
        box-shadow: 0px 0px 25px rgba(0, 242, 254, 0.2);
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
    st.markdown("<p style='text-align: right; color: #a0aec0;'>يرجى تسجيل الدخول أو إنشاء حساب جديد للوصول للمنظومة الذكية</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["تسجيل الدخول 🔑", "إنشاء حساب جديد ✨"])
    
    with tab1:
        login_user = st.text_input("اسم المستخدم", key="login_user")
        login_pass = st.text_input("كلمة المرور", type="password", key="login_pass")
        if st.button("دخول 🚀"):
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
        if st.button("تسجيل 🎉"):
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
        st.title("🧠 AuraAI")
    with col2:
        chat_text = ""
        for msg in st.session_state.messages:
            chat_text += f"{msg['role'].upper()}: {msg['content']}\n\n"
        
        st.download_button(label="💾 حفظ", data=chat_text, file_name=f"AuraAI_Chat_{st.session_state.username}.txt", mime="text/plain")
    with col3:
        if st.button("🚪 خروج"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.messages = []
            st.rerun()
            
    st.markdown(f"<div style='color: #00f2fe; direction: rtl; text-align: right; font-weight: bold;'>مرحباً بك يا {st.session_state.username}</div>", unsafe_allow_html=True)
    st.write("---")

    # الترحيب الافتراضي إذا كانت الذاكرة فارغة
    if not st.session_state.messages:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"أهلاً بك يا {st.session_state.username}! أنا AuraAI جاهز بكامل قواي الذكية لمساعدتك عبر الويب أو المستندات أو توليد الصور والرسوم. تفضل بطلباتك عبر لوحة التحكم السفلية! 🦾"
        })

    # عرض المحادثات السابقة المخزنة بشكل آمن للمتصفح
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "image" in msg:
                st.image(msg["image"])
            if "audio" in msg:
                st.audio(msg["audio"], format="audio/mp3")

    def توليد_رد_الذكاء_الاصطناعي(السؤال, السياق_الخارجي, نوع_السياق="ويب"):
        if نوع_السياق == "ملف":
            الطلب = f"المستند المرفوع يحتوي على النص التالي:\n{السياق_الخارجي}\n\nبناءً على محتوى المستند أعلاه، أجب بدقة على سؤال المستخدم: '{السؤال}'."
        else:
            الطلب = f"المستخدم يسأل: '{السؤال}'. المعلومات الحية المجلوبة من الويب هي:\n{السياق_الخارجي}\n\nفضلاً صغ إجابة ذكية، منسقة ومفصلة باللغة العربية بناءً على هذه المعلومات والتحية إن وجدت."
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

    # 🛠️ 📥 [شريط التحكم الأيقوني الموحد أسفل الشات]
    st.write("---")
    st.markdown("<h6 style='text-align: right; color: #00f2fe;'>🎛️ أدوات الإدخال والتحكم المدمجة:</h6>", unsafe_allow_html=True)
    
    # توزيع الأدوات على أعمدة بشكل متناسق عبر علامات مخصصة
    menu_col1, menu_col2 = st.columns([1, 2])
    
    file_context = ""
    with menu_col1:
        # علامة الدبوس 📎 لرفع المستندات والملفات بشكل مضغوط
        uploaded_file = st.file_uploader("📎", type=["pdf", "txt"], help="اضغط لرفع المستندات PDF/TXT وفحصها")
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".pdf"):
                try:
                    pdf_reader = PdfReader(uploaded_file)
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text:
                            file_context += text + "\n"
                    st.toast(f"📎 تم ربط المستند: {uploaded_file.name}", icon="📁")
                except Exception:
                    st.error("خطأ في قراءة الملف")
            elif uploaded_file.name.endswith(".txt"):
                file_context = uploaded_file.read().decode("utf-8")
                st.toast(f"📎 تم ربط المستند: {uploaded_file.name}", icon="📄")

    with menu_col2:
        # علامة المايكروفون 🎤 للتسجيل الصوتي الفوري المباشر مع ضبط اللغة
        voice_text = speech_to_text(start_prompt="🎙️ تحدث بالصوت", stop_prompt="⏳ معالجة ونطق", language='ar', use_container_width=True, key='microphone')

    # صندوق الكتابة الرئيسي الموحد لاستقبال الأسئلة وطلبات الصور (مثال: ارسم لي صقر طائر)
    chat_box = st.chat_input("اكتب رسالتك، أو اطلب صورة بعبارة (ارسم لي...)...")
    
    # دمج كافة مسارات الإدخال في متغير موحد
    user_input = ""
    if voice_text:
        user_input = voice_text
    elif chat_box:
        user_input = chat_box

    # معالجة الطلب بشكل مستقر وضمان عدم حدوث ردود فارغة
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        نص_تنظيف = user_input.strip().lower()
        current_msg_data = {"role": "assistant", "content": ""}

        with st.chat_message("assistant"):
            with st.spinner("🧠 جاري المعالجة الإبداعية وصناعة الرد..."):
                
                # 🔥 [تثبيت الهوية ومفهوم المطور الصانع]
                if any(كلمة in نص_تنظيف for كلمة in ["صنعك", "طورك", "مبرمجك", "سواك", "المطور", "الصانع", "creator", "developer"]):
                    reply = "👑 صانعي ومطوري هو المبرمج العبقري **محمد المعلوي**، من **المملكة العربية السعودية** 🇸🇦. لقد قام بهندستي وبرمجتي بالكامل من الجوال ليتحدى الصعاب التقنية ويصنع هذا النظام الذكي!"
                    st.write(reply)
                    current_msg_data["content"] = reply
                    # 🎨 [محرك توليد الرسوم والصور الذكية بتجاوز فوري]elif any(كلمة in نص_تنظيف for كلمة in ["ارسم", "رسم", "صورة", "صوره", "تخيل", "draw", "image", "picture"]):encoded_prompt = urllib.parse.quote(user_input)image_url = f"pollinations.ai{encoded_prompt}?width=1024&height=1024&nologo=true"reply = f"🎨 لقد قمت بتوليد ورسم الصورة بناءً على خيالك وطلبك: '{user_input}'"st.write(reply)st.image(image_url)current_msg_data["content"] = replycurrent_msg_data["image"] = image_url# 📁 [الأولوية الأولى: معالجة سياق ملف الـ PDF/TXT المربوط بالدبوس 📎]elif file_context != "":reply = توليد_رد_الذكاء_الاصطناعي(user_input, file_context, نوع_السياق="ملف")st.write(reply)current_msg_data["content"] = reply# 🌐 [الأولوية الثانية: تمشيط الويب الخارجي والاتصال التوليدي السحابي]else:try:with DDGS() as ddgs:نتائج = list(ddgs.text(user_input, max_results=3, region="wt-wt"))if نتائج:نص_الويب_الخام = "\n".join([r['body'] for r in نتائج])روابط_المصادر = "\n\n🔗 المصادر المرجعية:\n"for idx, ر in enumerate(نتائج, 1):روابط_المصادر += f"{idx}. {ر['title']}\n"reply = f"{توليد_رد_الذكاء_الاصطناعي(user_input, نص_الويب_الخام, نوع_السياق='ويب')}{روابط_المصادر}"else:reply = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": user_input}])except Exception:try:reply = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": user_input}])except Exception:if "وعليكم" in نص_تنظيف or "سلام" in نص_تنظيف:reply = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا صديقي في AuraAI، كيف يمكنني مساعدتك اليوم؟"else:reply = f"🤖 أهلاً بك! لقد استقبلت طلبك بنجاح: '{user_input}'. خوادم المعالجة المتقدمة تواجه ضغطاً مؤقتاً، لكنني متصل ومستعد لخدمتك دائماً."st.write(reply)current_msg_data["content"] = reply# 🎙️ [التوليد الصوتي التلقائي والناطق المسموع للمخرج النهائي للرد]if current_msg_data["content"]:audio_file = تحويل_النص_الى_صوت(current_msg_data["content"])if audio_file:st.audio(audio_file, format="audio/mp3")current_msg_data["audio"] = audio_file# حفظ المخرجات التراكمية في الذاكرة لتجنب مشكلة الـ removeChildst.session_state.messages.append(current_msg_data)st.rerun()
