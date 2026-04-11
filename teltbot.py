import telebot
import datetime
import time
import threading
import random
from telebot import apihelper
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

apihelper.CONNECT_TIMEOUT = 30
apihelper.READ_TIMEOUT = 30

def send_with_retry(func, *args, **kwargs):
    for attempt in range(3):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < 2:
                print(f"Попытка {attempt + 1} не удалась, повтор через 5 секунд...")
                time.sleep(5)
            else:
                raise e

@bot.message_handler(commands=['start'])
def start_message(message):
    send_with_retry(bot.reply_to, message, 'Привет! Я чат бот, который будет напоминать об умственных нагрузках!')
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.daemon = True
    reminder_thread.start()

@bot.message_handler(commands=['fact'])
def fact_message(message):
    facts = [
        "**Нейропластичность и когнитивный резерв.** Мозг постоянно меняется: при решении новых задач между нейронами образуются новые связи...",
        "**Борьба с деградацией внимания и «туманом».** Современные привычки приучают мозг к поверхностной обработке информации...",
        "**Эмоциональная регуляция и стрессоустойчивость.** Нагрузка на мозг снижает активность миндалевидного тела — центра страха..."
    ]
    random_fact = random.choice(facts)
    send_with_retry(bot.reply_to, message, f'Лови факт о нагрузке мозга: {random_fact}')

def send_reminders(chat_id):
    reminders = ["08:00", "14:00", "16:00"]
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now in reminders:
            try:
                bot.send_message(chat_id, "Напоминание - время мозговой нагрузки")
                time.sleep(61)
            except Exception as e:
                print(f"Ошибка отправки напоминания: {e}")
        time.sleep(1)

while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        print("Повторная попытка через 15 секунд...")
        time.sleep(15)

