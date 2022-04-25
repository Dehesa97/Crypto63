from cgitb import text
from time import time
from unittest import result
from urllib import request
from bs4 import BeautifulSoup
import requests
import json
import os
from transformers import pipeline
from pyparsing.core import Each

#---------------------------------------------------------------------------------------------------------------------------------
# Scrape from articles key data using the Beautiful Soup from the Websites:CryptoNews.com, CoinMarketCal.com and CoinTelegraph

def CoinMarketCal():
# Wev scraping from CoinMarketCal website
# Have to disguise the request as being sent from Firefox otherwise will get error. Website has security features to prevent this.

    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    url = 'https://coinmarketcal.com/en/news/microstrategy-buys-an-additional-190-million-worth-of-bitcoin'
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

    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    page = doc.find(attrs={"class" : "article-single__content category_contents_details"})
    textArray1 = []
    for paragraph in page.find_all("p") :
        textArray1.append(paragraph.text)
        print(paragraph.text)
    return textArray1

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

#-------------------Testing code ---------------------------
#sentiment analysis on CoinMarket
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
