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
    def get_addresses_bought_token_api(token_pair_address, start_block, end_block):
        erc_20_transaction_url = ApiService.make_api_url("account", "tokentx", token_pair_address, startblock=start_block, endblock=end_block, offset=10000,
                                                         sort='asc')
        response = get(erc_20_transaction_url)
        return response.json()["result"]

    @staticmethod
    def get_addresses_bought_token_desc_api(address):
        transaction_url = ApiService.make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1,
                                                  offset=10000,
                                                  sort='desc')
        response = get(transaction_url)
        return response.json()["result"]

    @staticmethod
    def get_internal_transactions_api(tx_hash):
        internal_transaction_url = BASE_URL + f"?module=account&action=txlistinternal&txhash={tx_hash}&apikey={API_KEY}"
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

    @staticmethod
    def get_token_abi(token_address):
        get_abi_url = BASE_URL + f"?module=contract&action=getabi&address={token_address}&apikey={API_KEY}"
        response = get(get_abi_url)
        return response.json()["result"]

# print(ApiService.get_erc_20_transaction_api("0xeaf24c54d3d531c0cc9130a500170e9c77fdc1b3"))
# print(ApiService.get_addresses_bought_token_api("0xa57ed6e54be8125bbe45d6ca330e45ebb71ef11e")[-1])
# print(ApiService.get_receipt("0x89d724b54343d1b17943d6daffe41365cbc93beb2a98a7a614d519a51b04d0ea"))
# print(ApiService.get_addresses_bought_token_api("0x0a86421ee3a48fa6a2e1b7775860b39d96e1453a", 18182182, 18182501))