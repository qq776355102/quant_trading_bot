# custom_strategy.py
import numpy as np
import pandas as pd
from strategy_base import StrategyBase

class TrendPullbackStrategy(StrategyBase):

    """多指标趋势确认与回调买入策略"""

    
    def __init__(self, short_window=12, long_window=26, signal_window=9, rsi_period=14, slope_window=5):
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        self.rsi_period = rsi_period
        self.slope_window = slope_window

    def calculate_macd(self, data):
        short_ema = data['Close'].ewm(span=self.short_window, adjust=False).mean()
        long_ema = data['Close'].ewm(span=self.long_window, adjust=False).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=self.signal_window, adjust=False).mean()
        data['MACD'] = macd
        data['Signal'] = signal
        return data

    def calculate_rsi(self, data):
        delta = data['Close'].diff(1)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        avg_gain = pd.Series(gain).rolling(window=self.rsi_period, min_periods=1).mean()
        avg_loss = pd.Series(loss).rolling(window=self.rsi_period, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        data['RSI'] = rsi
        return data

    def calculate_slope(self, data):
        data['SMA'] = data['Close'].rolling(window=self.slope_window).mean()
        data['Slope'] = data['SMA'].diff()
        return data

    def generate_signals(self, data):
        data = self.calculate_macd(data)
        data = self.calculate_rsi(data)
        data = self.calculate_slope(data)
        
        buy_signals = []
        position = False

        for i in range(len(data)):
            # MACD Trend Confirmation
            macd = data['MACD'].iloc[i]
            signal = data['Signal'].iloc[i]
            slope = data['Slope'].iloc[i]
            rsi = data['RSI'].iloc[i]

            macd_trend_up = (macd > signal) and (macd > 0 and signal > 0)
            slope_positive = slope > 0
            rsi_buy_zone = 30 <= rsi <= 50

            if macd_trend_up and slope_positive and rsi_buy_zone and not position:
                buy_signals.append(data.index[i])
                position = True  # Assume we buy here
            elif not macd_trend_up or rsi > 70:  # Exit conditions
                position = False

        return buy_signals

    def apply(self, data):
        """
        Main method to apply the strategy to the data.
        :param data: DataFrame with at least a 'Close' column.
        :return: DataFrame with signals and indicators.
        """
        buy_signals = self.generate_signals(data)
        data['Buy_Signal'] = data.index.isin(buy_signals)
        return data



    """方案一：多指标趋势确认与回调买入策略
        组合指标：
            MACD：趋势确认
            斜率：价格动量
            RSI：识别回调中的超卖点
        策略逻辑：
            趋势确认：使用MACD来确认趋势是否向上。MACD的DIF线上穿DEA线，并且两线均在零轴上方时，表明大趋势向上。
                斜率确认动量：计算短期价格均线的斜率（如5周期均线斜率），如果斜率为正且持续走高，则表明动量支持趋势延续。
                RSI识别买入点：当RSI处于30-50之间，表明价格可能出现了较好的回调买入机会，避免在超买区域（RSI>70）追高。
            买入信号：当RSI在回调至合理区间（如30-50）且MACD和斜率均支持趋势上升时，发出买入信号。
        优点：
            趋势强度确认：MACD和斜率结合确保买入信号只在明显的上升趋势中生成，避免追随假信号。
                回调买入机会：通过RSI捕捉回调后的入场机会，避免过于激进的追涨操作。
                适用于多种市场环境：无论是强趋势还是温和上升趋势，该策略都能较好地识别买入机会。
        不足：
            RSI滞后性：在某些强势趋势中，RSI回调可能非常有限，可能错过部分强势行情中的快速上涨。
                回调过浅时的信号缺失：如果回调幅度不大，RSI可能不会跌至合适的买入区间，导致错过入场时机。
        未考虑情况：
            市场极端波动：当市场出现极端波动时，RSI和MACD可能同时失效，未考虑在高波动性市场中的调整机制。
            成交量：该策略未考虑成交量因素，成交量的配合可以进一步提高趋势确认的准确性。
    """

# Example usage
if __name__ == "__main__":
    # Sample data
    data = pd.DataFrame({
        'Close': [100, 102, 101, 105, 107, 110, 108, 109, 107, 111, 113, 115, 114]
    })
    
    strategy = TrendPullbackStrategy()
    result = strategy.apply(data)
    print(result)