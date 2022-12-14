import telebot
from config import keys, TOKEN
from extensions import ConvertExeption, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):  # функция, выводящая сообщение на команды start, help
    text = 'Чтобы начать работу, введите комманду в следующем формате:\n<название валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nСписок доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):  # функция, выводящая сообщение и список доступных валют на команду values
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n  '.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):  # функция конвертации
    try:
        values = message.text.split(' ')  # получаем из строки список
        if len(values) > 3:  # проверка количества введенных параметров
            raise ConvertExeption('Введено больше трёх параметров')  # поднимаем исключение ConvertExeption
        elif len(values) < 3:  # проверка количества введенных параметров
            raise ConvertExeption('Введено меньше трёх параметров')  # поднимаем исключение ConvertExeption
        quote, base, amount = values  # присваиваем переменным значения из списка
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()

