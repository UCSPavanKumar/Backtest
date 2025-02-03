import pandas as pd
import sys
sys.path.insert(1,r'D:/Projects/Backtest')
from data_management.historical_data import HistoricalData
from strategy.golden_crossover import GoldenCrossOver

@GoldenCrossOver.runStrategy
def processdata(dates,resolution,symbols):
        """
        Fetch data from fyers for the time frame and symbol with multiple date range.
        Args
            Symbols: datatype [list]
            dates: '|' separated with from and to dates
            resolution: 1,2,3,5,.... or 1D .
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
        except Exception as e:
            print(str(e))
        return hist_data