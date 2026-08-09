import streamlit as st
from openai import OpenAI
from langchain_community.tools import DuckDuckGoSearchRun

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="🤖 المساعد الذكي المجاني الشامل", layout="wide")
st.title("🤖 المساعد الذكي المجاني الشامل")
st.caption("ذكاء اصطناعي قوي + بحث مباشر في الإنترنت = مجاني بالكامل 100% وبدون تكلفة")

# 2. تجهيز أداة البحث المجانية (DuckDuckGo)
try:
    search_tool = DuckDuckGoSearchRun()
except Exception as e:
    search_tool = None

# 3. إعداد القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات المجانية")
    st.markdown("[اضغط هنا للحصول على مفتاحك المجاني من OpenRouter](https://openrouter.ai)")
    
    # إدخال المفتاح المجاني
    api_key = st.text_input("أدخل مفتاح OpenRouter المجاني:", type="password")
    
    # قائمة النماذج المتاحة مجاناً بالكامل على المنصة
    model_options = {
        "DeepSeek V3 (الذكاء الأقوى والمجاني)": "deepseek/deepseek-chat",
        "Meta Llama 3.1 (نموذج فيسبوك المتطور)": "meta-llama/llama-3.1-8b-instruct:free",
        "Google Gemma 2 (نموذج جوجل السريع والمجاني)": "google/gemma-2-9b-it:free"
    }
    
    selected_model_name = st.selectbox("اختر عقل الذكاء الاصطناعي (كلها مجانية):", list(model_options.keys()))
    selected_model_id = model_options[selected_model_name]
    
    # خيار تفعيل تصفح الإنترنت
    web_search_enabled = st.checkbox("🌐 تفعيل البحث المباشر في الإنترنت", value=False)

# 4. تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 أهلاً بك! أنا مساعدك الذكي المجاني. يمكنني الإجابة مباشرة، أو تصفح الإنترنت وتلخيص النتائج لك إذا قمت بتفعيل خيار البحث الجانبي!"}
    ]

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. معالجة الإدخال
if user_query := st.chat_input("اكتب سؤالك هنا..."):
    
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    if not api_key:
        st.error("⚠️ يرجى إدخال مفتاح OpenRouter المجاني من القائمة الجانبية لتشغيل الذكاء الاصطناعي.")
    else:
        with st.chat_message("assistant"):
            # الخطوة أ: إذا كان البحث في الويب مفعلاً
            context_info = ""
            if web_search_enabled and search_tool:
                with st.spinner("🔍 جاري تصفح الويب مجاناً لجلب أحدث المعلومات..."):
                    try:
                        context_info = search_tool.invoke(user_query)
                    except Exception as e:
                        st.warning(f"تعذر جلب بيانات من الإنترنت: {e}، سيتم الرد بناءً على معلومات الذكاء الاصطناعي فقط.")

            # الخطوة ب: إرسال البيانات للذكاء الاصطناعي ليقوم بالصياغة والرد
            with st.spinner(f"🧠 جاري التحليل والصياغة باستخدام {selected_model_name}..."):
                try:
                    client = OpenAI(
                        base_url="https://openrouter.aiapi/v1",
                        api_key=api_key,
                    )
                    
                    # بناء تاريخ المحادثة
                    formatted_messages = []
                    
                    # إذا توفرت معلومات من البحث، ندمجها في رسالة النظام لتوجيه النموذج
                    if context_info:
                        formatted_messages.append({
                            "role": "system",
                            "content": f"استخدم نتائج البحث الحالية التالية للإجابة على سؤال المستخدم بدقة واحترافية باللغة العربية:\n\n{context_info}"
                        })
                    
                    # إضافة سياق المحادثة المعتاد
                    for m in st.session_state.messages:
                        formatted_messages.append({"role": m["role"], "content": m["content"]})
                    
                    # طلب الرد من النموذج المجاني
                    completion = client.chat.completions.create(
                        model=selected_model_id,
                        messages=formatted_messages
                    )
                    
                    response = completion.choices.message.content
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"❌ فشل الاتصال بالنموذج الذكي: {str(e)}")
