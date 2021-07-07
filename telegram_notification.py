from settings import API_KEY, CHAT_ID
from telegram import *
from telegram.ext import *

print('Bot start')
bot = Bot(API_KEY)
# # print(bot.get_me())

def send_notification(content, images, notification):
    if notification:
        """Send a telegram notification"""
        bot.send_message(CHAT_ID, content)
        # Send the 3 firsts images
        if len(images) > 3:
            for i in range(3):
                bot.send_photo(CHAT_ID, images[i]['url'])
        else:
            for image in images:
                bot.send_photo(CHAT_ID, image['url'])