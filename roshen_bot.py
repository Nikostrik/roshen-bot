import telebot
from telebot import types
import sqlite3

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
ROSHEN_WEBSITE_URL = 'https://roshen.com'

conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_name TEXT NOT NULL
)''')

conn.commit()

products = {
    '1': {'name': 'Шоколад Lacmi Peanut&Caramel', 'image': 'https://www.express-service.com.ua/upload/iblock/dc6/tqi5lf35jo722d5nv4vda6vy9ner6x6c/ua_pim_380538001001_01.png'},
    '2': {'name': 'Цукерки Ko-Ko Choco White', 'image': 'https://happypen-photos.s3.eu-north-1.amazonaws.com/14206/konfety-ko-ko-choco-white-1kg-roshen0'},
    '3': {'name': 'Печиво Есмеральда з шматочками глазурі', 'image': 'https://omixcdn.com/img/catalog/pechene-roshen-esmeralda-s-kusochkami-glazuri-150g-10715853.jpg'}
}

@bot.message_handler(commands=['start'])
def main(message):
    cursor.execute('''INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                      VALUES (?, ?, ?, ?)''',
                   (message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name))
    conn.commit()
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

    cursor.execute("INSERT INTO orders (user_id, product_name) VALUES (?, ?)",
                   (message.chat.id, product_name))
    conn.commit()

    bot.send_photo(message.chat.id, photo=product_image, caption=f"Ви обрали: {product_name}. Дякуємо за замовлення!")

@bot.message_handler(commands=['orders'])
def show_user_orders(message):
    cursor.execute("SELECT product_name FROM orders WHERE user_id = ?", (message.chat.id,))
    orders = cursor.fetchall()

    if orders:
        orders_list = "\n".join([f"- {order[0]}" for order in orders])
        bot.send_message(message.chat.id, f"Ваші замовлення:\n{orders_list}")
    else:
        bot.send_message(message.chat.id, "У вас поки що немає замовлень.")

bot.polling()
