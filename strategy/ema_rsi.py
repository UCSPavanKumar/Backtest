from fyers_apiv3 import fyersModel
import sys
import logging
import pandas as pd
pd.set_option('chained_assignment',None)
import numpy as np
sys.path.insert(1,r'/home/iob/algotrading')
from backtest.historical_data import HistoricalData
from datetime import datetime,timedelta
from collections import deque
logging.basicConfig(
    filename='algo.log',
    encoding='UTF-8',
    filemode='a',
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%d-%m-%Y %H:%M"
)
logger = logging.getLogger('algo')
class EmaRsi(HistoricalData):
    def __init__(self):
        super().__init__()


    def runStrategy(self,dates,resolution,symbol,res):
        """ 
        1. Entry when stock is breaking 40 day high
        2. Exit when breaking 20 day low
        Args
            Symbols: datatype [list]
            dates: '|' separated with from and to dates
        """
        flag = None
        dfs = []
        hist_data = pd.DataFrame()
        try:
            hist_data = pd.DataFrame()
            dfs = []
            count = 0
            print('processing symbol: {0}'.format(symbol))
            for row in dates:
                try:
                    from_date = row.split('|')[0]
                    to_date   = row.split('|')[1]
                    data      = HistoricalData().fetch_historical_data(symbol,from_date,to_date,resolution)
                    data['symbol'] = symbol
                    dfs.append(data)
                except Exception as e:
                    continue
            if len(dfs)>0:
                hist_data = pd.concat(dfs)
                count = 0    
                hist_data['dttime'] = pd.to_datetime(hist_data['date'], format='%y-%m-%d')
                hist_data = hist_data.sort_values(by='dttime')
                hist_data['ema20'] = hist_data['close'].ewm(span=20,adjust=False).mean()
                df = hist_data
                df['diff'] = df['close'].diff() #axis = 0 column
                df['gain'] = np.where(df['diff']>0,df['diff'],0)
                df['loss'] = -np.where(df['diff']<0,df['diff'],0)
                df['flag'] = np.where(df['close']>df['open'],'BU','BE')
                df['avg_gain'] = df['gain'].rolling(14).sum()/df['gain'].ne(0).rolling(14).sum()
                df['avg_loss'] = df['loss'].rolling(14).sum()/df['loss'].ne(0).rolling(14).sum()
                df['rsi'] = 100-(100/(1+(np.where(df['avg_gain'].ne(None),df['avg_gain']/df['avg_loss'],0))))
                df['rsi'] = round(df['rsi'],2)
                i = 3
                result = None
                flag = None
                while i<len(df[75:])-3:
                    idx1 = 73+i
                    idx2 = 74+i
                    idx3 = 75+i
                    idx4 = 76+i
                    if df.iloc[idx4].close > df.iloc[idx3].close and df.iloc[idx3].close > df.iloc[idx2].close and df.iloc[idx2].close > df.iloc[idx1].close and flag==None:
                        print(df.iloc[idx4].date)
                        flag = 'Y'
                    elif df.iloc[idx4].close < df.iloc[idx3].close and df.iloc[idx3].close < df.iloc[idx2].close and df.iloc[idx2].close < df.iloc[idx1].close and flag==None:
                        flag = 'Y'
                    else:
                        pass

                    pct = round(((df.iloc[idx3].close-df.iloc[74].close)/df.iloc[74].close)*100,2)
                    if df.iloc[idx1].close < df.iloc[idx1].open and \
                    df.iloc[idx2].close < df.iloc[idx2].open and \
                    df.iloc[idx3].close < df.iloc[idx3].open and \
                    df.iloc[idx3].close > df[:75]['high'].max() and pct>=2 and df.iloc[idx3].low < df.iloc[idx3].ema20 and flag=='Y':
                        if df.iloc[idx1].volume < df.iloc[idx2].volume and \
                        df.iloc[idx2].volume < df.iloc[idx3].volume  and df.iloc[idx3].rsi<58:
                            result  = 'Bullish Pattern Found for {0} at {1} with current percentage is {2} and RSI is {3}'.format(symbol, df.iloc[idx3].date,pct,df.iloc[idx3].rsi)
                    elif df.iloc[idx1].close > df.iloc[idx1].open and \
                         df.iloc[idx2].close > df.iloc[idx2].open and \
                         df.iloc[idx3].close > df.iloc[idx3].open and \
                         df.iloc[idx3].close < df[:75]['low'].min() and pct<=-2 and df.iloc[idx3].high > df.iloc[idx3].ema20 and flag=='Y':
                        if df.iloc[idx1].volume < df.iloc[idx2].volume and \
                        df.iloc[idx2].volume < df.iloc[idx3].volume and df.iloc[idx3].rsi>58 :
                            result = 'Bearish Pattern Found for {0} at {1} with current percentage is {2}'.format(symbol, df.iloc[idx3].date, pct, df.iloc[idx3].rsi )     
                    i = i+1
                if result is None:
                    pass
                else:
                    res.append(result)
            else:
                pass    
        except Exception as e:
            print(str(e))