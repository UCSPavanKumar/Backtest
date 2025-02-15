from datetime import datetime


class minEma:

    def __init__(self):
        pass

    def advances_declines(self,df):
        stocks = list(df['symbol'].unique())

    def set_index(self,df):
        """
            setting time frame range from morning 09.15  to 15.25
        """
        dts = deque()
        in_dt = datetime.now()
        dt = in_dt
        for i in range(1,len(df)):
            dt = dt+timedelta(minutes=1)
            dts.append(dt)
        dts.appendleft(in_dt)

        return dts


    def filter(self,df):
        bullish_count = 0
        bearish_count = 0
        
        for i in range(len(df)-1):
            if df.iloc[i+1].close > df.iloc[i].high and df.iloc[i+1].close > df.iloc[i+1].open:
                bullish_count +=1
            elif df.iloc[i+1].close< df.iloc[i+1].open and df.iloc[i+1].close < df.iloc[i].low:
                bearish_count +=1
        if bearish_count > bullish_count:
            return ('BEARISH',bearish_count)
        elif bullish_count > bearish_count:
            return ('BULLISH',bullish_count)
        else:
            return ('NEUTRAL',0)

    def closer_to_ema(self,df,pattern):
       
        df['ema'] = df['close'].ewm(span=20).mean()
        
        i = 0
        data = ()
        while i< len(df)-1:
            if pattern == 'BEARISH':
                if df.iloc[i].high > df.iloc[i].ema:
                    data = (df.iloc[i].dt_time,df.iloc[i].symbol)
                    break
                else:
                    pass
            elif pattern == 'BULLISH':
                if df.iloc[i].low < df.iloc[i].ema:
                    data = (df.iloc[i].dt_time,df.iloc[i].symbol)
                    break
                else:
                    pass
        return data




