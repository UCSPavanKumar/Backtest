from fyers_apiv3 import fyersModel
import sys
import pandas as pd
import numpy as np
sys.path.insert(1,r'/home/iob/algotrading')
from backtest.historical_data import HistoricalData

class BollingerBreakout(HistoricalData):
    def __init__(self):
        super().__init__()

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
    

    def runStrategy(self,dates,resolution,symbol):
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
        for row in dates:
                try:
                    from_date = row.split('|')[0]
                    to_date   = row.split('|')[1]
                    data      = HistoricalData().fetch_historical_data(symbol,from_date,to_date,resolution)
                    data['symbol'] = symbol
                    data['dt_format'] = data['date'].dt.strftime('%Y%m%d')
                    dfs.append(data)
                except Exception as e:
                    continue
        
        if len(dfs)>0:
                
                hist_data = pd.concat(dfs)
                dates = hist_data['dt_format'].unique()
                dates.sort()
                hist_data['vol_sma'] = hist_data['volume'].rolling(window=20).mean()
                hist_data = self.bollinger_bands(hist_data)
                hist_data = self.rsi(hist_data)
                for i in range(3,len(dates)):
                    h_data = hist_data[hist_data['dt_format']==dates[i]]
                    p_data = hist_data[hist_data['dt_format']==dates[i-1]]
                    data_list = []
                    nr3_df = hist_data[(hist_data['dt_format']==dates[(i-3):(i)][0]) | (hist_data['dt_format']==dates[(i-3):i][1]) | (hist_data['dt_format']==dates[(i-3):i][2])]
                    #print(dates[i],nr3_df['high'].max(),nr3_df['low'].min())
                    res                 = self.nr3(hist_data,dates[(i-3):i])
                    first_candle_volume = float(h_data.iloc[0].volume)
                    first_candle_close = float(h_data.iloc[0].close)
                    first_candle_high   = float(h_data.iloc[0].high)
                    first_candle_low    = float(h_data.iloc[0].low)
                    vol_sma             = float(h_data.iloc[0].vol_sma)
                    day_high            = h_data[1:len(h_data)]['high'].max()
                    day_low             = h_data[1:len(h_data)]['low'].min()
                    candle_diff         = float(h_data.iloc[0].close) - float(h_data.iloc[0].open)
                    rate                = round(float(first_candle_volume)/float(vol_sma),2)
                    #dt                  = hist_data.iloc[75*i].date.strftime('%Y%m%d')
                    prev_day_close      = float(p_data.iloc[len(p_data)-1].close)
                    pct                 = round((float(h_data.iloc[0].close) - float(prev_day_close) )/float(prev_day_close),2)*100
                    closing_candle      = float(h_data.iloc[len(h_data)-1].close)
                    closing_pct         = round((float(closing_candle) - float(prev_day_close) )/float(prev_day_close),2)*100
                    ub                  = float(h_data.iloc[0].UB)
                    lb                  = float(h_data.iloc[0].LB)
                    rsi                 = float(h_data.iloc[0].rsi)
                    
                    if (pct>0 and candle_diff>0) and first_candle_volume>500000 and rate>6 and day_high>first_candle_high and first_candle_close>nr3_df['high'].max():
                        data_list.append(symbol)
                        data_list.append(first_candle_volume)
                        data_list.append(vol_sma)
                        data_list.append(rate)
                        data_list.append(dates[i])
                        data_list.append(prev_day_close)
                        data_list.append(pct)
                        data_list.append(closing_pct)
                        data_list.append(ub)
                        data_list.append(lb)
                        data_list.append(rsi)
                        data_list.append(res)
                        result.append(data_list)
                    # elif (pct<0 and candle_diff<0)  and first_candle_volume>500000 and rate>6 and day_low<first_candle_low and first_candle_close<nr3_df['low'].min() :
                    #     data_list.append(symbol)
                    #     data_list.append(first_candle_volume)
                    #     data_list.append(vol_sma)
                    #     data_list.append(rate)
                    #     data_list.append(dates[i])
                    #     data_list.append(prev_day_close)
                    #     data_list.append(pct)
                    #     data_list.append(closing_pct)
                    #     data_list.append(ub)
                    #     data_list.append(lb)
                    #     data_list.append(rsi)
                    #     data_list.append(res)
                    #     result.append(data_list)
                    else:
                         pass
        else:
             pass
        # if len(result)>0:
        #     df = pd.DataFrame(result,columns=['symbol','first_candle_volume','vol_sma','rate','date','prev_day_close','pct','closing_pct','ub','lb','rsi','nr3'])
        #     df.to_csv('{0}.csv'.format(symbol))  
        # else:
        #      pass
        #     next_day            = hist_data.iloc[75*i:75*(i+1)]
        #     first_candle_of_day = abs(next_day.iloc[0].high - next_day.iloc[0].low)
        #     prev_day_close      = hist_data[75*(i-1):75*i].iloc[74].close
        #     pct_over_prev_close = round((first_candle_of_day/prev_day_close)*100,2)
        #     next_day_close      = next_day.iloc[74].close
        #     ema_200             = next_day.iloc[74].ema_200
        #     row = []
        #     row.append(next_day.iloc[74].date.strftime('%Y%m%d'))
        #     row.append(symbol)
        #     row.append(float(prev_day_close))
        #     row.append(float(next_day_close))
        #     row.append(float(pct_over_prev_close))
        #     row.append(float(next_day.iloc[74].ema_200))
            
        #     if (next_day_close > prev_day_close):
        #         pct_chg = round(((prev_day_close-next_day_close)/prev_day_close)*100,2) 
        #     else:
        #         pct_chg = -round(((prev_day_close-next_day_close)/prev_day_close)*100,2)
        #     row.append(float(pct_chg))
        #     backtest_data.append(row)
        # print('Processing Done for {0}'.format(symbol))
        # df_back = pd.DataFrame(backtest_data)
        # df_back.columns = ['trade_date','symbol','prev_day_close','next_day_close','pct_over_prev_close','day_pct_chg','first_candle_200_ema']      