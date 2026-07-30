import math
import datetime
import pandas as pd
import pandas_ta as ta
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.transforms as transform
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import CheckButtons
from mycolorpy import colorlist as mcp
from mplfinance.original_flavor import candlestick_ohlc

def figure_design(axs: list[matplotlib.axes.Axes]):
    for ax in axs:
        ax.set_facecolor("#1e1e1e")
        ax.tick_params(axis='both', labelsize=14, colors="#e4e4e4")
        ax.ticklabel_format(useOffset=False)
        ax.spines['bottom'].set_color('#787878')
        ax.spines['top'].set_color('#787878')
        ax.spines['left'].set_color('#787878')
        ax.spines['right'].set_color('#787878')
        

def plot_volume():
    pass

def plot_MACD():
    pass

def plot_RSI():
    pass

def plot_x_axis_time():
    pass

def process_data():
    pass

def interactive_TA():
    pass

def interactive_strategy():
    pass

def animate():
    pass



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

# ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()