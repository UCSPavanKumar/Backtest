import pandas as pd

class Analytics:
    def __init__(self,data:pd.DataFrame):
        self.data = data

    def win_rate(self):
        wins    = 0
        loses   = 0
        self.data['flag'] = self.data['PnL'].apply(lambda x: 'win' if x>0 else 'lose')
        wins = self.data[self.data['flag']=='win'].count()
        loses = self.data[self.data['flag']=='lose'].count()
        return round((wins/(wins+loses))*100,2)

    def draw_down(self):
        df = self.data.copy()
        df['Cumulative'] = df['PnL'].cumsum().round(2)
        df['HighValue'] = df['Cumulative'].cummax()

        df['Drawdown'] = df['Cumulative'] - df['HighValue']
        return round(df['Drawdown'].max(),2)

    def sharpe_ratio(self,risk_free_rate,monthly_rate,yearly_rate):
        return round(((yearly_rate-risk_free_rate)/monthly_rate)*100,2)

    def calculate_returns(self):
        return round(((self.data[-1]-self.data[0])/self.data[0])*100,2)
