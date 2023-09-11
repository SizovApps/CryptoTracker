import os
from datetime import datetime
from enum import Enum

from dotenv import load_dotenv
from requests import get

from model.BuyerTransactions import BuyerTransactions
from model.TransactionErc20 import *
from services.ApiService import ApiService
from services.DexHandlerService import dexHandlerService
from services.transaction_log_readers.UniswapV2LogReader import UniswapV2LogReader
from services.transaction_log_readers.UniswapV3LogReader import UniswapV3LogReader

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18
ETH_ADDRESS = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

MIN_AMOUNT_OF_TRANSACTIONS = 10
MAX_AMOUNT_OF_TRANSACTIONS = 50
AMOUNT_OF_FIRST_ADDRESSES = 100


class HandleStatus(Enum):
    CHECK = 1
    CONTINUE = 2
    BREAK = 3


class EthTrackerService:
    HASH_FIELD = "hash"
    ADDRESS_FIELD = "contractAddress"
    TOKEN_NAME_FIELD = "tokenName"
    TIME_STAMP_FIELD = "timeStamp"
    FROM_FIELD = "from"
    TO_FIELD = "to"
    VALUE_FIELD = "value"
    GAS_PRICE_FIELD = "gasPrice"
    GAS_USED_FIELD = "gasUsed"
    CONTRACT_ADDRESS_FIELD = "contractAddress"
    LOGS_FIELD = "logs"
    LOG_DATA_FIELD = "data"
    LOG_TOPICS_FIELD = "topics"
    LOG_ADDRESS_FIELD = "address"

    @staticmethod
    def get_account_balance(address):
        balance_url = ApiService.make_api_url("account", "balance", address, tag="latest")
        response = get(balance_url)
        data = response.json()
        value = int(data["result"]) / ETHER_VALUE
        return value

    @staticmethod
    def get_erc_20_transactions(address, stop_time, swap_factory, searching_token=None):
        all_transactions = set()
        erc20_transactions = dict()
        tokens_transactions = dict()

        data = ApiService.get_erc_20_transaction_api(address)
        count_of_transactions = 0
        for tx in data:
            tx_hash = tx[EthTrackerService.HASH_FIELD]
            token_name = tx[EthTrackerService.TOKEN_NAME_FIELD]

            handle_status = EthTrackerService.should_handle_transaction(tx, tx_hash, token_name, all_transactions,
                                                                        count_of_transactions, stop_time, searching_token)
            if handle_status == HandleStatus.BREAK:
                break
            if handle_status == HandleStatus.CONTINUE:
                continue
            count_of_transactions += 1
            all_transactions.add(tx_hash)
            token_swapped = dexHandlerService.factory_handler(tx_hash, token_name)
            if token_name not in erc20_transactions:
                erc20_transactions[token_name] = []
            erc20_transactions[token_name].append(EthTrackerService.make_erc_20_transaction(tx, address,
                                                                                            tokens_transactions, token_swapped))

        return erc20_transactions

    @staticmethod
    def factory_handler(tx_hash, swap_factory):
        if swap_factory == "uniswapv3":
            return UniswapV3LogReader().get_swapped_tokens(tx_hash)
        return UniswapV2LogReader().get_swapped_tokens(tx_hash)

    @staticmethod
    def make_erc_20_transaction(tx_data, address, tokens_transactions, tokens_swapped):
        time = datetime.fromtimestamp(int(tx_data[EthTrackerService.TIME_STAMP_FIELD]))
        token_name = tx_data[EthTrackerService.TOKEN_NAME_FIELD]
        tx_hash = tx_data[EthTrackerService.HASH_FIELD]
        from_address = tx_data[EthTrackerService.FROM_FIELD]
        to_address = tx_data[EthTrackerService.TO_FIELD]
        gas_price = tx_data[EthTrackerService.GAS_PRICE_FIELD]
        gas_used = tx_data[EthTrackerService.GAS_USED_FIELD]
        gas_value = int(gas_price) * int(gas_used) / 10 ** 18
        contract_address = tx_data[EthTrackerService.CONTRACT_ADDRESS_FIELD]
        is_from = False

        if from_address.lower() == address.lower():
            is_from = True

        if token_name not in tokens_transactions:
            tokens_transactions[token_name] = []

        token_hashes = tokens_transactions[token_name]
        token_hashes.append([tx_hash, is_from, gas_value])
        return TransactionErc20(token_name, tx_hash, time, from_address, to_address, tokens_swapped.token_amount,
                                gas_value, is_from, tx_data, contract_address, tokens_swapped)

    @staticmethod
    def should_handle_transaction(tx, tx_hash, token_name, all_transactions, count_of_transactions, stop_time, searching_token):
        if tx_hash in all_transactions:
            return HandleStatus.CONTINUE

        if count_of_transactions >= MAX_AMOUNT_OF_TRANSACTIONS:
            return HandleStatus.BREAK

        if stop_time is not None and datetime.fromtimestamp(int(tx[EthTrackerService.TIME_STAMP_FIELD])) < stop_time:
            return HandleStatus.BREAK

        if count_of_transactions >= MAX_AMOUNT_OF_TRANSACTIONS:
            return HandleStatus.BREAK

        if searching_token is not None and token_name != searching_token:
            return HandleStatus.CONTINUE

        return HandleStatus.CHECK

    @staticmethod
    def get_transaction_of_token(address, token_name, max_transactions_to_check, swap_factory, start_time=None, end_time=None):
        data = ApiService.get_addresses_bought_token_api(address)
        address_bought_token = [tx["from"] for tx in data]
        address_bought_token = address_bought_token[:max_transactions_to_check]
        checked_addresses = set()
        print(f"Количество транзакций: {len(data)}.")
        transactions = []
        count = 0
        for buyer in address_bought_token:
            if buyer in checked_addresses:
                continue
            if count > AMOUNT_OF_FIRST_ADDRESSES:
                break
            checked_addresses.add(buyer)
            count += 1
            print(f"Пользователь купивший токен {buyer}")
            transactions.append(
                BuyerTransactions(buyer, EthTrackerService.get_erc_20_transactions(buyer, start_time, swap_factory, token_name)))
        return transactions

    @staticmethod
    def get_first_addresses(address, startTime=None):
        transaction_url = ApiService.make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1,
                                                  offset=10000,
                                                  sort='asc')
        response = get(transaction_url)
        data = response.json()["result"]

        index = 0
        while startTime is not None and index < len(data):
            time = datetime.fromtimestamp(int(data[index][EthTrackerService.TIME_STAMP_FIELD]))
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

    @staticmethod
    def get_addresses_bought_token(address):
        transaction_url = ApiService.make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1,
                                                  offset=10000,
                                                  sort='desc')
        response = get(transaction_url)
        data = response.json()["result"]
        return [tx["from"] for tx in data]

    @staticmethod
    def get_best_wallets_by_win_rate(wallets):
        wallets.sort(key=lambda x: x.win_rate, reverse=True)
        return wallets
