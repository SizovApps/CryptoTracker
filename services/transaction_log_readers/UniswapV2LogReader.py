from eth_abi import abi

from model.TokensSwapped import TokensSwapped
from services.transaction_log_readers.ILogReader import ILogReader
from stats.stats import ETHER_VALUE

swap_method_hash_v2 = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"


class UniswapV2LogReader(ILogReader):
    typesArray = ['uint256', 'uint256', 'uint256', 'uint256']
    exchange_address = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"

    def get_swapped_tokens(self, logs, is_eth_first_token, wallet_address):
        tokens_swapped = TokensSwapped(0, 0, True)
        eth_token_amount = self.get_eth_token_amounts(logs)
        for log in logs:
            topics = log[self.LOGS_TOPICS_FIELD]
            if topics[0] == swap_method_hash_v2:
                data = log[self.LOGS_DATA_FIELD][2:]
                data_in_bytes = bytes.fromhex(data)
                decoded_abi = abi.decode(self.typesArray, data_in_bytes)
                if len(decoded_abi) != 4:
                    print("Error in decoded_abi: " + decoded_abi)

                if decoded_abi[0] in eth_token_amount or decoded_abi[2] in eth_token_amount:
                    if decoded_abi[0] != 0:
                        tokens_swapped = TokensSwapped(
                            eth_amount=tokens_swapped.eth_amount + decoded_abi[0] / ETHER_VALUE,
                            token_amount=tokens_swapped.token_amount + decoded_abi[3],
                            is_buying=True
                        )
                    else:
                        tokens_swapped = TokensSwapped(
                            eth_amount=tokens_swapped.eth_amount + decoded_abi[2] / ETHER_VALUE,
                            token_amount=tokens_swapped.token_amount + decoded_abi[1],
                            is_buying=False
                        )
                else:
                    if decoded_abi[0] != 0:
                        tokens_swapped = TokensSwapped(
                            eth_amount=tokens_swapped.eth_amount + decoded_abi[3] / ETHER_VALUE,
                            token_amount=tokens_swapped.token_amount + decoded_abi[0],
                            is_buying=False
                        )
                    else:
                        tokens_swapped = TokensSwapped(
                            eth_amount=tokens_swapped.eth_amount + decoded_abi[1] / ETHER_VALUE,
                            token_amount=tokens_swapped.token_amount + decoded_abi[2],
                            is_buying=True
                        )

        return tokens_swapped

    def get_eth_token_amounts(self, logs):
        eth_token_amounts = []
        for log in logs:
            if log[self.LOGS_ADDRESS_FIELD] == self.ETH_ADDRESS:
                eth_token_amounts.append(int(log[self.LOGS_DATA_FIELD], 16))
        return eth_token_amounts

# #
# val = UniswapV2LogReader().get_swapped_tokens("0xbbaf65d9b93e03067d90e541d01e4009a2d411272958a0a51cd6352752486beb")
# print(val.eth_amount)

# 0x7a250d5630b4cf539739df2c5dacb4c659f2488d v2

# 0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD v3
