import os
from datetime import datetime
from enum import Enum

from dotenv import load_dotenv
from requests import get

from model.BuyerTransactions import BuyerTransactions
from model.TransactionErc20 import *
from model.Wallet import BLOCKED_TOKENS
from services.api_service import make_api_url, get_addresses_bought_token_api, get_erc_20_transaction_api
from services.transactions_service import get_erc_20_transactions_by_token

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18

MIN_AMOUNT_OF_TRANSACTIONS = 10
MAX_AMOUNT_OF_TRANSACTIONS = 50
AMOUNT_OF_FIRST_ADDRESSES = 100


class HandleStatus(Enum):
    CHECK = 1
    CONTINUE = 2
    BREAK = 3


class EthTracker:
    HASH_FIELD = "hash"
    TOKEN_NAME_FIELD = "tokenName"
    TIME_STAMP_FIELD = "timeStamp"
    FROM_FIELD = "from"
    TO_FIELD = "to"
    VALUE_FIELD = "value"
    GAS_PRICE_FIELD = "gasPrice"
    GAS_USED_FIELD = "gasUsed"
    CONTRACT_ADDRESS_FIELD = "contractAddress"

    @staticmethod
    def get_account_balance(address):
        balance_url = make_api_url("account", "balance", address, tag="latest")
        response = get(balance_url)
        data = response.json()
        value = int(data["result"]) / ETHER_VALUE
        return value

    @staticmethod
    def get_erc_20_transactions(address, stop_time):
        all_transactions = set()
        erc20_transactions = dict()
        tokens_transactions = dict()

        data = get_erc_20_transaction_api(address)
        count_of_transactions = 0
        for tx in data:
            tx_hash = tx[EthTracker.HASH_FIELD]
            token_name = tx[EthTracker.TOKEN_NAME_FIELD]
            handle_status = EthTracker.should_handle_transaction(tx, tx_hash, token_name, all_transactions,
                                                                 count_of_transactions, stop_time)
            if handle_status == HandleStatus.BREAK:
                break
            if handle_status == HandleStatus.CONTINUE:
                continue
            count_of_transactions += 1
            all_transactions.add(tx_hash)

            if token_name not in erc20_transactions:
                erc20_transactions[token_name] = []
            erc20_transactions[token_name].append(EthTracker.make_erc_20_transaction(tx, address,
                                                                                     tokens_transactions))

        return erc20_transactions

    @staticmethod
    def make_erc_20_transaction(tx_data, address, tokens_transactions):
        time = datetime.fromtimestamp(int(tx_data[EthTracker.TIME_STAMP_FIELD]))
        token_name = tx_data[EthTracker.TOKEN_NAME_FIELD]
        tx_hash = tx_data[EthTracker.HASH_FIELD]
        from_address = tx_data[EthTracker.FROM_FIELD]
        to_address = tx_data[EthTracker.TO_FIELD]
        amount_of_tokens = tx_data[EthTracker.VALUE_FIELD]
        gas_price = tx_data[EthTracker.GAS_PRICE_FIELD]
        gas_used = tx_data[EthTracker.GAS_USED_FIELD]
        gas_value = int(gas_price) * int(gas_used) / 10 ** 18
        contract_address = tx_data[EthTracker.CONTRACT_ADDRESS_FIELD]
        is_from = False

        print(from_address)
        print(address)
        if from_address.lower() == address.lower():
            is_from = True

        if token_name not in tokens_transactions:
            tokens_transactions[token_name] = []

        token_hashes = tokens_transactions[token_name]
        token_hashes.append([tx_hash, is_from, gas_value])
        return TransactionErc20(token_name, tx_hash, time, from_address, to_address, amount_of_tokens,
                                gas_value, is_from, tx_data, contract_address)

    @staticmethod
    def should_handle_transaction(tx, tx_hash, token_name, all_transactions, count_of_transactions, stop_time):
        if tx_hash in all_transactions:
            return HandleStatus.CONTINUE

        if count_of_transactions >= MAX_AMOUNT_OF_TRANSACTIONS:
            return HandleStatus.BREAK

        if datetime.fromtimestamp(int(tx[EthTracker.TIME_STAMP_FIELD])) < stop_time:
            return HandleStatus.BREAK

        if count_of_transactions >= MAX_AMOUNT_OF_TRANSACTIONS:
            return HandleStatus.BREAK

        if token_name in BLOCKED_TOKENS:
            return HandleStatus.CONTINUE

        if token_name in BLOCKED_TOKENS:
            return HandleStatus.CONTINUE

        return HandleStatus.CHECK


def get_account_balance(address):
    balance_url = make_api_url("account", "balance", address, tag="latest")
    response = get(balance_url)
    data = response.json()
    value = int(data["result"]) / ETHER_VALUE
    return value


def get_transaction_of_token(address, start_time=None, end_time=None):
    data = get_addresses_bought_token_api(address)
    address_bought_token = [tx["from"] for tx in data]
    print(f"Количество транзакций: {len(data)}.")
    transactions = []
    count = 0
    for buyer in address_bought_token:
        if count > 700:
            break
        count += 1
        data = get_erc_20_transaction_api(buyer)
        print(buyer)
        transactions.append(
            BuyerTransactions(buyer, get_erc_20_transactions_by_token(data, start_time, end_time, address, buyer)))
    return transactions


def get_first_addresses(address, startTime=None):
    transaction_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000,
                                   sort='asc')
    response = get(transaction_url)
    data = response.json()["result"]

    index = 0
    while startTime is not None and index < len(data):
        time = datetime.fromtimestamp(int(data[index][EthTracker.TIME_STAMP_FIELD]))
        if time < startTime:
            index += 1
            continue
        else:
            break

    first_addresses = []
    counter = 0
    while index < len(data):
        if counter > AMOUNT_OF_FIRST_ADDRESSES:
            return first_addresses
        from_addr = data[index]["from"]
        first_addresses.append(from_addr)
        counter += 1
        index += 1
    return first_addresses
    # print(balances)


def get_erc_20_transactions(address, stop_time):
    all_transactions = dict()
    erc20_transactions = dict()
    tokens_transactions = dict()

    data = get_erc_20_transaction_api(address)
    data = reversed(data)
    count = 0
    for tx in data:
        time = datetime.fromtimestamp(int(tx[EthTracker.TIME_STAMP_FIELD]))
        if time < stop_time:
            break
        if count >= MAX_AMOUNT_OF_TRANSACTIONS:
            break
        token_name = tx[EthTracker.TOKEN_NAME_FIELD]
        if token_name in BLOCKED_TOKENS:
            continue
        count += 1
        hash = tx[EthTracker.HASH_FIELD]
        if hash in all_transactions.keys():
            continue
        all_transactions[hash] = 1
        from_address = tx["from"]
        to_address = tx["to"]
        amount_of_tokens = tx["value"]
        gas_price = tx["gasPrice"]
        gas_used = tx["gasUsed"]
        gas_value = int(gas_price) * int(gas_used) / 10 ** 18
        contract_address = tx["contractAddress"]
        is_from = False
        if from_address.lower() == address.lower():
            is_from = True
        if token_name in tokens_transactions:
            token_hashes = tokens_transactions[token_name]
            token_hashes.append([hash, is_from, gas_value])
            erc20_transaction = TransactionErc20(token_name, hash, time, from_address, to_address, amount_of_tokens,
                                                 gas_value, is_from, tx, contract_address)
            erc20_transactions[token_name].append(erc20_transaction)
        else:
            tokens_transactions[token_name] = [[hash, is_from, gas_value]]
            erc20_transaction = TransactionErc20(token_name, hash, time, from_address, to_address, amount_of_tokens,
                                                 gas_value, is_from, tx, contract_address)
            erc20_transactions[token_name] = [erc20_transaction]

    return erc20_transactions


def get_internal_transaction(transaction):
    internal_transaction_url = BASE_URL + f"?module=account&action=txlistinternal&txhash={transaction.tx_hash}&apikey={API_KEY}"
    response = get(internal_transaction_url)
    data = response.json()["result"]
    if len(data) == 0:
        return 100000000000
    first_value = data[-1]["value"]
    value = 0
    if len(data) > 1 and first_value != data[-2]["value"]:
        for tx in data:
            value += int(tx["value"])
        value /= ETHER_VALUE
    else:
        value = int(data[-1]["value"]) / ETHER_VALUE
    if not transaction.is_from:
        value = -value
    if transaction.from_address == '0x0000000000000000000000000000000000000000':
        return 0
    value -= transaction.gas_value
    return value
