import pandas as pd
import numpy as np
import pandas_ta as ta
import matplotlib.pyplot as plt  
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from mplfinance.original_flavor import candlestick_ohlc


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
    return df


def compute_profit(i, Profit, ax):
    pass

def backtest_day(i, data_full):
    time_stamp = date_list[i]   # retrieve a timestamp
    year = int(time_stamp[0:4])
    month = int(time_stamp[5:7])
    day = int(time_stamp[8:10])

    data_day = data_full[(data_full['year'] == year) & (data_full['month'] == month) & (data_full['day'] == day)] 
    data_day.reset_index(inplace=True)
    return data_day, time_stamp
    
    

def MA_strategy(data):
    pass


def figure_design(ax):
    ax.set_facecolor("#091217")
    ax.tick_params(axis="both", labelsize=14, colors="white")
    ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color("#808080")
    ax.spines['top'].set_color("#808080")
    ax.spines['left'].set_color("#808080")
    ax.spines['right'].set_color("#808080")
    

def main_plot(data, ax, current_date, showMA=True, showBB=True, MA=True):
    candle_counter = range(len(data["open"]) - 1)
    ohlc = []
    
    for candle in candle_counter:
        append_me = candle_counter[candle], data['open'][candle], data['high'][candle],data['low'][candle], data['close'][candle]
        ohlc.append(append_me)
        
    ax.clear()
    
    if MA == True:
        candlestick_ohlc(ax, ohlc, width=0.4, colorup="#8B0000", colordown="#006400")
    else:
        candlestick_ohlc(ax, ohlc, width=0.4, colorup="#ff3503", colordown="#18b800")

    if showMA == True:
        pass
    
    if showBB == True:
        pass

    if showMA == True | showBB == True:
        pass
    
    if MA == True:
        Profit = 0
    else:
        Profit = 0
    
    figure_design(ax)
    
    ax.text(0.5, 1.05, 'Apple Inc. (AAPL) '+current_date, transform=ax1.transAxes, color="white", fontsize=16,
             fontweight='bold', horizontalalignment='center', verticalalignment='center')
        
    ax.grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
    ax.set_xticklabels([])
    
    return Profit

def subplot_MACD(data, ax):
    pass

def subplot_RSI(data, ax):
    pass


fig = plt.figure()
fig.patch.set_facecolor("#121416")
gs = fig.add_gridspec(6, 6)

ax1 = fig.add_subplot(gs[0:4, 0:6])
ax2 = fig.add_subplot(gs[4, 0:6])
ax3 = fig.add_subplot(gs[5, 0:6])


data_full = pd.read_csv("AAPL/AAPL_2024-07-01_to_2026-07-01_cp2.csv", header=0)

date_list = sorted(set([x[0:10] for x in data_full['datetime']]))   # all trading dates


def animate(i):
    print(i)
    data_day, current_date = backtest_day(i, data_full)
    
    if not data_day.empty:
        Profit = main_plot(data_day, ax1, current_date)
        # subplot_MACD(data_day, ax2)
        # subplot_RSI(data_day, ax3)
        # compute_profit(i, Profit, ax1)


ani = animation.FuncAnimation(fig, animate, interval=100)
# animate(1)
plt.show()