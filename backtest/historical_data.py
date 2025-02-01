from fyers_apiv3 import fyersModel
import sys
from collections import deque
from datetime import datetime,timedelta
import pandas as pd
sys.path.insert(1,r'/home/iob/algotrading')
from config.config_update import ConfigUpdate
class HistoricalData(ConfigUpdate):
    def __init__(self):
        super().__init__()

    def get_dates_index(self,date_str:str,length):
        """

        """
        dts = deque()
        in_dt = datetime(int(date_str.split("-")[0]),int(date_str.split("-")[1]),int(date_str.split("-")[2]),9,15)
        dt = in_dt
        for i in range(1,length):
            dt = dt+timedelta(minutes=5)
            dts.append(dt)
        dts.appendleft(in_dt)

        return dts
    

    def fetch_historical_data(self,symbol,date_from,date_to,resolution):
        """
        Fetch historical data for analysing the stocks
        Args
            Symbol: Stock Symbol for fetching data NSE:SBIN-EQ
            date_from: format yyyy-mm-dd
            date_to: format yyyy-mm-dd


        """
        fyers = fyersModel.FyersModel(client_id=self.retrieveClientId(),
                                      token=self.retrieveAccessToken(),
                                      is_async=False,
                                      log_path="")
        data = {
            "symbol":symbol,
            "resolution": resolution,
            "date_format": "1",
            "range_from": date_from,
            "range_to": date_to,
            "cont_flag": "1"
        }

        response = fyers.history(data=data)
        
        df = pd.DataFrame(response['candles'])
        df.columns = ['date','open','high','low','close','volume']
        df['date'] = pd.to_datetime(df['date'],unit='s')
        df.sort_values(by=['date'])
        df['dt_time'] = df['date'].dt.strftime('%Y-%m-%d')
        dates = df['dt_time'].unique()
        dates.sort()
        dfs = []
        for dt in dates:
            try:
                temp_df = df[df['dt_time']==dt]
                len_df = len(temp_df)
                temp_df['date']= self.get_dates_index(dt,len_df)
                dfs.append(temp_df)
            except Exception as e:
                print(str(e))
        final_df = pd.concat(dfs)
        return final_df