


processes = []

if __name__ == '__main__':
    import sys
    import warnings
    from datetime import datetime,timedelta
    from concurrent.futures import ThreadPoolExecutor   ,ProcessPoolExecutor,as_completed
    from pandas.errors import SettingWithCopyWarning
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
    sys.path.insert(1,r'/home/ec2-user/Backtest/')
    from constants import constants
    from strategy.pivot_points import PivotPoint
    from core.login import TradeLogin
    from core.profile import Profile
    from data_management.historical_data import HistoricalData
    from order_management.order_management import OrderManagement
    from strategy.bollinger_breakout import BollingerBreakout
    from strategy.golden_crossover import GoldenCrossOver
    from strategy.turtle_trade import TurleTrade
    from strategy.ema_rsi import EmaRsi
    from multiprocessing import Process
    import multiprocessing as mp
    from multiprocessing import freeze_support
    import pandas as pd
    pd.set_option('display.max_columns', None)
    import numpy as np
    trade = TradeLogin()
    trade.login()
    import time
    trades = []
    from cls_s3 import cls_s3



    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        futures = []
        for symbol in constants.nifty_50_symbols:
            df = HistoricalData(2025).fetch_historical_data(symbol,'2025-02-12','2025-02-12','1')
            c = cls_s3()
            c.saveObject(df,'algowiztrades','Day_minus_one_1_min')
            #df = c.getObject(symbol,'algowiztrades','Day_minus_one_1_min')
            #print(df.head())
            time.sleep(0.3)

    









