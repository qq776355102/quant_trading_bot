from abc import ABC, abstractmethod

class StrategyBase(ABC):
    """
    策略基类，所有策略都应继承此类并实现其抽象方法。
    """
    
    def __init__(self, symbol='BTC/USDT'):
        self.symbol = symbol
        self.is_running = False

    @abstractmethod
    def start(self):
        """
        启动策略
        """
        pass

    @abstractmethod
    def stop(self):
        """
        停止策略
        """
        pass

    @abstractmethod
    def execute(self):
        """
        执行策略逻辑
        """
        pass
