import pandas as pd
import os

with open("AAPL/AAPL_2024-07-01_to_2026-07-01.csv", "r") as f:
    df = pd.read_csv(f)

data_full = df.rename(columns={
    "v": "volume",
    "vw": "weighted volume",
    "o": "open",
    "c": "close",
    "h": "high",
    "l": "low",
    "t": "timestamp",
    "n": "transactions"})

data_full['datetime'] = pd.to_datetime(data_full['date'], format="%Y-%m-%d %H:%M:%S")

data_full.drop('weighted volume', axis=1, inplace=True)
data_full.drop('timestamp', axis=1, inplace=True)
data_full.drop('transactions', axis=1, inplace=True)
data_full.drop('date', axis=1, inplace=True)

data_full['year'] = data_full['datetime'].dt.year
data_full['month'] = data_full['datetime'].dt.month
data_full['day'] = data_full['datetime'].dt.day
data_full['hour'] = data_full['datetime'].dt.hour
data_full['minute'] = data_full['datetime'].dt.minute

df = data_full.copy()

# 1st Period: Winter time (Jan to Feb) (Nov to Dec): 9:00am~3:59pm
cond_winter = df['month'].isin([1,2,11,12]) & (df['hour'] >= 9) & (df['hour'] <= 15)
# 2nd Period: Summer time (Mar to Oct): 8:00am~2:59pm
cond_summer = df['month'].between(3,10) & (df['hour'] >= 8) & (df['hour'] <= 14)

df = df[cond_winter | cond_summer]
df.reset_index(drop=True, inplace=True)

df.to_csv("AAPL/AAPL_2024-07-01_to_2026-07-01_cp2.csv", header=True, index=None)

