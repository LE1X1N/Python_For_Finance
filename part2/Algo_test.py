import pandas as pd
import numpy as np
import pandas_ta as ta
import matplotlib
import matplotlib.pyplot as plt  
import matplotlib.ticker as mticker
import matplotlib.animation as animation
from typing import Callable
from mplfinance.original_flavor import candlestick_ohlc

from Strategies import *

def compute_RSI(data, time_window):
    diff = data.diff(1).dropna()
    
    up_change = pd.Series(0, index=diff.index)
    down_change = pd.Series(0, index=diff.index)
    
    mask_up = diff > 0
    mask_down = diff < 0
    up_change[mask_up] = diff[mask_up]
    down_change[mask_down] = -diff[mask_down]   # abs
    
    up_avg = up_change.ewm(com=time_window-1, min_periods=time_window).mean()
    
    down_avg = down_change.ewm(com=time_window-1, min_periods=time_window).mean()
    down_avg = down_avg.mask(down_avg == 0, 1e-10)
    
    rs = up_avg / down_avg
    rsi = 100 - 100/(1+rs)
    return rsi

def compute_BollingerBands(df, n, m):   
    df['TP'] = (df['high'] + df['low'] + df['close']) / 3 # Typical Price
    df['std'] = df['TP'].rolling(n).std(ddof=0) # Standard Deviation 
    df['MA-TP'] = df['TP'].rolling(n).mean()    # Moving Average
    
    df['BBU'] = df['MA-TP'] + m * df["std"]    # Upper BollingerBand
    df['BBL'] = df['MA-TP'] - m * df["std"]    # Lower BollingerBand
    
    return df


def compute_profit(i, total_profit, Profit, ax: matplotlib.axes.Axes):
    total_profit = total_profit + Profit
    ax.text(0.9, 1.15, f'Total Profit: ${str(round(total_profit, 3))}',
            bbox = dict(facecolor='#FF7A01', alpha = 0.5),
            transform=ax.transAxes, color='white', fontsize=10, fontweight='bold',
            horizontalalignment='left', verticalalignment='center')
    return total_profit


def backtest_day(i, data_full):
    time_stamp = date_list[i]   # retrieve a timestamp
    year = int(time_stamp[0:4])
    month = int(time_stamp[5:7])
    day = int(time_stamp[8:10])

    data_day = data_full[(data_full['year'] == year) & (data_full['month'] == month) & (data_full['day'] == day)] 
    data_day.reset_index(inplace=True)
    return data_day, time_stamp
 
    
def figure_design(ax):
    ax.set_facecolor("#091217")
    ax.tick_params(axis="both", labelsize=14, colors="white")
    ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color("#808080")
    ax.spines['top'].set_color("#808080")
    ax.spines['left'].set_color("#808080")
    ax.spines['right'].set_color("#808080")


def main_plot(data, ax, current_date, showMA=True, showBB=True, showEMA=True):
    candle_counter = range(len(data["open"]) - 1)
    ohlc = []
    
    for candle in candle_counter:
        append_me = candle_counter[candle], data['open'][candle], data['high'][candle],data['low'][candle], data['close'][candle]
        ohlc.append(append_me)
        
    ax.clear()

    candlestick_ohlc(ax, ohlc, width=0.4, colorup="#8B0000", colordown="#006400")
    # candlestick_ohlc(ax, ohlc, width=0.4, colorup="#ff3503", colordown="#18b800")

    if showMA == True:
        data['MA5'] = data['close'].rolling(5).mean()
        data['MA10'] = data['close'].rolling(10).mean()
        data['MA20'] = data['close'].rolling(20).mean()
        
        ax.plot(data['MA5'], color='pink', linestyle='-', linewidth=1, label="5 minutes SMA")
        ax.plot(data['MA10'], color='orange', linestyle='-', linewidth=1, label="10 minutes SMA")
        ax.plot(data['MA20'], color='#08a0e9', linestyle='-', linewidth=1, label="20 minutes SMA")
        

    if showBB == True:
        # bb = ta.bbands(data['close'], length=20, lower_std=2, upper_std=2)
        # print(bb)
        
        data = compute_BollingerBands(data, 20, 2)
        
        ax.fill_between(data.index, data["BBU"], data["BBL"], 
                        facecolor='#666699', alpha=0.2, label="Bollinger Bands")
        ax.plot(data["BBU"], color="#666699", linestyle="-", linewidth=0.2)
        ax.plot(data["BBL"], color="#666699", linestyle="-", linewidth=0.2)
    
    if showEMA == True:
        data['EMA'] = data['close'].ewm(span=20, adjust=False).mean()
        ax.plot(data['EMA'], color='#08a0e9', linestyle='-', linewidth=1, label="20 periods EMA")
    
    if showMA or showBB or showEMA:
        leg = ax.legend(loc='upper left', facecolor="#121416", fontsize=10)
        # for text in leg.get_texts():
        #     text.set_color('w')
        plt.setp(leg.get_texts(), color='w')
    
    figure_design(ax)
    
    ax.text(0.5, 1.05, 'Apple Inc. (AAPL) '+current_date, transform=ax1.transAxes, color="white", fontsize=16,
             fontweight='bold', horizontalalignment='center', verticalalignment='center')
        
    ax.grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
    ax.set_xticklabels([])


def subplot_MACD(data: pd.DataFrame, ax: matplotlib.axes.Axes):
    # Moving Average Convergence Divergence
    ax.clear()
    figure_design(ax)
    
    macd = ta.momentum.macd(data['close']).fillna(0) * 100
    data = pd.concat([data, macd], axis=1).reindex(data.index)
    
    # MACD Line
    # ax.plot(np.where(data['MACD_12_26_9']==0, data['MACD_12_26_9'], None), label='MACD', linewidth=1, alpha=0)
    # ax.plot(np.where(data['MACD_12_26_9']!=0, data['MACD_12_26_9'], None), label='MACD', linewidth=1, color='white') # MACD Line
    ax.plot(data['MACD_12_26_9'], label='MACD', linewidth=1, color='white') 
     
    # Signal Line
    # ax.plot(np.where(data['MACDs_12_26_9']==0, data['MACDs_12_26_9'], None), label='signal', linewidth=1, color='orange')
    # ax.plot(np.where(data['MACDs_12_26_9']!=0, data['MACDs_12_26_9'], None), label='signal', linewidth=1, color='orange')
    ax.plot(data['MACDs_12_26_9'], label='signal', linewidth=1, color='orange')
    
    # Histogram
    pos = data['MACDh_12_26_9'] > 0  
    neg = data['MACDh_12_26_9'] < 0
    ax.bar(data.index[pos], data['MACDh_12_26_9'][pos], color="#8B0000", width=0.8, align='center')
    ax.bar(data.index[neg], data['MACDh_12_26_9'][neg], color="#006400", width=0.8, align='center')
    
    if len(data['MACD_12_26_9'] != 0):
        ax.text(0.01, 0.95, 'MACD(12, 26, 9)', transform=ax.transAxes, color='white', fontsize=10,
                fontweight='bold', horizontalalignment='left', verticalalignment='top')
    
    ax.grid(True, color='grey', linestyle="-", which='major', axis='both', linewidth='0.3')
    ax.set_xticklabels([])
    

def subplot_RSI(data: pd.DataFrame, ax: matplotlib.axes.Axes):
    ax.clear()
    figure_design(ax)
    
    ax.axes.yaxis.set_ticks([30, 70])
    ax.set_ylim([-2, 102])

    # data['RSI'] = compute_RSI(data['close'], 14)      # compute RSI
    data['RSI'] = ta.momentum.rsi(data['close'], 14).fillna(50)

    # data['x_axis'] = list(range(1, len(data['close']) + 1))
    # ax.plot(data['x_axis'], data['RSI'], color="white", linewidth=1)
    
    # ax.plot(np.where(data['RSI']== 0, data['RSI'], None), color='white', alpha=0)
    # ax.plot(np.where(data['RSI']!=0, data['RSI'], None), color='white', linewidth=1)
    
    ax.plot(data['RSI'], color="white", linewidth=1)
    
    if len(data['RSI'] != 0):
        ax.text(0.01, 0.95, f"RSI(14)", transform=ax.transAxes, color="white", 
               fontsize=9, fontweight='bold', horizontalalignment='left', verticalalignment='top') 

    ax.axhline(30, linestyle='-', color='green', linewidth=0.5)
    ax.axhline(50, linestyle='-', color='white', linewidth=0.5)
    ax.axhline(70, linestyle='-', color='red', linewidth=0.5)

    data['datetime'] = pd.to_datetime(data['datetime'], format="%Y-%m-%d %H:%M:%S")
    xdate = [i for i in data['datetime']]
    
    def mydate(x, pos=None):
        try:
            return xdate[int(x)].strftime('%H:%M')
        except IndexError:
            return ""
    
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(mydate))
    ax.grid(True, color='grey', linestyle='-', which='major')



def apply_strategy(data: pd.DataFrame, ax: matplotlib.axes.Axes, strategy_func: Callable, direction: str):
    # choose a strategy
    data, Record = strategy_func(data, direction)  
        
    # Open and Short signal scatter plot
    ax.scatter(data.index, data['OpenLong'], label="OpenLong", marker='^', color = "#FF6FFF", alpha=1, s=100)
    ax.scatter(data.index, data['CloseLong'], label="CloseLong", marker='v', color = "#00FFBD", alpha=1, s=100)
    ax.scatter(data.index, data['OpenShort'], label="OpenShort", marker='v', color = "#FF6FFF", alpha=1, s=100)
    ax.scatter(data.index, data['CloseShort'], label="CloseShort", marker='^', color = "#00FFBD", alpha=1, s=100)
    
    # Open and Short information on the right bar
    margin = 0.95
    for i, item in enumerate(Record):
        message = f"{i+1} {item[2]}@{item[1]}"
        if item[2] == 'OpenLong' or item[2] == 'OpenShort':
            ax.text(1.01, margin, message, bbox=dict(facecolor="#FF6FFF", alpha=0.5),
                        transform=ax.transAxes, color='white', fontsize=7, fontweight='bold',
                        horizontalalignment='left', verticalalignment='center')
        else:
            ax.text(1.01, margin, message, bbox=dict(facecolor="#00FFBD", alpha=0.5),
                        transform=ax.transAxes, color='white', fontsize=6, fontweight='bold',
                        horizontalalignment='left', verticalalignment='center')
        margin = margin - 0.055
        
    # compute day profit
    profit = 0
    for i, item in enumerate(Record):
        if item[2] == 'OpenLong' or item[2] == 'CloseShort':
            profit = profit - float(item[1])
        else:
            profit = profit + float(item[1])

    ax.text(0.9, 1.05, f"Daily Profit: ${str(round(profit, 3))}",
            bbox = dict(facecolor='white', alpha = 0.5),
            transform=ax.transAxes, color='black', fontsize=10, fontweight='bold',
            horizontalalignment='left', verticalalignment='center')
    return profit



fig = plt.figure(figsize=(16.0, 10.0))
fig.patch.set_facecolor("#121416")
gs = fig.add_gridspec(6, 6)

ax1 = fig.add_subplot(gs[0:4, 0:6])
ax2 = fig.add_subplot(gs[4, 0:6])
ax3 = fig.add_subplot(gs[5, 0:6])


data_full = pd.read_csv("AAPL/AAPL_2024-07-01_to_2026-07-01_cp2.csv", header=0)
date_list = sorted(set([x[0:10] for x in data_full['datetime']]))   # all trading dates
total_profit = 0.0

def animate(i):
    data_day, current_date = backtest_day(i, data_full)
    global total_profit
    
    if not data_day.empty:
        main_plot(data_day, ax1, current_date, showMA=False, showBB=False, showEMA=True)
        subplot_MACD(data_day, ax2)
        subplot_RSI(data_day, ax3)
        
        profit = apply_strategy(data_day, ax1, MA_Crossover_Strategy, direction="both")
        total_profit = compute_profit(i, total_profit, profit, ax1)

# ani = animation.FuncAnimation(fig, animate, interval=100)
animate(0)
plt.show()