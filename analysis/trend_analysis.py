import numpy as np
import pandas as pd

class TrendAnalysis:
    def __init__(self, data):
        self.data = data

    def moving_average(self, period):
        return self.data['close'].rolling(window=period).mean()

    def rsi(self, period=14):
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def analyze_trend(self):
        self.data['short_ma'] = self.moving_average(5)
        self.data['long_ma'] = self.moving_average(20)
        self.data['rsi'] = self.rsi()

        self.data['buy_signal'] = (self.data['short_ma'] > self.data['long_ma']) & (self.data['rsi'] < 70)
        self.data['sell_signal'] = (self.data['short_ma'] < self.data['long_ma']) & (self.data['rsi'] > 30)

        return self.data[['close', 'short_ma', 'long_ma', 'rsi', 'buy_signal', 'sell_signal']]
