import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun

# إعداد واجهة الشات الاحترافية الشبيهة بـ ChatGPT
st.set_page_config(page_title="🤖 مساعدك الذكي المستقل", layout="centered")
st.title("🤖 مساعدك الذكي المستقل")
st.caption("يبحث في الإنترنت ويحلل البيانات تلقائياً")

# تجهيز محرك البحث
search_tool = DuckDuckGoSearchRun()

# إنشاء ذاكرة للمحادثة لحفظ الشات على الشاشة
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "أهلاً بك! أنا هنا للبحث والتحليل تلقائياً دون أي قيود. اسألني عن أي شيء."}]

# عرض الرسائل السابقة على الشاشة بتصميم الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# صندوق إدخال النص السفلي (مثل ChatGPT)
if user_query := st.chat_input("اسألني عن أي شيء..."):
    
    # عرض رسالة المستخدم فوراً
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # معالجة البحث والرد
    with st.chat_message("assistant"):
        with st.spinner("جاري البحث في الويب وتحليل المعلومات..."):
            try:
                # 1. البحث التلقائي
                search_results = search_tool.run(user_query)
                
                # 2. عرض النتيجة (ملاحظة: النماذج المحلية مثل Llama3 لا تعمل على سيرفر Streamlit المجاني، لذا سنعرض نتائج البحث بشكل منسق ومباشر)
                response = f"🌐 **إليك نتائج البحث والتحليل المباشرة:**\n\n{search_results}"
                
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء البحث: {e}")
