from fyers_apiv3 import fyersModel
import sys
import logging
import pandas as pd
pd.set_option('chained_assignment',None)
import numpy as np
sys.path.insert(1,r'D:/Projects/Backtest')
from constants import constants
from time_management.dates import intraday_dates,back_test_dates
from data_management.historical_data import HistoricalData
from datetime import datetime,timedelta
from collections import deque
logging.basicConfig(
    filename='./logs/algo.log',
    encoding='UTF-8',
    filemode='a',
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%d-%m-%Y %H:%M"
)

logger = logging.getLogger('algo')
logger.setLevel(logging.DEBUG)
class EmaRsi(HistoricalData):
    def __init__(self,year):
        self.year = year
        super().__init__(year)


    def runStrategy(self,symbol):
        """
        1. Stock should be in NR3 range
        2. Stock should have ratio of minimum percentage of 2% from the previous day close
        3. 5 min candle rally to be checked
        4. 5 min candle consecuitive three red candles for buy side and 3 green candles for sell side
        5. last candle amongst three candles should break the 20 ema
        6. RSI should be below 58 for buy side and above 58 for sell side
        7.
        """
        flag = None
        dfs = []
        print('Processing for symbol:',symbol)
        hist_data = pd.DataFrame()
        try:
            hist_data = pd.DataFrame()
            dfs = []
            total = []
            res = []
            result = []
            for row in intraday_dates:
                try:
                    from_date = row.split('|')[0]
                    to_date   = row.split('|')[1]
                    data      = HistoricalData(self.year).fetch_historical_data(symbol,from_date,to_date,'5')
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
                result = []
                flag = None
                while i<len(df[75:])-3:
                    idx1 = 73+i
                    idx2 = 74+i
                    idx3 = 75+i
                    idx4 = 76+i
                    if df.iloc[idx4].close > df.iloc[idx3].close and df.iloc[idx3].close > df.iloc[idx2].close and df.iloc[idx2].close > df.iloc[idx1].close and flag==None:
                        flag = 'Y'
                    elif df.iloc[idx4].close < df.iloc[idx3].close and df.iloc[idx3].close < df.iloc[idx2].close and df.iloc[idx2].close < df.iloc[idx1].close and flag==None:
                        flag = 'Y'
                    else:
                        pass

                    pct = round(((df.iloc[idx3].close-df.iloc[74].close)/df.iloc[74].close)*100,2)
                    if  df.iloc[idx1].close < df.iloc[idx1].open and \
                        df.iloc[idx2].close < df.iloc[idx2].open and \
                        df.iloc[idx3].close < df.iloc[idx3].open and \
                        df.iloc[idx3].close > df[:75]['high'].max() and pct>=2 and df.iloc[idx3].low < df.iloc[idx3].ema20 :

                        if df.iloc[idx1].volume < df.iloc[idx2].volume and \
                        df.iloc[idx2].volume < df.iloc[idx3].volume  and df.iloc[idx3].rsi<58:
                            #result  = 'Bullish Pattern Found for {0} at {1} with current percentage is {2} and RSI is {3}'.format(symbol, df.iloc[idx3].date,pct,df.iloc[idx3].rsi)
                            res = [symbol,df.iloc[idx3].date,'BULLISH',float(pct)] 

                    elif df.iloc[idx1].close > df.iloc[idx1].open and \
                         df.iloc[idx2].close > df.iloc[idx2].open and \
                         df.iloc[idx3].close > df.iloc[idx3].open and \
                         df.iloc[idx3].close < df[:75]['low'].min() and pct<=-2 and df.iloc[idx3].high > df.iloc[idx3].ema20 :
                        if df.iloc[idx1].volume < df.iloc[idx2].volume and \
                        df.iloc[idx2].volume < df.iloc[idx3].volume and df.iloc[idx3].rsi>58 :
                            #result = 'Bearish Pattern Found for {0} at {1} with current percentage is {2}'.format(symbol, df.iloc[idx3].date, pct, df.iloc[idx3].rsi )
                            res = [symbol,df.iloc[idx3].date,'BEARISH',float(pct)] 
                    i = i+1

            else:
                pass
        except Exception as e:
            print(str(e))
        if len(res)>0:
            return res
        else:
            return None
