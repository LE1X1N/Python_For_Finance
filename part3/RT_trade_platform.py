import math
import datetime
import pandas as pd
import pandas_ta as ta
import numpy as np

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.transforms as transform
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import CheckButtons
from mycolorpy import colorlist as mcp
from mplfinance.original_flavor import candlestick_ohlc

COLORUP = "#eb4d5c"
COLORDOWN = "#53b987"

def figure_design(axs: list[Axes]):
    for ax in axs:
        ax.set_facecolor("#1e1e1e")
        ax.tick_params(axis='both', labelsize=14, colors="#e4e4e4")
        ax.ticklabel_format(useOffset=False)
        ax.spines['bottom'].set_color('#787878')
        ax.spines['top'].set_color('#787878')
        ax.spines['left'].set_color('#787878')
        ax.spines['right'].set_color('#787878')

def ax_design(ax: Axes, y_axis_visible: bool=False, x_axis_visible: bool=False):
    ax.clear()
    ax.grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
    
    if not y_axis_visible:
        ax.axes.yaxis.set_visible(False)
    else:
        ax.axes.yaxis.set_ticks_position('right')
    
    if not x_axis_visible:
        ax.axes.xaxis.set_visible(False)
    else:
        ax.tick_params(axis='x', which='major', labelsize=10)


def compute_plot_OHLC(ax: Axes, data: pd.DataFrame):
    # candlestick chart
    candle_counter = range(len(data['open']))   
    ohlc = []
    for i in candle_counter:
        append_ohlc = i, data['open'][i], data['high'][i], data['low'][i], data['close'][i]
        ohlc.append(append_ohlc)
    candlestick_ohlc(ax, ohlc, width=0.1, colorup=COLORUP, colordown=COLORDOWN)
    
    # price line
    if data['close'].iloc[-1] > data['open'].iloc[-1]:
        colorcode = COLORUP
    else:
        colorcode = COLORDOWN
    
    ax.axhline(data['close'].iloc[-1], linestyle='--', color=colorcode, linewidth=0.5)
    
    trans = transform.blended_transform_factory(ax.transAxes, ax.transData)
    ax.text(x=1.005, y=data['close'].iloc[-1], s=data['close'].iloc[-1], color='#e4e4e4', fontsize=12,
            transform=trans, horizontalalignment='left', verticalalignment='center',
            bbox=dict(facecolor=colorcode, edgecolor=colorcode))

    # OHLC text
    strings = ['Open', str(data['open'][i]), 
               'High', str(data['high'][i]), 
               'Low', str(data['low'][i]), 
               'Close', str(data['close'][i])]
    colors = ['#e4e4e4', colorcode, 
              '#e4e4e4', colorcode, 
              '#e4e4e4', colorcode, 
              '#e4e4e4', colorcode]

    margin_label = 0
    margin_price = 0
    
    for s, c in zip(strings, colors):
        ax.text(0.6+margin_label+margin_price, 0.95, s + " ", color=c,
                transform=ax.transAxes, fontsize=10, fontweight='bold',
                horizontalalignment='left', verticalalignment='center')
        
        if c == '#e4e4e4':
            margin_label = margin_label + 0.05
        else:
            margin_price = margin_price + 0.05
    return ohlc

def plot_header(ax: Axes, stock_code: str, latest_price: float, latest_change: str, target: float):
    ax.text(0.12, 0.95, stock_code, color='#e4e4e4',transform=ax.transAxes, fontsize=10, 
            fontweight='bold', horizontalalignment='left', verticalalignment='center')
    ax.text(0.18, 0.95, target, color='#08a0e9',transform=ax.transAxes, fontsize=10, 
            fontweight='bold', horizontalalignment='left', verticalalignment='center')
    ax.text(0.12, 0.90, latest_price, color='#e4e4e4',transform=ax.transAxes, fontsize=10, 
            fontweight='bold', horizontalalignment='left', verticalalignment='center')
    
    if latest_change[0] == '+':
        colorcode = COLORUP
    else:
        colorcode = COLORDOWN
    
    ax.text(0.18, 0.90, latest_change, color=colorcode,transform=ax.transAxes, fontsize=10, 
            fontweight='bold', horizontalalignment='left', verticalalignment='center')

    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ax.text(0.93, 1.05, time_stamp, color='white',transform=ax.transAxes, fontsize=10, 
            fontweight='bold', horizontalalignment='center', verticalalignment='center')

    ax.text(-0.08, 0.94, 'Indicators', color='white',transform=ax.transAxes, fontsize=10, 
            fontweight='bold', horizontalalignment='left', verticalalignment='center')
    
    ax.text(-0.08, 0.66, 'Strategy', color='white',transform=ax.transAxes, fontsize=10, 
            fontweight='bold', horizontalalignment='left', verticalalignment='center')

def plot_volume():
    pass

def plot_MACD():
    pass

def plot_RSI():
    pass

def plot_x_axis_time():
    pass

def process_data(filename: str, stock_name: str):
    df = pd.read_csv(filename, header=None, usecols=[1, 2, 3, 4, 5],
                     names=['time', 'price', 'change', 'volume', 'target'],
                     index_col= 'time', parse_dates=['time'])
    df.ffill(inplace=True)  # forward fill
    
    df['price'] = df['price'].astype(float)
    df['volume'] = df['volume'].str.replace(",", "", regex=False).astype(float)
    df['target'] = df['target'].astype(float)

    # data 
    data = df['price'].resample('1min').ohlc()      # resample price
    data['volume_diff'] = df['volume'].resample('1min').mean().diff().fillna(0)   # volume difference
    data['time'] = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
    data['RSI'] = ta.momentum.rsi(data['close'], 14)
    data['RSI'] = data['RSI'].fillna(50)
    data.reset_index(drop=True, inplace=True)
    
    latest_price = df['price'].iloc[-1]
    latest_change = df['change'].iloc[-1]
    target = df['target'].iloc[-1]
    volume = df['volume'].iloc[-1]
    
    return data, latest_price, latest_change, target, volume

def interactive_TA():
    pass

def interactive_strategy():
    pass

def animate(i):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # process raw tick data
    filename = f"stock_tick_{time_stamp[0:10]}.csv"
    data, latest_price, latest_change, target, volume= process_data(filename, Stock[0])
    
    
    # Main
    ax_design(ax1, y_axis_visible=True, x_axis_visible=False)
    plot_header(ax1, Stock[0], latest_price, latest_change, target)
    ohlc = compute_plot_OHLC(ax1, data)
    
    # Sub volume
    ax_design(ax2, y_axis_visible=False, x_axis_visible=False)
    
    # Sub MACD
    ax_design(ax3, y_axis_visible=True, x_axis_visible=False)
    
    # Sub RSI
    ax_design(ax4, y_axis_visible=True, x_axis_visible=True)



fig = plt.figure()
fig.patch.set_facecolor('#121416')
gs = fig.add_gridspec(10, 6)
ax1 = fig.add_subplot(gs[0:7, 0:6])
ax2 = fig.add_subplot(gs[7, 0:6])
ax3 = fig.add_subplot(gs[8, 0:6])
ax4 = fig.add_subplot(gs[9, 0:6])
figure_design([ax1, ax2, ax3, ax4])

Stock = ['AAPL']
plot_button_TA = interactive_TA()
plot_button_strategy = interactive_strategy()

# animate(0)  # for debug
ani = animation.FuncAnimation(fig, animate, interval=100)

plt.show()