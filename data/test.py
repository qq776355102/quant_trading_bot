def convert_pair(pair):
    base_currency = pair.split('/')[0].lower()
    return base_currency + 'usdt'

# 示例输入
input_pair = "BTC"
output = convert_pair(input_pair)
print(output)  # 输出: btcusdt
