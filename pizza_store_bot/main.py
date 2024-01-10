import telebot
from telebot import types
from check import check_int

bot = telebot.TeleBot('YOUR TOKEN')

menu = {"Маргаритта": 299, "4 сыра": 299, "Пепперони": 399, "Пица с морепродуктами": 399, "ПИЦЦА С СОСИСКОЙ КАМОЗИНА": 1000, "Пицца от моей 911 жены(9 месяцев)": 1234}
basket = {}
number_of_order = 1


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! я бот - пиццерия, готов принять ваш заказ! Чтобы посмотреть что я могу напиши /help')


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'Мои возможности:\n/order - сделать заказ\n/pay - оплатить корзину\n/basket - показать что есть в корзине\n/check - выписать чек\n/history - отправить текстовый файл с историей ваших заказов\n')


#оплата корзины
def get_change(message):
    #вызываем функцию проверки типа данных из файла check.py, если все хорошо, то оплата корзины происходит
    if check_int(message=message):
        global basket
        global number_of_order
        if int(message.text) < sum_basket:
            bot.reply_to(message, 'Недостаточно средств🫤')
        else:
            #уведомляем пользователя о успешной оплате корзины
            bot.send_message(message.chat.id, f'Корзина успешно оплачена на сумму {sum_basket} рублей, ваша сдача: {int(message.text) - sum_basket}руб. Спасибо за покупку😊\nНажмите /help чтобы сделать еще что-то')
            #записываем все товары из корзины в файл с историей заказов
            with open('order_history.txt', 'a') as file:
                for i in basket:
                    file.write(f'оплачен заказ №{number_of_order}, заказан товар: {i} на сумму {basket[i]}\n')
                    number_of_order += 1
            #отчищаем корзину
            basket = {}
    #если что то пошло не так, то пишем, что что то пошло не так
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так😥')


@bot.message_handler(commands=['pay'])
def pay(message):
    if basket != {}:
        #считаем сумму баксов которые нам должны
        global sum_basket
        sum_basket = [basket[i] for i in basket]
        sum_basket = int(sum(sum_basket))
        #фри хангред бакс
        bot.send_message(message.chat.id, f'🫰К оплате - {sum_basket} рублей🫰')

        #создаем итерактивное меню выбора
        markup1 = types.InlineKeyboardMarkup()

        but1 = types.InlineKeyboardButton(text='Картой💳', callback_data='optioncard')
        but2 = types.InlineKeyboardButton(text='Наличными💵', callback_data='optioncash')

        markup1.add(but1, but2)

        #отправляем вопрос и прикрепляем его к меню
        bot.send_message(message.chat.id, 'Оплата картой или наличными?🏦', reply_markup=markup1)
    else:
        bot.send_message(message.chat.id, 'Ваша корзина пуста😓')
#обработка выбора пользователя
@bot.callback_query_handler(func=lambda call: call.data.startswith('option'))
def check_callback(call):
    #делаем переменную для обозначения номера заказа
    global number_of_order
    global sum_basket
    if call.data == 'optioncard':
        bot.send_message(call.message.chat.id, f'Корзина успешно оплачена на сумму {sum_basket}, спасибо за покупку!😊\nНажмите /help чтобы сделать еще что-то')
        #записываем заказ в файл с историей заказов
        with open('order_history.txt', 'a') as file:
            for i in basket:
                file.write(f'оплачен заказ №{number_of_order}, заказан товар: {i} на сумму {basket[i]}\n')
                number_of_order += 1
    else:
        #задаем вопрос и вызываем функцию для оплаты наличными
        question = bot.send_message(call.message.chat.id, 'Сколько наличных вы даете?💸')
        bot.register_next_step_handler(question, get_change)


#выписываем чек
@bot.message_handler(commands=['check'])
def check(message):
    check = []
    j = 1
    sum = 0
    check_str = ''
    for i in basket:
        check.append(list(f'Товар №{j}: {i}, цена - {basket[i]}руб.'))
        j+=1
        sum += basket[i]
    check.append(list(f'Итого: {sum}руб.'))
    for i in range(len(check)):
        for j in range(len(check[i])):
            check_str += check[i][j]
        check_str += '\n'
    bot.send_message(message.chat.id, check_str)

#показываем содержимое корзины
@bot.message_handler(commands=['basket'])
def demonstrate_basket(message):
    if basket != {}:
        basket_text = ''
        for i in basket:
            basket_text += f'{i} - {basket[i]}\n'
        bot.send_message(message.chat.id, basket_text)
    else:
        bot.send_message(message.chat.id, 'Ваша корзина пуста')

#делаем заказ интерактивным меню
@bot.message_handler(commands=['order'])
def order(message):
    #создаем интерактивное меню выбора
    markup = types.InlineKeyboardMarkup()

    but = types.InlineKeyboardButton(text='Маргаритта', callback_data="pizzaМаргаритта")
    but1 = types.InlineKeyboardButton(text='4 Сыра', callback_data="pizza4 сыра")
    but2 = types.InlineKeyboardButton(text='Пепперони', callback_data="pizzaПепперони")
    but3 = types.InlineKeyboardButton(text='Пица с морепродуктами', callback_data="pizzaПица с морепродуктами")
    but4 = types.InlineKeyboardButton(text='ПИЦЦА С СОСИСКОЙ КАМОЗИНА', callback_data='pizzaПИЦЦА С СОСИСКОЙ КАМОЗИНА')
    but5 = types.InlineKeyboardButton(text='Пицца от моей 911 жены(ей -9 месяцев)', callback_data='pizzaПицца от моей 911 жены(9 месяцев)')
    markup.add(but, but1, but2, but3, but4, but5)
    #задаем вопрос и прикрепляем его к нашему меню выбора
    bot.send_message(message.chat.id, 'Что вы хотите заказать?🍕', reply_markup=markup)

#обработка результата выбора из меню
@bot.callback_query_handler(func=lambda call: call.data.startswith('pizza'))
def handle_callback(call):
    #убираем слово pizza из выбора для красивого вывода
    if call.data.replace('pizza', '') in menu:
        basket[call.data.replace('pizza', '')] = menu[call.data.replace('pizza', '')]
        bot.send_message(call.message.chat.id, f'Пицца {call.data.replace("pizza", "")} успешно добавлена в корзину!😁\nДля помощи пропишите /help')

    #если что то не так то пишем что что то не так
    else:
        bot.send_message(call.message.chat.id, 'Что-то пошло не так😥')


#отправка истории заказов
@bot.message_handler(commands=['history'])
def send_order_history(message):
    #отправляем историю оплаченных заказов в виде txt файла
    with open(r"order_history.txt", 'r') as file:
        if file.read() != '':
            bot.send_document(message.chat.id, open(r"order_history.txt", 'rb'))
        else:
            bot.send_message(message.chat.id, 'Вы ничего не заказывали!')


#ведем запись сообщений которые оказались нераспознанны
@bot.message_handler(content_types=['text'])
def write_to_undefinded(message):
    #говорим что бот ничего не понял
    bot.reply_to(message, 'Команда не распозанна😒')
    #запись в файл
    with open('undefinded_messages.txt', 'a') as file:
        file.write(f'пользователь {message.from_user.username} написал {message.text}\n')


bot.polling(none_stop=True)
