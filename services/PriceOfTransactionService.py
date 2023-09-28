from services.ApiService import ApiService
from static.fields_names import VALUE_FIELD, FROM_FIELD, TO_FIELD

ETHER_VALUE = 10 ** 18


class PriceOfTransactionService:

    @staticmethod
    def get_price_of_transactions(wallet):
        for key in wallet.erc20_transactions:
            for transaction in wallet.erc20_transactions[key]:
                price = PriceOfTransactionService.get_eth_value_of_transaction(transaction)
                if price:
                    transaction.set_internal_transaction_value(price)
                    wallet.add_internal_transaction(key, transaction)

    @staticmethod
    def get_eth_value_of_transaction(transaction):
        if transaction.from_address == '0x0000000000000000000000000000000000000000':
            return 0

        value = transaction.tokens_swapped.eth_amount
        if value is None:
            print(f"Null transaction! {transaction}")
            return 0

        if transaction.tokens_swapped.is_buying:
            value = -value
            value -= transaction.gas_value
        else:
            value -= transaction.gas_value
        return value

    @staticmethod
    def get_internal_transactions(tx_hash, from_address, to_address):
        internal_transactions = ApiService.get_internal_transactions_api(tx_hash)
        for internal_transaction in internal_transactions:
            if internal_transaction[FROM_FIELD] == from_address and internal_transaction[TO_FIELD] == to_address:
                return int(internal_transaction[VALUE_FIELD]) / ETHER_VALUE
