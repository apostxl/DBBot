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
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'{timestamp} - {event}'
    send_log_message(log_message)






