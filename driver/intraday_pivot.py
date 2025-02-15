


processes = []
import time





def place_counter_order(order_ids):
    order = OrderManagement()
    if len(order_ids.keys())>0:
        print(order_ids.keys())
        while len(order_ids)>0:
            for i in range(len(list(order_ids.keys()))):
                response = order.getOrderBookById(list(order_ids.keys())[i])
                print(response)
                if response['s']=='ok':
                    data = response['orderBook'][0]
                    if data['status'] == 2 :
                        response = order.placeMultiOrder(data=order_ids[list(order_ids.keys())[i]])
                        if response['s'] == 'ok':
                            order_ids.pop(list(order_ids.keys())[i])
                        else:
                            print('Target and SL order placement error: %s'%response['message'])
                else:
                    print(response['message'])
            time.sleep(0.5)

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
        order_df = pd.DataFrame(order.fetchPendingOrders()['orderBook'])
        if len(order_df)>0:
            order_df = order_df[(order_df['orderTag']=='intradaypivot') & (order_df['status']==6)]
        else:
            pass
        if len(order_df)== 0:
            for i in range(len(trade_df)):
                if trade_df.iloc[i].pattern =='BULLISH':
                    entry_keywords = {
                    "symbol":trade_df.iloc[i].symbol,
                    "qty":trade_df.iloc[i].qty,
                    "type":3,
                    "side":1,
                    "productType":"INTRADAY",
                    "limitPrice":0,
                    "stopPrice":trade_df.iloc[i].entry,
                    "validity":"DAY",
                    "disclosedQty":0,
                    "offlineOrder":False,
                    "orderTag":"intradaypivot"
                }
                    sl_keywords = {
                    "symbol":trade_df.iloc[i].symbol,
                    "qty":trade_df.iloc[i].qty,
                    "type":3,
                    "side":-1,
                    "productType":"INTRADAY",
                    "limitPrice":0,
                    "stopPrice":trade_df.iloc[i].sl,
                    "validity":"DAY",
                    "disclosedQty":0,
                    "offlineOrder":False,
                    "orderTag":"intradaypivot"
                }
                    exit_keywords = {
                    "symbol":trade_df.iloc[i].symbol,
                    "qty":trade_df.iloc[i].qty,
                    "type":1,
                    "side":-1,
                    "productType":"INTRADAY",
                    "limitPrice":trade_df.iloc[i].target,
                    "stopPrice":0,
                    "validity":"DAY",
                    "disclosedQty":0,
                    "offlineOrder":False,
                    "orderTag":"intradaypivot"
                }
                elif trade_df.iloc[i].pattern =='BEARISH':
                    entry_keywords = {
                    "symbol":trade_df.iloc[i].symbol,
                    "qty":trade_df.iloc[i].qty,
                    "type":3,
                    "side":-1,
                    "productType":"INTRADAY",
                    "limitPrice":0,
                    "stopPrice":trade_df.iloc[i].entry,
                    "validity":"DAY",
                    "disclosedQty":0,
                    "offlineOrder":False,
                    "orderTag":"intradaypivot"
                }
                    sl_keywords = {
                    "symbol":trade_df.iloc[i].symbol,
                    "qty":trade_df.iloc[i].qty,
                    "type":3,
                    "side":1,
                    "productType":"INTRADAY",
                    "limitPrice":0,
                    "stopPrice":trade_df.iloc[i].sl,
                    "validity":"DAY",
                    "disclosedQty":0,
                    "offlineOrder":False,
                    "orderTag":"intradaypivot"
                }
                    exit_keywords = {
                    "symbol":trade_df.iloc[i].symbol,
                    "qty":trade_df.iloc[i].qty,
                    "type":1,
                    "side":1,
                    "productType":"INTRADAY",
                    "limitPrice":trade_df.iloc[i].target,
                    "stopPrice":0,
                    "validity":"DAY",
                    "disclosedQty":0,
                    "offlineOrder":False,
                    "orderTag":"intradaypivot"
                }
                response = order.placeSingleOrder(data=entry_keywords)
                order_data[trade_iloc[i].symbol] = {}
                order_data[trade_df.iloc[i].symbol]['entry'] = entry_keywords
                order_data[trade_df.iloc[i].symbol]['sl'] = sl_keywords
                order_data[trade_df.iloc[i].symbol]['target'] = exit_keywords
                if response['s'] =='ok':
                    order_data[trade_df.iloc[i].symbol]['entry_order_flg'] = 'Y'
                else:
                    order_data[trade_df.iloc[i].symbol]['entry_order_flg'] = 'N'
                order.createOrder(order_data)
        else:
            print(order_ids)
            order_keys = list(order_df['id'].unique())
            if len(order_keys)>0:
                print(len(order_keys))
                while len(order_ids_keys)>0:
                    for i in range(len(order_keys)):
                        response = order.getOrderBookById(orderkeys[i])
                        print(response)
                        if response['s']=='ok':
                            data = response['orderbook'][0]
                            if data['status'] == 2 :
                                response = order.placeMultiOrder(data=order_ids[orderkeys[i]])
                                if response['s'] == 'ok':
                                    order_ids.pop(orderkeys[i])
                                else:
                                    print('Target and SL order placement error: %s'%response['message'])
                        else:
                            print(response['message'])
                    time.sleep(0.5)


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

    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = []
        for symbol in symbols:
            futures.append(executor.submit(PivotPoint(10000,2025).run, symbol))
            time.sleep(0.3)

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










