from eth_abi import abi

from model.TokensSwapped import TokensSwapped
from model.transaction_log_readers.UniswapV3LogReaderModel import UniswapV3LogReaderModel
from services.transaction_log_readers.ILogReader import ILogReader
from static.fields_names import LOG_ADDRESS_FIELD, LOG_DATA_FIELD
from static.stats import ETHER_VALUE

swap_method_hash_v3 = "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"


class UniswapV3LogReader(ILogReader):
    typesArray = ['int256', 'int256', 'uint160', 'uint128', 'int24']

    ETH_TRANSFER_ADDRESS = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

    def get_swapped_tokens(self, logs):
        tokens_swapped = TokensSwapped(0, 0, True)

        for log in logs:
            topics = log[self.LOGS_TOPICS_FIELD]
            if topics[0] == swap_method_hash_v3:
                data = log[self.LOGS_DATA_FIELD][2:]
                data_in_bytes = bytes.fromhex(data)
                decoded_abi = abi.decode(self.typesArray, data_in_bytes)
                if len(decoded_abi) != 5:
                    print("Error in decoded_abi: " + str(decoded_abi))

                decoded_log_model = UniswapV3LogReader.parse_model(decoded_abi)

                is_buying = True
                if decoded_log_model.amount0 < 0:
                    is_buying = False

                is_eth_first_token = self.is_eth_first(logs, decoded_log_model)

                if is_eth_first_token:
                    tokens_swapped = TokensSwapped(
                        eth_amount=tokens_swapped.eth_amount + abs(decoded_log_model.amount0) / ETHER_VALUE,
                        token_amount=tokens_swapped.token_amount + abs(decoded_log_model.amount1),
                        is_buying=is_buying)
                else:
                    tokens_swapped = TokensSwapped(
                        eth_amount=tokens_swapped.eth_amount + abs(decoded_log_model.amount1) / ETHER_VALUE,
                        token_amount=tokens_swapped.token_amount + abs(decoded_log_model.amount0),
                        is_buying=is_buying)
        return tokens_swapped

    def is_eth_first(self, logs, decoded_log_model):
        eth_transfer_amounts = self.get_ath_transfer_amounts(logs)
        if not eth_transfer_amounts:
            return False

        if abs(decoded_log_model.amount0) in eth_transfer_amounts:
            return True
        else:
            return False

    def get_ath_transfer_amounts(self, logs):
        eth_transfer_amounts = []
        for log in logs:
            topics = log[self.LOGS_TOPICS_FIELD]
            if topics[0] == self.ETH_TRANSFER_ADDRESS and log[LOG_ADDRESS_FIELD] == self.ETH_ADDRESS:
                eth_transfer_amounts.append(int(log[LOG_DATA_FIELD], 16))
        return eth_transfer_amounts

    @staticmethod
    def parse_model(decoded_abi):
        return UniswapV3LogReaderModel(
            amount0=decoded_abi[0],
            amount1=decoded_abi[1],
            sqrtPriceX96=decoded_abi[2],
            liquidity=decoded_abi[3],
            tick=decoded_abi[4]
        )


# val = UniswapV3LogReader().get_swapped_tokens("0xb9a59d8323b7d50a5b3e3f3400fa9ab44cc75f1a844e655631190bcd60558737")
# print(val.eth_amount, val.token_amount, val.is_buying)
