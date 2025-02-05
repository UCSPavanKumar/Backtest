


processes = []



def log_result(result):
    """this is called whenever PivotPoint.run,returns
        a result.trades list is modified by main process,not the pool workers
    """
    if result is not None:
        if len(result)>0 and result is not None:
            trades.append(result)
        else:
            pass
    else:
        pass



def fyers_order(trade_df):
    """Preparing entry,sl,target order for execution of strategy"""
    if len(trade_df)>0:
        order = OrderManagement()
        order_ids = {}
        for i in range(len(trade_df)): 
            if trade_df.iloc[i].pattern =='BULLISH': 
                data_entry = {
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
                data_sl = {
                "symbol":trade_df.iloc[i].symbol,
                "qty":trade_df.iloc[i].qty,
                "type":3,
                "side":0,
                "productType":"INTRADAY",
                "limitPrice":0,
                "stopPrice":trade_df.iloc[i].sl,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":False,
                "orderTag":"intradaypivot"
                    }
                
                data_target = {
                "symbol":trade_df.iloc[i].symbol,
                "qty":trade_df.iloc[i].qty,
                "type":1,
                "side":0,
                "productType":"INTRADAY",
                "limitPrice":trade_df.iloc[i].target,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":False,
                "orderTag":"intradaypivot"
                    }
            elif trade_df.iloc[i].pattern =='BEARISH': 
                data_entry = {
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
                data_sl = {
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
                
                data_target = {
                "symbol":trade_df.iloc[i].symbol,
                "qty":trade_df.iloc[i].qty,
                "type":1,
                "side":0,
                "productType":"INTRADAY",
                "limitPrice":trade_df.iloc[i].target,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":False,
                "orderTag":"intradaypivot"
                    }
            
            response = order.placeSingleOrder(data=data_entry)
            print(response)
            if response['s']=='ok':
                order_ids[response['id']] = [data_sl,data_target]
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

    
    


            
            


    #analytics = Analytics(trade_df)

    # print('Win Rate:%.2f'%analytics.win_rate())
    # print('Drawdown:%.2f'%analytics.draw_down())
    # print('Sharpe Ratio:%.2f'%analytics.sharpe_ratio(0.05,0.01,0.12))
    # print('Returns:%.2f'%analytics.calculate_returns())










