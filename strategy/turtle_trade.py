from fyers_apiv3 import fyersModel
import sys
import logging
import pandas as pd
sys.path.insert(1,r'/home/iob/algotrading')
from backtest.historical_data import HistoricalData
logging.basicConfig(
    filename='algo.log',
    encoding='UTF-8',
    filemode='a',
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%d-%m-%Y %H:%M"
)
logger = logging.getLogger('algo')
class TurleTrade(HistoricalData):
    def __init__(self):
        super().__init__()

    def runStrategy(self,dates,resolution,symbols):
        """ 
        1. Entry when stock is breaking 40 day high
        2. Exit when breaking 20 day low
        Args
            Symbols: datatype [list]
            dates: '|' separated with from and to dates
        """
        flag = None
        profits = []
        total_profit = 0
        qty = 100
        turnover = 0
        dfs = []
        hist_data = pd.DataFrame()
        try:
            for symbol in symbols:
                hist_data = pd.DataFrame()
                dfs = []
                profits=[]
                count = 0
                print('processing symbol: {0}'.format(symbol))
                for row in dates:
                    try:
                        from_date = row.split('|')[0]
                        to_date   = row.split('|')[1]
                        data = HistoricalData().fetch_historical_data(symbol,from_date,to_date,resolution)
                        data['symbol'] = symbol
                        dfs.append(data)
                    except Exception as e:
                        continue
                if len(dfs)>0:
                    hist_data = pd.concat(dfs)
                    hist_data['dttime'] = pd.to_datetime(hist_data['date'], format='%y-%m-%d')
                    hist_data = hist_data.sort_values(by='dttime')
            #hist_data.to_csv('history_'+resolution+'.csv')
                    for i in range(len(hist_data)-41):
                        high_of_forty_days = float(hist_data.iloc[i:40+i]['high'].max())
                        low_of_twenty_days = float(hist_data.iloc[i:20+i]['low'].min())
                        candle_close = float(hist_data.iloc[i+41].close)
                        if (candle_close > high_of_forty_days ) and (flag is None or flag =='SELL'):
                            logger.info("Buy {0} , Entry: {1} on {2}".format(symbol,candle_close,hist_data.iloc[i+41].date.strftime('%Y%m%d')))
                            print("Buy {0} , Entry: {1} on {2}".format(symbol,candle_close,hist_data.iloc[i+41].date.strftime('%Y%m%d')))
                            turnover = 100*candle_close
                            flag = 'BUY'
                            count = count+1
                        elif (candle_close< low_of_twenty_days ) and (flag=='BUY'):
                            logger.info("Sell {0} , Exit: {1} on {2}".format(symbol,candle_close,hist_data.iloc[i+41].date.strftime('%Y%m%d')))
                            print("Sell {0} , Exit: {1} on {2}".format(symbol,candle_close,hist_data.iloc[i+41].date.strftime('%Y%m%d')))
                            flag='SELL'
                            count = count+1
                            turnover = round((candle_close*qty)-turnover,2)
                            profits.append(turnover)
                            turnover = 0
                        else:
                            pass 
                    if count%2 ==1:
                        profits.append(float(round((hist_data.iloc[len(hist_data)-1].close*qty)-turnover,2)))
                    else:
                        pass
                    print(profits)
                    total_profit = total_profit + sum(profits)
                print("Total Profit: {0}".format(total_profit))   
                return hist_data
            else:
                pass    
        except Exception as e:
            print(str(e))