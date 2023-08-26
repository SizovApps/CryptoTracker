class TokenStats:
    def __init__(self, token, sum_in, sum_out, profit_in_percent, profit_in_ETH, profit_in_dollars, dollars_lost):
        self.token = token
        self.sum_in = float(sum_in)
        self.sum_out = sum_out
        self.profit_in_percent = profit_in_percent
        self.profit_in_ETH = profit_in_ETH
        self.profit_in_dollars = profit_in_dollars
        self.dollars_lost = dollars_lost

    def __str__(self):
        return f"{self.token};{self.sum_in};{self.sum_out};{self.profit_in_percent};{self.profit_in_ETH};{self.profit_in_dollars};{self.dollars_lost}"

    def to_row(self):
        return [self.token, self.sum_in, self.sum_out, self.profit_in_percent, self.profit_in_ETH, self.profit_in_dollars, self.dollars_lost]
