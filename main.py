import telebot
import requests

bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Для построения маршрута напишите свой адрес отправления и адрес назначения через запятую.')

@bot.message_handler(content_types=['text'])
def handle_message(message):
    addresses = message.text.split(',')
    if len(addresses) != 2:
        bot.send_message(message.chat.id, 'Неправильный формат! Пожалуйста, укажите адрес отправления и адрес назначения через запятую.')
    else:
        start_address = addresses[0].strip()
        end_address = addresses[1].strip()
        
        route = get_route(start_address, end_address)
        
        if route:
            bot.send_message(message.chat.id, f'Маршрут: {route}')
        else:
            bot.send_message(message.chat.id, 'Не удалось построить маршрут!')

def get_route(start_address, end_address):
    api_key = 'YOUR_YANDEX_MAPS_API_KEY'
    url = f'https://api.routing.yandex.net/v2.1/router?apikey={api_key}&from={start_address}&to={end_address}&format=json'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        route = response.json()['routes'][0]['legs'][0]['summary']['text']
        return route
    else:
        return None

bot.polling()
