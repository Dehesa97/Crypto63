

#TODO: Web scraped data from Internet using APIS
#Scrape numeric data using the APIS
#COINGECKO
import requests
import json
import os

#current Bitcoin price
coins1 = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").text
coins = json.loads(coins1)
price = int(coins["bitcoin"]["usd"])

#Bitcoin prices from 1st January 2018 till now
from datetime import datetime, timedelta

coins2 = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=1514764800&to=1648851926000").text
coins3 = json.loads(coins2) # dictionary containing all the prices from 1/1/18 till now in json format
UNIX_date = (coins3["prices"][0][0])/1000 #UNIX time needed in seconds so converts from milliseconds to second
print(datetime.fromtimestamp(int(UNIX_date)).strftime('%Y-%m-%d %H:%M:%S')) #date in specific format obtained
#TODO: get all prices printed along with corresponding date


#Scrape text data using the APIS

#------------------------------------------------------------

#TODO: Web scraped data from Internet using alternative methods.

