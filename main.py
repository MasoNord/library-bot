import logging
import psycopg2
import telebot

BOT_TOKEN = "7721061443:AAEexxN9tMgYbDrXKVdiNh5iGgIxxXMzWo4"
DB_HOST = "localhost" #5433 #Если БД находиться на одном компьютере с кодом бота!
#Если нет, то вводиться айпи и порт!
DB_USER = "postgres" # Название пользователя для БД
DB_PASSWORD = "" # Пароль
DB_NAME = "library-bot" # Как называеться БД ???

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для подключения к БД
def get_db_connection():
    return psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME, client_encoding='UTF8')
# Были проблемы с кодировкой! Нужно запомнить что писать именно как в БД!

# Эти 2 функции удалять буду! Они для проверки подключения к БД
# Команда /check_db
def check_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return False

@bot.message_handler(commands=['check_db'])
def check_db(message):
    if check_db_connection():
        bot.reply_to(message, "Подключение к базе данных успешно!")
    else:
        bot.reply_to(message, "Ошибка подключения к базе данных.")

# Функция для поиска книг
def search_books(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.title, b.author, b.publication_date, l.name, l.address 
        FROM books b
        JOIN book_library bl ON b.id = bl.book_id
        JOIN libraries l ON bl.library_id = l.id
        WHERE b.title ILIKE %s OR b.author ILIKE %s OR CAST(b.publication_date AS TEXT) ILIKE %s
    """, ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# Функция уведомлений пользователей
def add_notification(user_id, book_title):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notifications (user_id, book_title) VALUES (%s, %s)", (user_id, book_title))
    conn.commit()
    cur.close()
    conn.close()

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать people? Введдии назван книг, автар, дата выход для нахождения партнера по твайаму вкуссу!).")

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_search(message):
    results = search_books(message.text)
    if results:
        response = ""
        for result in results:
            response += f"Название: {result[0]}\nАвтор: {result[1]}\nДата выхода: {result[2]}\nБиблиотека: {result[3]}, {result[4]}\n\n"
        bot.reply_to(message, response)
    else:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="Уведомить о появлении", callback_data=f"notify_{message.text}"))
        bot.reply_to(message, "Книги не найдены. Хотите получить уведомление?", reply_markup=keyboard)

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: call.data.startswith('notify_'))
def process_callback_notify(call):
    book_title = call.data.split('_')[1]
    add_notification(call.from_user.id, book_title)
    bot.answer_callback_query(call.id, "Уведомление добавлено!")
    bot.send_message(call.from_user.id, "Вы будете уведомлены, когда книга появится.")
# Тут ошибка сейчас (сверху), выход за пределы диапазонов, В БД нужно поменять тип данных(на больший) в таблице уведомлений!

if __name__ == '__main__':
    bot.polling(none_stop=True)