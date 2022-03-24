import telebot
from config import TOKEN, keys
from extensions import CurrencyConverter, ConvertionExeption

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Привет! Этот бот конверитрует валюты. Формат запроса: \n <имя валюты>\
<валюта в которую переводим><количество> \
\n Что бы посмотреть все валюты, исользуте /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvertionExeption("Не верное количество параметров!")

        quote, base, amount = values
        result = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f"Ошибка ввода.\n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать комманду.\n {e}")
    else:
        text = f'Цена {amount} {quote} в {base} = {result}'
        bot.send_message(message.chat.id, text)


bot.polling()
