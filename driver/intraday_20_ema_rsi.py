


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
    from strategy.ema_rsi import EmaRsi
    from multiprocessing import Process
    import matplotlib.pyplot as plt
    import multiprocessing as mp
    import pandas as pd
    import time
    pd.set_option('display.max_columns', None)
    import numpy as np
    trade = TradeLogin()
    trade.login()
    trades = []
    dfs = []

    start  = time.time()

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = []
        for symbol in constants.fo_symbols:
            futures.append(executor.submit(EmaRsi(2025).runStrategy, symbol))
        for future in as_completed(futures):
            if future.result() is not None:
                dfs.append(future.result())
    
    end = time.time()
    print('total time taken for completion of script %.2f'%(end-start))

    trade_df = pd.DataFrame(dfs,columns=['symbol','date','pattern','pct'])
    print(trade_df)







