from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
print("hello1")
PATH = r"C:\Users\Andre\Downloads\chromedriver_win32\chromedriver.exe"
print("hello2")
driver = webdriver.Chrome(chrome_options = options, executable_path =PATH)
print("hello3")
driver.get("https://cointelegraph.com/")
print("hello4")
time.sleep(50)
print("hello5")
page_source = driver.page_source
print("hello6")
#print(page_source)
print("hello7")
soup = BeautifulSoup(page_source, 'html.parser')
print(soup.prettify())
