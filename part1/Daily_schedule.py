import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def xpath_element(driver, xpath):
    
    try:
        element = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        element = []

    return element



def real_time_price(stock_code):
    url = f"https://finance.yahoo.com/quote/{stock_code}/"
    driver.get(url)
    
    # Stock quote
    xpath = '//*[@id="main-content-wrapper"]/section[1]/div[2]/div[1]/section/div/section[1]/div[1]'
    stock_price_info = xpath_element(driver, xpath).text.split()
    
    if stock_price_info != []:
        price = stock_price_info[0]
        change = stock_price_info[1]+' '+stock_price_info[2]
    else:
        price = []
        change = []
        
    # Stock fundimentals
    xpath = '//*[@id="main-content-wrapper"]/section[3]/div/div/div/ul'
    li_elements = xpath_element(driver, xpath).find_elements(By.TAG_NAME, "li")
    
    if li_elements:
        fundimental_info = {}
        for li in li_elements:
            kv = li.text.split("\n", maxsplit=2)
            fundimental_info[kv[0]] = kv[1]
        
        volume = fundimental_info["Volume"]
        one_year_target = fundimental_info["1y Target Est"]
    else:
        volume = []
        one_year_target = []
     
    return price, change, volume, latest_pattern, one_year_target


chrome_options = Options()
chrome_options.add_argument("--headless")   # not show chrome windows
chrome_service = Service("E:/Google/chromedriver-win32/chromedriver-win32/chromedriver.exe")
driver = webdriver.Chrome(options=chrome_options, service=chrome_service)


Stock = ['BRK-B', "PYPL", "TWTR", "AAPL", "AMZN", "MSFT", "FB", "GOOG"]

price, change, volume, latest_pattern, one_year_target = real_time_price(Stock[0])

print(price)
print(change)

# while(True):
    # df.to_csv