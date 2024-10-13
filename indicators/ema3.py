import pandas as pd
import numpy as np
def check_consecutive_ema_vectorized(data, ema_period=10, timeframe=50, consecutive=20, condition='above', tolerance=0.002):
    """
    向量化方法：检查在指定时间框架内是否存在连续满足条件的K线，并返回相应的时间范围。

    参数：
    - data (pd.DataFrame): 包含至少 'close' 列的DataFrame。
    - ema_period (int): 计算EMA的周期。
    - timeframe (int): 检查的时间框架（最近多少根K线）。
    - consecutive (int): 需要连续满足条件的K线数量。
    - condition (str): 条件类型，'above' 表示收盘价高于EMA，'below' 表示收盘价低于EMA。
    - tolerance (float): 收盘价与EMA的允许误差范围（默认为0.002，即0.2%）。

    返回：
    - bool: 如果存在满足条件的连续K线，返回True，否则返回False。
    - pd.Timestamp or None: 满足条件的连续K线的结束时间。
    - pd.Timestamp or None: 满足条件的连续K线的开始时间。
    """
    # 计算EMA
    ema_column = f'EMA_{ema_period}'
    data[ema_column] = data['close'].ewm(span=ema_period, adjust=False).mean()
    
    # 确定条件
    if condition == 'above':
        # 收盘价 >= EMA * (1 - tolerance)
        condition_series = data['close'] >= data[ema_column] * (1 - tolerance)
    elif condition == 'below':
        # 收盘价 <= EMA * (1 + tolerance)
        condition_series = data['close'] <= data[ema_column] * (1 + tolerance)
    else:
        raise ValueError("condition 参数必须为 'above' 或 'below'")
    
    # 取最近 'timeframe' 根K线
    recent_conditions = condition_series.tail(timeframe)
    
    # 使用滚动窗口检查是否有连续 'consecutive' 个True
    rolling_sum = recent_conditions.rolling(window=consecutive).sum()
    
    # 条件满足的窗口
    condition_met = rolling_sum == consecutive
    
    if condition_met.any():
        # 获取第一个满足条件的窗口的结束位置
        end_pos = condition_met.idxmax()
        end_time = end_pos
        # 计算开始时间
        # 获取频率信息
        freq = data.index.freq
        if freq is None:
            # 如果频率信息缺失，尝试推断
            freq = data.index.inferred_freq
        if freq is None:
            # 如果无法推断，使用最近两个时间点的差值作为频率
            if len(data.index) >= 2:
                freq_delta = data.index[-1] - data.index[-2]
            else:
                freq_delta = pd.Timedelta(minutes=15)  # 默认15分钟
        else:
            freq_delta = pd.to_timedelta(freq)
        # 计算开始时间
        start_time = end_time - pd.Timedelta(minutes=(consecutive-1)*freq_delta.total_seconds()/60)
        return True, end_time, start_time
    else:
        return False, None, None
