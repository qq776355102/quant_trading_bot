import pandas as pd
from trend_analysis import TrendAnalysis
from risk_analysis import RiskAnalysis
from buy_sell_analysis import BuySellAnalysis
from target_analysis import TargetAnalysis

from data.data_fetcher import  DataFetcher

# 示例数据
# data = pd.DataFrame({
#     'close': [100, 102, 101, 105, 107, 106, 110, 109, 108, 111]
# })

dataFetcher =  DataFetcher()
data  = dataFetcher.fetch_redis_data('BTC/USDT')
# 进行趋势分析
trend_analyzer = TrendAnalysis(data)


trend_data = trend_analyzer.analyze_trend()
print(trend_data)
# # 风险分析
# risk_analyzer = RiskAnalysis(trend_data)
# max_dd, position_size = risk_analyzer.analyze_risk(account_balance=10000, risk_per_trade=0.02)

# # 买卖分析
# buy_sell_analyzer = BuySellAnalysis(trend_data)
# trades = buy_sell_analyzer.execute_trade()

# # 目标分析
# target_analyzer = TargetAnalysis(entry_price=110, target_profit=0.2, stop_loss=0.02)
# target_price = target_analyzer.set_target()
# stop_loss_price = target_analyzer.set_stop_loss()
# time_to_target = target_analyzer.predict_time_to_target(avg_daily_volatility=0.03)

# print(f"Max Drawdown: {max_dd}, Position Size: {position_size}")
# print(f"Trades: {trades}")
# print(f"Target Price: {target_price}, Stop Loss: {stop_loss_price}, Time to Target: {time_to_target} days")
