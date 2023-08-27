import stats.prices
from model.TokenProfit import TokenProfit
from model.TokenStats import TokenStats
from services.MoralisService import MoralisService
from services.WriterService import WriterService


class Wallet:
    BNB_PRICE = stats.prices.BNB_PRICE
    ETH_PRICE = stats.prices.ETH_PRICE

    def __init__(self, address, balance=0):
        self.address = address
        self.balance = balance
        self.erc20_transactions = dict()
        self.internal_transactions = dict()
        self.tokens = dict()
        self.max_tokens = dict()
        self.token_contracts = dict()
        self.count_of_profit = 0
        self.count_of_loss = 0

        self.profit_in_dollar = 0
        self.profit_in_ETH = 0
        self.full_enter = 0
        self.full_exit = 0
        self.win_rate = 0
        self.pnl = 0

    def __str__(self):
        return self.address

    def set_erc20_transactions(self, erc20_transactions):
        self.erc20_transactions = erc20_transactions

    def add_internal_transaction(self, token_name, internal_transaction):
        if token_name not in self.internal_transactions:
            self.internal_transactions[token_name] = []
        self.internal_transactions[token_name].append(internal_transaction)
        self.add_tokens(token_name, internal_transaction)

    def add_tokens(self, token_name, internal_transaction):
        self.token_contracts[token_name] = internal_transaction.contract_address
        if token_name in self.tokens:
            if internal_transaction.internal_transaction_value < 0:
                self.tokens[token_name] += internal_transaction.quantity_of_token
            else:
                self.tokens[token_name] -= internal_transaction.quantity_of_token
            if self.tokens[token_name] > self.max_tokens[token_name]:
                self.max_tokens[token_name] = internal_transaction.quantity_of_token
        else:
            if internal_transaction.internal_transaction_value < 0:
                self.tokens[token_name] = internal_transaction.quantity_of_token
            else:
                self.tokens[token_name] = -internal_transaction.quantity_of_token
            self.max_tokens[token_name] = internal_transaction.quantity_of_token

    def count_profit(self):
        if len(self.erc20_transactions.keys()) == 0:
            return
        tokens = []
        for token_name in self.internal_transactions:
            token_profit = self.get_sum_by_token(token_name)
            price_of_lost_tokens_in_dollars = self.tokens[token_name] * MoralisService.get_current_price(self.token_contracts[token_name])
            if self.tokens[token_name] < 0:
                price_of_lost_tokens_in_dollars = 0
            token_profit.sum_of_profit += price_of_lost_tokens_in_dollars / self.ETH_PRICE
            token_profit.sum_out += price_of_lost_tokens_in_dollars / self.ETH_PRICE
            if token_profit.sum_in == 0:
                continue
            if self.max_tokens[token_name] == 0:
                continue

            tokens.append(TokenStats(
                token=token_name,
                sum_in=token_profit.sum_in,
                sum_out=token_profit.sum_out,
                profit_in_percent=token_profit.profit_in_percent,
                profit_in_ETH=token_profit.sum_out - token_profit.sum_in,
                profit_in_dollars=(token_profit.sum_out - token_profit.sum_in) * self.ETH_PRICE,
                dollars_lost=price_of_lost_tokens_in_dollars
            ))
            self.profit_in_ETH += token_profit.sum_in
            self.profit_in_ETH += token_profit.sum_out
            self.full_enter += token_profit.sum_in
            self.full_exit += token_profit.sum_out

            if token_profit.sum_of_profit > 0:
                self.count_of_profit += 1
            else:
                self.count_of_loss += 1
        self.profit_in_dollar = self.profit_in_ETH * self.ETH_PRICE
        if self.count_of_profit + self.count_of_loss == 0:
            self.win_rate = 0
        else:
            self.win_rate = self.count_of_profit / (self.count_of_profit + self.count_of_loss) * 100
        if self.full_exit == 0:
            self.pnl = 0
        else:
            self.pnl = (self.full_exit / self.full_enter) * 100

        WriterService.write_full_stats(self.address, self.profit_in_dollar, self.profit_in_ETH, self.full_enter, self.full_exit,
                         self.count_of_profit, self.count_of_loss, tokens)

    def get_sum_by_token(self, token_name):
        sum_of_profit = 0
        sum_in = 0
        sum_out = 0
        for internal_transaction in self.internal_transactions[token_name]:
            sum_of_profit += internal_transaction.internal_transaction_value
            if internal_transaction.internal_transaction_value < 0:
                sum_in += internal_transaction.internal_transaction_value
            else:
                sum_out += internal_transaction.internal_transaction_value
        profit_in_percent = 0
        if sum_in != 0:
            profit_in_percent = sum_out / abs(sum_in)
        return TokenProfit(
            sum_of_profit=sum_of_profit,
            sum_in=abs(sum_in),
            sum_out=sum_out,
            profit_in_percent=profit_in_percent
        )
