import telebot
from telebot import types
import psycopg2
import datetime

TOKEN = '6240479093:AAHQt_UjSYTiphgQHTKMtdE79fNhjDdWfSc' # Замените на токен вашего бота
bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных
con = psycopg2.connect(
    database="lab_7",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

cur = con.cursor()

# Создаем кнопки
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Понедельник')
    itembtn2 = types.KeyboardButton('Вторник')
    itembtn3 = types.KeyboardButton('Среда')
    itembtn4 = types.KeyboardButton('Четверг')
    itembtn5 = types.KeyboardButton('Пятница')
    itembtn6 = types.KeyboardButton('Расписание на текущую неделю')
    itembtn7 = types.KeyboardButton('Расписание на следующую неделю')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
    bot.send_message(message.chat.id, "Выберите день недели:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']:
        cur.execute(f"SELECT * FROM Timetable WHERE day='{message.text}'")
        rows = cur.fetchall()
        for row in rows:
            bot.reply_to(message, f"{row[1]}\n_____________\n{row[2]} {row[3]} {row[4]} {row[5]}")
    elif message.text == 'Расписание на текущую неделю':
        cur.execute(f"SELECT * FROM Timetable")
        rows = cur.fetchall()
        for row in rows:
            bot.reply_to(message, f"{row[1]}\n_____________\n{row[2]} {row[3]} {row[4]} {row[5]}")
    elif message.text == 'Расписание на следующую неделю':
        # Добавьте логику для вывода расписания на следующую неделю
        pass
    else:
        bot.reply_to(message, 'Извините, я Вас не понял.')

@bot.message_handler(commands=['week'])
def send_week(message):
    week_number = datetime.date.today().isocalendar()[1]
    if week_number % 2 == 0:
        bot.reply_to(message, 'Сейчас верхняя неделя.')
    else:
        bot.reply_to(message, 'Сейчас нижняя неделя.')

    @bot.message_handler(commands=['mtuci'])
    def send_mtuci(message):
        bot.reply_to(message, 'https://mtuci.ru/')

    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.reply_to(message,
                     'Этот бот предназначен для отображения расписания занятий. Вы можете выбрать день недели или показать расписание на текущую или следующую неделю. Список доступных команд: \n /start - начать работу с ботом \n /week - показать текущую неделю \n /mtuci - ссылка на официальный сайт МТУСИ \n /help - показать эту справку.')

bot.polling()
