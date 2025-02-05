from fyers_apiv3 import fyersModel
import sys
from collections import deque
from datetime import datetime,timedelta
import warnings
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
import pandas as pd
sys.path.insert(1,r'D:/Projects/Backtest')
from config.config_update import ConfigUpdate
from time_management.dates import back_test_dates
class HistoricalData(ConfigUpdate):
    def __init__(self,year):
        self.year = year
        super().__init__()

    def get_dates_index(self,date_str:str,length):
        """
            setting time frame range from morning 09.15  to 15.25
        """
        dts = deque()
        in_dt = datetime(int(date_str.split("-")[0]),int(date_str.split("-")[1]),int(date_str.split("-")[2]),9,15)
        dt = in_dt
        for i in range(1,length):
            dt = dt+timedelta(minutes=5)
            dts.append(dt)
        dts.appendleft(in_dt)

        return dts

    def fetch_data_by_year(self,symbol):
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
        int_dfs = []
        for dt in back_test_dates:
            date_from = dt.split('|')[0]
            date_to = dt.split('|')[1]
            data = {
                "symbol":symbol,
                "resolution": '5',
                "date_format": "1",
                "range_from": date_from.format(self.year),
                "range_to": date_to.format(self.year),
                "cont_flag": "1"
            }
            try:
                response = fyers.history(data=data)
                df = pd.DataFrame(response['candles'])
                df.columns = ['date','open','high','low','close','volume']
                df['date'] = pd.to_datetime(df['date'],unit='s')
                df['symbol'] = symbol
                df.sort_values(by=['date'])
                df['dt_time'] = df['date'].dt.strftime('%Y-%m-%d')
                int_dfs.append(df)
            except Exception as e:
                print(str(e))
            df = pd.concat(int_dfs)
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
            if len(dfs)>0:
                final_df = pd.concat(dfs)
                return final_df
            else:
                return None


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
        try:
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
                    if len_df>75:
                        temp_df = temp_df.loc[75:149]
                        temp_df['date']= self.get_dates_index(dt,75)
                    else:
                        temp_df['date']= self.get_dates_index(dt,len_df)
                    dfs.append(temp_df)
                except Exception as e:
                    print(str(e))
            final_df = pd.concat(dfs)
            return final_df
        except Exception as e:
            return None
           
            
