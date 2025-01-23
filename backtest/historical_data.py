from fyers_apiv3 import fyersModel
import sys
import pandas as pd
sys.path.insert(1,r'/home/iob/algotrading')
from config.config_update import ConfigUpdate
class HistoricalData(ConfigUpdate):
    def __init__(self):
        super().__init__()

    def fetch_historical_data(self,symbol,date_from,date_to,resolution):
        """
        Fetch historical data for analysing the stocks
        Args
            Symbol: Stock Symbol for fetching data NSE:SBIN-EQ
            date_from: format yyyy-mm-dd
            date_to: format yyyy-mm-dd
            resolution: 1, 2, 3, 5, 10, 15, 20, 30, 45, 60, 120, 180, and 240 minutes

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
        return df