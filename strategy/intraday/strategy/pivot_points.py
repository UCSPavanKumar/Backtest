
import sys
import warnings
from datetime import datetime,timedelta
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
sys.path.insert(1,r'D:/Projects/Backtest')
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
trade = TradeLogin()
trade.login()
trades = []


processes = []
capital = 400000
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
        dates.sort()
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
            if (first_candle_close>first_candle_open) and (first_candle_close > r1) and (first_candle_close - r1)>0  and day_high>first_candle_high and rate>4  and df['rsi'].iloc[0]>60 and df['rsi'].iloc[0]<70:
                flag=None
                for j in range(2,len(df)):
                    if df['close'].iloc[j]>first_candle_high and (flag is None or flag=='SELL'):
                        flag='BUY'
                        sl = (first_candle_high*(1-stoploss))
                        print('Buy Signal for %s first 5 min candle high %.2f,r1:%.2f ,pct change: %.2f,sl:%.2f,rate:%.2f for date: %s'%(symbol,first_candle_high,r1,pct,sl,rate,dates[i+1]))
                        qty = int((capital*risk_per_trade)/(first_candle_high*stoploss))
                        target =first_candle_high+float((2*(first_candle_high-sl)))
                        print('Target: %.2f,Stoploss: %.2f'%(target,sl))
                        buy_turnover = qty*first_candle_high
                    elif df['high'].iloc[j]>target and flag=='BUY':
                        flag='SELL'
                        sell_turnover = qty*target
                        self.commisions.append(round(float(Brokerage().calculate_commission(buy_turnover,sell_turnover)),2))
                        self.capital = capital + float((qty*(target-first_candle_high))) - float(Brokerage().calculate_commission(buy_turnover,sell_turnover))
                        self.capital_movement.append(round(float(capital),2))
                        self.trades.append([symbol,dates[i+1],float((qty*(target-first_candle_high))) - float(Brokerage().calculate_commission(buy_turnover,sell_turnover))])
                        print('Target achieved at %.2f for %s on date %s'%(target,symbol,df['date'].iloc[j]))
                        break
                    if df['low'].iloc[j]<sl and flag=='BUY':
                        flag='SELL'
                        sell_turnover = qty*sl
                        self.capital = capital + float((qty*(sl-first_candle_high)))- float(Brokerage().calculate_commission(buy_turnover,sell_turnover))
                        self.trades.append([symbol,dates[i+1],float((qty*(sl-first_candle_high))) - float(Brokerage().calculate_commission(buy_turnover,sell_turnover))])
                        self.commisions.append(round(float(Brokerage().calculate_commission(buy_turnover,sell_turnover)),2))
                        self.capital_movement.append(round(float(capital),2))
                        print('Stoploss hit : %.2f for %s on date %s'%(sl,symbol,df['date'].iloc[j]))
                        break
                if flag=='BUY':
                    print('Square off at %.2f for %s on date %s'%(df['close'].iloc[-1],symbol,df['date'].iloc[j]))
                    sell_turnover = qty*df['close'].iloc[-1]
                    self.capital = capital + float((qty*(df['close'].iloc[-1]-first_candle_high))) -Brokerage().calculate_commission(buy_turnover,sell_turnover)
                    self.trades.append([symbol,dates[i+1],float((qty*(df['close'].iloc[-1]-first_candle_high))) - float(Brokerage().calculate_commission(buy_turnover,sell_turnover))])
                    self.commisions.append(round(float(Brokerage().calculate_commission(buy_turnover,sell_turnover)),2))
                    self.capital_movement.append(round(capital,2))
                else:
                    pass

            else:
                pass

    def sell(self,final_df,symbol):
        """
            1. First Candle volume is 4 times SMA volume
            2. First Candle close is less than S1
            3. RSI is
        """
        dates = final_df['dt_time'].unique()
        dates.sort()
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
            if (first_candle_close<first_candle_open) and (first_candle_close < s1) and (first_candle_close - s1)<0  and day_low>first_candle_low and rate>4  and df['rsi'].iloc[0]>20 and df['rsi'].iloc[0]<30:
                flag=None
                for j in range(2,len(df)):
                    if df['close'].iloc[j]<first_candle_low and (flag is None or flag=='BUY'):
                        flag='SELL'
                        sl = (first_candle_low*(1+stoploss))
                        print('Short Signal for %s first 5 min candle low %.2f,s1:%.2f ,pct change: %.2f,sl:%.2f,rate:%.2f for date: %s'%(symbol,first_candle_low,s1,pct,sl,rate,dates[i+1]))
                        qty = int((capital*risk_per_trade)/(first_candle_low*stoploss))
                        target =first_candle_low-float((2*abs(first_candle_low-sl)))
                        print('Target: %.2f,Stoploss: %.2f'%(target,sl))
                        sell_turnover = qty*first_candle_low
                    elif df['low'].iloc[j]<target and flag=='SELL':
                        flag='BUY'
                        buy_turnover = qty*target
                        self.commisions.append(round(float(Brokerage().calculate_commission(buy_turnover,sell_turnover)),2))
                        self.capital = capital + float((qty*(target-first_candle_low))) - float(Brokerage().calculate_commission(buy_turnover,sell_turnover))
                        self.capital_movement.append(round(float(capital),2))
                        self.trades.append([symbol,dates[i+1],float((qty*(target-first_candle_low))) - float(Brokerage().calculate_commission(buy_turnover,sell_turnover))])
                        print('Target achieved at %.2f for %s on date %s'%(target,symbol,df['date'].iloc[j]))
                        break
                    if df['high'].iloc[j]>sl and flag=='SELL':
                        flag='BUY'
                        buy_turnover = qty*sl
                        self.capital = capital + float((qty*(sl-first_candle_low)))- float(Brokerage().calculate_commission(buy_turnover,sell_turnover))
                        self.trades.append([symbol,dates[i+1],float((qty*(sl-first_candle_low))) - float(Brokerage().calculate_commission(buy_turnover,sell_turnover))])
                        self.commisions.append(round(float(Brokerage().calculate_commission(buy_turnover,sell_turnover)),2))
                        self.capital_movement.append(round(float(capital),2))
                        print('Stoploss hit : %.2f for %s on date %s'%(sl,symbol,df['date'].iloc[j]))
                        break
                if flag=='SELL':
                    print('Square off at %.2f for %s on date %s'%(df['close'].iloc[-1],symbol,df['date'].iloc[j]))
                    buy_turnover = qty*df['close'].iloc[-1]
                    self.capital = capital + float((qty*(df['close'].iloc[-1]-first_candle_low))) -Brokerage().calculate_commission(buy_turnover,sell_turnover)
                    self.trades.append([symbol,dates[i+1],float((qty*(df['close'].iloc[-1]-first_candle_low))) - float(Brokerage().calculate_commission(buy_turnover,sell_turnover))])
                    self.commisions.append(round(float(Brokerage().calculate_commission(buy_turnover,sell_turnover)),2))
                    self.capital_movement.append(round(capital,2))
                else:
                    pass

            else:
                pass


    def run(self,symbol):
        dfs = []
        print('Processing symbol: {0}'.format(symbol))
        for dates in intraday_dates:
            data = HistoricalData(year=self.year).fetch_historical_data(symbol,dates.split('|')[0],dates.split('|')[1],'5')
            if data is not None and len(data)>20:     
                dfs.append(data)
            else:
                pass
        if len(dfs)>0:
            final_df = pd.concat(dfs)
            dates = final_df['dt_time'].unique()
            dates.sort()
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
