


processes = []






def fyers_order(trade_df):
    """Preparing entry,sl,target order for execution of strategy
    1 => Limit Order
    2 => Market Order
    3 => Stop Order (SL-M)
    4 => Stoplimit Order (SL-L)

    1 => Buy
    -1 => Sell
    """
    if len(trade_df)>0:
        order = OrderManagement()
        order_ids = {}
        for i in range(len(trade_df)):

            if trade_df.iloc[i].pattern =='BULLISH':
                #entry order
                entry = order.prepareOrder(symbol=trade_df.iloc[i].symbol,
                                   qty=trade_df.iloc[i].qty,
                                   type=3,
                                   side=1,
                                   limit_price=0,
                                   sl=trade_df.iloc[i].entry)
                #sl order
                sl = order.prepareOrder(symbol=trade_df.iloc[i].symbol,
                                   qty=trade_df.iloc[i].qty,
                                   type=3,
                                   side=-1,
                                   limit_price=0,
                                   sl=trade_df.iloc[i].sl)
                #exit order
                exit = order.prepareOrder(symbol=trade_df.iloc[i].symbol,
                                   qty=trade_df.iloc[i].qty,
                                   type=1,
                                   side=-1,
                                   limit_price=trade_df.iloc[i].target,
                                   sl=0)

            elif trade_df.iloc[i].pattern =='BEARISH':
                #entry order
                entry = order.prepareOrder(symbol=trade_df.iloc[i].symbol,
                                   qty=trade_df.iloc[i].qty,
                                   type=3,
                                   side=-1,
                                   limit_price=0,
                                   sl=trade_df.iloc[i].entry)
                #sl order
                sl = order.prepareOrder(symbol=trade_df.iloc[i].symbol,
                                   qty=trade_df.iloc[i].qty,
                                   type=3,
                                   side=1,
                                   limit_price=0,
                                   sl=trade_df.iloc[i].sl)
                #exit order
                exit = order.prepareOrder(symbol=trade_df.iloc[i].symbol,
                                   qty=trade_df.iloc[i].qty,
                                   type=1,
                                   side=1,
                                   limit_price=trade_df.iloc[i].target,
                                   sl=0)

            response = order.placeSingleOrder(data=entry)
            print(response)
            if response['s']=='ok':
                order_ids[response['id']] = [sl,exit]
            else:
                response['message']
        i=0

        if len(order_ids.keys())>0  and len(order.fetchPendingOrders())==0:
            while True:
                for i in range(len(order_ids.keys())):
                    response = order.getOrderBookById(order_ids.keys()[i])
                    if response['s']=='ok':
                        data = response['orderbook'][0]
                        if data['status'] == 2 :

                            response = order.placeMultiOrder(data=order_ids[order_ids.keys()[i]])
                            if response['s'] == 'ok':
                                order_ids.pop(order_ids.keys()[i])
                            else:
                                print('Target and SL order placement error: %s'%response['message'])
                    else:
                        print(response['message'])


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
    from config.config_update import ConfigUpdate
    from constants import constants
    from strategy.pivot_points import PivotPoint
    from core.login import TradeLogin
    from core.profile import Profile
    from order_management.order_management import OrderManagement
    from multiprocessing import Process
    import matplotlib.pyplot as plt
    import multiprocessing as mp
    import pandas as pd
    import time
    pd.set_option('display.max_columns', None)
    import numpy as np
    trades = []
    dfs = []
    cu = ConfigUpdate()
    token = cu.retrieveAccessToken()
    if token is None:
        trade = TradeLogin()
        trade.login()
        sys.exit(0)
    else:
       pass

    start = time.time()
    sym_flag = sys.argv[1]
    symbols = []
    if sym_flag == '50':
        symbols = constants.nifty_50_symbols
    elif sym_flag=='500':
        symbols = constants.nifty_500_symbols
    elif sym_flag == 'fo':
        symbols = constants.fo_symbols

    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = []
        for symbol in symbols:
            futures.append(executor.submit(PivotPoint(100000,2025).run, symbol))
            time.sleep(1)
        for future in as_completed(futures):
            if future.result() is not None:
                df = pd.DataFrame(future.result(),columns=['symbol','Date','entry','pattern','qty','target','sl'])
                trades.append(df)
    end = time.time()
    print('------------------------------------------')
    print('Time taken for completion of script %.2f'%(end-start))
    print('------------------------------------------')
    trade_df = pd.concat(trades)
    trade_df = trade_df[trade_df['Date']==(datetime.now()+timedelta(days=0)).strftime('%Y-%m-%d')]
    print(trade_df)
    fyers_order(trade_df)










