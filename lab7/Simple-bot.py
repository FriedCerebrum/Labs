import telebot
from telebot import types
import psycopg2
import datetime

TOKEN = '6240479093:AAHQt_UjSYTiphgQHTKMtdE79fNhjDdWfSc'  # Замените на токен вашего бота
bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных
con = psycopg2.connect(
    database="lab7_1",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

cur = con.cursor()

def get_current_week_type():
    week_number = datetime.date.today().isocalendar()[1]
    return week_number % 2

# Создаем кнопки
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Какая неделя')
    itembtn2 = types.KeyboardButton('Сайт')
    itembtn3 = types.KeyboardButton('Помощь')
    itembtn4 = types.KeyboardButton('Расписание')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    if message.text == 'Расписание':
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Понедельник')
        itembtn2 = types.KeyboardButton('Вторник')
        itembtn3 = types.KeyboardButton('Среда')
        itembtn4 = types.KeyboardButton('Четверг')
        itembtn5 = types.KeyboardButton('Пятница')
        itembtn6 = types.KeyboardButton('Расписание на текущую неделю')
        itembtn7 = types.KeyboardButton('Расписание на следующую неделю')
        back_button = types.KeyboardButton('Назад')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, back_button)
        bot.send_message(message.chat.id, "Выберите день недели:", reply_markup=markup)

    elif message.text in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']:
        week_type = 1 if get_current_week_type() == 'верхняя' else 2
        day_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница'].index(message.text) + 1

        cur.execute(f"""
                SELECT t.start_time, s.name, st.name, te.full_name, tt.room_number
                FROM timetable tt
                JOIN class c ON tt.class = c.id
                JOIN subject s ON c.subject = s.id
                JOIN subject_type st ON c.subject_type = st.id
                JOIN teacher_subject ts ON ts.class = c.id
                JOIN teacher te ON ts.teacher = te.id
                JOIN time t ON tt.class_time = t.id
                WHERE tt.week = {week_type} AND tt.day = {day_of_week}
                ORDER BY t.id
            """)
        rows = cur.fetchall()
        if rows:
            schedule = [f"{i + 1}. {row[0]}\n{row[1]}\n{row[2]}\n{row[3]} | {row[4]}\n—————————" for i, row in
                        enumerate(rows)]
            for i in range(len(schedule), 5):
                schedule.append(f"{i + 1}. Нет пары\n—————————")
            bot.reply_to(message, "\n".join(schedule))
        else:
            bot.reply_to(message, "Расписание отсутствует")

    elif message.text == 'Расписание на текущую неделю':
        week_type = get_current_week_type()
        cur.execute(f"SELECT * FROM Timetable WHERE week_type='{week_type}'")
        rows = cur.fetchall()
        for row in rows:
            bot.reply_to(message, f"{row[1]}\n_____________\n{row[2]} {row[3]} {row[4]} {row[5]}")
    elif message.text == 'Расписание на следующую неделю':
        week_type = 'нижняя' if get_current_week_type() == 'верхняя' else 'верхняя'
        cur.execute(f"SELECT * FROM Timetable WHERE week_type='{week_type}'")
        rows = cur.fetchall()
        for row in rows:
            bot.reply_to(message, f"{row[1]}\n_____________\n{row[2]} {row[3]} {row[4]} {row[5]}")

    elif message.text == 'Какая неделя':
        week_number = datetime.date.today().isocalendar()[1]
        if week_number % 2 == 0:
            bot.reply_to(message, 'Сейчас нижняя (Чётная) неделя.')
        else:
            bot.reply_to(message, 'Сейчас верхняя (Нечётная) неделя.')
    elif message.text == 'Сайт':
        bot.reply_to(message, 'https://mtuci.ru/')

    elif message.text == 'Помощь':
        bot.reply_to(message,
                     'Этот бот предназначен для отображения расписания занятий. '
                     'Вы можете выбрать день недели или показать расписание на текущую или следующую неделю. '
                     'Список доступных команд: \n /start - начать работу с '
                     'ботом \n /week - показать текущую неделю \n /mtuci - ссылка на '
                     'официальный сайт МТУСИ \n /help - показать эту справку.')
    elif message.text == 'Назад':
        send_welcome(message)  # Возврат в главное меню
    else:
        bot.reply_to(message, 'Извините, я Вас не понял.')

bot.polling()