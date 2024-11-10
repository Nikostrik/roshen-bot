import telebot
from telebot import types

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
ROSHEN_WEBSITE_URL = 'https://roshen.com'

products = {
    '1': {'name': 'Шоколад Lacmi Peanut&Caramel', 'image': 'https://www.express-service.com.ua/upload/iblock/dc6/tqi5lf35jo722d5nv4vda6vy9ner6x6c/ua_pim_380538001001_01.png'},
    '2': {'name': 'Цукерки Ko-Ko Choco White', 'image': 'https://happypen-photos.s3.eu-north-1.amazonaws.com/14206/konfety-ko-ko-choco-white-1kg-roshen0'},
    '3': {'name': 'Печиво Есмеральда з шматочками глазурі', 'image': 'https://omixcdn.com/img/catalog/pechene-roshen-esmeralda-s-kusochkami-glazuri-150g-10715853.jpg'}
}

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    order_button = types.KeyboardButton("Замовити")
    website_button = types.KeyboardButton("Перейти на сайт")
    markup.add(order_button, website_button)
    bot.send_message(message.chat.id, "Вітаю! Оберіть дію:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Замовити")
def show_products(message):
    product_list = "\n".join([f"{k}. {v['name']}" for k, v in products.items()])
    bot.send_message(message.chat.id, f"Виберіть продукт для замовлення:\n{product_list}\n\nВведіть номер продукту.")

@bot.message_handler(func=lambda message: message.text == "Перейти на сайт")
def go_to_website(message):
    markup = types.InlineKeyboardMarkup()
    website_button = types.InlineKeyboardButton("Перейти на сайт Roshen", url=ROSHEN_WEBSITE_URL)
    markup.add(website_button)
    bot.send_message(message.chat.id, "Натисніть кнопку нижче, щоб перейти на сайт Roshen:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in products.keys())
def handle_order(message):
    selected_product = products[message.text]

    product_name = selected_product['name']
    product_image = selected_product['image']

    bot.send_photo(message.chat.id, photo=product_image, caption=f"Ви обрали: {product_name}. Дякуємо за замовлення!")

bot.polling()