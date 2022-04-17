from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
print("hello1")
PATH = r"C:\Users\Andre\Downloads\chromedriver_win32\chromedriver.exe"
print("hello2")
driver = webdriver.Chrome(chrome_options = options, executable_path =PATH)
print("hello3")
driver.get("https://coinmarketcal.com/en/news/microstrategy-buys-an-additional-190-million-worth-of-bitcoin")
print("hello4")
link = driver.find_element_by_link_text("View coin")
link.click()
#time.sleep(50)
#driver.manage().window().maximize();
#driver.findElement(By.id("News")).click();

print("hello5")

page_source = driver.page_source
print("hello6")
#print(page_source)
print("hello7")
soup = BeautifulSoup(page_source, 'html.parser')
print(soup.prettify())
