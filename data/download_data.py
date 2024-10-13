import requests
from redis_client import RedisClient
import json
import time
from datetime import datetime, timedelta

def fetch_and_store_trading_data(trading_pair, start_time, end_time, redis_key, available_url, redis_client):
    api_url = f"{available_url}/api/v3/klines"
    limit = 1000
    interval = '5m'  # 可以根据需要调整时间间隔

    while start_time < end_time:
        params = {
            'symbol': trading_pair.upper(),
            'interval': interval,
            'startTime': int(start_time.timestamp() * 1000),
            'endTime': int(end_time.timestamp() * 1000),
            'limit': limit,
        }

        response = requests.get(api_url, params=params)
        klines = response.json()
        print(print)

        if not klines:
            # 如果没有获取到更多数据，说明已经抓取完毕
            break

        for kline in klines:
            timestamp = int(kline[0])
            open_price = float(kline[1])
            high_price = float(kline[2])
            low_price = float(kline[3])
            close_price = float(kline[4])
            volume = float(kline[5])

            new_data = {
                'datetime': timestamp,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume
            }

            # 将数据插入或更新到Redis
            redis_client.hset(redis_key, timestamp, json.dumps(new_data))

        # 更新 start_time，避免重复抓取相同的数据，时间间隔取最后一个K线的时间
        start_time = datetime.utcfromtimestamp(klines[-1][0] / 1000) + timedelta(minutes=1)
        time.sleep(1)  # 避免过多请求触发API限流

# 使用例子
def main():
    redis_url = 'redis://localhost'
    available_url = 'https://api.binance.com'
    trading_pair = 'APTUSDT'
    redis_key = f"trading_data:{trading_pair}"

    # Redis客户端初始化
    redis_client = RedisClient()

    # 指定的开始时间和结束时间
    start_time = datetime(2024, 12, 12)
    end_time = datetime.now()  # 使用当前时间

    print(f"start_time:{start_time} end_time:{end_time}")
    # 下载并存储数据
    fetch_and_store_trading_data(trading_pair, start_time, end_time, redis_key, available_url, redis_client)

    # # 关闭Redis连接
    # redis_client.close()

# 同步运行 main 函数
if __name__ == '__main__':
    main()
