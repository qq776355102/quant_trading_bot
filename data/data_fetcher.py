

import json
import redis
import pandas as pd
from pandas.tseries.offsets import DateOffset

# from  redis_client  import RedisClient
# 交易对列表

# from datetime import datetime, timedelta


# Redis连接
# redis_client = RedisClient()

   

import ccxt  # 用于与交易所交互

from config.settings import REDIS_HOST, REDIS_PORT, DEFAULT_SYMBOL

class DataFetcher:
    def __init__(self):
        # 初始化Redis客户端
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        
        # 初始化币安交易所
        self.binance = ccxt.binance({
            'enableRateLimit': True,
        })




    def fetch_historical_data(self, symbol=DEFAULT_SYMBOL, timeframe='1d', limit=500):
        """
        从币安获取历史数据
        :param symbol: 交易对
        :param timeframe: 时间周期
        :param limit: 数据条数
        :return: 历史数据
        """
        ohlcv = self.binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        return ohlcv
    
    def convert_pair(self, pair):
        base_currency = pair.split('/')[0].lower()
        return base_currency + 'usdt'

    
    # def fetch_redis_data(self, trading_pair):
    #     """
    #     从Redis获取数据
    #     :param key: 数据键
    #     :return: 数据值
    #     """
    #     """
    # 从Redis获取数据
    # :param trading_pair: 交易对
    # :return: 数据值
    # """
    #     redis_key = self.convert_pair(trading_pair)

    #     # 获取 Redis 数据
    #     existing_data = self.redis_client.hgetall(redis_key)
    #     if not existing_data:
    #         print(f"No result found for redis_key: {redis_key}")
    #         return
        
    #     # 解析 Redis 数据为字典，并创建 DataFrame
    #     existing_data = {key.decode(): json.loads(value.decode()) for key, value in existing_data.items()}
    #     df = pd.DataFrame(existing_data).T  # 转置以使 key 成为 index

    #     # 转换列数据类型为数值型，确保 'close' 列是浮点数
    #     df['close'] = pd.to_numeric(df['close'], errors='coerce')

    #     # 处理 datetime 列并设置为 index，确保排序正确
    #     df['datetime'] = pd.to_datetime(df['datetime'], unit='ms') + DateOffset(hours=8)
    #     df.set_index('datetime', inplace=True)
    #     df.sort_index(inplace=True)  # 进行升序排序

    #     return df

    def fetch_redis_data(self, trading_pair, freq='5min', start_time=None, end_time=None):
        """
            从Redis获取数据，支持重塑时间级别和时间范围过滤
            :param trading_pair: 交易对
            :param freq: 重新采样的时间级别，默认为5分钟 ('5T')，可以设置为'15T'等
            :param start_time: 开始时间，默认为None表示不限制
            :param end_time: 结束时间，默认为None表示到当前时间
            :return: 数据值的DataFrame
        """
        redis_key = self.convert_pair(trading_pair)

        # 获取 Redis 数据
        existing_data = self.redis_client.hgetall(redis_key)
        if not existing_data:
            print(f"No result found for redis_key: {redis_key}")
            return
        
        # 解析 Redis 数据为字典，并创建 DataFrame
        existing_data = {key.decode(): json.loads(value.decode()) for key, value in existing_data.items()}
        df = pd.DataFrame(existing_data).T  # 转置以使 key 成为 index

        # 转换列数据类型为数值型，确保 'close' 列是浮点数
        df['close'] = pd.to_numeric(df['close'], errors='coerce')

        # 处理 datetime 列并设置为 index，确保排序正确
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms') + DateOffset(hours=8)
        df.set_index('datetime', inplace=True)
        df.sort_index(inplace=True)  # 进行升序排序

            # 设置时间范围过滤，默认返回从start_time到end_time的数据
        if start_time:
            start_time = pd.to_datetime(start_time)
        else:
            start_time = df.index.min()

        if end_time:
            end_time = pd.to_datetime(end_time)
        else:
            end_time = pd.Timestamp.now()

        df = df[(df.index >= start_time) & (df.index <= end_time)]

        # 按照用户需求重新采样数据（如15分钟数据）
        if freq:
            df_resampled = df.resample(freq).agg({
                'open': 'first',  # 每个时间段的第一个值
                'high': 'max',    # 每个时间段的最大值
                'low': 'min',     # 每个时间段的最小值
                'close': 'last',  # 每个时间段的最后一个值
                'volume': 'sum'   # 每个时间段的交易量总和
            }).dropna()  # 删除空值

        return df_resampled


        

    def save_to_redis(self, key, value):
        """
        将数据保存到Redis
        :param key: 数据键
        :param value: 数据值
        """
        # TO-DO
        # self.redis_client.set(key, value)
        return


# dataf = DataFetcher()
# data =  dataf.fetch_redis_data('apt')
# print(data)