import telebot as tl
from telebot import types

bot = tl.TeleBot('6963425483:AAGeQwSwm8gFYjFa96i96Q6XuUeSUoosABc')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    welcome_text = "Добро пожаловать в Калькулятор Бот!\n\n"
    instructions = "Чтобы использовать калькулятор, просто введите математическое выражение или выберите команду /calc."
    bot.send_message(message.chat.id, welcome_text + instructions)


@bot.message_handler(commands=['calc'])
def calcul(message):
    markup = calcul_markup()
    bot.send_message(message.chat.id, "Выберите команду:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def hide(call):
    try:
        expression = call.message.text.split(": ")[1] if ": " in call.message.text else ""
        if call.data == "result":
            if expression:
                result = eval(expression)
                bot.send_message(call.message.chat.id, f"Результат: {result}")
            else:
                bot.send_message(call.message.chat.id, "Нет данных для вычисления.")
        elif call.data == "clear":
            expression = ""
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ваше выражение: " + expression, reply_markup=calcul_markup())
        else:
            expression += call.data
            markup = calcul_markup()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ваше выражение: " + expression, reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Ошибка: {str(e)}")


def calcul_markup():
    markup = types.InlineKeyboardMarkup(row_width=4)
    buttons = [
        types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(10)
    ]
    operators = [
        types.InlineKeyboardButton('+', callback_data='+'),
        types.InlineKeyboardButton('-', callback_data='-'),
        types.InlineKeyboardButton('*', callback_data='*'),
        types.InlineKeyboardButton('/', callback_data='/'),
        types.InlineKeyboardButton('(', callback_data='('),
        types.InlineKeyboardButton(')', callback_data=')'),
        types.InlineKeyboardButton('C', callback_data='clear'),
        types.InlineKeyboardButton('=', callback_data='result'),
    ]
    markup.add(*buttons, *operators)
    return markup


if __name__ == "__main__":
    bot.polling(none_stop=True)
