


processes = []

if __name__ == '__main__':
    import sys
    import warnings
    from datetime import datetime,timedelta
    from concurrent.futures import ThreadPoolExecutor   ,ProcessPoolExecutor,as_completed
    from pandas.errors import SettingWithCopyWarning
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
    sys.path.insert(1,r'D:/Projects/Backtest')
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
    trades = []



    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        futures = []
        for year in range(2019,2025):
            for symbol in constants.nifty_50_symbols:
                futures.append(executor.submit(HistoricalData(year).fetch_data_by_year, symbol))
            for future in as_completed(futures):
                trades.append(future.result())

            trade_df = pd.concat(trades)
            trade_df.to_csv('./data/nifty_50_{0}.csv'.format(year))








