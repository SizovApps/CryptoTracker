import os

from dotenv import load_dotenv
from requests import get

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.etherscan.io/api"


class ApiService:
    @staticmethod
    def make_api_url(module, action, address, **kwargs):
        url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"
        for key, value in kwargs.items():
            url += f"&{key}={value}"
        return url

    @staticmethod
    def get_erc_20_transaction_api(address):
        erc_20_transaction_url = ApiService.make_api_url("account", "tokentx", address, startblock=0, endblock=99999999,
                                              sort='desc')
        response = get(erc_20_transaction_url)
        try:
            return response.json()["result"]
        except:
            print(response)
            return None

    @staticmethod
    def get_addresses_bought_token_api(address):
        transaction_url = ApiService.make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1,
                                                  offset=10000,
                                                  sort='asc')
        response = get(transaction_url)
        return response.json()["result"]

    @staticmethod
    def get_addresses_bought_token_desc_api(address):
        transaction_url = ApiService.make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1,
                                                  offset=10000,
                                                  sort='desc')
        response = get(transaction_url)
        return response.json()["result"]

    @staticmethod
    def get_internal_transactions_api(transaction):
        internal_transaction_url = BASE_URL + f"?module=account&action=txlistinternal&txhash={transaction.tx_hash}&apikey={API_KEY}"
        response = get(internal_transaction_url)
        return response.json()["result"]

    @staticmethod
    def get_receipt(tx_hash):
        receipt_url = BASE_URL + f"?module=proxy&action=eth_getTransactionReceipt&txhash={tx_hash}&apikey={API_KEY}"
        response = get(receipt_url)
        try:
            return response.json()["result"]
        except:
            print(response)
            return None

