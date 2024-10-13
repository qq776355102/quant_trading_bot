from telegram import Update
from telegram.ext import CallbackContext
from strategies.moving_average import MovingAverageStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.custom_strategy import CustomStrategy
from strategy_manager import StrategyManager

# 初始化策略管理器
manager = StrategyManager()

# 添加默认策略到管理器
manager.add_strategy("moving_average", MovingAverageStrategy(symbol="BTC/USDT"))
manager.add_strategy("macd", MACDStrategy(symbol="ETH/USDT"))
manager.add_strategy("custom", CustomStrategy(symbol="LTC/USDT", custom_param="buy"))

def start(update: Update, context: CallbackContext) -> None:
    """处理 /start 指令"""
    update.message.reply_text("欢迎使用量化交易机器人！你可以通过发送策略指令来控制交易。")

def add_strategy(update: Update, context: CallbackContext) -> None:
    """处理添加策略的指令，指令格式: /add_strategy <strategy_name>"""
    try:
        strategy_name = context.args[0]
        if strategy_name == 'moving_average':
            manager.add_strategy(strategy_name, MovingAverageStrategy())
        elif strategy_name == 'macd':
            manager.add_strategy(strategy_name, MACDStrategy())
        elif strategy_name == 'custom':
            manager.add_strategy(strategy_name, CustomStrategy(custom_param="buy"))
        update.message.reply_text(f"策略 {strategy_name} 已添加")
    except IndexError:
        update.message.reply_text("请输入正确的策略名称，例如 /add_strategy moving_average")

def start_strategy(update: Update, context: CallbackContext) -> None:
    """处理启动策略的指令，指令格式: /start_strategy <strategy_name>"""
    try:
        strategy_name = context.args[0]
        manager.start_strategy(strategy_name)
        update.message.reply_text(f"策略 {strategy_name} 已启动")
    except IndexError:
        update.message.reply_text("请输入正确的策略名称，例如 /start_strategy moving_average")

def stop_strategy(update: Update, context: CallbackContext) -> None:
    """处理停止策略的指令，指令格式: /stop_strategy <strategy_name>"""
    try:
        strategy_name = context.args[0]
        manager.stop_strategy(strategy_name)
        update.message.reply_text(f"策略 {strategy_name} 已停止")
    except IndexError:
        update.message.reply_text("请输入正确的策略名称，例如 /stop_strategy moving_average")

def execute_strategy(update: Update, context: CallbackContext) -> None:
    """处理执行策略的指令，指令格式: /execute_strategy <strategy_name>"""
    try:
        strategy_name = context.args[0]
        # 这里需要添加真实的市场数据，作为示例使用简单的价格数组
        sample_data = [100, 102, 104, 106, 108, 110, 112]
        signal = manager.execute_strategy(strategy_name, sample_data)
        update.message.reply_text(f"策略 {strategy_name} 执行结果: {signal}")
    except IndexError:
        update.message.reply_text("请输入正确的策略名称，例如 /execute_strategy moving_average")
