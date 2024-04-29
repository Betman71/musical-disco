import requests
import telebot
import math

bot = telebot.TeleBot("7165166523:AAH6jrfiWMylklIrjeKJGzOStkFsAMYWkB4")


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот-лицеист. Я могу помочь узнать что-то новое о лицеи")
    bot.send_message(message.chat.id, "Я имею функции, давай ознакомимся с ними.")
    bot.send_message(message.chat.id, "Функция address поможет на карте найти лицей."'\n'
                                      "Функция music поможет выдаст лучшее треки,написанные группой лицея CrazyPills."
                                      "Функция path_length поможет узнать расстояние от дома до школы"'\n'
                                      "Функция weather подскажет погоду на сегодня."'\n'
                                      "Функция sgo поможет быстро открыть свой сетевой журнал из telegram."'\n'
                                      "Функция shop  покажет магазины рядом."'\n'
                                      "Функция reviews поможет узнать лицей по реальным отзывам."'\n')
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    button_address = telebot.types.KeyboardButton('/address')
    button_music = telebot.types.KeyboardButton('/music')
    button_weather = telebot.types.KeyboardButton('/weather')
    button_sgo = telebot.types.KeyboardButton('/sgo')
    button_shop = telebot.types.KeyboardButton('/shop')
    button_path_length = telebot.types.KeyboardButton('/path_length')
    button_reviews = telebot.types.KeyboardButton('/reviews')
    keyboard.add(button_address, button_music, button_weather, button_sgo, button_shop, button_path_length,
                 button_reviews)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=keyboard)


@bot.message_handler(commands=['address'])
def address(message):
    bot.send_message(message.chat.id, "ул. Галкина, 14, координаты (37.622441; 54.208496")
    bot.send_message(message.chat.id,
                     "https://yandex.ru/maps/org/litsey_2_imeni_borisa_anatolyevicha_"
                     "slobodskova/39575323555/gallery/?ll=37.622441%2C54.208496&photos%5Bbusiness%5D=39575323555&photos"
                     "%5Bid%5D=urn%3Ayandex%3Asprav%3Aphoto%3A11732311-2a0000018e1ae341417dc58478a852946e3c"
                     "&tab=gallery&z=16.64")
    bot.send_photo(message.chat.id, photo=open('lyc.jpg', 'rb'))


@bot.message_handler(commands=['music'])
def music(message):
    tracks = ['давай проверим', 'navtomate', '31 ноября', 'новогодняя']
    bot.send_message(message.chat.id, "Список музыкальных треков:")
    for track in tracks:
        bot.send_message(message.chat.id, track)
    bot.send_message(message.chat.id, 'все треки можно послушать по ссылке https://vk.com/artist/crazypills')


@bot.message_handler(commands=['weather'])
def weather(message):
    city = 'Тула'
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid' \
                                                                        '=79d1ca96933b0328e1c7e3e7a26cb347'
    # отправляем запрос на сервер и сразу получаем результат
    weather_data = requests.get(url).json()
    # получаем данные о температуре и о том, как она ощущается
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    # выводим значения на экран
    bot.send_message(message.chat.id, f'Сейчас в городе {city} {str(temperature)} °C')
    bot.send_message(message.chat.id, f'Ощущается как {str(temperature_feels)} °C')


@bot.message_handler(commands=['sgo'])
def sgo(message):
    bot.send_message(message.chat.id, 'вот ссылка на электронный журнал')
    bot.send_message(message.chat.id, 'https://sgo1.edu71.ru/')


@bot.message_handler(commands=['shop'])
def shop(message):
    bot.send_message(message.chat.id, 'в этих местах ты можешь перекусить')
    bot.send_photo(message.chat.id, photo=open('shops.jpg', 'rb'))


@bot.message_handler(func=lambda message: True, commands=['path_length'])
def path_length(message):
    def lonlat_distance(a, b):
        degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
        a_lon, a_lat = a
        b_lon, b_lat = b

        # Берем среднюю по широте точку и считаем коэффициент для нее.
        radians_lattitude = math.radians((a_lat + b_lat) / 2.)
        lat_lon_factor = math.cos(radians_lattitude)

        # Вычисляем смещения в метрах по вертикали и горизонтали.
        dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
        dy = abs(a_lat - b_lat) * degree_to_meters_factor

        # Вычисляем расстояние между точками.
        distance = math.sqrt(dx * dx + dy * dy)

        return distance

    server_address = "http://geocode-maps.yandex.ru/1.x/"
    api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

    sp = []
    home = 'Макаренок 9'
    school = 'Галкина 14'
    sp.append(home)
    sp.append(school)

    coord = []
    for s in sp:
        params = {
            "apikey": api_key,
            "geocode": s,
            "format": "json"
        }
        response = requests.get(server_address, params)
        json_resp = response.json()
        if response:
            coord.append(tuple(map(float, json_resp["response"]["GeoObjectCollection"]["featureMember"][0]
            ["GeoObject"]["Point"]["pos"].split())))

    length = lonlat_distance(*coord)
    bot.send_message(message.chat.id, f"Длина пути: {round(length, 3)}")


bot.polling(none_stop=True, interval=0)
