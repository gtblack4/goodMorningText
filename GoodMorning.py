from telegram.client import Telegram
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from random import randint
import configparser
#gets the config information from 'config.ini'
#API credentials and the recipients number
config = configparser.ConfigParser()
config.read('config.ini')
settings = config['DEFAULT']

tg = Telegram(
	    api_id=settings["api_id"],
	    api_hash=settings['api_hash'],
	    phone=settings['phone'],
	    database_encryption_key=settings['database_encryption_key']
)
#gets the current day of the week
myDate = datetime.today().strftime('%A')
def sendText(phoneNumber,morningMessage):
	#api credentials


	#if its the first time the script runs, it needs to load the chats
	tg.login()
	result = tg.get_chats()
	result.wait()


	result = tg.send_message(
		chat_id=phoneNumber,
		text=morningMessage
	)

	result.wait()
	time.sleep(2)
	tg.stop()  # stops the telegram script

def getPetName():
	page = requests.get('https://www.robietherobot.com/pet-name-generator.htm')
	soup = BeautifulSoup(page.content,'html.parser')
	#gets the html part of the request
	html = list(soup.children)[2]
	#gets a list of all the h1 tags. There are 2. The 2nd tag contains the nickname and strips the html tags
	rawName = soup.find_all('h1')[1].get_text()
	#strips leading and trailing spaces, as well as removing excess spaces between words
	petName = rawName.lstrip().rstrip()
	petName = " ".join(petName.split())
	return petName
#adding a 20% chance to send use "Sweetcheeks" instead of a random name

dailyRoll = randint(1,10)
if dailyRoll in range(1,2):
	message = "Goodmorning Sweetcheeks. How did you sleep last night?"
else:
	petName = getPetName()
	message = "Happy " + str(myDate) + " my " + str(petName) + ". How is your morning going?" 
print(message)
sendText(settings['recipient'],message)