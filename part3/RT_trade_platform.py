import math
import datetime
import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib as mpl
from matplotlib.axes import Axes
import matplotlib.cm as cm
from matplotlib.colors import to_hex
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.transforms as transform
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import CheckButtons
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

def plot_volume(ax: Axes, data: pd.DataFrame, volume: float):
    pos = (data['open'] - data['close']) <= 0   # index
    neg = (data['open'] - data['close']) > 0
    
    ax.bar(data.index[pos], data['volume_diff'][pos], color=COLORUP, width=0.8, align='center')
    ax.bar(data.index[neg], data['volume_diff'][neg], color=COLORDOWN, width=0.8, align='center')
    
    ymax =  data['volume_diff'].max()
    ystd =  data['volume_diff'].std()
    
    if not (math.isnan(ymax) or math.isnan(ystd)):
        ax.set_ylim([0, ymax + ystd])
    
    ax.text(0.01, 0.95, f'Volume: {int(volume):,}', transform=ax.transAxes, color='#e4e4e4',
            fontsize=8, fontweight='bold', horizontalalignment='left', verticalalignment='top')


def plot_MACD(ax: Axes, data: pd.DataFrame):
    ax.text(0.01, 0.95, 'MACD(12, 26, 9)', transform=ax.transAxes, color='white', fontsize=8,
                fontweight='bold', horizontalalignment='left', verticalalignment='top')
    
    if len(data['close']) > 33:
        macd = ta.momentum.macd(data['close']).fillna(0)
        data = pd.concat([data, macd], axis=1).reindex(data.index)

        ax.plot(data['MACD_12_26_9'], label='MACD', linewidth=1, color='white')     # MACD line
        ax.plot(data['MACDs_12_26_9'], label='signal', linewidth=1, color='orange') # Signal line
            
        # Histogram
        pos = data['MACDh_12_26_9'] >= 0  
        neg = data['MACDh_12_26_9'] < 0
        ax.bar(data.index[pos], data['MACDh_12_26_9'][pos], color="#8B0000", width=0.8, align='center')
        ax.bar(data.index[neg], data['MACDh_12_26_9'][neg], color="#006400", width=0.8, align='center')
        
    else:
        ax.axhline(y=0.5, color="#666666", linestyle='--', linewidth=0.8)
    
def plot_RSI(ax: Axes, data: pd.DataFrame):
    ax.set_ylim([0, 100])
    ax.axhline(30, linestyle='-', color='green', linewidth=0.5)
    ax.axhline(50, linestyle='-', color='white', linewidth=0.5)
    ax.axhline(70, linestyle='-', color='red', linewidth=0.5)

    data['RSI'] = ta.momentum.rsi(data['close'], 14).fillna(50)
    
    ax.plot(data['RSI'], color="#37a6ef", linewidth=1)
    ax.bar(data.index, data['RSI'], color="#006400", width=0.8, align='center', alpha=0)   # invisible bar for alignement
    
    ax.text(0.01, 0.95, f"RSI(14): {str(round(data['RSI'].iloc[-1], 2))}", transform=ax.transAxes, color="white", 
        fontsize=8, fontweight='bold', horizontalalignment='left', verticalalignment='top')


def plot_x_axis_time(ax: Axes, data: pd.DataFrame):
    # time
    xdate = data['time'].tolist()

    def mydate(x, pos=None):
        return xdate[int(x)].strftime('%H:%M') if int(x) < len(xdate) else ""

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(mydate))
    ax.grid(True, color='grey', linestyle='-', which='major')


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
    check = plt.axes([0.07, 0.73, 0.05, 0.1])   # x, y, width, heigh
    figure_design([check])
    check.set_facecolor("#121416")
    
    labels = ['SMA', 'EMA', 'BB'] # create a check button under check axes
    actives = [True, True, True]
    labels_num = len(labels)
    
    plot_button = CheckButtons(check, labels, actives,
                               frame_props={"facecolor": ["w"]*labels_num,
                                            "edgecolor": ["w"]*labels_num},
                               check_props={"color": ["#37a6ef"]*labels_num,
                                            "linewidths": [1.5]*labels_num},
                               label_props={"color": ["w"]*labels_num,
                                            "fontsize": [10]*labels_num})
    return plot_button


def interactive_strategy():
    check = plt.axes([0.07, 0.58, 0.05, 0.1])   # x, y, width, heigh
    figure_design([check])
    check.set_facecolor("#121416")
    
    labels = ['SMA', 'MACD', 'RSI', 'BB'] 
    actives = [False, True, False, False]
    labels_num = len(labels)
    
    plot_button = CheckButtons(check, labels, actives,
                               frame_props={"facecolor": ["w"]*labels_num,
                                            "edgecolor": ["w"]*labels_num},
                               check_props={"color": ["#37a6ef"]*labels_num,
                                            "linewidths": [1.5]*labels_num},
                               label_props={"color": ["w"]*labels_num,
                                            "fontsize": [10]*labels_num})
    return plot_button



def compute_plot_TA(ax: Axes, data: pd.DataFrame, 
                    showMA: bool=True, MAs: list=[5, 10, 20], 
                    showEMA: bool=True, EMAs: list=[20], 
                    showBB: bool=True, BB: list=[20, 2]):
    color_num = len(MAs) + len(EMAs)
    rgba = mpl.colormaps['tab20'].resampled(color_num)
    color_list = [to_hex(r) for r in rgba.colors]

    if showMA:
        for MA in MAs:
            name = f'MA{MA}'
            data[name] = data['close'].rolling(MA).mean()
            ax.plot(data[name], color=color_list[0], linestyle='-', linewidth=1, label=f"{MA} periods SMA")
            color_list.pop(0)
            
    if showEMA:
        for EMA in EMAs:
            name = f'EMA{EMA}'
            data[name] = data['close'].ewm(span=EMA, adjust=False).mean()
            ax.plot(data[name], color=color_list[0], linestyle='-', linewidth=1, label=f"{EMA} periods EMA")
            color_list.pop(0)

    if showBB:
        bb = ta.bbands(data['close'], length=BB[0], lower_std=BB[1], upper_std=BB[1])
        bb.rename(columns={"BBU_20_2_2":"BBU", "BBL_20_2_2":"BBL"}, inplace=True)
        data = pd.concat([data, bb], axis=1).reindex(data.index)

        ax.fill_between(data.index, data["BBU"], data["BBL"], 
                        facecolor='#666699', alpha=0.2, label="Bollinger Bands")
        ax.plot(data["BBU"], color="#666699", linestyle="-", linewidth=0.2)
        ax.plot(data["BBL"], color="#666699", linestyle="-", linewidth=0.2)

    return data
    
def animate(i):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # process raw tick data
    filename = f"stock_tick_{time_stamp[0:10]}.csv"
    data, latest_price, latest_change, target, volume= process_data(filename, Stock[0])
    
    """
        ax1
    """
    # Main
    ax_design(ax1, y_axis_visible=True, x_axis_visible=False)
    plot_header(ax1, Stock[0], latest_price, latest_change, target)
    ohlc = compute_plot_OHLC(ax1, data)
    
    # Technical Analysis Button 
    showMA_status, showEMA_status, showBB_status = plot_button_TA.get_status()
    
    # Plot TA
    data = compute_plot_TA(ax1, data, 
                           showMA=showMA_status, MAs = [5, 10, 20],
                           showEMA=showEMA_status, EMAs = [20],
                           showBB=showBB_status, BB=[20, 2])
    
    # Strategy Button
    MA_status, MACD_status, RSI_status, BB_status = plot_button_strategy.get_status()
    
    if MA_status and (len(data['close'])>20):
        MA_Strategy(ax1, data)
    
    if MACD_status and (len(data['close'])>26):
        MACD_Strategy(ax1, data)

    if RSI_status and (data['RSI'][-1]!=50):
        RSI_Strategy(ax1, data)

    if BB_status and (len(data['close'])>20):
        BB_Strategy(ax1, data)
    
    
    # legend
    leg = ax1.legend(loc='upper left', facecolor='#121416', fontsize=10)
    plt.setp(leg.get_texts(), color='w')
    
    """
        ax2
    """   
    # Sub volume
    ax_design(ax2, y_axis_visible=False, x_axis_visible=False)
    plot_volume(ax2, data, volume)

    """
        ax3
    """       
    # Sub MACD
    ax_design(ax3, y_axis_visible=True, x_axis_visible=False)
    plot_MACD(ax3, data)
 
    """
        ax4
    """     
    # Sub RSI
    ax_design(ax4, y_axis_visible=True, x_axis_visible=True)
    ax4.axes.yaxis.set_ticks([30, 70])
    plot_RSI(ax4, data)
    plot_x_axis_time(ax4, data)
    

    

fig = plt.figure()
fig.patch.set_facecolor('#121416')
gs = fig.add_gridspec(10, 6)
ax1 = fig.add_subplot(gs[0:7, 0:6])
ax2 = fig.add_subplot(gs[7, 0:6])
ax3 = fig.add_subplot(gs[8, 0:6])
ax4 = fig.add_subplot(gs[9, 0:6])
figure_design([ax1, ax2, ax3, ax4])

Stock = ['AAPL']

plot_button_TA = interactive_TA()               # global variable
plot_button_strategy = interactive_strategy()   # global variable

animate(0)  # for debug
# ani = animation.FuncAnimation(fig, animate, interval=100)

plt.show()