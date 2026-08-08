import streamlit as st
import json
import os
from openai import OpenAI

# إعداد مكتبة OpenAI
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = None

# 1. إعداد ملف الحفظ التلقائي
SAVE_FILE = "chat_history_backup.json"

def load_chat_backup():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"حدث خطأ أثناء تحميل ملف النسخ الاحتياطي: {e}")
            return {}
    return {}

def save_chat_backup():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.rooms, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"فشل الحفظ التلقائي للمحادثة: {e}")

# 2. تهيئة الـ Session State
if "rooms" not in st.session_state:
    st.session_state.rooms = load_chat_backup()

if "current_room" not in st.session_state:
    st.session_state.current_room = list(st.session_state.rooms.keys()) if st.session_state.rooms else "المحادثة الأولى"

if st.session_state.current_room not in st.session_state.rooms:
    st.session_state.rooms[st.session_state.current_room] = []
    save_chat_backup()

# ==========================================
# 3. القائمة الجانبية (Sidebar) لإدارة الغرف
# ==========================================
with st.sidebar:
    st.title("📂 إدارة المحادثات")
    
    # إنشاء غرفة جديدة
    new_room_name = st.text_input("➕ إنشاء غرفة محادثة جديدة:", key="new_room_input")
    if st.button("إنشاء الغرفة", use_container_width=True) and new_room_name.strip():
        room_name_clean = new_room_name.strip()
        if room_name_clean not in st.session_state.rooms:
            st.session_state.rooms[room_name_clean] = []
            st.session_state.current_room = room_name_clean
            save_chat_backup()
            st.rerun()

    st.divider()

    # عرض الغرف الحالية
    st.subheader("💬 غرفك الحالية")
    for room in list(st.session_state.rooms.keys()):
        col1, col2 = st.columns([0.8, 0.2])
        
        with col1:
            is_active = room == st.session_state.current_room
            label = f"🔹 {room}" if is_active else f"📄 {room}"
            if st.button(label, key=f"select_{room}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.current_room = room
                st.rerun()
                
        with col2:
            if st.button("🗑️", key=f"delete_{room}", use_container_width=True):
                del st.session_state.rooms[room]
                if st.session_state.current_room == room:
                    st.session_state.current_room = list(st.session_state.rooms.keys()) if st.session_state.rooms else "المحادثة الأولى"
                    if st.session_state.current_room not in st.session_state.rooms:
                        st.session_state.rooms[st.session_state.current_room] = []
                save_chat_backup()
                st.rerun()

# ==========================================
# 4. الشاشة الرئيسية وعرض الرسائل السابقة
# ==========================================
st.title(f"💬 {st.session_state.current_room}")

current_chat_history = st.session_state.rooms[st.session_state.current_room]

# عرض الرسائل المخزنة في الغرفة الحالية
for chat in current_chat_history:
    role = chat.get("role", "user")
    content = chat.get("content", "")
    is_file = chat.get("is_file", False)
    file_type = chat.get("file_type", "")
    
    if role == "user":
        with st.chat_message("user", avatar="🧑‍💻"):
            if is_file and "image" in file_type:
                st.image(content, caption="الصورة المرفوعة")
            else:
                st.markdown(content)
    elif role == "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(content)

# ==========================================
# 5. منطقة تحميل الملفات وإدخال الرسائل الجديد
# ==========================================

# إضافة حقل تحميل الملفات في أسفل الشاشة قبل حقل النص
uploaded_file = st.file_uploader("📎 ارفق صورة أو ملف نصي للمحادثة:", type=["png", "jpg", "jpeg", "txt", "md", "pdf"])

if user_input := st.chat_input("اكتب رسالتك هنا..."):
    if not client:
        st.error("⚠️ لم يتم العثور على مفتاح OpenAI API Key في الإعدادات.")
        st.stop()

    context_text = user_input
    file_data_to_save = None

    # معالجة الملف المرفوع إن وجد
    if uploaded_file is not None:
        file_type = uploaded_file.type
        
        # حالة 1: الملف المرفوع صورة
        if "image" in file_type:
            # لقراءة وتحليل الصور يفضل استخدام gpt-4o، هنا سنقوم بعرضها وحفظها
            # ملاحظة: لحفظ الصورة في JSON نقوم بتحويلها لـ Base64 أو مسار محلي، للتبسيط سنعرضها هنا
            with st.chat_message("user", avatar="🧑‍💻"):
                st.image(uploaded_file, caption="الصورة المرفوعة")
            current_chat_history.append({"role": "user", "content": f"[صورة مرفوعة: {uploaded_file.name}]", "is_file": True, "file_type": file_type})
            context_text = f"المستخدم أرسل صورة باسم ({uploaded_file.name}). ورسالته هي: {user_input}"
            
        # حالة 2: الملف المرفوع ملف نصي
        elif "text" in file_type or uploaded_file.name.endswith(('.txt', '.md')):
            file_text = uploaded_file.read().decode("utf-8")
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(f"📄 **تم رفع ملف:** `{uploaded_file.name}`")
            current_chat_history.append({"role": "user", "content": f"📄 **ملف مرفق:** {uploaded_file.name}", "is_file": True, "file_type": file_type})
            # دمج محتوى الملف مع رسالة المستخدم ليفهمها الذكاء الاصطناعي
            context_text = f"محتوى الملف المرفق ({uploaded_file.name}):\n```\n{file_text}\n```\n\nسؤال المستخدم حول الملف: {user_input}"

    # عرض رسالة النص الحالية للمستخدم
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)
    
    # إضافة نص المستخدم النهائي للذاكرة
    current_chat_history.append({"role": "user", "content": user_input})
    save_chat_backup()

    # إنشاء مصفوفة الرسائل المخصصة لإرسالها للـ API (تشمل السياق الجديد)
    api_messages = [
        {"role": "system", "content": "أنت مساعد ذكي ومفيد تتحدث باللغة العربية بطلاقة وتستطيع تحليل الملفات المرفقة بنصوصها."}
    ]
    # إضافة التاريخ القديم
    for chat in current_chat_history[:-1]:
        api_messages.append({"role": chat["role"], "content": chat["content"]})
    # إضافة الرسالة الأخيرة بالسياق الكامل للملف
    api_messages.append({"role": "user", "content": context_text})

    # بدء توليد الرد مع البث المباشر
    with st.chat_message("assistant", avatar="🤖"):
        try:
            stream_response = client.chat.completions.create(
                model="gpt-4o", 
                messages=api_messages,
                stream=True,
            )
            
            full_response = st.write_stream(stream_response)
            
            # حفظ رد المساعد
            current_chat_history.append({"role": "assistant", "content": full_response})
            save_chat_backup()
            st.rerun()
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالـ API: {e}")
