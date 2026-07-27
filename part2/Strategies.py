import numpy as np
import pandas as pd
import pandas_ta as ta

def MA_Crossover_Strategy(data: pd.DataFrame):
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


def MACD_Crossover_Strategy(data: pd.DataFrame):
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
                          
            elif ((data['RSI'][i-1] > 70) & (data['RSI'][i] < 70)):
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