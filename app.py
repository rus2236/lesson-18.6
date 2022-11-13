import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> пробел <в какую валюту перевести>пробел" \
           "<количество переводимой валюты>\nУвидеть список всех доступных валют: /values \nПРИМЕР:\nрубль доллар 100"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')
        if len(values) != 3:
            raise APIException('Слишком много/мало параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
