import pandas as pd  
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

"""
    Find content inside the url
"""
def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_div[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    
    return texts


"""
    Get the information from the url
"""
def real_time_price(stock_code):
    url = f"https://finance.yahoo.com/quote/{stock_code}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://finance.yahoo.com/'
    }
    
    # params = {"interval": "1d", "range": "1mo"}
    
    try:
        r = requests.get(url, headers=headers)
        web_content = BeautifulSoup(r.text, "lxml")
        texts = web_content_div(web_content, "container yf-z2uro5")
        
        if texts != []:
            price, change = texts[0], texts[1]
        else:
            price, change = [], []
        
    except ConnectionError:
        price, change = [], []
    
    return price, change


Stock = ["BRK-B"]

print(real_time_price(Stock[0]))