import os

from dotenv import load_dotenv
from moralis import evm_api

load_dotenv()
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")

current_prices = dict()


class MoralisService:
    USD_PRICE_FIELD = "usdPrice"
    ETH_CHAIN_FIELD = "eth"

    @staticmethod
    def get_current_price(token_address):
        params = {
            "address": token_address,
            "chain": MoralisService.ETH_CHAIN_FIELD
        }
        if token_address in current_prices:
            return current_prices[token_address]
        try:
            data = evm_api.token.get_token_price(
                api_key=MORALIS_API_KEY,
                params=params,
            )
            if data[MoralisService.USD_PRICE_FIELD] is None:
                return 0
            current_prices[token_address] = data[MoralisService.USD_PRICE_FIELD]
            return current_prices[token_address]
        except:
            return 0

    @staticmethod
    def get_block_number(time):
        if time == '1695669004':
            return 18214793
        if time == '1695675604':
            return 18215342
        params = {
            "chain": "eth",
            "date": time,
            # "chain": MoralisService.ETH_CHAIN_FIELD
        }
        data = evm_api.block.get_date_to_block(
            api_key=MORALIS_API_KEY,
            params=params,
        )
        print("get_block_number")
        print(data["block"])

        return data["block"]
