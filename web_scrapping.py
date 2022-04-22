
from cgitb import text
from time import time
from unittest import result
from urllib import request
from bs4 import BeautifulSoup
import requests
import json
import os


def get_Bitcoin_price():
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


#---------------------------------------------------------------------------------------------------------------------------------

# 2) Scrape from articles key data using the Beautiful Soup from the Websites:CryptoNews.com, CoinMarketCal.com

def CoinMarketCal():
# Scraping from CoinMarketCal
# Have to disguise the request as being sent from Firefox otherwise will get error. Website has security features to prevent this.

    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    url = 'https://coinmarketcal.com/en/news/microstrategy-buys-an-additional-190-million-worth-of-bitcoin'
    #url = 'https://coinmarketcal.com/en/news/bitcoin-2022-loses-some-evangelical-luster-as-crypto-goes-mainstream'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")
    page = page_soup.find(attrs={"class" : "my-4 news-content"})
    textArray1 = []
    for paragraph in page.find_all("p") :
        textArray1.append(paragraph.text)
        print(paragraph.text)
    return textArray1


def CryptoNew(url):
#Scraping from CryptoNews. The scrapping is not perfect ao it needs refining.

    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    #url = 'https://cryptonews.com/news/bitcoin-and-ethereum-reverse-gains-doge-outperforms.htm'
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    page = doc.find(attrs={"class" : "article-single__content category_contents_details"})
    textArray1 = []
    for paragraph in page.find_all("p") :
        textArray1.append(paragraph.text)
        print(paragraph.text)
    return textArray1


def CryptoNew1():
# Scraping from CryptoNews
# Part of website is rendered in Javascript so cant use Beautiful soup just yet. Need to use Selenium first.

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
    #print(page_source)
    print("hello7")
    soup = BeautifulSoup(page_source, 'html.parser')
    print(soup.prettify())



def CoinTelegraph(url):
# Scraping from CoinTelegraph
# Have to disguise the request as being sent from Firefox otherwise will get error. Website has security features to prevent this.

    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    #url = 'https://cointelegraph.com/news/bitcoin-holds-40k-over-easter-but-thin-liquidity-capitulation-risk-haunt-traders'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")
    page = page_soup.find(attrs={"class" : "post post-page__article"})
    textArray1 = []
    for paragraph in page.find_all("p") :
        textArray1.append(paragraph.text)
        print(paragraph.text)
    return textArray1

#-------Connor Code---------------------------------------
from transformers import pipeline
from pyparsing.core import Each

#This function performs sentiment analysis. What do we do with the results of this functions? Also does Connor need the scraped data so
# it can be fed to the model?
def sentiment(textArray):
  neut = 0
  pos = 0
  neg = 0
  for each in textArray:
     tex = sentiment_analysis(each)[0]
     if tex['label'] == "neutral":
        neut = neut + 1
     if tex['label'] == "positive":
        pos = pos + 1
     if tex['label'] == "negative":
        neg = neg + 1

  return([pos, neg, neut])

#Allocate a pipeline for sentiment-analysis
sentiment_analysis = pipeline("sentiment-analysis",model='ProsusAI/finbert')
#----------------------------------------------

# sentiment analysis on CoinMarket
#text1 = CoinMarketCal()
#result1 = sentiment(text1)
#print(result1[0])
#print(result1[1])
#print(result1[2])

#sentiment analysis in Crypto News
#print('----------------------')

#text2 = CryptoNew()
#result2 = sentiment(text2)
#print(result2[0])
#print(result2[1])
#print(result2[2])


#sentiment analysis in Coin Telegraph
#print('----------------------')

#text3 = CoinTelegraph()
#result3 = sentiment(text3)
#print(result3[0])
#print(result3[1])
#print(result3[2])

#TODO: Refine the text scraping. We need to discuss if we can use Selenium to automate the grabbing of
#       articles periodically.
