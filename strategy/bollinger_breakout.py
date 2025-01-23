from fyers_apiv3 import fyersModel
import sys
import pandas as pd
sys.path.insert(1,r'/home/iob/algotrading')
from backtest.historical_data import HistoricalData
class BollingerBreakout(HistoricalData):
    def __init__(self):
        super().__init__()

    def runStrategy(self,from_date,to_date,resolution,symbols):
        """ 
        1. Checking for first 5 min candle of day with prev day close
        2. Day's Pct change over previous day candle
        3. 5 min high-low pct of previous day close
        
        Args
            Symbols: datatype [list]
        """
        backtest_data = []
        #symbols = ['NSE:COFORGE-EQ']#,'NSE:KEI-EQ','NSE:ZENSARTECH-EQ','NSE:UNITDSPR-EQ','NSE:APLAPOLLO-EQ','NSE:GPIL-EQ','NSE:APOLLOHOSP-EQ','NSE:BALKRISIND-EQ','NSE:SHYAMMETL-EQ','NSE:INDUSTOWER-EQ','NSE:NBCC-EQ','NSE:TTML-EQ','NSE:WIPRO-EQ','NSE:KOTAKBANK-EQ','NSE:BDL-EQ','NSE:GSPL-EQ','NSE:AADHARHFC-EQ','NSE:PNBHOUSING-EQ','NSE:ICICIPRULI-EQ','NSE:LTTS-EQ','NSE:ZOMATO-EQ','NSE:SCHNEIDER-EQ','NSE:ADANIPOWER-EQ','NSE:INDIANB-EQ','NSE:IRCON-EQ','NSE:HDFCLIFE-EQ','NSE:MPHASIS-EQ','NSE:JMFINANCIL-EQ','NSE:SWANENERGY-EQ','NSE:DEEPAKFERT-EQ','NSE:PEL-EQ','NSE:VEDL-EQ','NSE:MFSL-EQ','NSE:EIDPARRY-EQ','NSE:IDBI-EQ','NSE:BALRAMCHIN-EQ','NSE:UNOMINDA-EQ','NSE:MARUTI-EQ','NSE:WELCORP-EQ','NSE:WELSPUNLIV-EQ','NSE:ICICIGI-EQ','NSE:BSE-EQ','NSE:SUNDARMFIN-EQ','NSE:RKFORGE-EQ','NSE:PERSISTENT-EQ','NSE:FSL-EQ','NSE:TCS-EQ','NSE:ANANDRATHI-EQ','NSE:NAVINFLUOR-EQ','NSE:ZYDUSLIFE-EQ','NSE:SUVENPHAR-EQ','NSE:FLUOROCHEM-EQ','NSE:SRF-EQ','NSE:KIMS-EQ','NSE:GLAND-EQ','NSE:DRREDDY-EQ','NSE:MINDACORP-EQ','NSE:PAYTM-EQ','NSE:OIL-EQ','NSE:BIOCON-EQ','NSE:GVT&D-EQ','NSE:RAINBOW-EQ','NSE:GILLETTE-EQ','NSE:ONGC-EQ','NSE:KIRLOSBROS-EQ','NSE:SYRMA-EQ','NSE:HUDCO-EQ','NSE:LTIM-EQ','NSE:LALPATHLAB-EQ','NSE:JUBLFOOD-EQ','NSE:ANGELONE-EQ','NSE:SBICARD-EQ','NSE:PRAJIND-EQ','NSE:PATANJALI-EQ','NSE:TITAN-EQ','NSE:AEGISLOG-EQ','NSE:SAREGAMA-EQ','NSE:BLS-EQ','NSE:JUSTDIAL-EQ','NSE:IRFC-EQ','NSE:PFC-EQ','NSE:RVNL-EQ','NSE:GICRE-EQ','NSE:CENTURYPLY-EQ','NSE:SAPPHIRE-EQ','NSE:SAMMAANCAP-EQ','NSE:JUBLINGREA-EQ','NSE:RAILTEL-EQ','NSE:REDINGTON-EQ','NSE:GODFRYPHLP-EQ','NSE:BAJFINANCE-EQ','NSE:LEMONTREE-EQ','NSE:FACT-EQ','NSE:CLEAN-EQ','NSE:VGUARD-EQ','NSE:ACE-EQ','NSE:GODIGIT-EQ','NSE:IREDA-EQ','NSE:KAYNES-EQ','NSE:BBTC-EQ','NSE:CRISIL-EQ','NSE:ASTRAZEN-EQ','NSE:KNRCON-EQ','NSE:CONCORDBIO-EQ','NSE:ITI-EQ','NSE:ECLERX-EQ','NSE:FORTIS-EQ','NSE:COCHINSHIP-EQ','NSE:BAJAJHLDNG-EQ','NSE:FIVESTAR-EQ','NSE:HOMEFIRST-EQ','NSE:JSWENERGY-EQ','NSE:KEC-EQ','NSE:TRIVENI-EQ','NSE:CAMPUS-EQ','NSE:LLOYDSME-EQ','NSE:NEWGEN-EQ','NSE:CHALET-EQ','NSE:BLUESTARCO-EQ','NSE:GODREJIND-EQ','NSE:VIJAYA-EQ','NSE:CHEMPLASTS-EQ','NSE:AMBER-EQ','NSE:DATAPATTNS-EQ','NSE:KFINTECH-EQ','NSE:TATAINVEST-EQ','NSE:RAYMOND-EQ','NSE:QUESS-EQ','NSE:PTCIL-EQ','NSE:INTELLECT-EQ','NSE:DEVYANI-EQ','NSE:360ONE-EQ','NSE:MANAPPURAM-EQ','NSE:ASTERDM-EQ','NSE:INDIACEM-EQ','NSE:CAPLIPOINT-EQ','NSE:ANANTRAJ-EQ','NSE:AVANTIFEED-EQ','NSE:JWL-EQ','NSE:TITAGARH-EQ','NSE:TECHNOE-EQ','NSE:JYOTICNC-EQ','NSE:EXIDEIND-EQ','NSE:BASF-EQ','NSE:ARE&M-EQ','NSE:WESTLIFE-EQ','NSE:CRAFTSMAN-EQ','NSE:BHARTIHEXA-EQ']
        for symbol in symbols:
            hist_data = HistoricalData().fetch_historical_data(symbol,from_date,to_date,resolution)
            hist_data['ema_200'] = hist_data['close'].ewm(span=200,adjust=False).mean()
            number_of_days = int(len(hist_data)/75)
            for i in range(1,number_of_days):
                next_day            = hist_data.iloc[75*i:75*(i+1)]
                first_candle_of_day = abs(next_day.iloc[0].high - next_day.iloc[0].low)
                prev_day_close      = hist_data[75*(i-1):75*i].iloc[74].close
                pct_over_prev_close = round((first_candle_of_day/prev_day_close)*100,2)
                next_day_close      = next_day.iloc[74].close
                ema_200             = next_day.iloc[74].ema_200
                row = []
                row.append(next_day.iloc[74].date.strftime('%Y%m%d'))
                row.append(symbol)
                row.append(float(prev_day_close))
                row.append(float(next_day_close))
                row.append(float(pct_over_prev_close))
                row.append(float(next_day.iloc[74].ema_200))
                
                if (next_day_close > prev_day_close):
                    pct_chg = round(((prev_day_close-next_day_close)/prev_day_close)*100,2) 
                else:
                    pct_chg = -round(((prev_day_close-next_day_close)/prev_day_close)*100,2)
                row.append(float(pct_chg))
                backtest_data.append(row)
            print('Processing Done for {0}'.format(symbol))
        df_back = pd.DataFrame(backtest_data)
        df_back.columns = ['trade_date','symbol','prev_day_close','next_day_close','pct_over_prev_close','day_pct_chg','first_candle_200_ema']
        return df_back