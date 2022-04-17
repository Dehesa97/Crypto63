from xml.dom.minidom import Element
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

#----------Programming Selenium on CoinTelegraph-----------------------------------------------
def selenium_CoinTelegraph():

    current_date = datetime.today().strftime('%Y-%m-%d')

    #Point to the location of the chrome.exe file
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    #Point to the location of the chromedriver.exe file
    PATH = r"\\mfs01\user05\SGYJAVIE\Documents\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(chrome_options = options, executable_path =PATH)
    
    driver.maximize_window()
    
    driver.get("https://cointelegraph.com/tags/bitcoin")
    time.sleep(10)
   
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    #print(soup.prettify())

    #Looks for articles published in the previous day so if its 12/2/2022 it will look for articles published on 11/2/2022
    for dt in soup.select('time.post-card-inline__date'):
     date_time =dt.get('datetime')
     print(date_time)
    
    
    
    
    articles = soup.find_all("article")
    #print(articles)
   # for article in articles:
    #    print("--------------------------------")
     #   #print(article.prettify())
        #date_posted = article.find("class")
        #print(date_posted)
      #  if article.has_attr('datetime'):
       #     print(article['datetime'])
        ##else:
          #  print('no attribute present')
        


#--------------------------------------
selenium_CoinTelegraph()
