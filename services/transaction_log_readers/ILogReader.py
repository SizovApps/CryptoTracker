from abc import ABCMeta, abstractmethod


class ILogReader:
    __metaclass__ = ABCMeta

    LOGS_FIELD = "logs"
    TOPICS_FIELD = "topics"
    LOGS_DATA_FIELD = "data"

    ETH_ADDRESS = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

    swap_method_hash = ""
    typesArray = []

    @abstractmethod
    def get_swapped_tokens(self, tx_hash):
        pass
