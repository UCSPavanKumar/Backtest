
import numpy as np
class Indicators:

    def __init__(self):
        pass

    def pivotpoints(self,high,low,close):
        """
        Calculate pivot points
        """
        pivot = (high+low+close)/3
        r1 = 2*pivot - low
        s1 = 2*pivot - high
        r2 = pivot + (high - low)
        s2 = pivot - (high - low)
        r3 = high + 2*(pivot - low)
        s3 = low - 2*(high - pivot)
        return pivot,r1,s1,r2,s2,r3,s3

    def nr3(self,df,dates):
        """
        Finding NR3 range for the slice of dataframe
        """
        result = 'N'
        first_day_high = df[df['dt_time']==dates[0]]['high'].max()
        first_day_low = df[df['dt_time']==dates[0]]['low'].min()
        second_day = df[df['dt_time']==dates[1]]
        second_day_close = second_day.iloc[len(second_day)-1].close
        third_day  = df[df['dt_time']==dates[2]]
        third_day_close = third_day.iloc[len(third_day)-1].close
        if second_day_close<first_day_high and second_day_close>first_day_low and third_day_close<first_day_high and third_day_close>first_day_low:
            result = 'Y'
        return result


    def rsi(self,df):
        df['diff'] = df['close'].diff() #axis = 0 column
        df['gain'] = np.where(df['diff']>0,df['diff'],0)
        df['loss'] = -np.where(df['diff']<0,df['diff'],0)
        df['flag'] = np.where(df['close']>df['open'],'BU','BE')
        df['avg_gain'] = df['gain'].rolling(14).sum()/df['gain'].ne(0).rolling(14).sum()
        df['avg_loss'] = df['loss'].rolling(14).sum()/df['loss'].ne(0).rolling(14).sum()
        df['rsi'] = 100-(100/(1+(np.where(df['avg_gain'].ne(None),df['avg_gain']/df['avg_loss'],0))))
        df['rsi'] = round(df['rsi'],2)
        return df