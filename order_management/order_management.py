from config.config_update import ConfigUpdate
from fyers_apiv3 import fyersModel
class OrderManagement(ConfigUpdate):
    def __init__(self):
        super().__init__()
        self.fyers = fyersModel.FyersModel(client_id=self.retrieveClientId(),
                           token=self.retrieveAccessToken(),
                           is_async = False,
                           log_path='')

    def prepareOrder(self,*args,**kwargs):
        print(kwargs)
        """Prepare dict for bullish and bearish entry,SL,target order"""
        data = {
                    "symbol":kwargs['symbol'],
                    "qty":kwargs['qty'],
                    "type":kwargs['otype'],
                    "side":kwargs['side'],
                    "productType":"INTRADAY",
                    "limitPrice":kwargs['limit_price'],
                    "stopPrice":kwargs['sl'],
                    "validity":"DAY",
                    "disclosedQty":0,
                    "offlineOrder":False,
                    "orderTag":"intradaypivot"
                }
        return data

    def getOrderBookById(self,order_id):
        data = {"id":order_id}

        response = self.fyers.orderbook(data=data)
        return response

    def fetchPendingOrders(self):
        """Fetching all pending orders in trading account"""
        orders = self.fyers.orderbook()
        return orders

    def fetchCurrentTrades(self):
        """Fetching all trades"""
        trades = self.fyers.tradebook()
        return trades

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
        if 'overall' in response.keys():
            return round(response['overall']['pl_total'],2)
        else:
            return None

    def prepareOrder(self,*args,flag,qty,order_side,symbol,stop_price,side,limit_price):
        if args['flag'] =='BULLISH' and args['order_type']=='Limit':
            data = {
                                    "symbol": args['symbol'],
                                    "qty":args['qty'],
                                    "type":1,
                                    "side":-1,
                                    "productType":"INTRADAY",
                                    "limitPrice":args['limit_price'],
                                    "stopPrice":0,
                                    "validity":"DAY",
                                    "disclosedQty":0,
                                    "offlineOrder":False,
                                    "orderTag":args['tag']
                                        }
        elif args['flag'] =='BULLISH' and args['order_type']=='SL':
            data = {
                                    "symbol": args['symbol'],
                                    "qty":args['qty'],
                                    "type":1,
                                    "side":-1,
                                    "productType":"INTRADAY",
                                    "limitPrice":args['limit_price'],
                                    "stopPrice":0,
                                    "validity":"DAY",
                                    "disclosedQty":0,
                                    "offlineOrder":False,
                                    "orderTag":args['tag']
                                        }





    def fetchIndividualTradePositions(self):
        """Fetching each Trade Positions"""
        row_txt = ''
        positions = self.fyers.positions()
        if 'netPositions' in positions.keys():
            for row in positions['netPositions']:
                if row['unrealized_profit']!=0:
                    row_txt = row_txt+('Stock Name: {0}, Current Position: {1}'+'\n'+'---------------'+'\n').format(row['symbol'],round(row['pl'],2))
            return row_txt
        else:
            return None


    def placeSingleOrder(self,data):
        """Placing SL-M orders for Intraday Trades"""
        response = self.fyers.place_order(data=data)
        return response

    def placeMultiOrder(self,data):
        """placing basket orders"""
        response = self.fyers.place_basket_orders(data=data)
        return response

