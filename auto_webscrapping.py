from xml.dom.minidom import Element
import time
from bs4 import BeautifulSoup
from datetime import datetime
from web_scrapping import CoinTelegraph
from web_scrapping import CryptoNew
from web_scrapping import sentiment
from datetime import date


#----------Programming Selenium on CoinTelegraph-----------------------------------------------
def Auto_CoinTelegraph():

    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    url = 'https://cointelegraph.com/tags/bitcoin'
    #url = 'https://coinmarketcal.com/en/news/bitcoin-2022-loses-some-evangelical-luster-as-crypto-goes-mainstream'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    #print(soup.prettify())

    #Looks for articles published on the very same day so if its 12/2/2022 it will look for articles published on 11/2/2022.
    today = date.today()
    d = today.strftime("%Y-%m-%d")
    page = soup.find(attrs={"class" : "post-card-inline__header"})

    # Iterates through all the articles and their dates and find which were published on this day.
    count = 0
    for dt in soup.select('time.post-card-inline__date') :
      date_time = dt.get('datetime')
      if (date_time == d):
       count = count + 1
       #print(date_time)

    # Takes the url links of the articles taken today and they are passed to the 'CoinTelegraph' functions and performs
    # sentiment analysis on them.
    counterArray=[]
    counterP = 0
    counterN = 0
    count2 = 0
    prefab = 'https://cointelegraph.com'
    for dt in soup.select('a.post-card-inline__figure-link'):
        if(count2 < count):
            url = dt.get('href')
            count2 = count2 + 1
            #print(url)
            final_url = prefab + url
            #print(final_url)
            text3 = CoinTelegraph(final_url)
            result3 = sentiment(text3)
            #print(result3[0])
            #print(result3[1])
            #print(result3[2])
            counterP = counterP + result3[0]
            counterN = counterN + result3[1]

    counterArray.append(counterP)
    counterArray.append(counterN)

    print('CoinTelegraph')
    print('Positive articles: ', counterP)
    print('Negative articles: ', counterN)
    print('\n')
    return counterArray


def Auto_CryptoNews():


    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    url = 'https://cryptonews.com/news/bitcoin-news/'
    #url = 'https://coinmarketcal.com/en/news/bitcoin-2022-loses-some-evangelical-luster-as-crypto-goes-mainstream'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    #print(soup.prettify())

    #Looks for articles published on the very same day so if its 12/2/2022 it will look for articles published on 11/2/2022.
    today = date.today()
    d = today.strftime("%Y-%m-%d")
    page = soup.find(attrs={"class" : "category_contents_details"})
    #print('--------------------------------------')
    #print(page.text)

    # Iterates through all the articles and their dates and find which were published on this day.
    count = 0
    for dt in page.select('div.article__badge-date') :
      date_time = dt.get('data-utctime')
      date2 = date_time[:10]
      #print(date2)
      if (date2 == d):
       count = count + 1
       #print(date2)

    # Takes the url links of the articles taken today and they are passed to the 'CoinTelegraph' functions and performs
    # sentiment analysis on them.
    counterArray=[]
    counterP = 0
    counterN = 0
    count2 = 0
    prefab = 'https://cryptonews.com/'
    for dt in soup.select('a.article__image'):
        if(count2 < count):
            url = dt.get('href')
            count2 = count2 + 1
            #print(url)
            final_url = prefab + url
            #print(final_url)
            text3 = CryptoNew(final_url)
            result3 = sentiment(text3)
            #print(result3[0])
            #print(result3[1])
            #print(result3[2])
            counterP = counterP + result3[0]
            counterN = counterN + result3[1]

    counterArray.append(counterP)
    counterArray.append(counterN)

    print('CryptoNews')
    print('Positive articles: ', counterP)
    print('Negative articles: ', counterN)
    print('\n')
    return counterArray


#--------------------------------------
#Auto_CoinTelegraph()
#Auto_CryptoNews()
