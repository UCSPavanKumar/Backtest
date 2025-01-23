import sys
sys.path.insert(1,r'/home/iob/algotrading')
from core.login import TradeLogin
from config.config_update import ConfigUpdate
from core.profile import Profile
from core.order_management import OrderManagement
trade = TradeLogin()
trade.login()
while ConfigUpdate().retrieveAccessToken() is  None:
    print('waiting for access token')

client_profile = Profile().getProfile()
fund_details =  Profile().getFunds()
orderbook = OrderManagement().fetchPendingOrders()
tradebook = OrderManagement().fetchTradeBook()
positions = OrderManagement().fetchCurrentOverallPositions()
all_positions = OrderManagement().fetchIndividualTradePositions()
print(all_positions)
print('Total Overall Position: {0}'.format(positions))

