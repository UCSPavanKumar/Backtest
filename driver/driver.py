


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
            futures.append(executor.submit(PivotPoint(400000,2025).run, symbol))
        for future in as_completed(futures):
            if future.result() is not None:
                df = pd.DataFrame(future.result(),columns=['Symbol','Date','PnL'])
                trades.append(df)

    trade_df = pd.concat(trades)
    trade_df['pnl_c'] = trade_df['PnL'].cumsum()
    trade_df['capital'] =  trade_df['pnl_c'] + 400000
    print(trade_df)
    analytics = Analytics(trade_df)
    # print('Win Rate:%.2f'%analytics.win_rate())
    # print('Drawdown:%.2f'%analytics.draw_down())
    # print('Sharpe Ratio:%.2f'%analytics.sharpe_ratio(0.05,0.01,0.12))
    # print('Returns:%.2f'%analytics.calculate_returns())









