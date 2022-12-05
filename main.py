"""
Main.py

The main script

Goal : Creating a Vinted bot that will send a notification as soon as a new article is available.
We can pass some arguments like the price, the size, the type of article, etc...
"""
import json
from time import sleep
from traceback import print_exc
from random import randint, random

from pyVinted import Vinted

import config
from utils import log
from notify import send_notification
from constants import NOTIFICATION_CONTENT

def update_data(items, notification):
    """Main function of the program"""

    # current_items = []

    vinted = Vinted()
    data = vinted.items.search(config.URL)
    
    for item in data:
        # Collect data
        title = item.title
        price = item.price
        currency = item.currency
        price = "%f %s" % (price, currency)
        brand = item.brand_title
        images = item.photo
        url = item.url
        # item = "{login} - {title} {actual_price} € : {description}".format(login=login, title=title, actual_price=actual_price, description=description)
        item = "%s - %s" % (title, price)
        # Save the item
        # current_items.append(item)
        if item not in items:
            log("New item : {item} => {url}".format(item=item, url=url), domain="Vinted")
            content = NOTIFICATION_CONTENT.format(
                price = price,
                title = title,
                brand = brand,
                url = url
            )
            # Send notification
            send_notification(content, images, notification)
            items.append(item)
        else:
            log("{item} => {url}".format(item=item, url=url), domain="Vinted")


if __name__ == "__main__":
    items = []
    notification = False
    while True:
        try:
            update_data(items, notification)
        except Exception:
            print_exc()
        notification = True
        sleep(randint(60, 120) + random())
