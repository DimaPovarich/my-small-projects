import telebot
import time

bot = telebot.TeleBot('YOUR TOKEN')
anti_spam_list = []


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Напиши /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "/kick - кикнуть пользователя\n/mute - замутить пользователя на определенное время\n/unmute - размутить пользователя\n/info_user - информация о пользователе(использовать только в ответ на его сообщение\n")

# функция мута юзера
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно замутить администратора.")
        else:
            duration = 60  # Значение по умолчанию - 1 минута
            args = message.text.split()[1:]
            if args:
                try:
                    duration = int(args[0])
                except ValueError:
                    bot.reply_to(message, "Неправильный формат времени.")
                    return
                if duration < 1:
                    bot.reply_to(message, "Время должно быть положительным числом.")
                    return
                if duration > 1440:
                    bot.reply_to(message, "Максимальное время - 1 день.")
                    return
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration * 60)
            bot.reply_to(message,
                         f"Пользователь {message.reply_to_message.from_user.username} замучен на {duration} минут.")
    else:
        bot.reply_to(message,
                     "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")

# функция размута юзера
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True,
                                 can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} размучен.")
    else:
        bot.reply_to(message,
                     "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить.")

# удаление из чата юзера
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно кикнуть администратора.")
        else:
            bot.kick_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} был кикнут.")
    else:
        bot.reply_to(message,
                     "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.")

#получаем ай ди пользователя и чата
@bot.message_handler(commands=['info_user'])
def user_id(message):
    if message.reply_to_message:
        user_id_get = message.reply_to_message.from_user.id
        chat_id_get = message.chat.id
        chat_name = message.chat.title
        bot.send_message(chat_id_get, f'id чата {chat_name}: {chat_id_get}, id пользователя {message.reply_to_message.from_user.username}: {user_id_get}')
    else:
        bot.send_message(message.chat.id, 'я не могу выдать данные, используйте команду в ответ на сообщение')

# история чата
@bot.message_handler(content_types=['text'])
def save_chat_history(message):
    chat_name = message.chat.title
    filePath = 'chat_history.txt'
    file = open(filePath, 'a')
    message_user = f"пользователь {message.from_user.username} пишет: {message.text} в чат: {chat_name} "
    file.write(message_user)
    file.write('\n')

    #анти спам (коряво)
    chat_id = message.chat.id
    user_id = message.from_user.id
    anti_spam_a = 0
    anti_spam_list.append(message.text)
    if len(anti_spam_list) >= 5:
        for i in range(len(anti_spam_list) - 1):
            if anti_spam_list[i] == anti_spam_list[i + 1]:
                anti_spam_a += 1
                if anti_spam_a <= 3:
                    if bot.get_chat_member(chat_id, user_id).status == 'administrator' or bot.get_chat_member(chat_id,
                                                                                                              user_id).status == 'creator':
                        bot.send_message(chat_id, 'нельзя удалить админа за спам')
                        anti_spam_list.clear()
                        break
                    else:
                        bot.send_message(chat_id, f'пользователь{message.from_user.username} будет удален за спам')
                        bot.kick_chat_member(chat_id, user_id)
                        anti_spam_list.clear()

            else:
                anti_spam_list.clear()
                break

bot.polling(interval=0, none_stop=True)