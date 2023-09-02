import re
import telebot, sqlite3, hashlib
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

fio_dict = dict()
city_dict = dict()
age_dict = dict()
diabet_degree_dict = dict()

with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text="Начать анкетирование!")
    keyboard.add(button)
    # Send the keyboard as a reply to the /start command
    bot.send_message(message.chat.id, "Добро пожаловать на нашу анкету!☺️\nДля начала предлагаю познакомится. Расскажите немного о себе в форме опроса.\nПожалуйста, будьте внимательны и введите точную информацию, это поможет нам обработать вашу анкету более эффективно.", reply_markup=keyboard)

@bot.message_handler(commands=['info'])
def help_message(message):
    bot.send_message(message.chat.id, '')

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Начать анкетирование!":
        bot.send_message(message.from_user.id, "Введите фамилию: ")
        bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    if message.text == None or re.search(r"[\W\d]", message.text):
        bot.send_message(message.from_user.id, 'Вводите, пожалуйста, текст.\nВведите фамилию:')
        bot.register_next_step_handler(message, get_surname)
        return
    global fio_dict
    fio_dict[message.from_user.id] = message.text
    bot.send_message(message.from_user.id, 'Введите имя:')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    if message.text == None or re.search(r"[\W\d]", message.text):
        bot.send_message(message.from_user.id, 'Вводите, пожалуйста, текст.\nВведите имя:')
        bot.register_next_step_handler(message, get_name)
        return
    global fio_dict
    fio_dict[message.from_user.id] += str(" " + message.text)
    bot.send_message(message.from_user.id, 'Введите отчество:')
    bot.register_next_step_handler(message, get_patronymic)

def get_patronymic(message):
    if message.text == None or re.search(r"[\W\d]", message.text):
        bot.send_message(message.from_user.id, 'Вводите, пожалуйста, текст.\nВведите отчество:')
        bot.register_next_step_handler(message, get_patronymic)
        return
    global fio_dict
    fio_dict[message.from_user.id] += str(" " + message.text)
    # bot.send_message(message.from_user.id, fio_dict.get(message.from_user.id))
    bot.send_message(message.from_user.id, 'Введите город:')
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    if message.text == None:
        bot.send_message(message.from_user.id, 'Вводите, пожалуйста, текст.\nВведите город:')
        bot.register_next_step_handler(message, get_city)
        return
    global city_dict
    city_dict[message.from_user.id] = message.text
    bot.send_message(message.from_user.id, 'Введите ваш возраст:')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    if message.text == None or not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Возраст должен быть числом.\nВведите ваш возраст:')
        bot.register_next_step_handler(message, get_age)
        return
    global age_dict
    age_dict[message.from_user.id] = int(message.text)
    bot.send_message(message.from_user.id, 'Введите степень диабета (1, 2 или 3) или 0 в случае отсутствия диабета:')
    bot.register_next_step_handler(message, get_diabet_degree)

def get_diabet_degree(message):
    if message.text == None or not message.text in ['0', '1', '2', '3']:
        bot.send_message(message.from_user.id, 'Недопустимый вариант.\nВведите степень диабета (1, 2 или 3) или 0 в случае отсутствия диабета:')
        bot.register_next_step_handler(message, get_diabet_degree)
        return
    global age_dict
    diabet_degree_dict[message.from_user.id] = int(message.text)
    # bot.send_message(message.from_user.id, '')
    # bot.register_next_step_handler(message, )
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (_id, fio, age, city, diabet) VALUES(?, ?, ?, ?, ?)',
        (message.from_user.id,
         fio_dict.get(message.from_user.id),
         city_dict.get(message.from_user.id),
         age_dict.get(message.from_user.id),
         diabet_degree_dict.get(message.from_user.id)
        )
    )
    conn.commit()
    conn.close()
    bot.send_message(message.from_user.id, "Личные данные записаны. Перейти к анкетированию?")


bot.polling()


