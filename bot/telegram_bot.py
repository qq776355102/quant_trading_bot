import logging
from telegram.ext import Updater, CommandHandler
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers import start, add_strategy, start_strategy, stop_strategy, execute_strategy

# 设置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """启动Telegram机器人"""
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    
    # 获取调度器来注册处理程序
    dispatcher = updater.dispatcher

    # 注册命令处理程序
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add_strategy", add_strategy))
    dispatcher.add_handler(CommandHandler("start_strategy", start_strategy))
    dispatcher.add_handler(CommandHandler("stop_strategy", stop_strategy))
    dispatcher.add_handler(CommandHandler("execute_strategy", execute_strategy))

    # 启动机器人
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

"""在 Telegram 上，向你的机器人发送 /start 来确认机器人正常工作。
使用 /add_strategy <strategy_name> 可以添加新的策略，例如：
bash
复制代码
/add_strategy moving_average
使用 /start_strategy <strategy_name> 启动某个策略：
bash
复制代码
/start_strategy moving_average
使用 /stop_strategy <strategy_name> 停止某个策略：
bash
复制代码
/stop_strategy moving_average
使用 /execute_strategy <strategy_name> 执行策略并返回信号：
bash
复制代码
/execute_strategy moving_average
"""

