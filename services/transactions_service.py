from datetime import datetime
from requests import get
from model.TransactionErc20 import TransactionErc20
from services.api_service import make_api_url, get_internal_transactions_api

NO_DEFINED_VALUE = 100000000000
ETHER_VALUE = 10 ** 18


def get_addresses_bought_token(address):
    transaction_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000,
                                   sort='desc')
    response = get(transaction_url)
    data = response.json()["result"]
    address_bought_token = [tx["from"] for tx in data]


def get_erc_20_transactions_by_token(data, start_time, end_time, token_address, buyer_address):
    all_transactions = dict()
    erc20_transactions = dict()
    tokens_transactions = dict()
    count_of_transactions = 0
    count = 0
    for tx in data:
        if tx["contractAddress"] != token_address:
            continue
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        if start_time != None and time < start_time:
            continue
        token_name = tx["tokenName"]
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
        if from_address.lower() == buyer_address.lower():
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
    data = get_internal_transactions_api(transaction)
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


def set_internal_transactions(wallet):
    for key in wallet.erc20_transactions.keys():
        for transaction in wallet.erc20_transactions[key]:
            new_value = get_internal_transaction(transaction)
            if NO_DEFINED_VALUE != new_value:
                transaction.set_internal_transaction_value(new_value)
                wallet.add_internal_transaction(key, transaction)