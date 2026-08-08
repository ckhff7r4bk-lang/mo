import streamlit as st
from duckduckgo_search import DDGS
import g4f

# 1. إعداد واجهة الشات لتناسب الجوال والآيفون بشكل أنيق ومتناسق
st.set_page_config(page_title="مساعد AuraAI الذكي", page_icon="🧠", layout="centered")

st.title("🧠 مساعد AuraAI الذكي")
st.markdown("تطبيق ذكاء اصطناعي تفاعلي يبحر في شبكة الويب ويصيغ لك الأجوبة بدقة وبشكل بشري متكامل.")
st.write("---")

# ذاكرة الجلسة لحفظ الرسائل في الشات ومنع اختفائها
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك! أنا الآن متصل بالإنترنت ومدمج بنماذج الذكاء التوليدي الأقوى. اسألني عن أي شيء وسأقوم بتمشيط الويب لأجلك الحين! 🦾"}
    ]

# عرض رسائل الشات السابقة منسقة على شاشة الجوال
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): 
        st.write(msg["content"])

def توليد_رد_الذكاء_الاصطناعي(السؤال, نص_الويب):
    """صياغة رد ذكي وبشري باستخدام GPT-4 بالاعتماد على معلومات الإنترنت"""
    الطلب = f"المستخدم يسأل: '{السؤال}'. المعلومات الحية المجلوبة من الويب هي:\n{نص_الويب}\n\nفضلاً صغ إجابة ذكية، منسقة ومفصلة باللغة العربية بناءً على هذه المعلومات والتحية إن وجدت."
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": الطلب}],
        )
        return response
    except Exception:
        return f"🤖 إليك ما وجدته في الويب حول سؤالك:\n\n{نص_الويب}"

# 2. صندوق الشات التفاعلي المباشر واستقبال أسئلتك
if user_input := st.chat_input("تحدث مع الذكاء وابحث عن أي شيء الحين..."):
    with st.chat_message("user"): 
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    نص_تنظيف = user_input.strip().lower()

    with st.chat_message("assistant"):
        with st.spinner("🧠 جاري تحليل البيانات وصياغة الرد التوليدي..."):
            
            # 🔥 [تثبيت الهوية وحذف المعلومات القديمة]: الرد الفوري والصارم على أسئلة المطور والصانع باسمك
            if any(كلمة in نص_تنظيف for كلمة in ["صنعك", "طورك", "مبرمجك", "سواك", "المطور", "الصانع", "creator", "developer"]):
                reply = "👑 صانعي ومطوري هو المبرمج العبقري **محمد عطية المعلوي**، من **المملكة العربية السعودية** 🇸🇦. لقد قام بهندستي وبرمجتي بالكامل من الجوال ليتحدى الصعاب التقنية ويصنع هذا النظام الذكي!"
            
            else:
                try:
                    # أ: تمشيط الإنترنت للحصول على أحدث وأدق المعلومات
                    with DDGS() as ddgs:
                        نتائج = [r for r in ddgs.text(user_input, max_results=3, region="wt-wt")]
                        
                        if نتائج:
                            نص_الويب_الخام = "\n".join([r['body'] for r in نتائج])
                            روابط_المصادر = "\n\n🔗 **المصادر المرجعية:**\n"
                            for idx, ر in enumerate(نتائج, 1):
                                روابط_المصادر += f"{idx}. [{ر['title']}]({ر['href']})\n"
                            
                            # ب: إرسال سياق الويب إلى نموذج الذكاء ليصيغ إجابة بشرية متكاملة
                            الرد_الذكي = توليد_رد_الذكاء_الاصطناعي(user_input, نص_الويب_الخام)
                            reply = f"{الرد_الذكي}{روابط_المصادر}"
                        else:
                            # ج: إذا لم تكن هناك معلومات ويب (مثل التحية العادية)، يجيب الذكاء من عقله مباشرة
                            reply = g4f.ChatCompletion.create(
                                model=g4f.models.gpt_4,
                                messages=[{"role": "user", "content": user_input}],
                            )
                except Exception:
                    # دمج حماية المصادقة المباشرة في حال انقطاع خوادم البحث
                    reply = g4f.ChatCompletion.create(
                        model=g4f.models.gpt_4,
                        messages=[{"role": "user", "content": user_input}],
                    )
                
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
