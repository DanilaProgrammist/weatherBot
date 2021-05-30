import telebot
import pyowm
import time
owm = pyowm.OWM('9b65aaadc20dece694ffb1fd5c81acf1')
bot = telebot.TeleBot("1206910967:AAHnVvGM3ERtYg8UiNHMITFLnea1TqSKoIE")
@bot.message_handler(content_types=["text"])
def firs_message(message):
    if message.text == "/start":
        bot.send_message(message.chat.id,f'Привет, {message.from_user.first_name}!')
        bot.send_message(message.chat.id, "Пришли мне город и что хочешь узнать")
        time.sleep(3)
    else:
        bot.send_message(message.chat.id, "Напиши /help")
    else if message.text == "/help":
        bot.send_message(message.chat.id, "Напиши /start если хочешь начать")
def get_weather(message):
    city = message.text
    mgr = owm.weather_manager()
    obs = mgr.weather_at_place(message.text)
    weather = obs.weather
    bot.send_message(message.chat.id, weather)
bot.polling(none_stop= True, interval=0)
