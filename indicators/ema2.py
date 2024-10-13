import pandas as pd
import numpy as np

def check_consecutive_ema(data, ema_period=10, timeframe=50, consecutive=20, condition='above', tolerance=0.002):
    """
    检查在指定时间框架内是否存在连续满足条件的K线，并返回相应的时间范围。

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
    
    # 查找是否存在 'consecutive' 个连续满足条件的K线
    count = 0
    for i in range(len(recent_conditions)-1, -1, -1):
        if recent_conditions.iloc[i]:
            count += 1
            if count >= consecutive:
                # 计算开始时间
                end_time = recent_conditions.index[i]
                start_index = i - consecutive + 1
                start_time = recent_conditions.index[start_index]
                # 返回True和满足条件的开始时间和结束时间
                return True, end_time, start_time
        else:
            count = 0
    
    return False, None, None
