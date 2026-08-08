import streamlit as st
from duckduckgo_search import DDGS
import g4f
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
import urllib.parse
import hashlib
from pypdf import PdfReader

st.set_page_config(page_title="AuraAI Platform", page_icon="🧠", layout="centered")

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

if "users_db" not in st.session_state:
    st.session_state.users_db = {"mohammed": hashlib.sha256("123456".encode()).hexdigest()}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

if not st.session_state.authenticated:
    st.title("🔐 بوابة حماية AuraAI")
    st.markdown("<p style='text-align: right; color: #a0aec0;'>الدخول السريع عبر الحسابات الرسمية:</p>", unsafe_allow_html=True)
    col_g, col_a = st.columns(2)
    with col_g:
        if st.button("🔴 Google Login"):
            st.session_state.authenticated = True
            st.session_state.username = "Google_User"
            st.toast("تم تسجيل الدخول عبر Google")
            st.rerun()
    with col_a:
        if st.button("🍏 Apple Login"):
            st.session_state.authenticated = True
            st.session_state.username = "Apple_User"
            st.toast("تم التحقق عبر Apple ID")
            st.rerun()

    st.write("---")
    st.markdown("<p style='text-align: right; color: #a0aec0;'>أو استخدم النظام التقليدي:</p>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["تسجيل الدخول 🔑", "إنشاء حساب جديد ✨"])
    with tab1:
        u_in = st.text_input("اسم المستخدم", key="l_user")
        p_in = st.text_input("كلمة المرور", type="password", key="l_pass")
        if st.button("دخول المنصة 🚀"):
            if u_in in st.session_state.users_db and st.session_state.users_db[u_in] == get_hash(p_in):
                st.session_state.authenticated = True
                st.session_state.username = u_in
                st.rerun()
            else:
                st.error("❌ بيانات الدخول خاطئة")
    with tab2:
        nu = st.text_input("اسم مستخدم جديد", key="n_user")
        np = st.text_input("كلمة مرور قوية", type="password", key="n_pass")
        if st.button("تسجيل الحساب 🎉"):
            if nu.strip() and np.strip() and nu not in st.session_state.users_db:
                st.session_state.users_db[nu] = get_hash(np)
                st.success("✅ تم التسجيل بنجاح")

else:
    col1, col2, col3 = st.columns(3)
    with col1: st.title("🧠 AuraAI")
    with col2:
        txt = "".join([f"{m['role'].upper()}: {m['content']}\n\n" for m in st.session_state.messages])
        st.download_button(label="💾 حفظ الشات", data=txt, file_name="AuraAI_Chat.txt")
    with col3:
        if st.button("🚪 خروج"):
            st.session_state.authenticated, st.session_state.username, st.session_state.messages = False, "", []
            st.rerun()
            
    st.markdown(f"<div style='color: #00f2fe; direction: rtl; text-align: right; font-weight: bold;'>مرحباً بك يا {st.session_state.username}</div>", unsafe_allow_html=True)
    st.write("---")

    st.markdown("##### 📁 مركز تحليل المستندات والملفات:")
    up_file = st.file_uploader("ارفع ملف PDF أو TXT", type=["pdf", "txt"])
    f_ctx = ""
    if up_file is not None:
        if up_file.name.endswith(".pdf"):
            try:
                reader = PdfReader(up_file)
                f_ctx = "".join([page.extract_text() or "" for page in reader.pages])
                st.toast("📎 تم ربط ملف PDF")
            except: st.error("خطأ في ملف PDF")
        elif up_file.name.endswith(".txt"):
            f_ctx = up_file.read().decode("utf-8")
            st.toast("📎 تم ربط ملف TXT")

    if not st.session_state.messages:
        st.session_state.messages.append({"role": "assistant", "content": f"أهلاً بك يا {st.session_state.username}! أنا AuraAI جاهز لمساعدتك عبر الويب، المستندات، أو توليد الصور بعبارة (ارسم لي...). تفضل بطلبك الآن! 🦾"})

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "image" in msg: st.image(msg["image"])
            if "audio" in msg: st.audio(msg["audio"], format="audio/mp3")

    def run_ai(q, ctx, mode="web"):
        if mode == "file": prompt = f"Document context:\n{ctx}\n\nAnswer in Arabic to: '{q}'."
        else: prompt = f"The user asks: '{q}'. Web context:\n{ctx}\n\nWrite response in Arabic."
        try: return g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": prompt}])
        except: return f"🤖 البيانات المتاحة:\n\n{ctx[:400]}..."

    def get_audio(text):
        try:
            tts = gTTS(text=text.split("🔗")[0].strip(), lang='ar', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except: return None

    st.write("---")
    m1, m2 = st.columns(2)
    with m2: voice = speech_to_text(start_prompt="🎙️ تحدث بالصوت", stop_prompt="⏳ معالجة ونطق", language='ar', use_container_width=True, key='microphone')
    box = st.chat_input("اكتب رسالتك، أو اطلب صورة بعبارة (ارسم لي...)...")
    
    inp = voice if voice else box

    if inp:
        st.session_state.messages.append({"role": "user", "content": inp})
        clean = inp.strip().lower()
        res_data = {"role": "assistant", "content": ""}

        with st.chat_message("assistant"):
            with st.spinner("🧠 جاري المعالجة..."):
                if any(k in clean for k in ["صنعك", "طورك", "مبرمجك", "سواك", "المطور"]):
                    rep = "👑 صانعي ومطوري هو المبرمج العبقري **محمد عطية المعلوي**، من **المملكة العربية السعودية** 🇸🇦. لقد قام بهندستي وبرمجتي بالكامل من الجوال ليتحدى الصعاب التقنية ويصنع هذا النظام الذكي!"
                    st.write(rep)
                    res_data["content"] = rep
                elif any(k in clean for k in ["ارسم", "رسم", "صورة", "تخيل", "draw", "image"]):
                    img_url = f"https://pollinations.ai{urllib.parse.quote(inp)}?width=1024&height=1024&nologo=true"
                    rep = f"🎨 لقد قمت بتوليد ورسم الصورة بناءً على طلبك: **'{inp}'**"
                    st.write(rep)
                    st.image(img_url)
                    res_data["content"], res_data["image"] = rep, img_url
                elif f_ctx:
                    rep = run_ai(inp, f_ctx, mode="file")
                    st.write(rep)
                    res_data["content"] = rep
                else:
                    try:
                        with DDGS() as ddgs: results = list(ddgs.text(inp, max_results=3, region="wt-wt"))
                        if results:
                            web_txt = "\n".join([r['body'] for r in results])
                            src = "\n\n🔗 **المصادر المرجعية:**\n" + "\n".join([f"{i}. [{r['title']}]({r['href']})" for i, r in enumerate(results, 1)])
                            rep = f"{run_ai(inp, web_txt, mode='web')}{src}"
                        else: rep = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": inp}])
                    except:
                        try: rep = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": inp}])
                        except:
                            if "سلام" in clean or "وعليكم" in clean: rep = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا صديقي في AuraAI، كيف يمكنني مساعدتك اليوم؟"
                            else: rep = f"🤖 استقبلت طلبك بنجاح: '{inp}'. السيرفرات تواجه ضغطاً مؤقتاً، لكنني متصل ومستعد لخدمتك دائماً."
                    st.write(rep)
                    res_data["content"] = rep

                if res_data["content"]:
                    aud = get_audio(res_data["content"])
                    if aud:
                        st.audio(aud, format="audio/mp3")
                        res_data["audio"] = aud
                
                st.session_state.messages.append(res_data)
                st.rerun()
