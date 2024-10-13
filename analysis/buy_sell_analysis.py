class BuySellAnalysis:
    def __init__(self, data):
        self.data = data

    def execute_trade(self):
        trades = []
        for index, row in self.data.iterrows():
            if row['buy_signal']:
                trades.append(('buy', row['close'], index))
            elif row['sell_signal']:
                trades.append(('sell', row['close'], index))
        return trades
