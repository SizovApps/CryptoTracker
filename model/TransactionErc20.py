ETHER_VALUE = 10 ** 18


class TransactionErc20:
    def __init__(self, token_name, tx_hash, date_time, from_address, to_address, quantity_of_token, gas_value, is_from,
                 data, contract_address):
        self.token_name = token_name
        self.tx_hash = tx_hash
        self.date_time = date_time
        self.from_address = from_address
        self.to_address = to_address
        self.quantity_of_token = float(quantity_of_token) / ETHER_VALUE
        self.gas_value = gas_value
        self.is_from = is_from
        self.internal_transaction_value = 0
        self.data = data
        self.contract_address = contract_address

    def __str__(self):
        name = self.token_name + ": " + str(self.internal_transaction_value) + " -> " + str(self.quantity_of_token)
        return name

    def set_internal_transaction_value(self, internal_transaction_value):
        self.internal_transaction_value = internal_transaction_value
