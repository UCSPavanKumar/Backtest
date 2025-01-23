from config.config_update import ConfigUpdate
from fyers_apiv3 import fyersModel
from datetime import datetime


class Profile(ConfigUpdate):
    def __init__(self):
        ConfigUpdate.__init__(self)
        self.fyers = fyersModel.FyersModel(client_id=self.retrieveClientId(),
                           token=self.retrieveAccessToken(),
                           is_async = False,
                           log_path='')
    
    def getProfile(self):
        """fetch profile data for the client"""
        response = self.fyers.get_profile()
        return response

    def getFunds(self):
        """fetch trading account available funds"""
        response = self.fyers.funds()
        return response
        
    
                