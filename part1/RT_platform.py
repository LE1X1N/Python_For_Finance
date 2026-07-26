import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
from mplfinance.original_flavor import candlestick_ohlc
from datetime import datetime
import math
import os
import time

fig = plt.figure()
fig.patch.set_facecolor('#121416')
gs = fig.add_gridspec(6,6)
ax0 = fig.add_subplot(gs[0:4, 0:4])
ax1 = fig.add_subplot(gs[0, 4:6])
ax2 = fig.add_subplot(gs[1, 4:6])
ax3 = fig.add_subplot(gs[2, 4:6])
ax4 = fig.add_subplot(gs[3, 4:6])
ax5 = fig.add_subplot(gs[4, 4:6])
ax6 = fig.add_subplot(gs[5, 4:6])
ax7 = fig.add_subplot(gs[4, 0:4])
ax8 = fig.add_subplot(gs[5, 0:4])

Stock = ["AAPL", "BRK-B", "PYPL", "AMZN", "BABA", "MSFT", "GOOG"]

def color_up_down(num):
    color_up = "#ff3503"
    color_down = "#18b800"
    if (isinstance(num, int) and num < 0) or (isinstance(num, str) and num[0] == "-"):
        return color_down
    else:
        return color_up
            

def figure_design(ax):
    ax.set_facecolor("#091217")
    ax.tick_params(axis="both", labelsize=14, colors="white")
    ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color("#808080")
    ax.spines['top'].set_color("#808080")
    ax.spines['left'].set_color("#808080")
    ax.spines['right'].set_color("#808080")

def subplot_plot(ax, stock_code, data, latest_price, latest_change, target):
    ax.clear()
    ax.plot(list(range(1, len(data['close'])+1)), data['close'], color='white', linewidth=2)  # line chart
    
    ymin = data['close'].min()
    ymax = data['close'].max()
    ystd = data['close'].std()
    
    if not math.isnan(ymax) and not math.isnan(ystd) and not math.isnan(ymin) and ystd!=0.0:
        ax.set_ylim([ymin-ystd*0.5, ymax+ystd*3])

    ax.text(0.02, 0.95, stock_code, transform=ax.transAxes, color="#FFBF00", fontsize=11, fontweight='bold', 
            horizontalalignment='left', verticalalignment='top')

    ax.text(0.22, 0.95, latest_price, transform=ax.transAxes, color="white", fontsize=11, fontweight='bold', 
            horizontalalignment='left', verticalalignment='top')

    ax.text(0.4, 0.95, latest_change, transform=ax.transAxes, color=color_up_down(latest_change), fontsize=11, fontweight='bold', 
            horizontalalignment='left', verticalalignment='top')

    ax.text(0.84, 0.95, target, transform=ax.transAxes, color="#08a0e9", fontsize=11, fontweight='bold', 
            horizontalalignment='left', verticalalignment='top') 
    
    figure_design(ax)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    

def string_to_number(df, column):
    if isinstance(df.iloc[0, df.columns.get_loc(column)], str):
        df[column] = df[column].str.replace(",", "")
        df[column] = df[column].astype(float)
    return df


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



def read_data_ohlc(filename, stock_code, usecols):
    # base df
    df = pd.read_csv(filename, header=None, usecols=usecols,
                     names=['time', 'price', 'change', 'volume', 'target'],
                     index_col= 'time', parse_dates=['time'])
    
    index_with_nan = df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan, axis=0, inplace=True)
    
    df.index = pd.DatetimeIndex(df.index)
    
    df = string_to_number(df, 'price')
    df = string_to_number(df, 'volume')
    df = string_to_number(df, 'target')
    
    latest_info = df.iloc[-1, :]
    latest_price = str(latest_info.iloc[0])
    latest_change = str(latest_info.iloc[1])
    
    # resample to 1Min
    data = df['price'].resample('30s').ohlc()   # resample price
    data['time'] = data.index
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
    
    # MA
    data['MA5'] = data['close'].rolling(5, min_periods=1).mean()
    data['MA10'] = data['close'].rolling(10, min_periods=1).mean()
    data['MA20'] = data['close'].rolling(20, min_periods=1).mean()
    # RSI
    data['RSI'] = compute_RSI(data['close'], time_window=14)
    data['RSI'] = data['RSI'].fillna(50)    # NAN -> 50
    
    # difference the accumulate volume
    df_vol = df['volume'].resample('30s').mean()    # resample volume
    data['volume_diff'] = df_vol.diff()
    data.loc[data['volume_diff'] < 0, 'volume_diff'] = None
    
    data.reset_index(drop=True, inplace=True)
    
    return data, latest_price, latest_change, df['target'][-1], df['volume'][-1]

def animate(i, filename):

    data, latest_price, latest_change, target, volume = read_data_ohlc(filename, Stock[0], [1, 2, 3, 4, 5])
    
    ohlc = []
    for candle in  range(len(data)):
        append_me = data.index[candle], data['open'][candle], data['high'][candle],data['low'][candle], data['close'][candle],
        ohlc.append(append_me) 
    
    """
       Ax0, Candlestick
    """
    ax0.clear()
    candlestick_ohlc(ax0, ohlc, width=0.4, colorup="#ff3503", colordown="#18b800")
    
    ax0.plot(data["MA5"], color="pink", linestyle="-", linewidth=1, label="  5 minutes SMA")
    ax0.plot(data["MA10"], color="orange", linestyle="-", linewidth=1, label="10 minutes SMA")
    ax0.plot(data["MA20"], color="#08a0e9", linestyle="-", linewidth=1, label="20 minutes SMA")
    
    # legend
    leg = ax0.legend(loc="upper left", facecolor = "#121416", fontsize=10)
    for text in leg.get_texts():
        plt.setp(text, color = "w")

    figure_design(ax0)
    
    # statistics above plot
    ax0.text(0.005, 1.05, Stock[0], transform=ax0.transAxes, color="black", fontsize=18,
             fontweight='bold', horizontalalignment='left', verticalalignment='center',
             bbox=dict(facecolor='#FFBF00'))
    
    ax0.text(0.22, 1.05, latest_price, transform=ax0.transAxes, color="white", fontsize=18,
             fontweight='bold', horizontalalignment='center', verticalalignment='center')
        
    ax0.text(0.5, 1.05, latest_change, transform=ax0.transAxes, color=color_up_down(latest_change), fontsize=18,
             fontweight='bold', horizontalalignment='center', verticalalignment='center')
    
    ax0.text(0.8, 1.05, target, transform=ax0.transAxes, color="#08a0e9", fontsize=18,
             fontweight='bold', horizontalalignment='center', verticalalignment='center') 
    
    # timestampe
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ax0.text(1.35, 1.05, time_stamp, transform=ax0.transAxes, color="white", fontsize=12,
             fontweight='bold', horizontalalignment='center', verticalalignment='center')

    ax0.grid(True, color="grey", linestyle="-", which='major', axis='both', linewidth=0.3)
    
    ax0.set_xticklabels([])
    
    """
       ax1 - ax6, Linechart
    """
    data_ax1, latest_price, latest_change, target, _ = read_data_ohlc(filename, Stock[1], [1, 6, 7, 8, 9])
    subplot_plot(ax1, Stock[1], data_ax1, latest_price, latest_change, target)
    
    data_ax2, latest_price, latest_change, target, _ = read_data_ohlc(filename, Stock[2], [1, 10, 11, 12, 13])
    subplot_plot(ax2, Stock[2], data_ax2, latest_price, latest_change, target)
    
    data_ax3, latest_price, latest_change, target, _ = read_data_ohlc(filename, Stock[3], [1, 14, 15, 16, 17])
    subplot_plot(ax3, Stock[3], data_ax3, latest_price, latest_change, target)
    
    data_ax4, latest_price, latest_change, target, _ = read_data_ohlc(filename, Stock[4], [1, 18, 19, 20, 21])
    subplot_plot(ax4, Stock[4], data_ax4, latest_price, latest_change, target)
    
    data_ax5, latest_price, latest_change, target, _ = read_data_ohlc(filename, Stock[5], [1, 22, 23, 24, 25])
    subplot_plot(ax5, Stock[5], data_ax5, latest_price, latest_change, target)
    
    data_ax6, latest_price, latest_change, target, _ = read_data_ohlc(filename, Stock[6], [1, 26, 27, 28, 29])
    subplot_plot(ax6, Stock[6], data_ax6, latest_price, latest_change, target)

    """
        Ax7, Barchart
    """
    ax7.clear()
    figure_design(ax7)
    ax7.axes.yaxis.set_visible(False)
    
    pos = (data['open'] - data['close']) < 0
    neg = (data['open'] - data['close']) > 0
    data['x_axis'] = list(range(1, len(data['volume_diff'])+1))
    ax7.bar(data['x_axis'][pos], data['volume_diff'][pos], color="#ff3503", width=0.8, align='center')
    ax7.bar(data['x_axis'][neg], data['volume_diff'][neg], color="#18b800", width=0.8, align='center')
    
    ymax = data['volume_diff'].max() 
    ystd = data['volume_diff'].std()
    if not math.isnan(ymax) and not math.isnan(ystd):
        ax7.set_ylim([0, ymax + ystd*3])
    
    ax7.text(0.01, 0.95, f"Volume: {int(volume):,}", transform=ax7.transAxes, color="white", fontsize=9, fontweight='bold', 
                horizontalalignment='left', verticalalignment='top') 
    ax7.grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
    ax7.set_xticklabels([])
    
    """
        Ax8, RSI
    """
    ax8.clear()
    figure_design(ax8)
    ax8.axes.yaxis.set_visible(False)
    ax8.set_ylim([-5, 105])
    
    ax8.axhline(30, linestyle='-', color='green', linewidth=0.5)
    ax8.axhline(50, linestyle='-', color='white', linewidth=0.5)
    ax8.axhline(70, linestyle='-', color='red', linewidth=0.5)
    ax8.plot(data['x_axis'], data['RSI'], color="#08a0e9", linewidth=1.5)

    ax8.text(0.01, 0.95, f"RSI: {str(round(data['RSI'].iloc[-1], 2))}", transform=ax8.transAxes, color="white", 
             fontsize=9, fontweight='bold', horizontalalignment='left', verticalalignment='top') 
    
    xdate = [i for i in data['time']]
    
    def mydate(x, pos=None):
        try:
            return xdate[int(x)].strftime('%H:%M')
        except IndexError:
            return ""
    
    ax8.xaxis.set_major_formatter(mticker.FuncFormatter(mydate))
    ax8.grid(True, color='grey', linestyle='-', which='major')

# animate(1)
# plt.show()


filename = f"stock_tick_{datetime.now().strftime('%Y-%m-%d')}.csv"

print("等待开盘...")
while (not os.path.exists(filename)):
    time.sleep(3)

print("开始渲染...")
ani = animation.FuncAnimation(fig, animate, fargs=(filename, ), interval=100, cache_frame_data=False)
plt.show()
    
    
    
    