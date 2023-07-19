import string
import random
import sqlite3
import datetime
import telebot
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
token = config.get('Bot', 'bot_token')
bot = telebot.TeleBot(token)
LOG_CHAT_ID = config.get('Bot', 'LOG_CHAT_ID')


def generate_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=12))
    return code

def send_log_message(message):
    bot.send_message(LOG_CHAT_ID, message)

def register_event(event):
    logging.info(event)


def send_and_update_log_file(file_path, user_ids):
    while True:
        with open(file_path, 'rb') as log_file:
            for user_id in user_ids:
                bot.send_document(user_id, log_file)
        time.sleep(60)






