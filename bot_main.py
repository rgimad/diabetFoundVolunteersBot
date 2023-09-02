import telebot, sqlite3, hashlib
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

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

# def message_reply(message):
#     if message.text=="Начать анкетирование!":
#         bot.send_message(message.chat.id, "")


bot.polling()


