
import sys
import warnings
from datetime import datetime,timedelta
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
from analytics.analytics import Analytics
from constants import constants
from core.login import TradeLogin
from commisions.brokerage import Brokerage
from core.profile import Profile
from order_management.order_management import OrderManagement
from strategy.bollinger_breakout import BollingerBreakout
from strategy.golden_crossover import GoldenCrossOver
from strategy.turtle_trade import TurleTrade
from strategy.ema_rsi import EmaRsi
from multiprocessing import Process
import multiprocessing as mp
from data_management.historical_data import HistoricalData
from time_management.dates import back_test_dates, intraday_dates
from multiprocessing import freeze_support
import pandas as pd
import matplotlib.pyplot as plt
from indicators.stock_indicators import Indicators
pd.set_option('display.max_columns', None)
import numpy as np
#trade = TradeLogin()
#trade.login()
#trades = []


processes = []
capital = 100000
stoploss    = 0.005
risk_per_trade = 0.01
reward_per_trade = 0.02
capital_movement = [400000]
commisions = [0]
trades = []
class PivotPoint:
    def __init__(self,capital,year):
       
        self.year = year
        self.stoploss = 0.05
        self.risk_per_trade = 0.01
        self.reward_per_trade = 0.02
        self.capital = capital
        self.capital_movement = [capital]
        self.commisions = [0]
        self.trades = []

    def buy(self,final_df,symbol):
        dates = final_df['dt_time'].unique()
        #dates.sort()
        target = 0
        sl=0
        for i in range(0,len(dates)-1):
            prev_df = final_df[final_df['dt_time']==dates[i]]
            df = final_df[final_df['dt_time']==dates[i+1]]
            day_high = df['high'].max()
            #result  = Indicators().nr3(final_df,[dates[i-3],dates[i-2],dates[i-1]])
            pivot,r1,s1,r2,s2,r3,s3 = Indicators().pivotpoints(prev_df['high'].max(),prev_df['low'].min(),prev_df['close'].iloc[-1])
            first_candle_close = float(df['close'].iloc[0])
            first_candle_open = float(df['open'].iloc[0])
            first_candle_high = float(df['high'].iloc[0])
            first_candle_volume = df['volume'].iloc[0]
            pct = ((first_candle_close-prev_df['close'].iloc[-1])/prev_df['close'].iloc[-1])*100
            rate = first_candle_volume/df['vol_smav'].iloc[0]
            if (first_candle_close>first_candle_open) and (first_candle_close > r1) and (first_candle_close - r1)>0  and rate>4  and df['rsi'].iloc[0]>60 and df['rsi'].iloc[0]<70:
                sl = round((first_candle_high*(1-stoploss))*20)/20
                qty = int((capital*risk_per_trade)/abs(first_candle_high-sl))
                target =round((first_candle_high+float((2*(first_candle_high-sl))))*20)/20
                self.trades.append([symbol,dates[i+1],round(first_candle_high*20)/20,'BULLISH',qty,target,sl])

            else:
                pass

    def sell(self,final_df,symbol):
        """
            1. First Candle volume is 4 times SMA volume
            2. First Candle close is less than S1
            3. RSI is
        """
        dates = final_df['dt_time'].unique()
        #dates.sort()
        target = 0
        sl=0
        for i in range(0,len(dates)-1):
            prev_df = final_df[final_df['dt_time']==dates[i]]
            df = final_df[final_df['dt_time']==dates[i+1]]
            day_high = df['high'].max()
            day_low = df['low'].min()
            #result  = Indicators().nr3(final_df,[dates[i-3],dates[i-2],dates[i-1]])
            pivot,r1,s1,r2,s2,r3,s3 = Indicators().pivotpoints(prev_df['high'].max(),prev_df['low'].min(),prev_df['close'].iloc[-1])
            first_candle_close = float(df['close'].iloc[0])
            first_candle_open = float(df['open'].iloc[0])
            first_candle_low= float(df['low'].iloc[0])
            first_candle_volume = df['volume'].iloc[0]
            pct = ((first_candle_close-prev_df['close'].iloc[-1])/prev_df['close'].iloc[-1])*100
            rate = first_candle_volume/df['vol_smav'].iloc[0]
            if (first_candle_close<first_candle_open) and (first_candle_close < s1) and (first_candle_close - s1)<0  and rate>4  and df['rsi'].iloc[0]>20 and df['rsi'].iloc[0]<30:
                sl = round((first_candle_low*(1+stoploss))*20)/20
                qty = int((capital*risk_per_trade)/abs(first_candle_low-sl))
                target =round((first_candle_low+float((2*(sl-first_candle_low))))*20)/20     
                self.trades.append([symbol,dates[i+1],round(first_candle_low*20)/20,'BEARISH',qty,target,sl])
            else:
                pass


    def run(self,symbol):
        dfs = []
        for dates in intraday_dates:
            data = HistoricalData(year=self.year).fetch_historical_data(symbol,dates.split('|')[0],dates.split('|')[1],'5')
            if data is not None and len(data)>20:     
                dfs.append(data)
            else:
                pass
        if len(dfs)>0:
            final_df = pd.concat(dfs)
            dates = final_df['dt_time'].unique()
            #dates.sort()
            final_df = Indicators().rsi(final_df)
            final_df['vol_smav'] = final_df['volume'].rolling(window=20).mean()
            self.buy(final_df,symbol)
            self.sell(final_df,symbol)
            #self.showAnalysis(symbol)
            return self.trades
        else:
            return None


    def showAnalysis(self,symbol):
        # plt.plot(self.capital_movement)
        # #plt.plot(np.subtract(capital_movement,commisions),'-')
        # plt.title("Capital Movement : "+symbol)
        # plt.show()
        trade_df = pd.DataFrame(self.trades,columns=['Symbol','Date','PnL'])
        # trade_df['month'] = trade_df['Date'].apply(lambda x: x.split('-')[1])
        # result = trade_df.groupby('month')['PnL'].sum()
        # result['monthly_returns'] = result['PnL']/result['PnL'].sum()
        # result['std'] = result['PnL'].std()
        #trade_df.to_csv('./result/trades_fo.csv')
        print('----------------------------------------------')
        print('Total Commisions: %.2f'%(sum(self.commisions)))
        print("Total Returns: %.2f"%(Analytics(self.capital_movement).calculate_returns()))
        print("Win Rate : %.2f"%(Analytics(self.capital_movement).win_rate()))
        print("Drawdown: %.2f"%(Analytics(self.capital_movement).draw_down()))
        print('Total Profit: %.2f'%(sum(self.trade_df['PnL'])))
