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
    df = pd.read_csv(filename, header=None, usecols=usecols,
                     names=['time', stock_code, 'change', 'volume', 'pattern', 'target'],
                     index_col= 'time', parse_dates=['time'])
    
    index_with_nan = df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan, 0, inplace=True)
    
    df.index = pd.DatetimeIndex(df.index)
    
    df = string_to_number(df, stock_code)
    df = string_to_number(df, 'volume')
    df = string_to_number(df, 'target')
    
    latest_info = df.iloc[-1, :]
    latest_price = str(latest_info.iloc[0])
    latest_change = str(latest_info.iloc[1])
    
    df_vol = df['volume'].resample('1Min').mean()
    data = df[stock_code].resample('1Min').ohlc()
    data['time'] = data.index
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
    
    data['MA5'] = data['close'].rolling(5).mean()
    data['MA10'] = data['close'].rolling(10).mean()
    data['MA20'] = data['close'].rolling(20).mean()
    
    data['volume_diff'] = df_vol.diff()
    data[data['volume_diff'] < 0] = None
    
    index_with_nan = data.index(data.isnull().any(axis=1))
    data.drop(index_with_nan, 0, inplace = True)
    data.reset_index(drop=True, inplace=True)
    
    return data, latest_price, latest_change, df['pattern'][-1], df['target'][-1], df['volume'][-1]

def animate(i):
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime("%Y-%m-%d")
    filename =  str(time_stamp) + "stock data.csv"
    
    data, latest_price, latest_change, pattern, target, volume = read_data_ohlc(filename, Stock[0], [1, 2, 3, 4, 5, 6])
    
    
    
    
    