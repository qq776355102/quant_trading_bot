class RiskAnalysis:
    def __init__(self, data):
        self.data = data

    def max_drawdown(self):
        self.data['drawdown'] = (self.data['close'] / self.data['close'].cummax()) - 1
        return self.data['drawdown'].min()

    def position_size(self, account_balance, risk_per_trade):
        return account_balance * risk_per_trade

    def analyze_risk(self, account_balance, risk_per_trade):
        max_dd = self.max_drawdown()
        position_size = self.position_size(account_balance, risk_per_trade)
        return max_dd, position_size
