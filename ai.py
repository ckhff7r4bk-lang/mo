import os
import json
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# --- 1. إعدادات قاعدة البيانات والملفات الدائمة ---
DATABASE_FILE = "ai_brain_db.json"
SETTINGS_FILE = "site_settings.json"

def load_json(filename, default_structure):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_structure

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تحميل البيانات الأساسية
brain_db = load_json(DATABASE_FILE, {"internet_knowledge": [], "chat_history": [], "rules": []})
site_settings = load_json(SETTINGS_FILE, {"theme": "داكن (Dark)", "primary_color": "#4A90E2"})

# إعداد عميل OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE"))

# --- 2. محرك البحث التلقائي واستخراج المعرفة ---
def search_and_learn(query):
    """يبحث في الإنترنت، يستخرج النصوص، ويحفظها في عقل الذكاء الاصطناعي تلقائياً"""
    search_url = f"https://duckduckgo.com{query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('a', class_='result__snippet')
        
        extracted_texts = []
        for res in results[:3]: # أخذ أفضل 3 نتائج
            extracted_texts.append(res.get_text().strip())
        
        if extracted_texts:
            full_knowledge = " | ".join(extracted_texts)
            # حفظ المعرفة المكتسبة حديثاً في الذاكرة الدائمة
            new_knowledge = {"query": query, "info": full_knowledge}
            brain_db["internet_knowledge"].append(new_knowledge)
            save_json(DATABASE_FILE, brain_db)
            return full_knowledge
    except Exception as e:
        return f"فشل البحث التلقائي بسبب: {e}"
    return "لم يتم العثور على نتائج جديدة."

# --- 3. إدارة مظهر الموقع (Theming) ---
bg_color = "#121212" if site_settings["theme"] == "داكن (Dark)" else "#F5F7FA"
text_color = "#FFFFFF" if site_settings["theme"] == "داكن (Dark)" else "#1A1A1A"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. تصميم واجهة المستخدم والموازنة بين الزائر والأدمن ---
st.title("🤖 نظام الذكاء الاصطناعي الباحث والمستقل")
tab_visitor, tab_admin = st.tabs(["💬 ساحة الزوار والدردشة", "🔐 لوحة تحكم الأدمن (المشرف)"])

# ----------------- [ نافذة الزوار ] -----------------
with tab_visitor:
    st.subheader("مرحباً بك! أنا ذكاء اصطناعي أمتلك عقلاً نامياً وأبحث في الإنترنت لأجيبك بدقة.")
    
    # إعدادات المظهر للزوار
    with st.expander("🎨 تخصيص مظهر الموقع (خاص بالزائر)"):
        chosen_theme = st.selectbox("اختر النمط المفضل لديك:", ["داكن (Dark)", "فاتح (Light)"], index=0 if site_settings["theme"] == "داكن (Dark)" else 1)
        if chosen_theme != site_settings["theme"]:
            site_settings["theme"] = chosen_theme
            save_json(SETTINGS_FILE, site_settings)
            st.rerun()

    # صندوق المحادثة
    user_query = st.text_input("اسألني عن أي شيء (سأبحث في الويب تلقائياً إن لم أكن أعرف):", key="visitor_input")
    
    if user_query:
        # 1. البحث التلقائي وحفظ البيانات في العقل
        with st.spinner("🧠 العقل يبحث في الإنترنت ويحفظ المعلومات حالياً..."):
            web_info = search_and_learn(user_query)
            
        # 2. صياغة الرد بناءً على الذاكرة المحفوظة والإنترنت
        all_past_knowledge = "\n".join([f"- {k['info']}" for k in brain_db["internet_knowledge"][-5:]]) # آخر 5 معلومات مكتسبة
        
        system_instruction = f"""
        أنت ذكاء اصطناعي فائق الذكاء، تسولف بشكل طبيعي وممتاز وودي باللغة العربية كصديق حقيقي.
        لديك عقل نامٍ، وقد قمت بالبحث في الإنترنت وحفظت هذه المعلومات المفيدة لتجيب منها:
        {web_info}
        
        سياق من معلوماتك السابقة المحفوظة:
        {all_past_knowledge}
        """
        
        with st.spinner("🤖 صياغة الرد الذكي..."):
            try:
                chat_res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_query}
                    ]
                )
                ai_reply = chat_res.choices.message.content
                st.write("### 🤖 الرد المطور:")
                st.write(ai_reply)
                
                # حفظ تاريخ المحادثات للزوار ليتعلم منها النظام
                brain_db["chat_history"].append({"user": user_query, "ai": ai_reply})
                save_json(DATABASE_FILE, brain_db)
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الرد: {e}")

# ----------------- [ لوحة تحكم الأدمن ] -----------------
with tab_admin:
    st.subheader("🔐 صلاحيات المالك الحصرية")
    password = st.text_input("أدخل كلمة مرور الأدمن للوصول المباشر:", type="password")
    
    # كلمة المرور الافتراضية (يمكنك تعديلها هنا)
    if password == "admin123":
        st.success("تم التحقق بنجاح! أنت تملك الصلاحية الكاملة الآن.")
        
        # التحكم بالمعلومات المحفوظة
        st.write("### 📁 إدارة المعرفة المحفوظة في عقل النظام")
        st.write("هذه هي البيانات التي جمعها الذكاء الاصطناعي بنفسه من بحث الإنترنت والزوار:")
        
        if brain_db["internet_knowledge"]:
            for idx, item in enumerate(brain_db["internet_knowledge"]):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.text_area(f"معلومة رقم {idx+1} (عن بحث: {item['query']})", value=item['info'], key=f"info_{idx}")
                with col2:
                    if st.button("🗑️ حذف", key=f"del_{idx}"):
                        brain_db["internet_knowledge"].pop(idx)
                        save_json(DATABASE_FILE, brain_db)
                        st.success("تم حذف المعلومة من عقل النظام!")
                        st.rerun()
        else:
            st.info("لا توجد معلومات محفوظة في قاعدة البيانات حتى الآن.")
            
        # تصفير الذاكرة بالكامل
        if st.button("🚨 مسح وعمل فورمت كامل لعقل النظام"):
            brain_db = {"internet_knowledge": [], "chat_history": [], "rules": []}
            save_json(DATABASE_FILE, brain_db)
            st.success("تمت إعادة النظام إلى نقطة الصفر!")
            st.rerun()
            
    elif password != "":
        st.error("كلمة المرور غير صحيحة! الصلاحية مرفوضة.")
