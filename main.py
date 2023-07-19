import configparser
import telebot
import datetime
from telebot import types
from functions import*
from security import*
from db_functions import*
from keys import*
import requests

config = configparser.ConfigParser()
config.read('config.ini')
token = config.get('Bot', 'bot_token')
LOG_CHAT_ID = config.get('Bot', 'LOG_CHAT_ID')
bot = telebot.TeleBot(token)
adminIDs = [admin_id.strip() for admin_id in config.get('Bot', 'adminID', fallback='').split(',')]

user_state = {}
logging.basicConfig(filename='log_file.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
selected_user_ids = [1085178918, 1075338656]  
send_and_update_log_file('log_file.log', selected_user_ids)

@bot.message_handler(commands=['admin'])
def admin_menu(message):
    user_ID = message.chat.id
    if check_admin_status(user_ID):
        markup = types.ReplyKeyboardMarkup(row_width=True)
        item1 = types.KeyboardButton('Пошук по базі даних')
        item2 = types.KeyboardButton('Панель адміністратора')
        markup.add(item1, item2)

        bot.reply_to(message, "Виберіть опцію:", reply_markup=markup)
    else:
        bot.reply_to(message, "Помилка")


@bot.message_handler(func=lambda message: message.text == 'Пошук по базі даних')
def search_database(message):
    user_ID = message.chat.id
    if check_admin_status(user_ID):
        bot.reply_to(message, "Введіть пошуковий запит")
         # Отправка запроса на API
        url = 'http://localhost:51001'  # Замените на ваш адрес API
        response = requests.post(url, data=payload)
    
    # Обработка ответа от API
        if response.status_code == 200:
            print('Данные успешно отправлены на API.')
        # Получение названия файла из заголовка ответа
            filename = response.headers.get('Content-Disposition').split('=')[1]
        # Сохранение файла
            with open(filename, 'wb') as file:
                file.write(response.content)
                print(f'Файл {filename} успешно сохранен.')
        
        # Отправка файла пользователю через Telegram
            chat_id = user_id 
            bot.send_document(chat_id=chat_id, document=open(filename, 'rb'))
            print(f'Файл {filename} успешно отправлен пользователю.')
        
        else:
            print(f'Ошибка при отправке данных на API. Код ошибки: {response.status_code}')
            bot.reply_to(message, "Запит оброблюється")
    elif check_access_key_by_user(user_ID):
        access_code = get_user_access_code(user_ID)
        if access_code:
            update_usage_left(access_code)  
            update_usage_left_users(user_ID)
            bot.reply_to(message, "Введіть пошуковий запит")
            bot.reply_to(message, "Запит оброблюється")
        else:
            bot.reply_to(message, "Ваш ключ доступу не знайдено")
    else:
        bot.reply_to(message, "Помилка")


@bot.message_handler(func=lambda message: message.text == 'Панель адміністратора')
def admin_panel(message):
    user_ID = message.chat.id
    if check_admin_status(user_ID):
        markup = types.ReplyKeyboardMarkup(row_width=True)
        item1 = types.KeyboardButton('Додати адміністратора')
        item2 = types.KeyboardButton('Отримати код доступу')
        item3 = types.KeyboardButton('Повернутися')
        markup.add(item1, item2, item3)
        event = f'Користувач {message.from_user.username} увійшов у панель адміністратора.'
        register_event(event)
        bot.reply_to(message, "Виберіть опцію:", reply_markup=markup)
    else:
        bot.reply_to(message, "Помилка")


@bot.message_handler(func=lambda message: message.text == 'Додати адміністратора')
def add_admin(message):
    user_ID = message.chat.id
    if check_admin_status(user_ID):
        bot.reply_to(message, "Уведіть ID користувача:")
        user_state[user_ID] = 'awaiting_admin_id'  # Установка состояния ожидания ID администратора
        markup = types.ReplyKeyboardMarkup(row_width=True)
    else:
        bot.reply_to(message, "Помилка")


@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == 'awaiting_admin_id')
def save_admin_id(message):
    user_ID = message.chat.id
    if message.text.isdigit():
        admin_ID = int(message.text)
        if not check_admins_database(admin_ID):
            add_admin_to_database(admin_ID)
            bot.reply_to(message, "ID адміністратора було збережено")
        else:
            bot.reply_to(message, "Цей користувач вже є адміністратором")
        user_state[user_ID] = None
    else:
        bot.reply_to(message, "Неправильний формат ID. Спробуйте ще раз.")
        user_state[user_ID] = None


@bot.message_handler(func=lambda message: message.text == 'Згенерувати код доступу')
def get_access_code(message):
    user_ID = message.chat.id
    if check_admin_status(user_ID):
        access_code = generate_code()
        add_key_to_database(access_code)
        event = f'Користувач {message.from_user.username} отримав код доступу.'
        register_event(event)
        bot.reply_to(message, f"Ваш код доступу: {access_code}")
    else:
        bot.reply_to(message, "Помилка")


@bot.message_handler(func=lambda message: message.text == 'Повернутися')
def go_back(message):
    user_ID = message.chat.id
    if check_admin_status(user_ID):
        markup = types.ReplyKeyboardMarkup(row_width=True)
        item1 = types.KeyboardButton('Пошук по базі даних')
        item2 = types.KeyboardButton('Панель адміністратора')
        markup.add(item1, item2)
        bot.reply_to(message, "Повертаємось назад", reply_markup=markup)
    else:
        bot.reply_to(message, "Помилка")

@bot.message_handler(func=lambda message: message.text == 'Статус ключа')
def get_usage_left_message(message):
    user_ID = message.chat.id
    if check_access_key_by_user(user_ID):
        usage_left = get_usage_left(user_ID)
        bot.reply_to(message, f"Залишилось запитів: {usage_left}")
    else:
        bot.reply_to(message, "Помилка")

#===========ОБРАБОТКА КОМАНДЫ /KEY И ПРОВЕРКА ВАЛИДНОСТИ КЛЮЧА===============================
@bot.message_handler(commands=['key'])
def handle_key_command(message):
    user_ID = message.chat.id
    bot.reply_to(message, "Введіть ключ доступу:")
    user_state[user_ID] = 'awaiting_key'  # Установка состояния ожидания ключа

@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == 'awaiting_key')
def handle_access_key(message):
    user_ID = message.chat.id
    if check_access_key(message.text):
        markup = types.ReplyKeyboardMarkup(row_width=True)
        item1 = types.KeyboardButton('Пошук по базі даних')
        item2 = types.KeyboardButton('Статус ключа')
        markup.add(item1, item2)
        event = f'Користувач {message.from_user.username} увійшов за допомогою ключа.'
        register_event(event)
        bot.reply_to(message, "Ви маєте доступ до бота", reply_markup=markup)
        user_state[user_ID] = 'access_granted'
        username = message.from_user.username
        access_code = message.text
        usage_left = 10
        save_user_to_database(user_ID, username, "", access_code, usage_left)
    else:
        bot.reply_to(message, "Введено неправильний ключ доступу")


bot.infinity_polling()
