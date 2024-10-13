from .strategy_base import StrategyBase
import numpy as np

class MovingAverageStrategy(StrategyBase):
    """
    简单移动平均策略实现
    """

    def __init__(self, symbol='BTC/USDT', short_window=10, long_window=30):
        super().__init__(symbol)
        self.short_window = short_window
        self.long_window = long_window

    def start(self):
        self.is_running = True
        print(f"启动移动平均策略：{self.symbol}")

    def stop(self):
        self.is_running = False
        print(f"停止移动平均策略：{self.symbol}")

    def execute(self, data):
        """
        执行策略逻辑，输入参数为价格数据
        :param data: 历史价格数据 (list or np.array)
        :return: 策略信号 (买入/卖出/持有)
        """
        if not self.is_running:
            print("策略未启动，无法执行")
            return None

        short_ma = np.mean(data[-self.short_window:])
        long_ma = np.mean(data[-self.long_window:])

        if short_ma > long_ma:
            return "买入信号"
        elif short_ma < long_ma:
            return "卖出信号"
        else:
            return "持有"
