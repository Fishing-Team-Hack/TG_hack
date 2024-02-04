from telebot import types
import telebot
import cv2
from io import BytesIO
import sqlite3
from config import settings


def connect_to_database():
    conn = sqlite3.connect('')
    return conn


bot = telebot.TeleBot(settings['TOKEN_SEC'])


def open_img(img_path):
    carplate_img = cv2.imread(img_path)
    carplate_img = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)
    return carplate_img


def carplate_extract(image, carplate_haar_cascade):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    for x, y, w, h in carplate_rects:
        carplate_img = image[y+15:y+h-10, x+15:x+w-20]
        return carplate_img


def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image


def process_image(img_path):
    carplate_img_rgb = open_img(img_path)
    carplate_haar_cascade = cv2.CascadeClassifier('C:\code_c\Tg_hack\haarcascade_russian_plate_number.xml')

    carplate_extract_img = carplate_extract(carplate_img_rgb, carplate_haar_cascade)
    carplate_extract_img = enlarge_img(carplate_extract_img, 150)

    return carplate_extract_img


@bot.message_handler(commands=['get_car_plate'])
def handle_get_car_plate(message):
    img_path = 'C:\code_c\TG_hack\cars\car4.jpg'
    processed_img = process_image(img_path)

    _, buffer = cv2.imencode('.png', processed_img)
    img_bytes = BytesIO(buffer.tobytes())

    bot.send_photo(message.chat.id, img_bytes)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()
    conn.close()

    if existing_user:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('/view_guest_accesses_all_users'))
        markup.add(types.KeyboardButton('/all_guest_accesses'))
        markup.add(types.KeyboardButton('/list_users'))

        bot.reply_to(message, "Добро пожаловать в панель администрирования! Вот функции, которые вам доступны:",
                     reply_markup=markup)

    else:
        bot.reply_to(message, "Добро пожаловать! Пожалуйста, введите ваше имя:")


def process_first_name(message):
    first_name = message.text
    bot.send_message(message.chat.id, "Теперь введите вашу фамилию:")
    bot.register_next_step_handler(message, process_last_name, first_name)


def process_last_name(message, first_name):
    last_name = message.text
    bot.send_message(message.chat.id, "Введите ваш номер телефона:")
    bot.register_next_step_handler(message, process_phone_number, first_name, last_name)


def process_phone_number(message, first_name, last_name):
    phone_number = message.text
    user_id = message.chat.id
    add_security_user(user_id, first_name, last_name, phone_number)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/start'))

    bot.send_message(user_id, "Спасибо! Ваши данные добавлены в базу.", reply_markup=markup)


def add_security_user(user_id, first_name, last_name, phone_number):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (user_id, first_name, last_name, phone_number, apartment_number) VALUES (?, ?, ?, ?, 'security')",
                   (user_id, first_name, last_name, phone_number))
    conn.commit()
    conn.close()


@bot.message_handler(commands=['view_guest_accesses_all_users'])
def view_guest_accesses_all_users(message):
    conn = sqlite3.connect('C:\code_c\TG_hack\parking_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT g.user_id, g.car_number, g.start_date, g.end_date, g.start_time, g.end_time FROM Guest_Accesses g")
    accesses = cursor.fetchall()
    response = "Список гостевых доступов для всех жильцов:\n"
    for access in accesses:
        response += f"ID гостя: {access[0]}\nНомер машины: {access[1]}\nНачало доступа: {access[2]} {access[4]}\nКонец доступа: {access[3]} {access[5]}\n\n"
    bot.send_message(message.chat.id, response)
    conn.close()


@bot.message_handler(commands=['all_guest_accesses'])
def handle_all_guest_accesses(message):
    view_guest_accesses_all_users(message)


def list_users(message):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE apartment_number != 'security'")
    users = cursor.fetchall()
    conn.close()
    response = "Список жильцов:\n"
    for user in users:
        response += f"ID: {user[0]}, {user[2]} {user[1]}\n"
    bot.reply_to(message, response)
    get_user_info(message)


@bot.message_handler(commands=['list_users'])
def handle_list_users(message):
    list_users(message)


def get_user_info(message):
    bot.reply_to(message, "Введите ID пользователя, чтобы получить его информацию:")


@bot.message_handler(func=lambda message: True)
def handle_user_id(message):
    try:
        user_id = int(message.text)
    except ValueError:
        return
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        full_info = f"ID: {user_data[0]}\nФамилия: {user_data[1]}\nИмя: {user_data[2]}\nНомер телефона: {user_data[3]}\nНомер квартиры: {user_data[4]}"
        bot.reply_to(message, full_info)
    else:
        bot.reply_to(message, "Пользователь с таким ID не найден.")


bot.polling()