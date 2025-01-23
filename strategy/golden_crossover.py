from fyers_apiv3 import fyersModel
import sys
import logging
import pandas as pd
sys.path.insert(1,r'/home/iob/algotrading')
logging.basicConfig(
    filename='algo.log',
    encoding='UTF-8',
    filemode='a',
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%d-%m-%Y %H:%M"
)
from backtest.historical_data import HistoricalData
class GoldenCrossOver(HistoricalData):
    def __init__(self):
        super().__init__()
        

    def runStrategy(self,from_date,to_date,resolution,symbols):
        """ 
        1. Checking for first 5 min candle of day with prev day close
        2. Day's Pct change over previous day candle
        3. 5 min high-low pct of previous day close
        
        Args
            Symbols: datatype [list]
        """
        flag = None
        for symbol in symbols:
            try:
                hist_data = HistoricalData().fetch_historical_data(symbol,from_date,to_date,resolution)
                hist_data['ema200'] = hist_data['close'].ewm(span=200,adjust=False).mean()
                hist_data['ema50']  = hist_data['close'].ewm(span=50,adjust=False).mean()
                hist_data['ema200'] = hist_data['ema200'].round(2)
                hist_data['ema50']  = hist_data['ema50'].round(2)
                for i in range(len(hist_data)):
                    if (float(hist_data.iloc[i].ema50) > float(hist_data.iloc[i].ema200) ) and (flag is None or flag =='SELL'):
                        print("Buy {0} , Entry: {1} on {2}".format(symbol,hist_data.iloc[i].ema50,hist_data.iloc[i].date.strftime('%Y%m%d')))
                        flag = 'BUY'
                    elif (float(hist_data.iloc[i].ema200) > float(hist_data.iloc[i].ema50) ) and (flag is None or flag=='BUY'):
                        print("Sell {0} , Entry: {1} on {2}".format(symbol,hist_data.iloc[i].ema200,hist_data.iloc[i].date.strftime('%Y%m%d')))
                        flag='SELL'
                    else:
                        pass 
            except Exception as e:
                print(str(e))   
            return hist_data