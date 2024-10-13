import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import yfinance as yf

def find_all_consecutive_ema_periods(data, ema_period=10, timeframe=50, consecutive=20, condition='above', tolerance=0.002):
    """
    找出指定时间框架内所有满足条件的连续K线区间，并返回它们的开始时间和结束时间。

    参数：
    - data (pd.DataFrame): 包含至少 'close' 列的DataFrame。
    - ema_period (int): 计算EMA的周期。
    - timeframe (int): 检查的时间框架（最近多少根K线）。
    - consecutive (int): 需要连续满足条件的K线数量。
    - condition (str): 条件类型，'above' 表示收盘价高于EMA，'below' 表示收盘价低于EMA。
    - tolerance (float): 收盘价与EMA的允许误差范围（默认为0.002，即0.2%）。

    返回：
    - periods (list): 一个列表，包含所有满足条件的区间。每个区间是一个字典，包含 'start_time' 和 'end_time'。
    """
    ema_column = f'EMA_{ema_period}'
    data[ema_column] = data['close'].ewm(span=ema_period, adjust=False).mean()
    
    if condition == 'above':
        condition_series = data['close'] >= data[ema_column] * (1 - tolerance)
    elif condition == 'below':
        condition_series = data['close'] <= data[ema_column] * (1 + tolerance)
    else:
        raise ValueError("condition 参数必须为 'above' 或 'below'")

    recent_conditions = condition_series.tail(timeframe)
    rolling_sum = recent_conditions.rolling(window=consecutive).sum()
    condition_met_indices = rolling_sum[rolling_sum == consecutive].index

    periods = []
    processed_indices = set()

    for end_time in condition_met_indices:
        if end_time in processed_indices:
            continue

        end_pos = recent_conditions.index.get_loc(end_time)
        start_pos = end_pos - consecutive + 1
        start_time = recent_conditions.index[start_pos]

        while end_pos + 1 < len(recent_conditions) and recent_conditions.iloc[end_pos + 1]:
            end_pos += 1
            end_time = recent_conditions.index[end_pos]
            processed_indices.add(end_time)

        period = {'start_time': start_time, 'end_time': end_time, 'length': end_pos - start_pos + 1}
        periods.append(period)

        for idx in range(start_pos, end_pos + 1):
            processed_indices.add(recent_conditions.index[idx])

    return periods

# def fetch_and_resample_data(ticker, start_date, end_date, freq=None):
#     """
#     获取股票数据并按指定频率重新采样。

#     参数：
#     - ticker (str): 股票代码，例如 'AAPL'
#     - start_date (str): 开始日期，例如 '2020-01-01'
#     - end_date (str): 结束日期，例如 '2023-12-31'
#     - freq (str, optional): 数据频率，例如 '1d'、'1h'、'15min'

#     返回：
#     - pd.DataFrame: 数据集
#     """
#     # 下载历史数据
#     df = yf.download(ticker, start=start_date, end=end_date, interval=freq if freq else '1d')
    
#     # 将列名转换为小写，以匹配函数中的 'close'
#     df.columns = [col.lower() for col in df.columns]
#     return df

# # 示例使用
# if __name__ == "__main__":
#     # 定义股票代码和时间范围
#     ticker = 'AAPL'
#     start_date = '2023-01-01'
#     end_date = '2023-12-31'
#     freq = '1h'  # 1小时数据
    
#     # 获取数据
#     data = fetch_and_resample_data(ticker, start_date, end_date, freq)
    
#     # 确保数据按时间排序
#     data = data.sort_index()
    
#     # 应用函数，找到所有满足条件的时间区间
#     periods = find_all_consecutive_ema_periods(
#         data, 
#         ema_period=10, 
#         timeframe=500, 
#         consecutive=20, 
#         condition='above',
#         tolerance=0.002  # 0.2% 误差范围
#     )
    
#     # 输出结果
#     if periods:
#         print(f"共找到 {len(periods)} 个满足条件的时间区间：")
#         for idx, period in enumerate(periods, 1):
#             print(f"第 {idx} 个区间：开始时间 {period['start_time']}, 结束时间 {period['end_time']}")
#     else:
#         print("没有找到满足条件的时间区间。")
    
#     # 可视化示例
#     plt.figure(figsize=(14,7))
#     plt.plot(data['close'], label='Close Price', alpha=0.5)
#     plt.plot(data[f'ema_{10}'], label='EMA10', alpha=0.9)
    
#     # 标记满足条件的区域
#     for period in periods:
#         plt.axvspan(period['start_time'], period['end_time'], color='green', alpha=0.3)
    
#     plt.title(f'{ticker} Price with EMA Periods')
#     plt.xlabel('Date')
#     plt.ylabel('Price')
#     plt.legend()
#     plt.show()
