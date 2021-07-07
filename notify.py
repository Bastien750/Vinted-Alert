"""
Notify.py

Holds the notification logic, using the Telegram API
"""

#from telegram import *
#from telegram.ext import *

from utils import log
from config import TELEGRAM_KEY, CHAT_ID

log("Connecting to the Telegram API", "Telegram")
#bot = Bot(TELEGRAM_KEY)

def send_notification(content, images, notification):
    '''Sends a telegram notification'''
    # log(content, "Telegram")
    # print(images)
    # print(notification)
#    if notification:       
#        log("Notifying user about a new product", "Telegram")
#        bot.send_message(CHAT_ID, content)
#        # Send the 3 firsts images
#        for image in images[:3]:
#            bot.send_photo(CHAT_ID, image['url'])