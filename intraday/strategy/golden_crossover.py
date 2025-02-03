from fyers_apiv3 import fyersModel
import sys
import logging
from datetime import datetime,timedelta
from collections import deque
import pandas as pd
sys.path.insert(1,r'/home/iob/algotrading')
logging.basicConfig(
    filename='crossover.log',
    encoding='UTF-8',
    filemode='a',
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%d-%m-%Y %H:%M"
)
logger =logging.getLogger('crossover')
from data_management.historical_data import HistoricalData
class GoldenCrossOver(HistoricalData):
    def __init__(self):
        super().__init__()

    def get_dates_index(self,date_str:datetime,length):
        """

        """
        dts = deque()
        in_dt = datetime(date_str.year,date_str.month,date_str.day,9,15)
        dt = in_dt
        for i in range(1,length):
            dt = dt+timedelta(minutes=5)
            dts.append(dt)
        dts.appendleft(in_dt)
        return dts

    def runStrategy(self,dates:str,symbol:str,resolution:str,high_ema:int,low_ema:int,dct:list,logs:list):
        """
        1. Checking for first 5 min candle of day with prev day close
        2. Day's Pct change over previous day candle
        3. 5 min high-low pct of previous day close

        Args
            Symbols: datatype [list]
        """
        print('Processing Symbol: {0}'.format(symbol))

        hist_data = pd.DataFrame()
        dfs = []
        result = {}
        for row in dates:
            try:
                from_date = row.split('|')[0]
                to_date   = row.split('|')[1]
                data      = self.fetch_historical_data(symbol,from_date,to_date,resolution)
                data['symbol'] = symbol
                dfs.append(data)
            except Exception as e:
                continue
        if len(dfs)>0:
                hist_data = pd.concat(dfs)
                count = 0
                for i in range(int(len(hist_data)/75)):
                    date_values = self.get_dates_index(hist_data.iloc[75*i].date,75)
                    hist_data[75*i:75*(i+1)]['date']= date_values
                    count = count+75

                flag = None
                qty = 0
                SL = 0
                trades = 0
                profits = []
                hist_data['high_ema'] = hist_data['close'].ewm(span=high_ema,adjust=False).mean()
                hist_data['low_ema']  = hist_data['close'].ewm(span=low_ema,adjust=False).mean()
                hist_data['high_ema'] = hist_data['high_ema'].round(2)
                hist_data['low_ema']  = hist_data['low_ema'].round(2)
                for i in range(len(hist_data)):

                    if (float(hist_data.iloc[i].low_ema) > float(hist_data.iloc[i].high_ema) ) and (float(hist_data.iloc[i].close) > float(hist_data.iloc[i].high_ema) )  and (flag is None or flag =='SELL'):
                        logs.append("Buy {0} , Entry: {1} on {2}".format(symbol,hist_data.iloc[i].close,hist_data.iloc[i].date.strftime('%Y%m%d')))
                        SL = float(hist_data.iloc[i].high_ema)
                        qty = int(10000/abs(float(hist_data.iloc[i].close)-float(hist_data.iloc[i].high_ema)))
                        turnover = qty*float(hist_data.iloc[i].close)
                        flag = 'BUY'
                    elif float(hist_data.iloc[i].low) <= SL and flag=='BUY':
                        flag='SELL'
                        trades = trades+1
                        turnover = round((SL*qty)-turnover,2)
                        profits.append(round(turnover,2))
                        turnover = 0
                    elif (float(hist_data.iloc[i].high_ema) > float(hist_data.iloc[i].low_ema) ) and (flag=='BUY'):
                        logs.append("Sell {0} , Entry: {1} on {2}".format(symbol,hist_data.iloc[i].close,hist_data.iloc[i].date.strftime('%Y%m%d')))
                        flag='SELL'
                        trades = trades+1
                        turnover = round((float(hist_data.iloc[i].close)*qty)-turnover,2)
                        profits.append(round(turnover,2))
                        turnover = 0
                    else:
                        pass

                result['symbol'] = symbol
                result['profit'] = sum(profits)
                result['trades'] = trades
                dct.append(result)
                return hist_data
        else:
            pass
