

#TODO: Web scraped data from Internet using APIS

#Scrape numeric data using the APIS

#COINGECKO
import requests
import json
import os

coins1 = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").text
coins = json.loads(coins1)
for coin in coins:
    print(coin, ' : ', coins[coin])
price = int(coins["bitcoin"]["usd"])
print(price)

os.system(f"notify-send  \"the price of BTC is {price}\"")
#TODO: Web scraped data from Internet using alternative methods.
