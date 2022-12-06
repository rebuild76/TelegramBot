import telebot
from config import TOKEN, keys
from extension import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)


# Обработчик start, stop
@bot.message_handler(commands=['start', 'help'])
def help_info(message: telebot.types.Message):
    help_text = 'Чтобы начать работу, введите команду в следующем формате:\n' \
                '<имя валюты> ' \
                '<валюта в которую перевести> ' \
                '<количество переводимой валюты>\n' \
                'Увидеть список всех доступных валют: /values'
    bot.reply_to(message, help_text)

#---------------
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += f'\n{key}'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException("Неверное количество параметров")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.reply_to(message, text)

bot.polling(non_stop=True)