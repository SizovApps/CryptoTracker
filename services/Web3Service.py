import json
import os

from dotenv import load_dotenv
from web3 import Web3

from services.ApiService import ApiService
from static.stats import CHECKSUM_ETH_ADDRESS

load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")

web3 = Web3(Web3.HTTPProvider(INFURA_URL))

UNISWAP_V2_FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
UNISWAP_V3_FACTORY_ADDRESS = "0x1F98431c8aD98523631AE4a59f267346ea31F984"

NO_FACTORY_PAIR_ADDRESS = "0x0000000000000000000000000000000000000000"
NO_CONTRACT = "Contract source code not verified"

FACTORY_FEES = [100, 300, 500, 1000, 3000, 5000, 10000, 30000, 5000]

token_decimals = dict()


class Web3Service:

    @staticmethod
    def is_contract(address):
        address = web3.to_checksum_address(address)
        code = web3.eth.get_code(address)
        if code.hex() != '0x':
            return True
        return False

    @staticmethod
    def get_uniswap_v2_pair(token_contract_address):
        with open("../static/abi/factory-v2.abi") as f:
            abi = json.load(f)
        token_contract_address = web3.to_checksum_address(token_contract_address)
        factory_v2_contract = web3.eth.contract(address=UNISWAP_V2_FACTORY_ADDRESS, abi=abi)
        pair_address = factory_v2_contract.functions.getPair(token_contract_address, CHECKSUM_ETH_ADDRESS).call()
        if pair_address != NO_FACTORY_PAIR_ADDRESS:
            return pair_address
        return None

    @staticmethod
    def get_uniswap_v3_pair(token_contract_address):
        with open("../static/abi/factory-v3.abi") as f:
            abi = json.load(f)
        token_contract_address = web3.to_checksum_address(token_contract_address)
        factory_v2_contract = web3.eth.contract(address=UNISWAP_V3_FACTORY_ADDRESS, abi=abi)
        for fee in FACTORY_FEES:
            pair_address = factory_v2_contract.functions.getPool(token_contract_address, CHECKSUM_ETH_ADDRESS, fee).call()
            if pair_address != NO_FACTORY_PAIR_ADDRESS:
                return pair_address
        return None

    @staticmethod
    def get_token_decimals(token_contract_address):
        if token_contract_address in token_decimals:
            return token_decimals[token_contract_address]

        token_contract_address = web3.to_checksum_address(token_contract_address)
        abi = ApiService.get_token_abi(token_address=token_contract_address)
        if abi == NO_CONTRACT:
            return 18
        try:
            token_contract = web3.eth.contract(address=token_contract_address, abi=abi)
            decimals = token_contract.functions.decimals().call()
            token_decimals[token_contract_address] = decimals
            return decimals
        except:
            print(token_contract_address)
            return 18

Web3Service.get_token_decimals(0xa4f9650ebafde62afc7fd272db7d22057f4fe801)