"""
Objectif : Create a vinted bot that will send a notification as soon as a new article is available.
We can pass some arguments like the price, the size, the type of article, etc...

"""

# import sys, getopt # Option in the execution

import requests
from bs4 import BeautifulSoup

import json
import datetime

import time
from random import randint

import settings
from telegram_notification import send_notification

# Stock all the current items
items = []

notification = False

# def clean_data(current_items):
#     for item in items:
#             """Check for item that are not available anymore"""
#             if item not in current_items:
#                 print(f"{item} is not available anymore")
#                 items.remove(item)
#                 content = f"❌ {item}"
#                 # Send a notification
#                 # send_notification(content, images)

def update_data():
    """Main function of the program"""

    current_items = []

    response = requests.get(settings.url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            script = soup.find_all('script')[47]
            data = json.loads(script.string)
            data = data['items']['byId'].values()
            print(data)
            for item in data:
                # Collect data
                title = item['title']
                description = item['description']
                original_price = item['original_price_numeric']
                actual_price = item['price_numeric'] # Format numérique
                # price = item['price'] # Format 4,00 €
                brand = item['brand']
                images = item['photos']
                login = item['user']['login']
                number_of_positive_feedback = item['user']['positive_feedback_count']
                number_of_neutral_feedback = item['user']['neutral_feedback_count']
                number_of_negative_feedback = item['user']['negative_feedback_count']
                # feedback_reputation = item['user']['feedback_reputation']
                created_at = item['user']['created_at']
                last_login = item['user']['last_loged_on_ts']
                last_log_on = item['user']['last_loged_on'] # Format type : "Hier à 19h"
                url = item['url']
                status = item['status']
                item = f"{login} - {title} {actual_price} € : {description}"
                # Save the item
                current_items.append(item)
                if item not in items:
                    items.append(item)
                    print(f"New item : {item} => {url}")
                    content = f'''🆕 {actual_price} € - {title}
📕 Description : {description}
Etat : {status}
Marque : {brand}
Prix original : {original_price} €
👤 {login}
Connecté pour la dernière fois {last_log_on.lower()}
🤗 Nombre de retour positifs : {number_of_positive_feedback}
😐 Nombre de retour neutres : {number_of_neutral_feedback}
😥 Nombre de retour négatifs : {number_of_negative_feedback}
🔗 {url}
                    '''                    
                    # Compte cré le {datetime.datetime.strptime(created_at[0:10], "%Y-%m-%d").strftime("%d-%m-%Y")}            
                    # {f"Ecart par rapport au prix de départ : {actual_price - original_price} €" if original_price != actual_price else None}
                    # content = f"✅ {price} - {title}\n🔗 {url}"
                    # Send notification
                    send_notification(content, images, notification)
                else:
                    print(f"{item} => {url}")

                # Clean our data
                # clean_data(current_items)
        except Exception as e:
            print(e)            
    else:
        print(response.status)


if __name__ == "__main__":
    while True:
        update_data()
        notification = True
        time.sleep(randint(60, 120))