from enum import Enum

from model.TokensSwapped import TokensSwapped
from services.ApiService import ApiService
from services.transaction_log_readers.BananaBotLogReader import BananaBotLogReader
from services.transaction_log_readers.UniswapV2LogReader import swap_method_hash_v2, UniswapV2LogReader
from services.transaction_log_readers.UniswapV3LogReader import swap_method_hash_v3, UniswapV3LogReader


class DEX(Enum):
    UNISWAP_V2 = 1
    UNISWAP_V3 = 2
    BANANA_BOT = 3


class DexHandlerService:
    LOGS_FIELD = "logs"
    LOGS_ADDRESS_FIELD = "address"
    TOPICS_FIELD = "topics"

    ETH_NAME = "eth"

    def factory_handler(self, tx_hash, token_name, wallet_address, tokens_amount):
        transaction_receipt = ApiService.get_receipt(tx_hash)
        selected_dex = DEX.UNISWAP_V2
        if not transaction_receipt:
            return TokensSwapped(eth_amount=0, token_amount=0, is_buying=True)

        logs = transaction_receipt[self.LOGS_FIELD]
        for log in logs:
            # if log[self.LOGS_ADDRESS_FIELD] == BananaBotLogReader.BANANA_BOT_ADDRESS:
            #     selected_dex = DEX.BANANA_BOT
            #     break
            topics = log[self.TOPICS_FIELD]
            if topics[0] == swap_method_hash_v2:
                selected_dex = DEX.UNISWAP_V2
            elif topics[0] == swap_method_hash_v3:
                selected_dex = DEX.UNISWAP_V3

        if selected_dex == DEX.UNISWAP_V2:
            return UniswapV2LogReader(tx_hash).get_swapped_tokens(logs, token_name < self.ETH_NAME, wallet_address)
        elif selected_dex == DEX.UNISWAP_V3:
            return UniswapV3LogReader(tx_hash).get_swapped_tokens(logs)
        elif selected_dex == DEX.BANANA_BOT:
            return BananaBotLogReader(tx_hash).get_swapped_tokens(logs, token_name < self.ETH_NAME, wallet_address, tokens_amount)

        return TokensSwapped(eth_amount=0, token_amount=0, is_buying=True)


dexHandlerService = DexHandlerService()

# tokens_swapped = dexHandlerService.factory_handler("0x5cdb92c54a512b9580b964681efc1d9e5d5d447e548d9373c7bd6e548c241735", "ZZ")
# print(tokens_swapped.eth_amount, tokens_swapped.token_amount, tokens_swapped.is_buying)
# tokens_swapped = dexHandlerService.factory_handler("0xb8f19f0ab2ddb841ceea555805be26464d32819d85a4b323b95f328795caa975", "ZZ")
# print(tokens_swapped.eth_amount, tokens_swapped.token_amount, tokens_swapped.is_buying)
# tokens_swapped = dexHandlerService.factory_handler("0xc724b1432acfd6ba675d39f2acf4694b1f7e86372df57c85c62db8afc2ff743f", "ZZ")
# print(tokens_swapped.eth_amount, tokens_swapped.token_amount, tokens_swapped.is_buying)
# tokens_swapped = dexHandlerService.factory_handler("0x7e682b4e41ba48860aea4ee6695f1eab13feda508a424e6e536fcd6b72e1df76", "ZZ")
# print(tokens_swapped.eth_amount, tokens_swapped.token_amount, tokens_swapped.is_buying)
