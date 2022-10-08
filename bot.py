import argparse

import pyowm
import telebot


def parse_args():
	parser = argparse.ArgumentParser(description="Telegram bot to obtain weather in given city")
	parser.add_argument('--telegram-token', required=True, help="Telegram token")
	parser.add_argument('--owm-api-key', required=True, help='OpenWeatherMap API key')
	return parser.parse_args()

args = parse_args()

owm = pyowm.OWM(args.owm_api_key)
bot = telebot.TeleBot(args.telegram_token)


@bot.message_handler(content_types=['text'])
def echo_all(message):
	observation = owm.weather_at_place(message.text)
	w = observation.get_weather()
	temp = w.get_temperature("celsius")["temp"]

	answer = (f"В городе {message.text} сейчас {w.get_detailed_status()}\n"
			  f"Температура в районе {str(temp)}\n")

	if temp < 10:
		answer += "Холодно"
	elif temp < 20:
		answer += "Прохладно"
	else:
		answer += "Тепло"

	bot.send_message(message.chat.id, answer)
bot.polling(none_stop = True)
