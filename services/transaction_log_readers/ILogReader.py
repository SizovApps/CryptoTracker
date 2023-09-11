from abc import ABCMeta, abstractmethod


class ILogReader:
    __metaclass__ = ABCMeta

    LOGS_FIELD = "logs"
    LOGS_TOPICS_FIELD = "topics"
    LOGS_DATA_FIELD = "data"
    LOGS_ADDRESS_FIELD = "address"

    ETH_ADDRESS = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

    exchange_address = ""
    typesArray = []

    @abstractmethod
    def get_swapped_tokens(self, tx_hash, is_eth_first_token):
        pass