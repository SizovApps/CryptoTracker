from requests import get
from datetime import datetime

from model.BuyerTransactions import BuyerTransactions
from model.Wallet import BLOCKED_TOKENS
from model.TransactionErc20 import *
from services.transactions_service import get_erc_20_transactions_by_token
from services.api_service import make_api_url, get_addresses_bought_token_api, get_erc_20_transaction_api
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18

MIN_AMOUNT_OF_TRANSACTIONS = 10
MAX_AMOUNT_OF_TRANSACTIONS = 50
AMOUNT_OF_FIRST_ADDRESSES = 100


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
        transactions.append(BuyerTransactions(buyer, get_erc_20_transactions_by_token(data, start_time, end_time, address, buyer)))
    return transactions


def get_first_addresses(address, startTime=None):
    transaction_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000,
                                   sort='asc')
    response = get(transaction_url)
    data = response.json()["result"]

    index = 0
    while startTime is not None and index < len(data):
        time = datetime.fromtimestamp(int(data[index]["timeStamp"]))
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
    erc_20_transaction_url = make_api_url("account", "tokentx", address, startblock=0, endblock=99999999)
    response = get(erc_20_transaction_url)
    data = response.json()["result"]
    data = reversed(data)
    count_of_transactions = 0
    count = 0
    for tx in data:
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        if time < stop_time:
            break
        if count >= MAX_AMOUNT_OF_TRANSACTIONS:
            break
        token_name = tx["tokenName"]
        if token_name in BLOCKED_TOKENS:
            continue
        count += 1
        hash = tx["hash"]
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
        count_of_transactions += 1

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
