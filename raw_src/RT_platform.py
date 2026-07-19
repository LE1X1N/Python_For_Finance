import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
from mplfinance.original_flavor import candlestick_ohlc
import datetime
import math

fig = plt.figure()
fig.patch.set_facecolor('#121416')
gs = fig.add_gridspec(6,6)
ax1 = fig.add_subplot(gs[0:4, 0:4])
ax2 = fig.add_subplot(gs[0, 4:6])
ax3 = fig.add_subplot(gs[1, 4:6])
ax4 = fig.add_subplot(gs[2, 4:6])
ax5 = fig.add_subplot(gs[3, 4:6])
ax6 = fig.add_subplot(gs[4, 4:6])
ax7 = fig.add_subplot(gs[5, 4:6])
ax8 = fig.add_subplot(gs[4, 0:4])
ax9 = fig.add_subplot(gs[5, 0:4])

Stock = ["AAPL", "BRK-B", "PYPL", "AMZN", "BABA", "MSFT", "GOOG"]

def figure_design(ax):
    ax.set_facecolor("#091217")
    ax.tick_params(axis="both", labelsize=14, colors="white")
    ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color("#808080")
    ax.spines['top'].set_color("#808080")
    ax.spines['left'].set_color("#808080")
    ax.spines['right'].set_color("#808080")
    
def string_to_number(df, column):
    if isinstance(df.iloc[0, df.columns.get_loc(column)], str):
        df[column] = df[column].str.replace(",", "")
        df[column] = df[column].astype(float)
    return df

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
    data['MA5'] = data['close'].rolling(5).mean()
    data['MA10'] = data['close'].rolling(10).mean()
    data['MA20'] = data['close'].rolling(20).mean()
    
    # difference the accumulate volume
    df_vol = df['volume'].resample('30s').mean()    # resample volume
    data['volume_diff'] = df_vol.diff()     
    data[data['volume_diff'] < 0] = None
    
    index_with_nan = data.index[data.isnull().any(axis=1)]
    data.drop(index_with_nan, axis=0, inplace=True)
    data.reset_index(drop=True, inplace=True)
    
    return data, latest_price, latest_change, df['target'][-1], df['volume'][-1]

def animate(i):
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime("%Y-%m-%d")
    filename =  str(time_stamp) + " stock data.csv"
    
    data, latest_price, latest_change, target, volume = read_data_ohlc(filename, Stock[0], [1, 2, 3, 4, 5])
    
    ohlc = []
    for candle in  range(len(data['open'])-1):
        append_me = candle, data['open'][candle], data['high'][candle],data['low'][candle], data['close'][candle],
        ohlc.append(append_me) 
    
    ax1.clear()
    candlestick_ohlc(ax1, ohlc, width=0.4, colorup="#ff3503", colordown="#18b800")
    
    ax1.plot(data["MA5"], color="pink", linestyle="-", linewidth=1, label="5 minutes SMA")
    ax1.plot(data["MA10"], color="orange", linestyle="-", linewidth=1, label="10 minutes SMA")
    ax1.plot(data["MA20"], color="#08a0e9", linestyle="-", linewidth=1, label="20 minutes SMA")
    
    # legend
    leg = ax1.legend(loc="upper left", facecolor = "#121416", fontsize=10)
    for text in leg.get_texts():
        plt.setp(text, color = "w")

    figure_design(ax1)
    
    # statistics above plot
    ax1.text(0.005, 1.05, Stock[0], transform=ax1.transAxes, color="black", fontsize=18,
             fontweight='bold', horizontalalignment='left', verticalalignment='center',
             bbox=dict(facecolor='#FFBF00'))
    
    ax1.text(0.22, 1.05, latest_price, transform=ax1.transAxes, color="white", fontsize=18,
             fontweight='bold', horizontalalignment='center', verticalalignment='center')

    if latest_change[0] == "+":
        colorcode = "#ff3503"
    else:
        colorcode = "#18b800"
        
    ax1.text(0.5, 1.05, latest_change, transform=ax1.transAxes, color=colorcode, fontsize=18,
             fontweight='bold', horizontalalignment='center', verticalalignment='center')
    
    ax1.text(0.8, 1.05, target, transform=ax1.transAxes, color="#08a0e9", fontsize=18,
             fontweight='bold', horizontalalignment='center', verticalalignment='center') 
    
    # timestampe
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ax1.text(1.4, 1.05, time_stamp, transform=ax1.transAxes, color="white", fontsize=12,
             fontweight='bold', horizontalalignment='center', verticalalignment='center')

    ax1.grid(True, color="grey", linestyle="-", which='major', axis='both', linewidth=0.3)
    
    ax1.set_xticklabels([])
    

# animate(1)
# plt.show()

ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()
    
    
    
    