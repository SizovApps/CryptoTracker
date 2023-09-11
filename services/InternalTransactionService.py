ETHER_VALUE = 10 ** 18


class InternalTransactionService:
    PRICE_FIELD = "value"

    @staticmethod
    def set_internal_transactions(wallet):
        for key in wallet.erc20_transactions:
            for transaction in wallet.erc20_transactions[key]:
                price = InternalTransactionService.get_internal_transaction(transaction)
                if price:
                    transaction.set_internal_transaction_value(price)
                    wallet.add_internal_transaction(key, transaction)

    @staticmethod
    def get_internal_transaction(transaction):
        if transaction.from_address == '0x0000000000000000000000000000000000000000':
            return 0

        value = transaction.tokens_swapped.eth_amount

        if transaction.tokens_swapped.is_buying:
            value = -value
            value -= transaction.gas_value
        else:
            value -= transaction.gas_value
        return value
