from ..core import BaseStockEngine
import requests
import pandas as pd  
import datetime
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

class YahooEngine(BaseStockEngine):
    
    def __init__(self):
        super().__init__()
        
        self.url =  "https://finance.yahoo.com/quote/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://finance.yahoo.com/'
        }
        self.class_path = "container yf-z2uro5"  
    
    def get_real_time_quote(self, stock_code):
        price, change, rate = -1,-1,-1
        
        try:
            r = requests.get(self.url+stock_code, headers=self.headers)
            
            if r.status_code != 200:
                raise ConnectionError(f"Statue Code: {r.status_code}")
            
            web_content = BeautifulSoup(r.text, "lxml")
            web_content_div = web_content.find_all('div', {'class': self.class_path})
            try:
                spans = web_content_div[0].find_all('span')
                texts = [span.get_text() for span in spans]
            except IndexError:
                raise
            
            if texts != []:
                price, change, rate = texts[0], texts[1], texts[2]
            else:
                raise ValueError
            
        except ConnectionError:
            print("网络链接失败，请尝试其他数据源！")
        except IndexError as e :
            print(f"页面解析失败, 无法找到div: {self.class_path}" + e)
        except ValueError:
            print(f"页面解释失败，在div: {self.class_path}下无法找到可用数据")
        
        return price, change, rate