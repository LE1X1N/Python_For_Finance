import pandas as pd  
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

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

def web_content_li(web_content, class_path):
    web_content_li = web_content.find_all('li', {'class': class_path})
    fundimentals = {}
    try:
        for tag in web_content_li:
            spans = tag.find_all('span')
            texts = [span.get_text() for span in spans]
            fundimentals[str(texts[0]).strip()] = str(texts[1]).strip()
    except IndexError:
        texts = []
    
    return fundimentals


"""
    Get the information from the url
"""
def real_time_price(stock_code):
    
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://finance.yahoo.com/'
        }
    url = f"https://finance.yahoo.com/quote/{stock_code}/"
    try:
        r = requests.get(url, headers=headers)
        web_content = BeautifulSoup(r.text, "lxml")
        texts = web_content_div(web_content, "container yf-z2uro5")
        
        if texts != []:
            price, change = texts[0], texts[1]+texts[2]
        else:
            price, change = [], []
        
        fundimentals = web_content_li(web_content, "yf-gf32ga")
        
        volume = fundimentals["Volume"]
        one_year_target = fundimentals["1y Target Est"]
    
        
    except ConnectionError:
        price, change, volume, one_year_target = [], [], [], []
    
    return price, change, volume, one_year_target


Stock = ["AAPL", "BRK-B", "PYPL", "AMZN", "BABA", "MSFT", "GOOG"]

while (True):
    info = []
    col = []
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
    
    for stock_code in Stock:
        price, change, volume, one_year_target = real_time_price(stock_code)
        info.append(price)
        info.extend([change])
        info.extend([volume])
        info.extend([one_year_target])
    
    col = [time_stamp]
    col.extend(info)
    df = pd.DataFrame(col).T
    df.to_csv(str(time_stamp[0:11])+'stock data.csv', mode='a', header=False)
    print(col)
        