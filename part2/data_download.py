import os
import requests
import pandas as pd
from datetime import datetime, timedelta

ticker = "AAPL"
multiplier = "1"
timespan = "minute"
start_date_str = "2024-07-01"   # start
end_date_str = "2026-07-01"
limit = '50000'
API_KEY = os.environ.get('MASSIVE_API_KEY')

def fetch_agg_data(ticker, multiplier, timespan, start, end, limit, api_key):
    base_url = (
        f"https://api.massive.com/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start}/{end}?adjusted=true&sort=asc&limit={limit}&apiKey={api_key}"
    )
    resp = requests.get(base_url)
    res_json = resp.json()
    return res_json["results"]

all_results = []
current_start = start_date_str

while True:
    print(f"正在请求区间: {current_start} -> {end_date_str}")
    batch = fetch_agg_data(ticker, multiplier, timespan, current_start, end_date_str, limit, API_KEY)
    
    if not batch:
        break
    
    all_results.extend(batch)
    
    last_ts = batch[-1]["t"]        # 获取当前批次最后一条时间戳，转为下一轮起始日期
    last_dt = pd.to_datetime(last_ts, unit="ms")
    next_start_dt = last_dt + timedelta(minutes=1)
    current_start = next_start_dt.strftime("%Y-%m-%d")
    
    if next_start_dt >= pd.to_datetime(end_date_str):
        break

df = pd.DataFrame(all_results)
df['date'] = pd.to_datetime(df['t'], unit='ms')

output_name = f"{ticker}_{start_date_str}_to_{end_date_str}.csv"
df.to_csv(output_name, index=False)
print(f"完成！总共获取 {len(df)} 条K线，保存至 {output_name}")