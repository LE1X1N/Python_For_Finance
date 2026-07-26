import numpy as np
import pandas as pd

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
    
    data['Buy'] = Buy
    data['Sell'] = Sell
    return data, Record