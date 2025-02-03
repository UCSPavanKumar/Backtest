

class Brokerage:
    def __init__(self):
        pass

    def calculate_commission(self, buy_turnover,sell_turnover):
        brokerage = 40
        stt_ctt   = 0.00025*sell_turnover
        sebi_charges = 0.000001*sell_turnover
        txn_charges = 0.0000297*(buy_turnover+sell_turnover)
        gst =   0.18*(brokerage+txn_charges+sebi_charges)
        stamp_duty = 0.00003*buy_turnover
        total_charges = brokerage+stt_ctt+sebi_charges+txn_charges+gst+stamp_duty
        return total_charges
