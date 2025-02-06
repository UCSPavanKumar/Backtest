


processes= []

import sys
import warnings
from datetime import datetime,timedelta
from concurrent.futures import ThreadPoolExecutor   ,ProcessPoolExecutor,as_completed
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
sys.path.insert(1,r'/home/ec2-user/Backtest')
from analytics.analytics import Analytics
from constants import constants
from strategy.pivot_points import PivotPoint
from core.login import TradeLogin
from core.profile import Profile
from order_management.order_management import OrderManagement
from strategy.bollinger_breakout import BollingerBreakout
from strategy.golden_crossover import GoldenCrossOver
from strategy.turtle_trade import TurleTrade
from strategy.ema_rsi import EmaRsi
from multiprocessing import Process
import matplotlib.pyplot as plt
import multiprocessing as mp
from multiprocessing import freeze_support
import pandas as pd
import time
pd.set_option('display.max_columns', None)
import numpy as np
trade = TradeLogin()
trade.login()
trades = []
dfs = []
for symbol in ['NSE:ADANIGREEN-EQ']:#constants.nifty_50_symbols:
    data = BollingerBreakout(2024).runStrategy(symbol) 
    print(data)







