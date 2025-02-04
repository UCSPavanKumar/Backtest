


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
    trade = TradeLogin()
    trade.login()
    trades = []
    dfs = []
    cu = ConfigUpdate()
    token = cu.retrieveAccessToken()
    if token is None:
        sys.exit(0) 

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
            futures.append(executor.submit(PivotPoint(50000,2025).run, symbol))
        for future in as_completed(futures):
            if future.result() is not None:
                df = pd.DataFrame(future.result(),columns=['symbol','Date','entry','pattern','qty','target','sl'])
                trades.append(df)
    end = time.time()
    print('Time taken for completion of script %.2f'%(end-start))
    trade_df = pd.concat(trades)
    print(trade_df)
    trade_df = trade_df[trade_df['Date']==(datetime.now()+timedelta(days=0)).strftime('%Y-%m-%d')]
    if len(trade_df)>0:
        print(trade_df)
        order = OrderManagement()
        trades_list = [] 
        order_ids = []
        for i in range(len(trade_df)): 
            if trade_df.iloc[i].pattern =='BULLISH': 
                data = {
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
            else:
                data = {
                "symbol":trade_df.iloc[i].symbol,
                "qty":10,
                "type":3,
                "side":0,
                "productType":"INTRADAY",
                "limitPrice":0,
                "stopPrice":trade_df.iloc[i].entry,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":False,
                "orderTag":"intradaypivot"
                    }
            response = order.placeSingleOrder(data=data)
            print(response) 
            if response['s']=='ok':
                order_ids.append(response['id'])
            else:
                response['message']
        i=0

        if len(order_ids)>0  and len(order.fetchPendingOrders()):
            while True:
                if len(order_ids)>0:
                    for i in range(len(order_ids)):
                        response = order.getOrderBookById(order_ids[i])
                        if response['s']=='ok':
                            data = response['orderbook'][0]
                            if data['status'] == 2 and data['side']==1:
                                order_ids.pop(order_ids[i])
                                #placing SL order
                                data_1 = {
                                    "symbol":trade_df.iloc[i].symbol,
                                    "qty":data['qty'],
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
                                #placing target order
                                data_2 = {
                                    "symbol":trade_df.iloc[i].symbol,
                                    "qty":data['qty'],
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
                                response = order.placeMultiOrder(data=[data_1,data_2])
                            elif  data['status'] == 2 and data['side']==-1:
                                order_ids.pop(order_ids[i])
                                data_1 = {
                                    "symbol":trade_df.iloc[i].symbol,
                                    "qty":data['qty'],
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
                                data_2 = {
                                    "symbol":trade_df.iloc[i].symbol,
                                    "qty":data['qty'],
                                    "type":3,
                                    "side":1,
                                    "productType":"INTRADAY",
                                    "limitPrice":trade_df.iloc[i].target,
                                    "stopPrice":0,
                                    "validity":"DAY",
                                    "disclosedQty":0,
                                    "offlineOrder":False,
                                    "orderTag":"intradaypivot"
                                        } 
                                response = order.placeMultiOrder(data=[data_1,data_2]) 


            
            


    #analytics = Analytics(trade_df)

    # print('Win Rate:%.2f'%analytics.win_rate())
    # print('Drawdown:%.2f'%analytics.draw_down())
    # print('Sharpe Ratio:%.2f'%analytics.sharpe_ratio(0.05,0.01,0.12))
    # print('Returns:%.2f'%analytics.calculate_returns())









