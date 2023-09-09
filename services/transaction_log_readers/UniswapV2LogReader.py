from eth_abi import abi

from model.TokensSwapped import TokensSwapped
from services.ApiService import ApiService
from services.transaction_log_readers.ILogReader import ILogReader
from stats.stats import ETHER_VALUE


class UniswapV2LogReader(ILogReader):
    swap_method_hash = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"
    typesArray = ['uint256', 'uint256', 'uint256', 'uint256']

    def get_swapped_tokens(self, tx_hash):
        transaction_receipt = ApiService.get_receipt(tx_hash)
        if not transaction_receipt:
            return TokensSwapped(eth_amount=0, token_amount=0, is_buying=True)
        logs = transaction_receipt[self.LOGS_FIELD]

        for log in logs:
            topics = log[self.TOPICS_FIELD]
            if topics[0] == self.swap_method_hash:
                data = log[self.LOGS_DATA_FIELD][2:]
                data_in_bytes = bytes.fromhex(data)
                decoded_abi = abi.decode(self.typesArray, data_in_bytes)
                if len(decoded_abi) != 4:
                    print("Error in decoded_abi: " + decoded_abi)
                    return TokensSwapped(eth_amount=0, token_amount=0, is_buying=True)

                print(decoded_abi)

                if decoded_abi[0] != 0:
                    return TokensSwapped(eth_amount=decoded_abi[3] / ETHER_VALUE, token_amount=decoded_abi[0], is_buying=False)
                else:
                    return TokensSwapped(eth_amount=decoded_abi[1] / ETHER_VALUE, token_amount=decoded_abi[2], is_buying=False)

#
# val = UniswapV2LogReader().get_swapped_tokens("0xdef3303423dbeff37d0a7a1b990c1c4c390f6efe7c5edb764eaa8c0aca34bb3c")
# print(val.eth_amount)
