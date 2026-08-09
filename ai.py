import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
import requests
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="AI Pro", 
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("<style>.main-title { font-size: 2.2rem; font-weight: bold; text-align: center; color: #1E88E5; margin-bottom: 5px; }.sub-title { font-size: 1rem; text-align: center; color: #757575; margin-bottom: 25px; }.evolution-box { background-color: #f0fdf4; padding: 12px; border-radius: 8px; border-right: 5px solid #22c55e; font-size: 0.9rem; margin-bottom: 15px; color: #14532d; }.priority-tag { background-color: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; padding: 4px 10px; border-radius: 15px; font-size: 0.85rem; display: inline-block; margin: 2px; }.developer-footer { position: fixed; bottom: 10px; left: 0; right: 0; text-align: center; font-size: 0.85rem; color: #888; background-color: rgba(255,255,255,0.9); padding: 5px; z-index: 100; border-top: 1px solid #eee; }@media (prefers-color-scheme: dark) {.evolution-box { background-color: #14532d; color: #bbf7d0; border-right: 5px solid #22c55e; }.priority-tag { background-color: #1e3a8a; color: #93c5fd; border: 1px solid #1e40af; }.developer-footer { background-color: rgba(14,17,23,0.9); color: #aaa; border-top: 1px solid #262730; }}</style>", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, date_only TEXT, user_question TEXT, web_context TEXT, ai_response TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS evolution_knowledge (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, topic TEXT, learned_fact TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS admin_priorities (id INTEGER PRIMARY KEY AUTOINCREMENT, keyword TEXT UNIQUE)")
    conn.commit()
    conn.close()

def save_to_history(question, web_context, response):
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("INSERT INTO history (timestamp, date_only, user_question, web_context, ai_response) VALUES (?, ?, ?, ?, ?)", (now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d"), question, web_context, response))
    conn.commit()
    conn.close()

def save_learned_fact(topic, learned_fact):
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO evolution_knowledge (timestamp, topic, learned_fact) VALUES (?, ?, ?)", (timestamp, topic, learned_fact))
    conn.commit()
    conn.close()

def load_all_learned_knowledge():
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT topic, learned_fact FROM evolution_knowledge ORDER BY id DESC LIMIT 15")
    rows = cursor.fetchall()
    conn.close()
    knowledge_text = ""
    for row in rows:
        knowledge_text += "- Learned Topic: " + str(row[0]) + " Info: " + str(row[1]) + "\n"
    return knowledge_text

def get_evolution_df():
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM evolution_knowledge ORDER BY id DESC", conn)
    conn.close()
    return df

def add_priority_keyword(keyword):
    if keyword.strip():
        conn = sqlite3.connect("app_data.db", check_same_thread=False)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT OR IGNORE INTO admin_priorities (keyword) VALUES (?)", (keyword.strip(),))
            conn.commit()
        except Exception:
            pass
        conn.close()

def remove_priority_keyword(keyword_txt):
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admin_priorities WHERE keyword=?", (keyword_txt,))
    conn.commit()
    conn.close()

def get_priority_keywords():
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT keyword FROM admin_priorities")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def clear_all_db():
    conn = sqlite3.connect("app_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    cursor.execute("DELETE FROM evolution_knowledge")
    conn.commit()
    conn.close()

init_db()

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
        payload = {"messages": [{"role": "user", "content": prompt_text}], "model": "llama", "json": False}
        response = requests.post(url, json=payload, timeout=25)
        if response.status_code == 200 and response.text.strip():
            return response.text
        return "N/A"
    except Exception:
        return "Error"

with st.sidebar:
    st.header("🔑 Control Panel")
    admin_password = st.text_input("Password:", type="password")
    if admin_password == "admin123":
        st.success("🔓 Welcome Mohammed Al-Malwi")
        st.write("---")
        st.subheader("🎯 Target Priorities")
        new_keyword = st.text_input("Add new topic:")
        if st.button("➕ Add"):
            add_priority_keyword(new_keyword)
            st.success("Added!")
            st.rerun()
        current_priorities = get_priority_keywords()
        if current_priorities:
            for kw in current_priorities:
                col_txt, col_btn = st.columns([4, 1])
                with col_txt:
                    st.markdown("<span class='priority-tag'>🎯 " + str(kw) + "</span>", unsafe_allow_html=True)
                with col_btn:
                    if st.button("❌", key="del_" + str(kw)):
                        remove_priority_keyword(kw)
                        st.rerun()
        st.write("---")
        st.subheader("📚 Evolution Memory")
        st.dataframe(get_evolution_df())
        if st.button("🗑️ Clear Database"):
            clear_all_db()
            st.success("Cleared!")
            st.rerun()
    elif admin_password != "":
        st.error("Incorrect password!")

st.markdown('<div class="main-title">🧠 المساعد الذكي الخارق</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">نظام محادثة ذكي يبحث في الويب، ويتطور تلقائياً وفق أولويات واهتمامات مبرمجه الأول</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 أهلاً بك في تطبيقي الذكي المتطور! أنا نظام مستقل يبحث في الويب، ويستخلص المعارف، ويحدث معلوماته تلقائياً لمساعدتك بذكاء."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_query := st.chat_input("اكتب سؤالك أو ما تبحث عنه هنا..."):
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        with st.spinner("🔍..."):
            extracted_web_context = ""
            if search_tool:
                try:
                    extracted_web_context = search_tool.invoke(user_query)
                except Exception:
                    extracted_web_context = ""
            past_knowledge = load_all_learned_knowledge()
            priority_list = get_priority_keywords()
            priority_instruction = ""
            if priority_list:
                priority_instruction = "This app is developed by Mohammed Al-Malwi. Focus highly on these topics: " + ", ".join(priority_list) + "\n"
            system_instruction = "You are an advanced AI assistant responding in structured Arabic like ChatGPT. " + priority_instruction + " Previously learned: " + past_knowledge + " Current web details: " + extracted_web_context
            conversation_history = ""
            for m in st.session_state.messages[-4:]:
                conversation_history += str(m['role']) + ": " + str(m['content']) + "\n"
            final_prompt = system_instruction + "\n\nConversation:\n" + conversation_history + "\nUser: " + user_query + "\nAssistant:"
            ai_response = query_ai_engine(final_prompt)
            if ai_response == "N/A" or ai_response == "Error":
                ai_response = "⚠️ تعذر الاتصال بالخادم الذكي حالياً، يرجى إعادة إرسال سؤالك."
            st.write(ai_response)
            save_to_history(user_query, extracted_web_context, ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        if extracted_web_context:
            focus_context = ""
            if priority_list:
                focus_context = " with special focus on: " + ", ".join(priority_list)
            evolution_prompt = "Based on the text, extract one important single-line fact in Arabic " + focus_context + " to save: " + extracted_web_context
            new_fact = query_ai_engine(evolution_prompt)
            if new_fact and new_fact != "N/A" and new_fact != "Error":
                save_learned_fact(user_query[:30], new_fact.strip())
                st.markdown('<div class="evolution-box">🌱 <b>تحديث ذاتي للنظام تلقائياً:</b> تم تحليل بيانات الويب وتخزينها: ' + str(new_fact.strip()) + '</div>', unsafe_allow_html=True)

st.markdown('<div class="developer-footer">تم التطوير والبرمجة بواسطة المبرمج: 💻 <b>محمد المعلوي</b> 🇸🇦</div>', unsafe_allow_html=True)
