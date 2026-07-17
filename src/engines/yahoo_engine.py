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
        self.realtime_class = "container yf-z2uro5"  
        self.fundimental_class = "yf-gf32ga"
    
    def get_real_time_quote(self, stock_code):
        
        try:
            r = requests.get(self.url+stock_code, headers=self.headers)
            
            if r.status_code != 200:
                raise ConnectionError(f"Statue Code: {r.status_code}")
            web_content = BeautifulSoup(r.text, "lxml")
            
            # real time stock quote
            web_content_div = web_content.find_all('div', {'class': self.realtime_class})
            try:
                spans = web_content_div[0].find_all('span')
                texts = [str(span.get_text()).strip() for span in spans]
            except IndexError:
                raise
            
            if texts != []:
                realtime = {
                    "price": texts[0],
                    "change": texts[1],
                    "rate": texts[2]
                }
            else:
                raise ValueError

            # real time stock fundimentals
            web_content_li = web_content.find_all('li', {'class': self.fundimental_class})
            try:
                fundimentals = {}
                for tag in web_content_li:
                    spans = tag.find_all('span')
                    texts = [span.get_text() for span in spans]
                    fundimentals[str(texts[0]).strip()] = str(texts[1]).strip()
            except IndexError:
                raise
            
        except ConnectionError:
            print("网络链接失败，请尝试其他数据源！")
        except IndexError as e :
            print(f"页面解析失败, 无法找到对应数据块" + e)
        except ValueError:
            print(f"页面解释失败，在div: {self.class_path}下无法找到可用数据")
        
        time_stamp = datetime.datetime.now()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        
        result = {
            "stock_code": stock_code,
            "time": time_stamp,
            "realtime": realtime,
            "fundimentals": fundimentals
        }
        
        return result