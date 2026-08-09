import chainlit as cl
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.llms import Ollama

# إعداد محرك البحث ونموذج الذكاء الاصطناعي المحلي
search_tool = DuckDuckGoSearchRun()

# نستخدم نموذج Llama 3 المجاني والمستقل تماماً على جهازك
try:
    llm = Ollama(model="llama3", temperature=0.3)
except Exception:
    llm = None

@cl.on_chat_start
async def start():
    """هذه الدالة ترحب بالمستخدم عند فتح واجهة الشات لأول مرة"""
    await cl.Message(
        content="👋 أهلاً بك في نظامك المستقل! أنا هنا للبحث والتحليل تلقائياً دون أي قيود. اسألني عن أي شيء."
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """هذه الدالة تستقبل رسالة المستخدم وتجعله يبحث ويحلل تلقائياً"""
    
    # إرسال رسالة انتظار للمستخدم أثناء المعالجة والبحث
    msg = cl.Message(content="🔄 جاري البحث في الإنترنت وتحليل المعلومات...")
    await msg.send()
    
    user_query = message.content
    
    try:
        # 1. البحث التلقائي في الويب
        search_results = search_tool.run(user_query)
        
        # 2. صياغة التوجيه للذكاء الاصطناعي لدمج نتائج البحث
        prompt = f"""
        سؤال المستخدم: {user_query}
        بناءً على معلومات الإنترنت المحدثة التالية، اكتب إجابة ذكية، منسقة ومفصلة باللغة العربية:
        {search_results}
        """
        
        # 3. توليد الإجابة
        if llm:
            # تشغيل نموذج الذكاء الاصطناعي وجلب الرد
            final_response = llm.invoke(prompt)
            msg.content = final_response
        else:
            # حل بديل يعرض نتائج البحث مباشرة إذا لم يعمل النموذج المحلي
            msg.content = f"⚠️ لم يتم العثور على نموذج محلي، إليك نتائج البحث المباشرة:\n\n{search_results}"
            
        await msg.update()
        
    except Exception as e:
        msg.content = f"❌ حدث خطأ أثناء معالجة طلبك: {str(e)}"
        await msg.update()
