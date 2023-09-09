import os

from dotenv import load_dotenv
from moralis import evm_api

load_dotenv()
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")


class MoralisService:
    USD_PRICE_FIELD = "usdPrice"
    ETH_CHAIN_FIELD = "eth"

    @staticmethod
    def get_current_price(token_address):
        params = {
            "address": token_address,
            "chain": MoralisService.ETH_CHAIN_FIELD
        }
        try:
            data = evm_api.token.get_token_price(
                api_key=MORALIS_API_KEY,
                params=params,
            )
            if data[MoralisService.USD_PRICE_FIELD] is None:
                return 0
            return data[MoralisService.USD_PRICE_FIELD]
        except:
            return 0

    @staticmethod
    def get_current_price(token_address):
        params = {
            "address": token_address,
            "chain": MoralisService.ETH_CHAIN_FIELD
        }
        try:
            data = evm_api.token.get_token_price(
                api_key=MORALIS_API_KEY,
                params=params,
            )
            if data[MoralisService.USD_PRICE_FIELD] is None:
                return 0
            return data[MoralisService.USD_PRICE_FIELD]
        except:
            return 0
