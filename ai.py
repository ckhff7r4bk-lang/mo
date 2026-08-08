import streamlit as st
from duckduckgo_search import DDGS

# 1. إعدادات شاشة التطبيق الرئيسية لتناسب الجوال والآيفون
st.set_page_config(page_title="مساعد AuraAI الذاتي التطور", page_icon="🧠", layout="centered")

st.title("🧠 مساعد AuraAI الخارق ذاتي التطور")
st.markdown("هذا البوت يبحر في الإنترنت بالكامل، ويعدل معلوماته، وينمي ذاكرته تلقائياً مع كل سؤال جديد ليتطور للأبد!")
st.write("---")

# 2. إنشاء خلايا الذاكرة الدائمة المكتسبة وتحديثها حياً (Session State Memory)
if "خلايا_الذاكرة" not in st.session_state:
    st.session_state.خلايا_الذاكرة = {
        "مرحبا": "مرحباً بك! أنا AuraAI الذكي، بوابتك الشاملة لتمشيط الويب وتنمية المعرفة حياً. كيف يمكنني إسنادك اليوم؟ 🤖",
        "من أنت": "أنا نظام ذكاء اصطناعي محلي متصل بالإنترنت، مبرمج لأطور نفسي ذاتياً وأعدل معلوماتي بناءً على أسئلتك! 🧠",
        "من صنعك": "تم تصميمي وتطويري بالكامل بواسطة مبرمج عبقري ومكافح، يمتلك آيفون وهواوي قديم ويتحدى كل الصعاب! 👑"
    }

if "messages" not in st.session_state: 
    st.session_state.messages = []

# 3. عرض سجل المحادثة السابقة منسقاً على الشاشة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): 
        st.write(msg["content"])

# 4. صندوق الشات واستقبال كلامك وأسئلتك
if user_input := st.chat_input("ابحث عن أي شيء في الإنترنت بالكامل الحين..."):
    # عرض رسالة المستخدم فوراً
    with st.chat_message("user"): 
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    كلمة_البحث = user_input.strip().lower()

    with st.chat_message("assistant"):
        # أ: إذا كانت المعلومة محفوظة ومعدلة مسبقاً في خلايا الذاكرة المتنامية
        if كلمة_البحث in st.session_state.خلايا_الذاكرة:
            reply = f"🧠 **[استدعاء من الذاكرة المطورة ذاتياً]:**\n\n{st.session_state.خلايا_الذاكرة[كلمة_البحث]}"
            st.write(reply)
        
        # ب: إذا كانت معلومة جديدة، يتم تمشيط الويب بالكامل وتعديل خلايا الذاكرة تلقائياً
        else:
            with st.spinner("🔍 جاري تمشيط شبكة الويب بالكامل وتنمية خلايا الذاكرة وتعديلها..."):
                try:
                    # تفعيل البحث العميق للحصول على أفضل الأجوبة من عدة مواقع
                    with DDGS() as ddgs:
                        نتائج = [r for r in ddgs.text(user_input, max_results=2, region="wt-wt")]
                        
                        if نتائج:
                            إجابة_شاملة = "🌐 **[معلومات جديدة تم جلبها وتمشيطها من الويب]:**\n\n"
                            روابط_المصادر = "\n\n🔗 **المصادر والمواقع المرجعية:**\n"
                            
                            for idx, نتيجة in enumerate(نتائج, 1):
                                إجابة_شاملة += f"• {نتيجة['body']}\n\n"
                                روابط_المصادر += f"{idx}. [{نتيجة['title']}]({نتيجة['href']})\n"
                            
                            reply = إجابة_شاملة + روابط_المصادر
                            
                            # 🔥 تنمية وتعديل الذاكرة: حفظ المعلومة الجديدة تلقائياً لكي يتذكرها مستقبلاً دون الحاجة للبحث عنها مجدداً
                            st.session_state.خلايا_الذاكرة[كلمة_البحث] = reply
                        else:
                            reply = "❌ بحثت في شبكة الويب بالكامل ولكن لم أجد نتائج كافية لأتعلم منها حول هذا الموضوع حالياً."
                except Exception:
                    reply = "⚠️ تعذر الاتصال بالشبكة الافتراضية حالياً لتنمية الذاكرة، يرجى إعادة المحاولة."
                    
            st.write(reply)
            
        st.session_state.messages.append({"role": "assistant", "content": reply})
