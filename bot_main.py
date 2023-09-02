import telebot, sqlite3, hashlib

with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Вас приветствует бот! TODO /info -')

@bot.message_handler(commands=['info'])
def help_message(message):
    bot.send_message(message.chat.id, 'TODO TEXT')


bot.polling()


