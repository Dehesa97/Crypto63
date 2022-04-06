

#TODO: 1) Web scraped data from Internet using APIS
    # 1.1) Scrape numeric data using the APIS
    #COINGECKO
from cgitb import text
from time import time
from unittest import result
from urllib import request
from bs4 import BeautifulSoup
import requests
import json
import os

#current Bitcoin price
def get_Bitcoin_price():
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

#---------------------------------------------------------------------------------------------------------------------------------

# 2) Scrape from articles key data using the Beautiful Soup from the Websites:CryptoNews.com, CoinMarketCal.com

# Scraping from CoinMarketCal 
# Have to disguise the request as being sent from Firefox otherwise will get error. Website has security features to prevent this.
def CoinMarketCal():
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    url = 'https://coinmarketcal.com/en/news/microstrategy-buys-an-additional-190-million-worth-of-bitcoin'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")
    print(page_soup.prettify())

# Scraping from CryptoNews
# Part of website is rendered in Javascript so cant use Beautiful soup just yet. Need to use Selenium first.
def CryptoNew():
    from selenium import webdriver
    import time

    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    print("hello1")
    PATH = r"C:\chromedriver.exe"
    print("hello2")
    driver = webdriver.Chrome(chrome_options = options, executable_path =PATH)
    print("hello3")
    driver.get("https://cryptonews.com/news/bitcoin-and-ethereum-reverse-gains-doge-outperforms.htm")
    print("hello4")
    time.sleep(50)
    print("hello5")
    page_source = driver.page_source
    print("hello6")
    print(page_source)
    print("hello7")
    #soup = BeautifulSoup(page_source, 'html.parser')
    #print(soup.prettify())


#CoinMarketCal()
CryptoNew()