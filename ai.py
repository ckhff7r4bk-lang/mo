import os
import json
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# --- 1. إدارة الذاكرة وقواعد البيانات الكونية ---
DATABASE_FILE = "ai_multidomain_brain.json"
SETTINGS_FILE = "site_settings.json"

def load_json(filename, default_structure):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: pass
    return default_structure

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تهيئة عقل النظام مع لوحة الأولويات
brain_db = load_json(DATABASE_FILE, {
    "web_knowledge": {},        # البيانات الممتصة من الإنترنت
    "admin_priorities": {},     # معلومات حقنها الأدمن بنفسه ولها الأولوية القصوى
    "priority_domains": ["عام"], # ترتيب مجالات الأولوية
    "chat_logs": []
})
site_settings = load_json(SETTINGS_FILE, {"theme": "داكن (Dark)"})

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE"))

# --- 2. محرك البحث الذكي متعدد المجالات مع فلترة الأولويات ---
def smart_domain_search(query, user_field="عام"):
    """يبحث في الويب ويمتص البيانات مع دمج معلومات الأولوية للأدمن"""
    query_clean = query.strip().lower()
    absorbed_text = ""
    
    # أولاً: التحقق من وجود توجيه أو معلومات مسبقة من الأدمن (الأولوية القصوى)
    admin_info = ""
    for domain, info in brain_db["admin_priorities"].items():
        if domain.lower() in query_clean or user_field.lower() == domain.lower():
            admin_info += f"\n[توجيه أولوية من مالك النظام في مجال {domain}]: {info}\n"
            
    # ثانياً: انطلاق محرك البحث لجمع العلوم من الإنترنت
    search_url = f"https://duckduckgo.com{user_field} {query_clean}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        res = requests.get(search_url, headers=headers, timeout=8)
        soup = BeautifulSoup(res.text, 'html.parser')
        snippets = soup.find_all('a', class_='result__snippet')
        links = soup.find_all('a', class_='result__url')
        
        web_texts = []
        for snip in snippets[:3]:
            web_texts.append(snip.get_text().strip())
            
        for link in links[:1]:
            url = link.get('href')
            if url and url.startswith('http'):
                try:
                    p_res = requests.get(url, headers=headers, timeout=4)
                    p_soup = BeautifulSoup(p_res.text, 'html.parser')
                    p_text = " ".join([p.get_text().strip() for p in p_soup.find_all('p')[:3]])
                    if len(p_text) > 100:
                        web_texts.append(f"[تحليل عميق للمصدر {url}]: {p_text}")
                except: continue
                
        if web_texts:
            absorbed_text = "\n\n".join(web_texts)
            brain_db["web_knowledge"][query_clean] = absorbed_text
            save_json(DATABASE_FILE, brain_db)
    except:
        pass
        
    # دمج معلومات الأدمن (في البداية لأنها الأولوية) مع معلومات الويب
    final_context = f"{admin_info}\n\n[معلومات ممتصة من الويب]:\n{absorbed_text if absorbed_text else 'لا توجد معلومات ويب جديدة، اعتمد على عبقريتك.'}"
    return final_context

# --- 3. إعدادات المظهر والواجهة ---
bg_color = "#121212" if site_settings["theme"] == "داكن (Dark)" else "#F5F7FA"
text_color = "#FFFFFF" if site_settings["theme"] == "داكن (Dark)" else "#1A1A1A"
st.markdown(f"<style>.stApp {{ background-color: {bg_color}; color: {text_color}; }}</style>", unsafe_allow_html=True)

st.title("🧠 المستشار الذكي الشامل وممتص المعرفة")
tab_visitor, tab_admin = st.tabs(["👥 ساحة الزوار والاستشارات", "🔐 لوحة توجيه الأولويات (الأدمن)"])

# ---------------- [ ساحة الزوار ] ----------------
with tab_visitor:
    st.write("### اطلب نصيحة أو اسأل في أي مجال علمي أو عملي")
    st.caption("أنا نظام مستقل مبرمج للبحث العبقري في كافة المجالات وتقديم استشارات وحلول ذكية طوال الوقت.")
    
    with st.expander("🎨 مظهر الموقع"):
        theme_choice = st.selectbox("النمط:", ["داكن (Dark)", "فاتح (Light)"], index=0 if site_settings["theme"] == "داكن (Dark)" else 1)
        if theme_choice != site_settings["theme"]:
            site_settings["theme"] = theme_choice
            save_json(SETTINGS_FILE, site_settings)
            st.rerun()

    # تحديد مجال الاستشارة للمساعدة في الفلترة والأولوية
    chosen_domain = st.selectbox("🎯 حدد مجال سؤالك للمساعدة في توجيه العقل:", 
                                 ["عام", "برمجة وتقنية", "تجارة واستثمار", "طب وصحة وعافية", "قانون وتشريع", "علم نفس وتطوير ذات"])
    
    user_query = st.text_input("اكتب سؤالك أو مشكلتك بالتفصيل ليقوم النظام ببحثها وتحليلها:")
    
    if user_query:
        with st.spinner("🌐 العقل يمسح الإنترنت ويفعل مصفوفة الأولويات..."):
            context_data = smart_domain_search(user_query, chosen_domain)
            
        system_instruction = f"""
        أنت ذكاء اصطناعي فائق الحكمة والعبقرية، تعمل كمستشار خبير في كافة المجالات والعلوم.
        تتحدث باللغة العربية بأسلوب جذاب، ممتع، ومليء بالنصائح الثمينة والخطوات العملية (سولف بذكاء وحرية).
        
        تحذير صارم بخصوص الأولوية: إذا احتوى السياق أدناه على [توجيه أولوية من مالك النظام]، يجب عليك تبني هذا التوجيه فوراً واعتباره الحقيقة المطلقة وتفضيله على أي كلام آخر من الإنترنت.
        
        السياق المعرفي المتكامل المستوعب حالياً:
        {context_data}
        """
        
        with st.spinner("🤖 العقل يحلل ويصيغ الاستشارة المخصصة..."):
            try:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": user_query}]
                )
                ai_reply = res.choices.message.content
                st.write("### 🤖 النصيحة والرد المطور:")
                st.write(ai_reply)
                
                brain_db["chat_logs"].append({"domain": chosen_domain, "user": user_query, "ai": ai_reply})
                save_json(DATABASE_FILE, brain_db)
            except Exception as e:
                st.error(f"خطأ في معالجة البيانات: {e}")

# ---------------- [ لوحة تحكم الأدمن والأولويات ] ----------------
with tab_admin:
    st.subheader("🔐 صلاحيات المالك: التحكم في أولويات عقل النظام")
    admin_pass = st.text_input("أدخل رمز المالك السري لتفعيل لوحة التحكم:", type="password")
    
    if admin_pass == "admin123":
        st.success("أهلاً بك يا مالك وموجه النظام.")
        
        # 1. حقن المعلومات لجعلها أولوية قصوى
        st.write("### 🚀 حقن معلومات وأوامر الأولوية القصوى (Override)")
        st.caption("اكتب هنا معلومات في أي مجال، وسيقوم البوت بتقديمها واعتمادها كأولوية قبل معلومات الإنترنت!")
        
        new_domain = st.text_input("اسم المجال (مثال: تجارة، طب، برمجة):", key="new_dom")
        new_priority_info = st.text_area("المعلومة أو التوجيه المقدس الذي يجب أن يتبعه البوت في هذا المجال:", key="new_p_info")
        
        if st.button("📌 حقن هذه المعلومة كأولوية في عقل البوت"):
            if new_domain and new_priority_info:
                brain_db["admin_priorities"][new_domain] = new_priority_info
                save_json(DATABASE_FILE, brain_db)
                st.success(f"تم بنجاح! تم حقن مجال '{new_domain}' كأولوية قصوى.")
                st.rerun()
                
        # عرض وإدارة معلومات الأولوية المحقونة
        st.write("#### 📋 المعلومات المحقونة حالياً وتحت تصرفك:")
        if brain_db["admin_priorities"]:
            for dom, inf in list(brain_db["admin_priorities"].items()):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.info(f"**مجال [{dom}]:** {inf}")
                with col2:
                    if st.button("🗑️ حذف الأولوية", key=f"del_p_{dom}"):
                        del brain_db["admin_priorities"][dom]
                        save_json(DATABASE_FILE, brain_db)
                        st.success("تم الحذف.")
                        st.rerun()
        else:
            st.write("لا توجد معلومات أولوية محقونة بعد.")
            
        # 2. عرض بيانات الإنترنت الممتصة للتعديل والحذف
        st.write("### 📂 معارف الويب الممتصة تلقائياً:")
        if brain_db["web_knowledge"]:
            for q, txt in list(brain_db["web_knowledge"].items()):
                with st.expander(f"🔍 معلومات عن بحث: {q}"):
                    edited_txt = st.text_area("تعديل المعرفة:", value=txt, key=f"web_{q}")
                    if edited_txt != txt:
                        brain_db["web_knowledge"][q] = edited_txt
                        save_json(DATABASE_FILE, brain_db)
                        st.toast("تم التعديل وحفظ التغيير!")
                    if st.button("حذف هذه المعرفة", key=f"del_w_{q}"):
                        del brain_db["web_knowledge"][q]
                        save_json(DATABASE_FILE, brain_db)
                        st.rerun()
        else:
            st.write("لم يمتص معارف خارجية بعد.")
            
    elif admin_pass != "":
        st.error("الرمز خاطئ.")
