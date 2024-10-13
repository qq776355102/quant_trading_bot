class StrategyManager:
    """
    策略管理模块，用于管理多个策略
    """
    
    def __init__(self):
        self.strategies = {}  # 策略注册表

    def add_strategy(self, name, strategy_instance):
        """
        添加策略到注册表
        :param name: 策略名称
        :param strategy_instance: 策略实例
        """
        self.strategies[name] = strategy_instance
        print(f"策略 {name} 已添加")

    def remove_strategy(self, name):
        """
        从注册表中删除策略
        :param name: 策略名称
        """
        if name in self.strategies:
            del self.strategies[name]
            print(f"策略 {name} 已删除")
        else:
            print(f"策略 {name} 不存在")

    def start_strategy(self, name):
        """
        启动指定策略
        :param name: 策略名称
        """
        if name in self.strategies:
            self.strategies[name].start()
        else:
            print(f"策略 {name} 不存在")

    def stop_strategy(self, name):
        """
        停止指定策略
        :param name: 策略名称
        """
        if name in self.strategies:
            self.strategies[name].stop()
        else:
            print(f"策略 {name} 不存在")

    def execute_strategy(self, name, data):
        """
        执行指定策略
        :param name: 策略名称
        :param data: 价格数据
        :return: 策略信号
        """
        if name in self.strategies:
            return self.strategies[name].execute(data)
        else:
            print(f"策略 {name} 不存在")
            return None
