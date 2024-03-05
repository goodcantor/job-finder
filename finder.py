from telethon import TelegramClient, events
import random
import asyncio

api_id = 25574126
api_hash = '932f49ddd31a72c7a095d1f3501a9498'

client = TelegramClient('anon', api_id, api_hash)

keywords = [
    "react", "reactjs", "react.js",
    "next.js", "nextjs", "next",
    "node.js", "nodejs",
    "mongodb",
    "postgresql", "postgres",
    "javascript", "js",
    "frontend", 
    "backend",
    "fullstack", "full stack",
    "express.js", "expressjs", "express",
    "typescript", "ts",
    "graphql",
    "вакансия"
]


blocked_keywords = [
 "мошенничество"
]

my_channel_username = 'anasunfindjob'

banned_usernames = ['esli_kto-to_zaebet']  # Исправлено на нижний регистр

@client.on(events.NewMessage(incoming=True))
async def handler(event):      
    # Проверяем длину сообщения
    if len(event.raw_text) < 90:
        return

    sender = await event.get_sender()
    sender_username = sender.username.lower() if sender.username else ''
    message_id = event.id
    chat = await event.get_chat()
    chat_id = chat.id

    # Преобразование отрицательного ID чата в формат ссылки
    chat_id_formatted = f"-100{abs(chat_id)}" if chat_id < 0 else str(chat_id)
    
    # Создание URL для чата (если у чата есть username)
    chat_link = f"https://t.me/{chat.username}" if chat.username else f"https://t.me/c/{chat_id_formatted}"
    
    # Создание URL для сообщения
    message_link = f"https://t.me/c/{chat_id_formatted}/{message_id}"

    text_lower = event.raw_text.lower()

    # Проверка на запрещенные ключевые слова
    if any(blocked_keyword.lower() in text_lower for blocked_keyword in blocked_keywords):
        # Если найдено запрещенное ключевое слово, игнорируем сообщение
        return

    if sender_username not in banned_usernames and any(keyword.lower() in text_lower for keyword in keywords):
        sender_name = getattr(sender, 'first_name', 'Нет имени')
        if hasattr(sender, 'last_name') and sender.last_name:
            sender_name += f" {sender.last_name}"

        message_to_send = (
            f"Сообщение от: {sender_name}\n"
            f"Ссылка на сообщение: {message_link}\n"
            f"Ссылка на чат: {chat_link}\n\n"  
            f"Текст сообщения:\n{event.raw_text}"
        )

        # Пересылка сообщения в ваш Telegram канал
        try:
            delay = random.uniform(2, 11)  # Уменьшенная задержка для быстроты
            await asyncio.sleep(delay)
            # Отправка сообщения используя username канала
            await client.send_message(my_channel_username, message_to_send)
        except Exception as e:
            print(f"Произошла ошибка при отправке сообщения в канал @{my_channel_username}: {e}")

# Запуск клиента
client.start()
client.run_until_disconnected()