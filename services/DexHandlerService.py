from model.TokensSwapped import TokensSwapped
from services.ApiService import ApiService

from services.transaction_log_readers.UniswapV2LogReader import swap_method_hash_v2, UniswapV2LogReader
from services.transaction_log_readers.UniswapV3LogReader import swap_method_hash_v3, UniswapV3LogReader


class DexHandlerService:
    LOGS_FIELD = "logs"
    TOPICS_FIELD = "topics"
    ETH_NAME = "eth"

    def factory_handler(self, tx_hash, token_name):
        transaction_receipt = ApiService.get_receipt(tx_hash)

        if not transaction_receipt:
            return TokensSwapped(eth_amount=0, token_amount=0, is_buying=True)

        logs = transaction_receipt[self.LOGS_FIELD]
        for log in logs:
            topics = log[self.TOPICS_FIELD]
            if topics[0] == swap_method_hash_v2:
                return UniswapV2LogReader().get_swapped_tokens(logs, token_name < self.ETH_NAME)
            elif topics[0] == swap_method_hash_v3:
                return UniswapV3LogReader().get_swapped_tokens(logs, token_name < self.ETH_NAME)
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
