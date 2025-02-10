import pandas as pd
import numpy as np
import sys
df = pd.read_csv('/home/ec2-user/data/NSE:'+sys.argv[1]+'-EQ.csv')
hcltech = df[df['symbol']=='NSE:'+sys.argv[1]+'-EQ']
hcltech['long_ema'] = hcltech['close'].ewm(span=200).mean()
hcltech['diff']=hcltech['UB']-hcltech['LB']
hcltech['flg'] = np.where(hcltech['diff']<(0.005*hcltech['close']),'Y','N')
dates = df['dt_time'].unique()
dates.sort()
df = hcltech
for i in range(len(dates)-1):
    dff = df[df['dt_time']==dates[i]]
    first_candle = float(df[df['dt_time']==dates[i+1]].iloc[0].close)
    last_candle = float(df[df['dt_time']==dates[i+1]].iloc[-1].close)
    bb_check = dff[len(dff)-25:len(dff)-1]
    count = len(bb_check[bb_check['flg']=='Y'])
    pct = float(round(((first_candle - dff.iloc[-1].close)/dff.iloc[-1].close)*100,2))
    pct_close = float(round(((dff.iloc[-1].close-last_candle)/dff.iloc[-1].close)*100,2))
    print(dates[i],count,pct,pct_close)
