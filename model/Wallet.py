import csv

from model.TokenStats import TokenStats
from moralis_info import get_current_price
import openpyxl

from writer import write_full_stats

BLOCKED_TOKENS = ["Binance-Peg BSC-USD", "Binance-Peg Dogecoin Token", "Binance-Peg BUSD Token", "Factr", "XEN Crypto"]


class Wallet:
    BNB_PRICE = 305
    ETH_PRICE = 1788

    def __init__(self, address):
        self.address = address
        self.erc20_transactions = dict()
        self.internal_transactions = dict()
        self.profit = dict()
        self.tokens = dict()
        self.max_tokens = dict()
        self.token_contracts = dict()
        self.count_of_profit = 0
        self.count_of_loss = 0

        self.profit_in_ETH = 0
        self.profit_in_dollar = 0
        self.full_enter = 0
        self.full_exit = 0
        self.win_rate = 0
        self.pnl = 0

    def __str__(self):
        return self.address

    def set_erc20_transactions(self, erc20_transactions):
        self.erc20_transactions = erc20_transactions

    def add_internal_transaction(self, token_name, internal_transaction):
        if token_name in BLOCKED_TOKENS:
            return
        if token_name in self.internal_transactions.keys():
            self.internal_transactions[token_name].append(internal_transaction)
            self.add_tokens(token_name, internal_transaction)
        else:
            self.internal_transactions[token_name] = [internal_transaction]
            self.add_tokens(token_name, internal_transaction)

    def add_tokens(self, token_name, internal_transaction):
        self.token_contracts[token_name] = internal_transaction.contract_address
        if token_name in self.tokens.keys():
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
            return False, [0, self.address], [0, self.address]
        full_profit = 0
        full_enter = 0
        full_exit = 0

        tokens = []
        for token_name in self.internal_transactions:
            sum_of_profit, sum_in, sum_out = self.get_sum_by_token(token_name)
            token_lost = self.tokens[token_name] * get_current_price(self.token_contracts[token_name], 'eth')
            if self.tokens[token_name] < 0:
                token_lost = 0
            sum_of_profit += token_lost / self.ETH_PRICE
            sum_out += token_lost / self.ETH_PRICE
            if sum_in == 0:
                continue
            if self.max_tokens[token_name] == 0:
                continue
            # if self.tokens[token_name] / self.max_tokens[token_name] > 0.25:
            #     continue
            self.profit[token_name] = [sum_of_profit, abs(sum_in), sum_out, sum_out / abs(sum_in)]
            tokens.append(TokenStats(token_name, float(self.profit[token_name][1]), self.profit[token_name][2],
                                     self.profit[token_name][3],
                                     sum_out - abs(sum_in), (sum_out - abs(sum_in)) * self.ETH_PRICE, token_lost))
            full_profit += sum_in
            full_profit += sum_out
            full_enter += abs(sum_in)
            full_exit += sum_out

            if sum_of_profit > 0:
                self.count_of_profit += 1
            else:
                self.count_of_loss += 1

        print()

        print("Wallet: ", self.address)
        print("Итого в долларах:", full_profit * self.ETH_PRICE)
        print("Итого в альткоине:", full_profit)
        print("Итого вход:", full_enter)
        print("Итого выход:", full_exit)
        print("Количество успешных:", self.count_of_profit)
        print("Количество неуспешных:", self.count_of_loss)

        self.profit_in_ETH = full_profit * self.ETH_PRICE
        self.profit = full_profit
        self.full_enter = full_enter
        self.full_exit = full_exit
        if self.count_of_profit + self.count_of_loss == 0:
            self.win_rate = 0
        else:
            self.win_rate = self.count_of_profit / (self.count_of_profit + self.count_of_loss) * 100
        if full_exit == 0:
            self.pnl = 0
        else:
            self.pnl = (full_exit / full_enter) * 100

        write_full_stats(self.address, self.profit_in_ETH, self.profit, self.full_enter, self.full_exit,
                         self.count_of_profit, self.count_of_loss, tokens)

        if self.count_of_profit + self.count_of_loss == 0:
            return False, [0, self.address], [0, self.address]
        if full_exit / 3 > full_enter:
            return True, [full_profit * self.ETH_PRICE, self.address], [
                self.count_of_profit / (self.count_of_profit + self.count_of_loss), self.address]
        return False, [0, self.address], [0, self.address]

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
        return sum_of_profit, sum_in, sum_out
