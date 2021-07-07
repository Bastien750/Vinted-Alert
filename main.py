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

from requests import get
from bs4 import BeautifulSoup

import config
from utils import log
from notify import send_notification
from constants import NOTIFICATION_CONTENT

def update_data(items, notification):
    """Main function of the program"""

    # current_items = []

    response = get(config.URL)
    response.raise_for_status() # exception catched in the main loop
    soup = BeautifulSoup(response.text, 'lxml') # lxml is faster but a dependency, "html.parser" is quite fast and installed by default
    script = soup.find_all('script')[47] # careful with this as it might change at any update
    data = json.loads(script.string) # might check the type="application/json"
    data = data['items']['byId'].values()
    # log(data, "Vinted") # --> debug
    
    for item in data:
        # Collect data
        title = item.get("title", "N/A")
        description = item.get("description", "No description")
        original_price = item.get("original_price_numeric", -1) # snake cased?!
        actual_price = item.get("price_numeric", -1) # digits
        # price = item.get("price", "ERR") # Format 4,00 €
        brand = item.get("brand", "N/A")
        images = item.get("photos", "No Photo") # should it be an URL --> provide a "Not Found URL"
        login = item.get("user", {}).get("login", "N/A")
        number_of_positive_feedback = item.get("user", {}).get("positive_feedback_count", -1)
        number_of_neutral_feedback = item.get("user", {}).get("neutral_feedback_count", -1)
        number_of_negative_feedback = item.get("user", {}).get("negative_feedback_count", -1)
        # feedback_reputation = item['user']['feedback_reputation']
        # created_at = item['user']['created_at']
        # last_login = item['user']['last_loged_on_ts']
        last_log_on = item.get("user", {}).get("last_loged_on", "Error") # Format type : "Hier à 19h"
        url = item.get("url", "N/A") # provide not found as default
        status = item.get("status", "N/A")
        item = "{login} - {title} {actual_price} € : {description}".format(login=login, title=title, actual_price=actual_price, description=description)
        # Save the item
        # current_items.append(item)
        if item not in items:
            log("New item : {item} => {url}".format(item=item, url=url), domain="Vinted")
            content = NOTIFICATION_CONTENT.format(
                actual_price = actual_price,
                title = title,
                description = description,
                status = status,
                brand = brand,
                original_price = original_price,
                login = login,
                last_log_on = str(last_log_on).lower(),
                positive_feedback = number_of_positive_feedback,
                neutral_feedback = number_of_neutral_feedback,
                negative_feedback = number_of_negative_feedback,
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