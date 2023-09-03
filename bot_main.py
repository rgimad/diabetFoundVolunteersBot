import re
import telebot, sqlite3, hashlib
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from xlsxwriter.workbook import Workbook

admin_password_hash = '44fe45de0bee447b6a9101036c54b81b'

fio_dict = dict()
city_dict = dict()
age_dict = dict()
diabet_degree_dict = dict()
skill_dict = dict()
contacts_dict = dict()

with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT fio, age, city, diabet, skills, contacts FROM users WHERE _id = ' + str(message.from_user.id))
    # print(message.from_user.id)
    rows = cur.fetchall()
    conn.close()
    if rows:
        bot.send_message(message.chat.id,
            f"Вы уже заполняли анкету.\nВаши данные:\n\nФИО: {rows[0][0]}\nГород: {rows[0][1]}\nВозраст: {rows[0][2]}\nСтепень диабета: {rows[0][3]}\nНавыки и умения: {rows[0][4]}\nКонтакты: {rows[0][5]}"
        )
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text="Заполнить анкету заново"))
        bot.send_message(message.chat.id, "Нажмите, если вы хотите заполнить анкету заново", reply_markup=keyboard)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text="Начать анкетирование!"))
        bot.send_message(message.chat.id, "Нажмите, чтобы начать анкетирование", reply_markup=keyboard)


@bot.message_handler(commands=['admin'])
def admin_login(message):
    if len(message.text.split()) > 1:
        input_admin_password = message.text.split()[1]
    else:
        input_admin_password = ''
    input_admin_password_hash = hashlib.md5(input_admin_password.encode("ascii")).hexdigest() 
    if input_admin_password_hash == admin_password_hash:
        export_db_to_excel('output.xlsx')
        with open('output.xlsx', 'rb') as f:
            bot.send_document(message.chat.id, f)
    else:
        bot.send_message(message.chat.id, "Ошибка: неверный пароль администратора.")


def export_db_to_excel(fname):
    workbook = Workbook(fname)
    worksheet = workbook.add_worksheet()
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    mysel = c.execute("select fio, age, city, diabet, skills, contacts from users")
    for j, x in enumerate(['ФИО', 'Возраст', 'Город', 'Степень диабета', 'Навыки', 'Контакты']):
        worksheet.write(0, j, x, workbook.add_format({'bold': True}))
    for i, row in enumerate(mysel):
        for j, value in enumerate(row):
            worksheet.write(i + 1, j, row[j])
    worksheet.autofit()
    workbook.close()
    conn.close()

def write_all_to_db(user_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO users (_id, fio, age, city, diabet, skills, contacts) VALUES(?, ?, ?, ?, ?, ?, ?)',
        (user_id,
         fio_dict.get(user_id),
         city_dict.get(user_id),
         age_dict.get(user_id),
         diabet_degree_dict.get(user_id),
         skill_dict.get(user_id),
         contacts_dict.get(user_id)
        )
    )
    conn.commit()
    conn.close()

def clean_data_for(user_id):
    fio_dict.pop(user_id, None)
    city_dict.pop(user_id, None)
    age_dict.pop(user_id, None)
    diabet_degree_dict.pop(user_id, None)
    skill_dict.pop(user_id, None)
    contacts_dict.pop(user_id, None)

def get_surname(message):
    if message.text == None or re.search(r"[\W\d]", message.text):
        bot.send_message(message.chat.id, 'Вводите, пожалуйста, текст.\nВведите фамилию:')
        bot.register_next_step_handler(message, get_surname)
        return
    global fio_dict
    fio_dict[message.from_user.id] = message.text
    bot.send_message(message.chat.id, 'Введите имя:')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    if message.text == None or re.search(r"[\W\d]", message.text):
        bot.send_message(message.chat.id, 'Вводите, пожалуйста, текст.\nВведите имя:')
        bot.register_next_step_handler(message, get_name)
        return
    global fio_dict
    fio_dict[message.from_user.id] += str(" " + message.text)
    bot.send_message(message.chat.id, 'Введите отчество:')
    bot.register_next_step_handler(message, get_patronymic)

def get_patronymic(message):
    if message.text == None or re.search(r"[\W\d]", message.text):
        bot.send_message(message.chat.id, 'Вводите, пожалуйста, текст.\nВведите отчество:')
        bot.register_next_step_handler(message, get_patronymic)
        return
    global fio_dict
    fio_dict[message.from_user.id] += str(" " + message.text)
    # bot.send_message(message.chat.id, fio_dict.get(message.from_user.id))
    bot.send_message(message.chat.id, 'Введите город:')
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    if message.text == None:
        bot.send_message(message.chat.id, 'Вводите, пожалуйста, текст.\nВведите город:')
        bot.register_next_step_handler(message, get_city)
        return
    global city_dict
    city_dict[message.from_user.id] = message.text
    bot.send_message(message.chat.id, 'Введите ваш возраст:')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    if message.text == None or not message.text.isdigit():
        bot.send_message(message.chat.id, 'Возраст должен быть числом.\nВведите ваш возраст:')
        bot.register_next_step_handler(message, get_age)
        return
    global age_dict
    age_dict[message.from_user.id] = int(message.text)
    bot.send_message(message.chat.id, 'Введите степень диабета (1, 2 или 3) или 0 в случае отсутствия диабета:')
    bot.register_next_step_handler(message, get_diabet_degree)

def get_diabet_degree(message):
    if message.text == None or not message.text in ['0', '1', '2', '3']:
        bot.send_message(message.chat.id, 'Недопустимый вариант.\nВведите степень диабета (1, 2 или 3) или 0 в случае отсутствия диабета:')
        bot.register_next_step_handler(message, get_diabet_degree)
        return
    global age_dict
    diabet_degree_dict[message.from_user.id] = int(message.text)
    # bot.send_message(message.chat.id, '')
    # bot.register_next_step_handler(message, )
    bot.send_message(message.chat.id, 'Навыки и умения, которыми вы могли бы быть полезными фонду:')
    bot.register_next_step_handler(message, get_skills)

def get_skills(message):
    if message.text == None:
        bot.send_message(message.chat.id, 'Введите, пожалуйста, текст\nНавыки и умения, которыми вы могли бы быть полезными фонду:')
        bot.register_next_step_handler(message, get_skills)
        return
    global skill_dict
    skill_dict[message.from_user.id] = message.text

    bot.send_message(message.chat.id, 'Введите ваш телефон/email:')
    bot.register_next_step_handler(message, get_contacts)

def get_contacts(message):
    if message.text == None:
        bot.send_message(message.chat.id, 'Введите, пожалуйста, текст\nВведите ваш телефон/email:')
        bot.register_next_step_handler(message, get_contacts)
        return
    
    global contacts_dict
    contacts_dict[message.from_user.id] = message.text

    keyboard_yes_no = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_yes_no.add(KeyboardButton(text="Да, все верно"))
    keyboard_yes_no.add(KeyboardButton(text="Заполнить анкету заново"))
    bot.send_message(
        message.from_user.id,
        f"Ваши данные:\n\nФИО: {fio_dict.get(message.from_user.id)}\nГород: {city_dict.get(message.from_user.id)}\nВозраст: {age_dict.get(message.from_user.id)}\nСтепень диабета: {diabet_degree_dict.get(message.from_user.id)}\nНавыки и умения: {skill_dict.get(message.from_user.id)}\nКонтакты: {contacts_dict.get(message.from_user.id)}\n\nВсе верно?",
        reply_markup=keyboard_yes_no
    )


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Начать анкетирование!":
        bot.send_message(message.chat.id, "Введите фамилию: ")
        bot.register_next_step_handler(message, get_surname)
    elif message.text == "Да, все верно":
        write_all_to_db(message.from_user.id)
        bot.send_message(message.chat.id, "Спасибо за заявку, мы с вами свяжемся.")
    elif message.text == "Заполнить анкету заново":
        clean_data_for(message.from_user.id)
        bot.send_message(message.chat.id, "Введите фамилию: ")
        bot.register_next_step_handler(message, get_surname)
    else:
        bot.send_message(message.chat.id, "Ошибка: неизвестная команда. ")

bot.polling()


