import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
import requests
import sqlite3
import pandas as pd
from datetime import datetime

# 1. إعداد واجهة التطبيق واحتواء عناصر التصميم المتقدمة
st.set_page_config(
    page_title="المساعد الذكي الخارق Pro", 
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تخصيص واجهة التطبيق وحقوق المطور عبر CSS المتقدم
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: bold; text-align: center; color: #1E88E5; margin-bottom: 5px; }
    .sub-title { font-size: 1rem; text-align: center; color: #757575; margin-bottom: 25px; }
    .developer-footer { position: fixed; bottom: 10px; left: 0; right: 0; text-align: center; font-size: 0.85rem; color: #888; background-color: rgba(255,255,255,0.9); padding: 5px; z-index: 100; border-top: 1px solid #eee; }
    @media (prefers-color-scheme: dark) {
        .developer-footer { background-color: rgba(14,17,23,0.9); color: #aaa; border-top: 1px solid #262730; }
    }
    </style>
""", unsafe_allow_html=True)

# 2. إدارة قاعدة البيانات المحلية (SQLite) وتخزين البيانات المجمعة
def init_db():
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            date_only TEXT,
            user_question TEXT,
            ai_response TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(question, response):
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date_only = now.strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO history (timestamp, date_only, user_question, ai_response) VALUES (?, ?, ?, ?)", 
        (timestamp, date_only, question, response)
    )
    conn.commit()
    conn.close()

def get_all_history():
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)
    conn.close()
    return df

def clear_db():
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()

# تفعيل قاعدة البيانات وتجهيزها للعمل
init_db()

# 3. إعداد محرك البحث ودالة الاستدعاء المجانية للذكاء الاصطناعي
@st.cache_resource
def load_search_engine():
    try:
        return DuckDuckGoSearchRun()
    except Exception:
        return None

search_tool = load_search_engine()

def query_ai_engine(prompt_text):
    try:
        url = "https://pollinations.ai"
        payload = {
            "messages": [{"role": "user", "content": prompt_text}],
            "model": "searchgpt",
            "json": False
        }
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code == 200:
            return response.text
        return "⚠️ النظام يواجه ضغطاً خفيفاً حالياً، يرجى إعادة محاولة إرسال رسالتك."
    except Exception:
        return "❌ فشل الاتصال بخادم المعالجة الآمن، تحقق من اتصال الجوال بالإنترنت."

# 4. لوحة تحكم الآدمن المتقدمة (Admin Control Panel) داخل الشريط الجانبي السرّي
with st.sidebar:
    st.header("🔑 بوابة تحكم المبرمج")
    admin_password = st.text_input("أدخل كلمة مرور الآدمن السرية:", type="password")
    
    # كلمة المرور الافتراضية
    if admin_password == "admin123":
        st.success("🔓 تم تسجيل الدخول بصلاحية الإدارة المطلقة")
        st.write("---")
        
        df_logs = get_all_history()
        
        # عرض المؤشرات السريعة
        st.metric(label="📊 إجمالي الاستفسارات المجمعة", value=len(df_logs))
        
        if not df_logs.empty:
            # إضافة رسم بياني يوضح معدل الاستخدام اليومي للتطبيق
            st.subheader("📈 نشاط الاستخدام اليومي")
            daily_counts = df_logs['date_only'].value_counts().sort_index()
            st.line_chart(daily_counts)
            
            # محرك بحث داخلي خاص بالآدمن للتفتيش في السجلات
            st.subheader("🔍 تصفية والبحث في البيانات")
            search_keyword = st.text_input("ابحث عن كلمة معينة في الأسئلة المجمعة:")
            if search_keyword:
                filtered_df = df_logs[df_logs['user_question'].str.contains(search_keyword, case=False, na=False)]
                st.dataframe(filtered_df[['timestamp', 'user_question', 'ai_response']])
            else:
                st.dataframe(df_logs[['id', 'timestamp', 'user_question', 'ai_response']])
            
            # أدوات التحكم بالبيانات واستخراج التقارير
            st.subheader("⚙️ أدوات البيانات")
            csv = df_logs.to_csv(index=False).encode('utf-8')
            st.download_button("📥 تحميل كافة البيانات (Excel / CSV)", data=csv, file_name="developer_collected_data.csv", mime="text/csv")
            
            st.write("")
            if st.button("🗑️ تصفير ومسح قاعدة البيانات نهائياً"):
                clear_db()
                st.success("تم مسح السجلات وإعادة تهيئة النظام بنجاح!")
                st.rerun()
        else:
            st.info("قاعدة البيانات فارغة حالياً، لا توجد معلومات مجمعة بعد.")
            
    elif admin_password != "":
        st.error("❌ كلمة المرور غير صحيحة!")

# الواجهة الأساسية التي يراها المستخدمون العاديون والتطبيق بعد التثبيت
st.markdown('<div class="main-title">🧠 المساعد الذكي الخارق</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">نظام محادثة وبحث فوري ذكي يجمع ويحلل البيانات تلقائياً</div>', unsafe_allow_html=True)

# 5. إدارة جلسة ذاكرة الشات المؤقتة على الشاشة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 أهلاً بك في تطبيقي الذكي المتطور! تم تطوير هذا النظام للبحث في الويب وتلخيص المعلومات فوراً وبشكل مجاني تماماً."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. استقبال مدخلات المستخدمين وحفظها تلقائياً داخل قاعدة البيانات
if user_query := st.chat_input("اكتب سؤالك أو ما تبحث عنه هنا..."):
    
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        with st.spinner("🔍 جاري تصفح الويب واستخراج البيانات وتحليلها..."):
            
            context_info = ""
            if search_tool:
                try:
                    context_info = search_tool.invoke(user_query)
                except Exception:
                    context_info = ""

            system_instruction = "أنت مساعد ذكي ومبرمج باحترافية لتجيب بدقة ووضوح باللغة العربية."
            if context_info:
                system_instruction += f" اعتمد على المعلومات الحية الموثوقة التالية للإجابة على سؤال المستخدم بشكل مفصل ومنظم: {context_info}"
            
            final_prompt = f"{system_instruction}\n\nالسؤال المطلوب الإجابة عليه الآن هو: {user_query}"
            
            ai_response = query_ai_engine(final_prompt)
            st.write(ai_response)
            
            # الحفظ التلقائي والفوري للبيانات المجمعة في الـ Database
            save_to_db(user_query, ai_response)
            
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

# التوقيع البرمجي الثابت لحفظ حقوقك الكاملة كمطور
st.markdown('<div class="developer-footer">تم التطوير والبرمجة بواسطة المبرمج: 💻 <b>محمد المعلوي</b></div>', unsafe_allow_html=True)
