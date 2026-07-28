import numpy as np
import pandas as pd
import pandas_ta as ta

import deprecation
from typing import Literal


def MA_Crossover_Strategy(data: pd.DataFrame, direction: Literal["both", "long", "short"]="both"):
    assert direction in ["both", "long", "short"], "direction should be chosen from (both / long / short)"
    
    if "MA5" not in data.columns:
        data['MA5'] = data['close'].rolling(5).mean()
    if "MA10" not in data.columns:
        data['MA10'] = data['close'].rolling(10).mean()
    if "MA20" not in data.columns:
        data['MA20'] = data['close'].rolling(20).mean()  

    OpenLong = []            # long signal
    CloseLong = []
    OpenShort = []           # short signal
    CloseShort = []
    Record = []          # record trade signal
    Long_position = False   
    Short_position = False
    
    def empty_signal():
        OpenLong.append(np.nan)
        CloseLong.append(np.nan)
        OpenShort.append(np.nan)
        CloseShort.append(np.nan)
    
    for i in range(len(data['close'])):
        if pd.notna(data['MA20'][i]):
            if (data['MA5'][i] > data['MA10'][i]) & (data['MA5'][i] > data['MA20'][i]): 
                if not Long_position and not Short_position:   # 开多
                    if direction in ("both", "long"):
                        OpenLong.append(data['close'][i])   
                        CloseLong.append(np.nan)
                        OpenShort.append(np.nan)
                        CloseShort.append(np.nan)
                        Long_position = True
                        Short_position = False
                        Record.append([i, data['close'][i], 'OpenLong'])
                    else:
                        empty_signal()
                elif Short_position and not Long_position:    # 平空
                    OpenLong.append(np.nan)   
                    CloseLong.append(np.nan)
                    OpenShort.append(np.nan)
                    CloseShort.append(data['close'][i])
                    Long_position = False
                    Short_position = False
                    Record.append([i, data['close'][i], 'CloseShort'])
                else:
                    empty_signal()   
            elif (data['MA5'][i] < data['MA10'][i]) & (data['MA5'][i] < data['MA20'][i]):
                if Long_position and not Short_position:        # 平多
                    OpenLong.append(np.nan)
                    CloseLong.append(data['close'][i])
                    OpenShort.append(np.nan)
                    CloseShort.append(np.nan)
                    Long_position = False
                    Short_position = False
                    Record.append([i, data['close'][i], 'CloseLong']) 
                elif not Short_position and not Long_position:  # 开空
                    if direction in ("both", "short"):
                        OpenLong.append(np.nan)
                        CloseLong.append(np.nan)
                        OpenShort.append(data['close'][i])
                        CloseShort.append(np.nan)
                        Long_position = False
                        Short_position = True
                        Record.append([i, data['close'][i], 'OpenShort'])
                    else:
                        empty_signal()
                else:
                    empty_signal()
            else:
                empty_signal()
        else:
            empty_signal()
    
    if len(Record) % 2 == 1:
        if Record[-1][2] == 'OpenLong':
            OpenLong[Record[-1][0]] = np.nan
        if Record[-1][2] == 'OpenShort':
            OpenShort[Record[-1][0]] = np.nan
        Record.pop()
    
    data['OpenLong'] = OpenLong
    data['CloseLong'] = CloseLong
    data['OpenShort'] = OpenShort
    data['CloseShort'] = CloseShort
    
    return data, Record


def MACD_Crossover_Strategy(data: pd.DataFrame, direction: Literal["both", "long", "short"]="both"):
    assert direction in ["both", "long", "short"], "direction should be chosen from (both / long / short)"

    if 'MACD_12_26_9' not in data.columns:
        macd = ta.momentum.macd(data['close']) * 100    # percentage
        macd.rename(columns={'MACD_12_26_9': 'MACD', 'MACDh_12_26_9': 'Histogram', 'MACDs_12_26_9': 'Signal'}, inplace=True)
        data = pd.concat([data, macd], axis=1).reindex(data.index)
    
    OpenLong = []            # long signal
    CloseLong = []
    OpenShort = []           # short signal
    CloseShort = []
    Record = []          # record trade signal
    Long_position = False   
    Short_position = False
    
    def empty_signal():
        OpenLong.append(np.nan)
        CloseLong.append(np.nan)
        OpenShort.append(np.nan)
        CloseShort.append(np.nan)
    
    for i in range(len(data['close'])):
        if i == 0:
            empty_signal()
        elif pd.notna(data['Histogram'][i-1]):
            if ((data['Histogram'][i-1] < 0) & (data['Histogram'][i] > 0)) & \
                ((data['MACD'][i] < 0) & (data['Signal'][i] < 0)):
                # Check the OpenLong or CloseShort position
                if not Long_position and not Short_position:   # 开多
                    if direction in ("both", "long"):
                        OpenLong.append(data['close'][i])   
                        CloseLong.append(np.nan)
                        OpenShort.append(np.nan)
                        CloseShort.append(np.nan)
                        Long_position = True
                        Short_position = False
                        Record.append([i, data['close'][i], 'OpenLong'])
                    else:
                        empty_signal()
                elif Short_position and not Long_position:    # 平空
                    OpenLong.append(np.nan)   
                    CloseLong.append(np.nan)
                    OpenShort.append(np.nan)
                    CloseShort.append(data['close'][i])
                    Long_position = False
                    Short_position = False
                    Record.append([i, data['close'][i], 'CloseShort'])
                else:
                    empty_signal()      
                          
            elif ((data['Histogram'][i-1] > 0) & (data['Histogram'][i] < 0)) & \
                ((data['MACD'][i] > 0) & (data['Signal'][i] > 0)):
                # Check the CloseLong or OpenShort position
                if Long_position and not Short_position:        # 平多
                    OpenLong.append(np.nan)
                    CloseLong.append(data['close'][i])
                    OpenShort.append(np.nan)
                    CloseShort.append(np.nan)
                    Long_position = False
                    Short_position = False
                    Record.append([i, data['close'][i], 'CloseLong']) 
                elif not Short_position and not Long_position:  # 开空
                    if direction in ("both", "short"):
                        OpenLong.append(np.nan)
                        CloseLong.append(np.nan)
                        OpenShort.append(data['close'][i])
                        CloseShort.append(np.nan)
                        Long_position = False
                        Short_position = True
                        Record.append([i, data['close'][i], 'OpenShort'])
                    else:
                        empty_signal()
                else:
                    empty_signal()
            else:
                empty_signal()
        else:
            empty_signal()
    
    if len(Record) % 2 == 1:
        if Record[-1][2] == 'OpenLong':
            OpenLong[Record[-1][0]] = np.nan
        if Record[-1][2] == 'OpenShort':
            OpenShort[Record[-1][0]] = np.nan
        Record.pop()
    
    data['OpenLong'] = OpenLong
    data['CloseLong'] = CloseLong
    data['OpenShort'] = OpenShort
    data['CloseShort'] = CloseShort
    
    return data, Record


def RSI_Crossover_Strategy(data: pd.DataFrame, direction: Literal["both", "long", "short"]="both"):
    assert direction in ["both", "long", "short"], "direction should be chosen from (both / long / short)"
    
    if "RSI" not in data.columns:
        data['RSI'] = ta.momentum.rsi(data['close'], 14)
 
    OpenLong = []            # long signal
    CloseLong = []
    OpenShort = []           # short signal
    CloseShort = []
    Record = []          # record trade signal
    Long_position = False   
    Short_position = False
    
    def empty_signal():
        OpenLong.append(np.nan)
        CloseLong.append(np.nan)
        OpenShort.append(np.nan)
        CloseShort.append(np.nan)
    
    for i in range(len(data['close'])):
        if i == 0:
            empty_signal()
        elif pd.notna(data['RSI'][i-1]):
            if ((data['RSI'][i-1] < 30) & (data['RSI'][i] > 30)):   # oversold
                # Check the OpenLong or CloseShort position
                if not Long_position and not Short_position:  # 开多
                    if direction in ("both", "long"):
                        OpenLong.append(data['close'][i])   
                        CloseLong.append(np.nan)
                        OpenShort.append(np.nan)
                        CloseShort.append(np.nan)
                        Long_position = True
                        Short_position = False
                        Record.append([i, data['close'][i], 'OpenLong'])
                    else:
                        empty_signal()
                elif Short_position and not Long_position:    # 平空
                    OpenLong.append(np.nan)   
                    CloseLong.append(np.nan)
                    OpenShort.append(np.nan)
                    CloseShort.append(data['close'][i])
                    Long_position = False
                    Short_position = False
                    Record.append([i, data['close'][i], 'CloseShort'])
                else:
                    empty_signal()      
                          
            elif ((data['RSI'][i-1] > 70) & (data['RSI'][i] < 70)):  # overbought
                # Check the CloseLong or OpenShort position
                if Long_position and not Short_position:       # 平多
                    OpenLong.append(np.nan)
                    CloseLong.append(data['close'][i])
                    OpenShort.append(np.nan)
                    CloseShort.append(np.nan)
                    Long_position = False
                    Short_position = False
                    Record.append([i, data['close'][i], 'CloseLong']) 
                elif not Short_position and not Long_position:  # 开空
                    if direction in ("both", "short"):
                        OpenLong.append(np.nan)
                        CloseLong.append(np.nan)
                        OpenShort.append(data['close'][i])
                        CloseShort.append(np.nan)
                        Long_position = False
                        Short_position = True
                        Record.append([i, data['close'][i], 'OpenShort'])
                    else:
                        empty_signal()
                else:
                    empty_signal()
            else:
                empty_signal()
        else:
            empty_signal()
    
    if len(Record) % 2 == 1:
        if Record[-1][2] == 'OpenLong':
            OpenLong[Record[-1][0]] = np.nan
        if Record[-1][2] == 'OpenShort':
            OpenShort[Record[-1][0]] = np.nan
        Record.pop()
    
    data['OpenLong'] = OpenLong
    data['CloseLong'] = CloseLong
    data['OpenShort'] = OpenShort
    data['CloseShort'] = CloseShort
    
    return data, Record
 

@deprecation.deprecated("This function has been deprecated, use MA_Crossover_Strategy instead.")
def MA_Strategy(data: pd.DataFrame):
    data['MA5'] = data['close'].rolling(5).mean()
    data['MA10'] = data['close'].rolling(10).mean()
    data['MA20'] = data['close'].rolling(20).mean()  

    Buy = []            # show buy in the graph
    Sell = []           # show sell in the graph
    Record = []         # record buy and sell
    position = False    # no short selling
    
    for i in range(len(data['close'])):
        if pd.notna(data['MA20'][i]):
            if (data['MA5'][i] > data['MA10'][i]) & (data['MA5'][i] > data['MA20'][i]): 
                # Buy Signal
                if position == False:    # don't hold stock
                    Buy.append(data['close'][i])
                    Sell.append(np.nan)
                    position = True      # reset 
                    Record.append([i, data['close'][i], 'Buy'])
                else:
                    Buy.append(np.nan)
                    Sell.append(np.nan)
            elif (data['MA5'][i] < data['MA10'][i]) & (data['MA5'][i] < data['MA20'][i]):
                # Sell Signal
                if position == True:    # hold stock
                    Buy.append(np.nan)
                    Sell.append(data['close'][i])
                    position = False    # reset
                    Record.append([i, data['close'][i], "Sell"])
                else:
                    Buy.append(np.nan)
                    Sell.append(np.nan)
            else:
                # Do nothing.
                Buy.append(np.nan)
                Sell.append(np.nan)
        else:
            # Do nothing.
            Buy.append(np.nan)
            Sell.append(np.nan) 
    
    if len(Record) % 2:
        if Record[-1][2] == 'Buy':
            Buy[Record[-1][0]] = np.nan
        Record.pop()
    
    data['Buy'] = Buy
    data['Sell'] = Sell
    return data, Record

@deprecation.deprecated("This function has been deprecated, use MACD_Crossover_Strategy instead.")
def MACD_Strategy(data: pd.DataFrame):
    macd = ta.momentum.macd(data['close']) * 100    # percentage
    macd.rename(columns={'MACD_12_26_9': 'MACD', 'MACDh_12_26_9': 'Histogram', 'MACDs_12_26_9': 'Signal'}, inplace=True)
    data = pd.concat([data, macd], axis=1).reindex(data.index)
 
    Buy = []            # show buy in the graph
    Sell = []           # show sell in the graph
    Record = []         # record buy and sell
    Buy_position = False   
    Sell_position = False
    
    for i in range(len(data['close'])):
        if i == 0:
            Buy.append(np.nan)
            Sell.append(np.nan)
        elif pd.notna(data['Histogram'][i-1]):
            if ((data['Histogram'][i-1] < 0) & (data['Histogram'][i] > 0)) & \
                ((data['MACD'][i] < 0) & (data['Signal'][i] < 0)):
                # Check the buying signal
                if Sell_position == True:
                    Buy.append(data['close'][i])
                    Sell.append(np.nan)
                    Buy_position = False
                    Sell_position = False
                    Record.append([i, data['close'][i], 'Buy'])
                elif Buy_position == False:
                    Buy.append(data['close'][i])
                    Sell.append(np.nan)
                    Buy_position = True
                    Sell_position = False
                    Record.append([i, data['close'][i], 'Buy'])    
                else:
                    Buy.append(np.nan)
                    Sell.append(np.nan)      
                          
            elif ((data['Histogram'][i-1] > 0) & (data['Histogram'][i] < 0)) & \
                ((data['MACD'][i] > 0) & (data['Signal'][i] > 0)):
                # Check the selling signal
                if Buy_position == True:
                    Buy.append(np.nan)
                    Sell.append(data['close'][i])
                    Buy_position = False
                    Sell_position = False
                    Record.append([i, data['close'][i], 'Sell']) 
                elif Sell_position == False:    # short-sell
                    Buy.append(np.nan)
                    Sell.append(data['close'][i])
                    Buy_position = False
                    Sell_position = True
                    Record.append([i, data['close'][i], 'Sell'])
                else:
                    Buy.append(np.nan)
                    Sell.append(np.nan)
            else:
                Buy.append(np.nan)
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)
    
    if len(Record) % 2:
        if Record[-1][2] == 'Buy':
            Buy[Record[-1][0]] = np.nan
        if Record[-1][2] == 'Sell':
            Sell[Record[-1][0]] = np.nan
        Record.pop()
    
    data['Buy'] = Buy
    data['Sell'] = Sell
    return data, Record


@deprecation.deprecated("This function has been deprecated, use RSI_Crossover_Strategy instead.")
def RSI_Strategy(data: pd.DataFrame):
    data['RSI'] = ta.momentum.rsi(data['close'], 14)
 
    Buy = []            # show buy in the graph
    Sell = []           # show sell in the graph
    Record = []         # record buy and sell
    Buy_position = False   
    Sell_position = False
    
    for i in range(len(data['close'])):
        if i == 0:
            Buy.append(np.nan)
            Sell.append(np.nan)
        elif pd.notna(data['RSI'][i-1]):
            if ((data['RSI'][i-1] < 30) & (data['RSI'][i] > 30)):   # oversold
                # Check the buying signal
                if Sell_position == True:
                    Buy.append(data['close'][i])
                    Sell.append(np.nan)
                    Buy_position = False
                    Sell_position = False
                    Record.append([i, data['close'][i], 'Buy'])
                elif Buy_position == False:
                    Buy.append(data['close'][i])
                    Sell.append(np.nan)
                    Buy_position = True
                    Sell_position = False
                    Record.append([i, data['close'][i], 'Buy'])    
                else:
                    Buy.append(np.nan)
                    Sell.append(np.nan)      
                          
            elif ((data['RSI'][i-1] > 70) & (data['RSI'][i] < 70)):  # overbought
                # Check the selling signal
                if Buy_position == True:
                    Buy.append(np.nan)
                    Sell.append(data['close'][i])
                    Buy_position = False
                    Sell_position = False
                    Record.append([i, data['close'][i], 'Sell']) 
                elif Sell_position == False:    # short-sell
                    Buy.append(np.nan)
                    Sell.append(data['close'][i])
                    Buy_position = False
                    Sell_position = True
                    Record.append([i, data['close'][i], 'Sell'])
                else:
                    Buy.append(np.nan)
                    Sell.append(np.nan)
            else:
                Buy.append(np.nan)
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)
    
    if len(Record) % 2:
        if Record[-1][2] == 'Buy':
            Buy[Record[-1][0]] = np.nan
        if Record[-1][2] == 'Sell':
            Sell[Record[-1][0]] = np.nan
        Record.pop()
    
    data['Buy'] = Buy
    data['Sell'] = Sell
    return data, Record