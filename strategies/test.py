from strategies.moving_average import MovingAverageStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.custom_strategy import CustomStrategy
from strategy_manager import StrategyManager

# 初始化策略管理器
manager = StrategyManager()

# 添加策略
moving_avg = MovingAverageStrategy(symbol="BTC/USDT")
macd = MACDStrategy(symbol="ETH/USDT")
custom = CustomStrategy(symbol="LTC/USDT", custom_param="buy")

manager.add_strategy("moving_average", moving_avg)
manager.add_strategy("macd", macd)
manager.add_strategy("custom", custom)

# 启动策略
manager.start_strategy("moving_average")
manager.start_strategy("macd")

# 执行策略
sample_data = [100, 102, 104, 106, 108, 110, 112, 114, 116]  # 示例价格数据
signal = manager.execute_strategy("moving_average", sample_data)
print(f"移动平均策略信号: {signal}")

# 停止策略
manager.stop_strategy("moving_average")
