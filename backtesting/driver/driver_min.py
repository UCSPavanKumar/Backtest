


processes = []

if __name__ == '__main__':
    import sys
    import warnings
    from datetime import datetime,timedelta
    from concurrent.futures import ThreadPoolExecutor   ,ProcessPoolExecutor,as_completed
    from pandas.errors import SettingWithCopyWarning
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
    sys.path.insert(1,r'/home/ec2-user/Backtest')
    from analytics.analytics import Analytics
    from constants import constants
    from strategy.pivot_points import PivotPoint
    from core.login import TradeLogin
    from core.profile import Profile
    from order_management.order_management import OrderManagement
    from strategy.bollinger_breakout import BollingerBreakout
    from strategy.golden_crossover import GoldenCrossOver
    from strategy.turtle_trade import TurleTrade
    from strategy.ema_rsi import EmaRsi
    from multiprocessing import Process
    import matplotlib.pyplot as plt
    import multiprocessing as mp
    from strategy.backtest.minute_20_ema import minEma
    from multiprocessing import freeze_support
    import pandas as pd
    from data_management.cls_s3 import cls_s3
    pd.set_option('display.max_columns', None)
    import numpy as np
    trade = TradeLogin()
    trade.login()
    trades = []
    dfs = []


    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        futures = []
        for symbol in constants.nifty_50_symbols:
            c = cls_s3()
            df = c.getObject(symbol,'algowiztrades','Day_minus_one_1_min')
            df = df.loc[:50]
            (pattern,count) = minEma().filter(df)
            futures.append([symbol,pattern,count])
        final_df = pd.DataFrame(futures,columns=['symbol','pattern','count'])
        final_df = final_df.astype({'symbol':'str','pattern':'str','count':'int'})
        bull_df = final_df[(final_df['pattern']=='BULLISH') & (final_df['count']>0)]
        bull_df = bull_df.sort_values('count',ascending=False)
        bear_df = final_df[(final_df['pattern']=='BEARISH') & (final_df['count']>0)]
        bear_df = bear_df.sort_values('count',ascending=False)
        if len(bull_df) > len(bear_df):
            print(bull_df)
        elif len(bear_df) > len(bull_df):
            print(bear_df)







