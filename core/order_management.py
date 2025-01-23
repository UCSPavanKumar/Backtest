from config.config_update import ConfigUpdate
from fyers_apiv3 import fyersModel
class OrderManagement(ConfigUpdate):
    def __init__(self):
        super().__init__()
        self.fyers = fyersModel.FyersModel(client_id=self.retrieveClientId(),
                           token=self.retrieveAccessToken(),
                           is_async = False,
                           log_path='')
    

    def fetchPendingOrders(self):
        """Fetching all pending orders in trading account"""
        orders = self.fyers.orderbook()
        return orders

    def cancelAllPendingOrders(self):
        """Cancellation of all Pending Orders"""
        pass

    def fetchTradeBook(self):
        """Fetch all executed Trades"""
        trades = self.fyers.tradebook()
        return trades
    

    def fetchCurrentOverallPositions(self):
        """Fetch Running P&L"""
        response = self.fyers.positions()
        return round(response['overall']['pl_total'],2)
    

    def fetchIndividualTradePositions(self):
        """Fetching each Trade Positions"""
        row_txt = ''
        positions = self.fyers.positions()
        for row in positions['netPositions']:
            if row['unrealized_profit']!=0:
                row_txt = row_txt+('Stock Name: {0}, Current Position: {1}'+'\n'+'---------------'+'\n').format(row['symbol'],round(row['pl'],2))
        return row_txt