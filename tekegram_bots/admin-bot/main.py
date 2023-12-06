import telebot

bot = telebot.TeleBot('6470336387:AAHFjnDBZpUqppe1p8H-aS7Pke4WoqmKorc')


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Напиши /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "/kick - кикнуть пользователя\n/mute - замутить пользователя на определенное время\n/unmute - размутить пользователя\n/info_user - информация о пользователе(использовать только в ответ на его сообщение\n")

#получаем ай ди пользователя и чата
@bot.message_handler(commands=['info_user'])
def user_id(message):
    if message.reply_to_message:
        user_id_get = message.reply_to_message.from_user.id
        chat_id_get = message.chat.id
        chat_name = message.chat.title
        bot.send_message(chat_id_get, f'id чата "{chat_name}": {chat_id_get}, id пользователя "{message.reply_to_message.from_user.username}": {user_id_get}')
    else:
        bot.send_message(message.chat.id, 'я не могу выдать данные, используйте команду в ответ на сообщение')

@bot.message_handler(content_types=['document'])
def forward_file(message):
    bot.forward_message(2140441367, from_chat_id=message.chat.id, message_id=message.id)

@bot.message_handler(content_types=['text'])
def save_chat_history(message):
    chat_name = message.chat.title
    filePath = 'chat_history.txt'
    file = open(filePath, 'a')
    message_user = f"пользователь {message.from_user.username} пишет: {message.text} в чат: {chat_name} "
    file.write(message_user)
    file.write('\n')

bot.polling(interval=0, none_stop=True)