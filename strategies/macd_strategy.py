from .strategy_base import StrategyBase

class MACDStrategy(StrategyBase):
    """
    MACD策略实现
    """

    def __init__(self, symbol='BTC/USDT', short_period=12, long_period=26, signal_period=9):
        super().__init__(symbol)
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period

    def start(self):
        self.is_running = True
        print(f"启动MACD策略：{self.symbol}")

    def stop(self):
        self.is_running = False
        print(f"停止MACD策略：{self.symbol}")

    def execute(self, data):
        """
        执行MACD策略逻辑，输入参数为价格数据
        :param data: 历史价格数据 (list or np.array)
        :return: 策略信号 (买入/卖出/持有)
        """
        if not self.is_running:
            print("策略未启动，无法执行")
            return None

        short_ema = self._calculate_ema(data, self.short_period)
        long_ema = self._calculate_ema(data, self.long_period)
        macd_line = short_ema - long_ema
        signal_line = self._calculate_ema(macd_line, self.signal_period)

        if macd_line[-1] > signal_line[-1]:
            return "买入信号"
        elif macd_line[-1] < signal_line[-1]:
            return "卖出信号"
        else:
            return "持有"

    def _calculate_ema(self, data, period):
        """
        计算指数移动平均 (EMA)
        :param data: 历史价格数据
        :param period: 计算周期
        :return: EMA值
        """
        ema = [sum(data[:period]) / period]  # 初始化EMA
        multiplier = 2 / (period + 1)

        for price in data[period:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
        
        return ema
 