


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
    from intraday.strategy.pivot_points import PivotPoint
    from core.login import TradeLogin
    from core.profile import Profile
    from order_management.order_management import OrderManagement
    from strategy.bollinger_breakout import BollingerBreakout
    from strategy.golden_crossover import GoldenCrossOver
    from strategy.turtle_trade import TurleTrade
    from intraday.strategy.ema_rsi import EmaRsi
    from multiprocessing import Process
    import matplotlib.pyplot as plt
    import multiprocessing as mp
    from multiprocessing import freeze_support
    import pandas as pd
    pd.set_option('display.max_columns', None)
    import numpy as np
    trade = TradeLogin()
    trade.login()
    trades = []
    dfs = []


    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        futures = []
        for symbol in constants.nifty_50_symbols:
            futures.append(executor.submit(EmaRsi(2025).runStrategy, symbol))
        for future in as_completed(futures):
            if future.result() is not None:
                trades.append(future.result())

    print(trades)







