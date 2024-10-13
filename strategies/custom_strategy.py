from .strategy_base import StrategyBase

class CustomStrategy(StrategyBase):
    """
    用户自定义策略
    """

    def __init__(self, symbol='BTC/USDT', custom_param=None):
        super().__init__(symbol)
        self.custom_param = custom_param

    def start(self):
        self.is_running = True
        print(f"启动自定义策略：{self.symbol}，参数：{self.custom_param}")

    def stop(self):
        self.is_running = False
        print(f"停止自定义策略：{self.symbol}")

    def execute(self, data):
        """
        执行自定义策略逻辑，输入参数为价格数据
        :param data: 历史价格数据 (list or np.array)
        :return: 策略信号 (买入/卖出/持有)
        """
        if not self.is_running:
            print("策略未启动，无法执行")
            return None

        # 这里用户可以定义自己的逻辑
        if self.custom_param == 'buy':
            return "买入信号"
        elif self.custom_param == 'sell':
            return "卖出信号"
        else:
            return "持有"
