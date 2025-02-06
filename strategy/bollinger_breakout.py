from fyers_apiv3 import fyersModel
import sys
import pandas as pd
import numpy as np
sys.path.insert(1,r'D:/Projects/Backtest')
from time_management.dates import back_test_dates
from data_management.historical_data import HistoricalData

class BollingerBreakout(HistoricalData):
    def __init__(self,year):
        self.year = year
        super().__init__(year)

    def bollinger_bands(self,df:pd.DataFrame):
        """
        Calculate Bollinger upper band and lower band and return the dataframe
        """
        df['SMA'] = df['close'].rolling(window=20).mean()
        df['STD'] = df['close'].rolling(window=20).std()
        df['UB']  = df['SMA'] + (2*df['STD'])
        df['LB']  = df['SMA'] -  (2*df['STD'])
        return df

    def rsi(self,df):
        """
        Finding 5 min TF RSI for the dataframe input
        """
        df['diff'] = df['close'].diff() #axis = 0 column
        df['gain'] = np.where(df['diff']>0,df['diff'],0)
        df['loss'] = -np.where(df['diff']<0,df['diff'],0)
        df['flag'] = np.where(df['close']>df['open'],'BU','BE')
        df['avg_gain'] = df['gain'].rolling(14).sum()/df['gain'].ne(0).rolling(14).sum()
        df['avg_loss'] = df['loss'].rolling(14).sum()/df['loss'].ne(0).rolling(14).sum()
        df['rsi'] = 100-(100/(1+(np.where(df['avg_gain'].ne(None),df['avg_gain']/df['avg_loss'],0))))
        df['rsi'] = round(df['rsi'],2)
        return df

    def nr3(self,df,dates):
        """
        Finding NR3 range for the slice of dataframe
        """
        result = 'N'
        first_day_high = df[df['dt_format']==dates[0]]['high'].max()
        first_day_low = df[df['dt_format']==dates[0]]['low'].min()
        second_day = df[df['dt_format']==dates[1]]
        second_day_close = second_day.iloc[len(second_day)-1].close
        third_day  = df[df['dt_format']==dates[2]]
        third_day_close = third_day.iloc[len(third_day)-1].close
        if second_day_close<first_day_high and second_day_close>first_day_low and third_day_close<first_day_high and third_day_close>first_day_low:
             result = 'Y'
        return result


    def runStrategy(self,symbol):
        """
        1. Checking for first 5 min candle of day with prev day close
        2. Day's Pct change over previous day candle
        3. 5 min high-low pct of previous day close

        Args
            Symbols: datatype [list]
        """
        print('processing symbol: {0}'.format(symbol))
        dfs = []
        result = []
        data_list = []
        data      = HistoricalData(self.year).fetch_data_by_year(symbol)
        data['symbol'] = symbol
        data['dt_format'] = data['date'].dt.strftime('%Y%m%d')
        if len(data)>0:
            hist_data = data
            dates = hist_data['dt_format'].unique()
            dates.sort()
            hist_data['vol_sma'] = hist_data['volume'].rolling(window=20).mean()
            hist_data = self.bollinger_bands(hist_data)
            hist_data = self.rsi(hist_data)
            return hist_data
        else:
             pass
