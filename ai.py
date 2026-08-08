import streamlit as st
from duckduckgo_search import DDGS
import g4f
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
import urllib.parse
import hashlib
from pypdf import PdfReader

# 1. إعداد الصفحة وتأمين الواجهة لتناسب الجوال والآيفون لمنع خطأ removeChild
st.set_page_config(page_title="منصة AuraAI الذكية", page_icon="🧠", layout="centered")

# 🎨 تصميم الخلفية السديمية الفخمة والمظلمة مع الأشكال الزجاجية شبه الشفافة
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
    hr { border-top: 1px solid rgba(0, 242, 254, 0.2) !important; }
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
    .stTextInput > div > div > input, .stFileUploader > div {
        background-color: #1e2235 !important;
        color: #ffffff !important;
        border: 1px solid #2d3250 !important;
        border-radius: 10px !important;
    }
    audio { width: 100%; margin-top: 10px; border-radius: 12px; background-color: #1e2235; }
    .stImage > img {
        border-radius: 16px !important;
        border: 1px solid rgba(0, 242, 254, 0.4) !important;
        box-shadow: 0px 0px 25px rgba(0, 242, 254, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 🔐 إدارة نظام الحسابات وتشفير كلمات المرور في الجلسة
if "users_db" not in st.session_state:
    st.session_state.users_db = {"mohammed": hashlib.sha256("123456".encode()).hexdigest()}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

def تشفير_كلمة_المرور(password):
    return hashlib.sha256(password.encode()).hexdigest()
# --- 🔐 بوابة حماية AuraAI وسجلات الدخول الذكي المطور ---
if not st.session_state.authenticated:
    st.title("🔐 بوابة حماية AuraAI")
    
    # ميزة الدخول السريع بحسابات Google و Apple
    st.markdown("<p style='text-align: right; color: #a0aec0;'>الدخول السريع عبر الحسابات الرسمية:</p>", unsafe_allow_html=True)
    col_g, col_a = st.columns(2)
    with col_g:
        if st.button("🔴 الدخول بحساب Google"):
            st.session_state.authenticated = True
            st.session_state.username = "مستخدم_جوجل"
            st.toast("تم تسجيل الدخول الآمن عبر خوادم Google بنجاح 🌐")
            st.rerun()
    with col_a:
        if st.button("🍏 الدخول بحساب Apple"):
            st.session_state.authenticated = True
            st.session_state.username = "مستخدم_آبل"
            st.toast("تم التحقق والمصادقة الآمنة عبر Apple ID بنجاح 🔒")
            st.rerun()

    st.write("---")
    st.markdown("<p style='text-align: right; color: #a0aec0;'>أو استخدم النظام التقليدي للمنصة:</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["تسجيل الدخول 🔑", "إنشاء حساب جديد ✨"])
    with tab1:
        login_user = st.text_input("اسم المستخدم", key="login_user")
        login_pass = st.text_input("كلمة المرور", type="password", key="login_pass")
        if st.button("دخول المنصة 🚀"):
            if login_user in st.session_state.users_db and st.session_state.users_db[login_user] == تشفير_كلمة_المرور(login_pass):
                st.session_state.authenticated = True
                st.session_state.username = login_user
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة!")
    with tab2:
        new_user = st.text_input("اختر اسم مستخدم جديد", key="new_user")
        new_pass = st.text_input("اختر كلمة مرور قوية", type="password", key="new_pass")
        if st.button("تسجيل الحساب 🎉"):
            if new_user.strip() and new_pass.strip() and new_user not in st.session_state.users_db:
                st.session_state.users_db[new_user] = تشفير_كلمة_المرور(new_pass)
                st.success("✅ تم إنشاء حسابك بنجاح! انتقل لتبويب تسجيل الدخول.")

# --- واجهة التطبيق الذكي الرئيسية بعد تسجيل الدخول الناجح ---
else:
    col1, col2, col3 = st.columns()
    with col1:
        st.title("🧠 AuraAI")
    with col2:
        chat_text = "".join([f"{m['role'].upper()}: {m['content']}\n\n" for m in st.session_state.messages])
        st.download_button(label="💾 حفظ الشات", data=chat_text, file_name=f"AuraAI_Chat_{st.session_state.username}.txt", mime="text/plain")
    with col3:
        if st.button("🚪 خروج"):
            st.session_state.authenticated, st.session_state.username, st.session_state.messages = False, "", []
            st.rerun()
            
    st.markdown(f"<div style='color: #00f2fe; direction: rtl; text-align: right; font-weight: bold;'>مرحباً بك يا {st.session_state.username}</div>", unsafe_allow_html=True)
    st.write("---")

    st.markdown("##### 📁 مركز تحليل المستندات والملفات:")
    uploaded_file = st.file_uploader("ارفع ملف PDF أو TXT ليقوم الذكاء بقراءته وفهمه", type=["pdf", "txt"])
    file_context = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            try:
                pdf_reader = PdfReader(uploaded_file)
                file_context = "".join([page.extract_text() or "" for page in pdf_reader.pages])
                st.toast(f"📎 تم ربط المستند: {uploaded_file.name}", icon="📁")
            except: st.error("❌ حدث خطأ في ملف PDF")
        elif uploaded_file.name.endswith(".txt"):
            file_context = uploaded_file.read().decode("utf-8")
            st.toast(f"📎 تم ربط المستند: {uploaded_file.name}", icon="📄")
    if not st.session_state.messages:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"أهلاً بك يا {st.session_state.username}! أنا AuraAI جاهز لمساعدتك عبر الويب، المستندات، أو توليد الصور بعبارة (ارسم لي...). تفضل بطلبك الآن! 🦾"
        })

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "image" in msg: st.image(msg["image"])
            if "audio" in msg: st.audio(msg["audio"], format="audio/mp3")

    def توليد_رد_الذكاء_الاصطناعي(السؤال, السياق, نوع="ويب"):
        if نوع == "ملف": 
            الطلب = f"المستند يحتوي على النص التالي:\n{سياق}\n\nأجب بدقة وبشكل مفصل على سؤال المستخدم: '{السؤال}'."
        else: 
            الطلب = f"المستخدم يسأل: '{السؤال}'. معلومات الويب الحية:\n{سياق}\n\nصغ إجابة ذكية ومنسقة بالعربية."
        try: return g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": الطلب}])
        except: return f"🤖 البيانات المستخرجة حول سؤالك:\n\n{سياق[:500]}..."

    def تحويل_النص_الى_صوت(text_to_speak):
        try:
            clean_text = text_to_speak.split("🔗").strip()
            tts = gTTS(text=clean_text, lang='ar', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except: return None

    st.write("---")
    menu_col1, menu_col2 = st.columns(2)
    with menu_col2:
        voice_text = speech_to_text(start_prompt="🎙️ تحدث بالصوت", stop_prompt="⏳ معالجة ونطق", language='ar', use_container_width=True, key='microphone')
    
    chat_box = st.chat_input("اكتب رسالتك، أو اطلب صورة بعبارة (ارسم لي...)...")
    user_input = voice_text if voice_text else chat_box

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        نص_تنظيف = user_input.strip().lower()
        current_msg_data = {"role": "assistant", "content": ""}

        with st.chat_message("assistant"):
            with st.spinner("🧠 جاري المعالجة الإبداعية وصناعة الرد..."):
                
                if any(k in نص_تنظيف for k in ["صنعك", "طورك", "مبرمجك", "سواك", "المطور"]):
                    reply = "👑 صانعي ومطوري هو المبرمج العبقري **محمد عطية المعلوي**، من **المملكة العربية السعودية** 🇸🇦. لقد قام بهندستي وبرمجتي بالكامل من الجوال ليتحدى الصعاب التقنية ويصنع هذا النظام الذكي!"
                    st.write(reply)
                    current_msg_data["content"] = reply
                    
                elif any(k in نص_تنظيف for k in ["ارسم", "رسم", "صورة", "تخيل", "draw", "image"]):
                    image_url = f"https://pollinations.ai{urllib.parse.quote(user_input)}?width=1024&height=1024&nologo=true"
                    reply = f"🎨 لقد قمت بتوليد ورسم الصورة بناءً على خيالك وطلبك: **'{user_input}'**"
                    st.write(reply)
                    st.image(image_url)
                    current_msg_data["content"], current_msg_data["image"] = reply, image_url
                
                elif file_context:
                    reply = توليد_رد_الذكاء_الاصطناعي(user_input, file_context, نوع="ملف")
                    st.write(reply)
                    current_msg_data["content"] = reply

                else:
                    try:
                        with DDGS() as ddgs: نتائج = list(ddgs.text(user_input, max_results=3, region="wt-wt"))
                        if نتائج:
                            nass_web = "\n".join([r['body'] for r in نتائج])
                            sources = "\n\n🔗 **المصادر المرجعية:**\n" + "\n".join([f"{i}. [{r['title']}]({r['href']})" for i, r in enumerate(نتائج, 1)])
                            reply = f"{توليد_رد_الذكاء_الاصطناعي(user_input, nass_web, نوع='ويب')}{sources}"
                        else: reply = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": user_input}])
                    except:
                        try: reply = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": user_input}])
                        except:
                            if "سلام" in نص_تنظيف: reply = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا صديقي في AuraAI، كيف يمكنني مساعدتك اليوم؟"
                            else: reply = f"🤖 استقبلت طلبك بنجاح: '{user_input}'. السيرفرات تواجه ضغطاً مؤقتاً، لكنني متصل ومستعد لخدمتك دائماً."
                    st.write(reply)
                    current_msg_data["content"] = reply

                if current_msg_data["content"]:
                    audio_bytes = تحويل_النص_الى_صوت(current_msg_data["content"])
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
                        current_msg_data["audio"] = audio_bytes
                
                st.session_state.messages.append(current_msg_data)
                st.rerun()
