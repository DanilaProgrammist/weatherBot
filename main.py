import  telebot
from telebot import types
from pyowm import  OWM
from pyowm.utils.config import get_default_config

telebot_token = "Your-token"
weather_token = "Your-token"

keyboard = types.ReplyKeyboardMarkup();
keyboard.row("Ещё город", "Спасибо, но пока не надо")

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM(weather_token)
mgr = owm.weather_manager()

bot = telebot.TeleBot(telebot_token)

@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(content_types=['text'])

def first_message(message):
    city = bot.send_message(message.chat.id, "Привет, я погодный бот, пришли мне город, я пришлю тебе погоду в нём")
    bot.register_next_step_handler(city, send_weather)
@bot.message_handler(func=lambda message: True)
def send_weather(message):
    observation = mgr.weather_at_place(message.text)
    weather_city = observation.weather
    temp = weather_city.temperature('celsius')['temp']
    bot.send_message(message.chat.id, "В городе " + message.text + " сейчас " + str(temp) + " градусов")
    wind_speed = weather_city.wind()['speed']
    bot.send_message(message.chat.id, "Скорость ветра в городе " + message.text + " " + str(wind_speed) + " метров в секунду")
    humidity_level = weather_city.humidity
    bot.send_message(message.chat.id, "Влажность в городе " + message.text + " " + str(humidity_level) + " %")
    continue_answer = bot.send_message(message.chat.id, "Что дальше?", reply_markup= keyboard)
    bot.register_next_step_handler(continue_answer, continue_weather)
def continue_weather(message):
    if message.text == "Ещё город":
        new_city = bot.send_message(message.chat.id, "Пришли следующий город")
        bot.register_next_step_handler(new_city, send_weather)
    if message.text == "Спасибо, но пока не надо":
        bot.send_message(message.chat.id, "Пока")
    if message.text != "Ещё город" and message.text != "Нет" :
        bot.send_message(message.chat.id, "Прости, я тебя не понимаю")
        new_answer = bot.send_message(message.chat.id, "Напиши ещё раз")
        bot.register_next_step_handler(new_answer, continue_weather)
bot.polling()
