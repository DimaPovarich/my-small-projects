import telebot
from telebot import types

bot = telebot.TeleBot('YOUR TOKEN')

menu = {"Маргаритта": 299, "4 сыра": 299, "Пепперони": 399, "пица с морепродуктами": 399}

basket = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! я бот - пиццерия, готов принять ваш заказ! Чтобы посмотреть что я могу напиши /help')


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'Мои возможности:\n/order - сделать заказ\n/pay - оплатить корзину\n/basket - показать что есть в корзине\n/check - выписать чек')


#оплата корзины
def get_change(message):
    if int(message.text) < sum_basket:
        bot.reply_to(message, 'Недостаточно средств')
        basket = {}
    else:
        bot.send_message(message.chat.id, f'Корзина успешно оплачена на сумму {sum_basket} рублей, ваша сдача: {int(message.text) - sum_basket}руб. Спасибо за покупку')
        basket = {}
@bot.message_handler(commands=['pay'])
def pay(message):
    global sum_basket
    sum_basket = [basket[i] for i in basket]
    sum_basket = int(sum(sum_basket))
    bot.send_message(message.chat.id, f'К оплате - {sum_basket} рублей')

    markup1 = types.InlineKeyboardMarkup()

    but4 = types.InlineKeyboardButton(text='Картой', callback_data='optioncard')
    but5 = types.InlineKeyboardButton(text='Наличными', callback_data='optioncash')

    markup1.add(but4, but5)
    bot.send_message(message.chat.id, 'Оплата картой или наличными?', reply_markup=markup1)
@bot.callback_query_handler(func=lambda call: call.data.startswith('option'))
def check_callback(call):
    if call.data == 'optioncard':
        bot.send_message(call.message.chat.id, f'Корзина успешно оплачена на сумму {sum_basket}, спасибо за покупку!')
    else:
        question = bot.send_message(call.message.chat.id, 'Сколько наличных вы даете?')
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
    markup = types.InlineKeyboardMarkup()

    but = types.InlineKeyboardButton(text='Маргаритта', callback_data="pizzaМаргаритта")
    but1 = types.InlineKeyboardButton(text='4 Сыра', callback_data="pizza4 сыра")
    but2 = types.InlineKeyboardButton(text='Пепперони', callback_data="pizzaПепперони")
    but3 = types.InlineKeyboardButton(text='Пица с морепродуктами', callback_data="pizzaпица с морепродуктами")

    markup.add(but, but1, but2, but3)
    bot.send_message(message.chat.id, 'Что вы хотите заказать?', reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith('pizza'))
def handle_callback(call):
    if call.data.replace('pizza', '') in menu:
        basket[call.data.replace('pizza', '')] = menu[call.data.replace('pizza', '')]
        bot.send_message(call.message.chat.id, f'Пицца {call.data.replace("pizza", "")} успешно добавлена в корзину!')
    else:
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')



bot.polling(none_stop=True)