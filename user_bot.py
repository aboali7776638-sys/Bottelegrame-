import os
from telethon import TelegramClient, events
import asyncio

# --- قراءة الإعدادات من متغيرات البيئة في Railway ---
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
# هذا السطر مهم جدًا لـ Railway لأنه يقرأ جلسة تسجيل الدخول المحفوظة
SESSION_STRING = os.environ.get('SESSION_STRING') 

# --- التحقق من وجود المتغيرات ---
if not all([API_ID, API_HASH, SESSION_STRING]):
    print("خطأ: تأكد من إضافة API_ID, API_HASH, و SESSION_STRING في متغيرات المشروع على Railway.")
    exit()

# --- إنشاء الاتصال باستخدام Session String ---
# هذه الطريقة لا تتطلب تسجيل الدخول التفاعلي على المنصة
client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)

# --- دالة الرد التلقائي ---
# هذا "المستمع" يعمل عند وصول أي رسالة جديدة لك
@client.on(events.NewMessage(incoming=True))
async def auto_responder(event):
    # التأكد من أن الرسالة خاصة (ليست في مجموعة) وأنها ليست صادرة منك
    if event.is_private and not event.message.out:
        sender = await event.get_sender()
        sender_name = sender.first_name
            
        # طباعة سجل في المنصة للمتابعة
        print(f"رسالة جديدة من {sender_name}: {event.message.text}")
            
        # الرد على الرسالة برسالة ترحيبية
        await event.reply(f"مرحبًا {sender_name}، شكرًا لتواصلك. سأقوم بالرد عليك في أقرب وقت ممكن.")
        print("تم إرسال الرد التلقائي.")

# --- الدالة الرئيسية للتشغيل ---
async def main():
    print("اليوزر بوت قيد التشغيل على Railway...")
    # بدء الاتصال بتليجرام
    await client.start()
    print("تم تسجيل الدخول بنجاح باستخدام جلسة محفوظة!")
    # إبقاء البرنامج يعمل للاستماع للرسائل
    await client.run_until_disconnected()

# --- نقطة انطلاق البرنامج ---
if __name__ == '__main__':
    # تشغيل الدالة الرئيسية
    asyncio.run(main())

