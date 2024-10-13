


from indicators.ema  import find_all_consecutive_ema_periods
from data.data_fetcher import DataFetcher
import matplotlib.pyplot as plt
# import yfinance as yf
# 过滤出5分钟最近200根k曾表现出强势的标的
def test1():
    ticker = 'turbo'
    dataf = DataFetcher()
    data =  dataf.fetch_redis_data(ticker,freq='15min')
    # print(data)
     # 确保数据按时间排序
    data = data.sort_index()
    
    # 应用函数，找到所有满足条件的时间区间
    periods = find_all_consecutive_ema_periods(
        data, 
        ema_period=10, 
        timeframe=500, 
        consecutive=20, 
        condition='above',
        tolerance=0.002  # 0.2% 误差范围
    )
    
    # 输出结果
    if periods:
        print(f"共找到 {len(periods)} 个满足条件的时间区间：")
        for idx, period in enumerate(periods, 1):
            print(f"第 {idx} 个区间：开始时间 {period['start_time']}, 结束时间 {period['end_time']}, 长度 {period['length']} 根K线")
    else:
        print("没有找到满足条件的时间区间。")
    
    # 可视化示例
    plt.figure(figsize=(14,7))
    plt.plot(data['close'], label='Close Price', alpha=0.5)
    plt.plot(data['EMA_10'], label='EMA10', alpha=0.9)

    # 标记满足条件的区域，并显示注释
    for period in periods:
        start_time = period['start_time']
        end_time = period['end_time']
        length = period['length']
        duration = end_time - start_time

        # 绘制绿色区域
        plt.axvspan(start_time, end_time, color='green', alpha=0.3)

        # 添加注释，显示区间信息
        mid_point = start_time + (end_time - start_time) / 2  # 中间位置
        plt.text(mid_point, data['close'].max() * 0.95, 
                 f'start: {start_time.strftime("%Y-%m-%d %H:%M")}\nend: {end_time.strftime("%Y-%m-%d %H:%M")}\nNKlines: {length}\nduration: {duration}', 
                 horizontalalignment='left', verticalalignment='top', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

    plt.title(f'{ticker} Price with EMA Periods')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
test1()


