import telebot
from telebot import types
import sqlite3
from config import settings
from datetime import datetime
# Установка токена вашего бота
bot = telebot.TeleBot(settings['TOKEN_MANG'])


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if not is_user_exists(user_id):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, "Привет! Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        show_main_menu(message)


def show_main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button1 = types.KeyboardButton(text='/change_data🥶')
    button2 = types.KeyboardButton(text='/add_car😈')
    button3 = types.KeyboardButton(text='/remove_car💀')
    button4 = types.KeyboardButton(text='/create_guest_access🙏🏿')
    button5 = types.KeyboardButton(text='/delete_guest_access🤡')

    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    keyboard.add(button5)

    bot.send_message(message.chat.id, "С возвращением! Вот функции, которыми ты можешь воспользоваться:", reply_markup=keyboard)


@bot.message_handler(commands=['change_data🥶'])
def change_data(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    # Создаем кнопки с текстами
    button1 = types.KeyboardButton(text='Изменить имя')
    button2 = types.KeyboardButton(text='Изменить фамилию')
    button3 = types.KeyboardButton(text='Изменить номер квартиры')
    button4 = types.KeyboardButton(text='Изменить номер телефона')
    back_button = types.KeyboardButton(text='Назад')

    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    keyboard.add(back_button)

    bot.send_message(message.chat.id, "Выберите, что вы хотите изменить:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text.lower() == "назад")
def process_go_back(message):
    show_main_menu(message)


@bot.message_handler(func=lambda message: message.text.lower() in ["изменить имя", "изменить фамилию", "изменить номер квартиры", "изменить номер телефона"])
def process_change_data_choice(message):
    choice = message.text.lower()
    user_id = message.chat.id

    if "имя" in choice:
        bot.send_message(user_id, "Введите новое имя:")
        bot.register_next_step_handler(message, update_name)
    elif "фамилию" in choice:
        bot.send_message(user_id, "Введите новую фамилию:")
        bot.register_next_step_handler(message, update_surname)
    elif "номер квартиры" in choice:
        bot.send_message(user_id, "Введите новый номер квартиры:")
        bot.register_next_step_handler(message, update_apartment_number)
    elif "номер телефона" in choice:
        bot.send_message(user_id, "Введите новый номер телефона:")
        bot.register_next_step_handler(message, update_phone_number)


def is_user_exists(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_name(message):
    name = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET first_name = ? WHERE user_id = ?", (name, user_id))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    surname = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET last_name = ? WHERE user_id = ?", (surname, user_id))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "В какой квартире ты живешь?")
    bot.register_next_step_handler(message, get_apartment_number)


def get_apartment_number(message):
    apartment_number = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET apartment_number = ? WHERE user_id = ?", (apartment_number, user_id))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "Какой у тебя номер телефона?")
    bot.register_next_step_handler(message, get_phone_number)


def get_phone_number(message):
    phone_number = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET phone_number = ? WHERE user_id = ?", (phone_number, user_id))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "Спасибо! Теперь у нас есть твои данные.")


def update_name(message):
    name = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET first_name = ? WHERE user_id = ?", (name, user_id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Имя успешно обновлено.")


def update_surname(message):
    surname = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET last_name = ? WHERE user_id = ?", (surname, user_id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Фамилия успешно обновлена.")


def update_apartment_number(message):
    apartment_number = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET apartment_number = ? WHERE user_id = ?", (apartment_number, user_id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Номер квартиры успешно обновлен.")


def update_phone_number(message):
    phone_number = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET phone_number = ? WHERE user_id = ?", (phone_number, user_id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Номер телефона успешно обновлен.")


def connect_to_database():
    conn = sqlite3.connect('parking_management.db')
    return conn


@bot.message_handler(commands=['add_car😈'])
def add_car(message):
    bot.send_message(message.chat.id, "Введите номер вашего автомобиля:")
    bot.register_next_step_handler(message, process_add_car)


def process_add_car(message):
    car_number = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Cars (user_id, car_number) VALUES (?, ?)", (user_id, car_number))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Автомобиль успешно добавлен в список.")


@bot.message_handler(commands=['remove_car💀'])
def remove_car(message):
    bot.send_message(message.chat.id, "Введите номер автомобиля, который хотите удалить из списка:")
    bot.register_next_step_handler(message, process_remove_car)


def process_remove_car(message):
    car_number = message.text
    user_id = message.chat.id
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cars WHERE user_id=? AND car_number=?", (user_id, car_number))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Автомобиль успешно удален из списка.")


@bot.message_handler(commands=['create_guest_access🙏🏿'])
def process_create_guest_access_car(message):
    car_number = message.text
    bot.send_message(message.chat.id, "Введите дату начала доступа в формате ГГГГ-ММ-ДД:")
    bot.register_next_step_handler(message, process_create_guest_access_start_date, car_number)


def process_create_guest_access_start_date(message, car_number):
    try:
        start_date = datetime.strptime(message.text, "%Y-%m-%d").date()
        bot.send_message(message.chat.id, "Введите время начала доступа в формате ЧЧ:ММ:")
        bot.register_next_step_handler(message, process_create_guest_access_start_time, car_number, start_date)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
        bot.register_next_step_handler(message, process_create_guest_access_car)


def process_create_guest_access_start_time(message, car_number, start_date):
    try:
        start_time = datetime.strptime(message.text, "%H:%M").time()
        bot.send_message(message.chat.id, "Введите дату окончания доступа в формате ГГГГ-ММ-ДД:")
        bot.register_next_step_handler(message, process_create_guest_access_end_date, car_number, start_date, start_time)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ.")
        bot.register_next_step_handler(message, process_create_guest_access_start_date, car_number)


def process_create_guest_access_end_date(message, car_number, start_date, start_time):
    try:
        end_date = datetime.strptime(message.text, "%Y-%m-%d").date()
        bot.send_message(message.chat.id, "Введите время окончания доступа в формате ЧЧ:ММ:")
        bot.register_next_step_handler(message, process_create_guest_access_end_time, car_number, start_date, start_time, end_date)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
        bot.register_next_step_handler


def process_create_guest_access_end_time(message, car_number, start_date, start_time, end_date):
    try:
        end_time = datetime.strptime(message.text, "%H:%M").time()

        # Convert dates and times to string format compatible with SQLite
        str_start_date = start_date.strftime("%Y-%m-%d")
        str_end_date = end_date.strftime("%Y-%m-%d")
        str_start_time = start_time.strftime("%H:%M")
        str_end_time = end_time.strftime("%H:%M")

        user_id = message.chat.id
        conn = connect_to_database()
        cursor = conn.cursor()

        # Use the converted string formats in the SQL query
        cursor.execute("INSERT INTO Guest_Accesses (user_id, car_number, start_date, end_date, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, car_number, str_start_date, str_end_date, str_start_time, str_end_time))

        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Разовый гостевой доступ успешно создан.")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ.")
        bot.register_next_step_handler(message, process_create_guest_access_end_date, car_number, start_date, start_time)


@bot.message_handler(commands=['delete_guest_access🤡'])
def delete_guest_access(message):
    conn = connect_to_database()
    cursor = conn.cursor()
    user_id = message.chat.id
    cursor.execute("SELECT * FROM Guest_Accesses WHERE user_id=?", (user_id,))
    guest_accesses = cursor.fetchall()
    conn.close()

    if guest_accesses:
        bot.send_message(message.chat.id, "Выберите гостевой доступ для удаления:")
        for guest_access in guest_accesses:
            bot.send_message(message.chat.id, f"ID: {guest_access[0]}, Номер автомобиля: {guest_access[2]}, "
                                              f"Начало: {guest_access[3]} {guest_access[5]}, "
                                              f"Окончание: {guest_access[4]} {guest_access[6]}")
        bot.register_next_step_handler(message, process_delete_guest_access)
    else:
        bot.send_message(message.chat.id, "У вас нет созданных гостевых доступов.")


def process_delete_guest_access(message):
    guest_access_id = message.text
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Guest_Accesses WHERE guest_access_id=?", (guest_access_id,))
    guest_access = cursor.fetchone()
    if guest_access:
        cursor.execute("DELETE FROM Guest_Accesses WHERE guest_access_id=?", (guest_access_id,))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Гостевой доступ успешно удален.")
    else:
        conn.close()
        bot.send_message(message.chat.id, "Гостевой доступ с указанным идентификатором не найден.")


# Запуск бота
bot.polling()