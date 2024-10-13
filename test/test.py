


from indicators.ema  import check_consecutive_ema
from data.data_fetcher import DataFetcher

# 过滤出5分钟最近200根k曾表现出强势的标的
def test1():
    dataf = DataFetcher()
    data =  dataf.fetch_redis_data('apt')
    result =  check_consecutive_ema(data,timeframe=1000)
    print(result)
test1()



