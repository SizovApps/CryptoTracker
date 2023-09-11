
from model.TokensSwapped import TokensSwapped
from services.PriceOfTransactionService import PriceOfTransactionService


class BananaBotLogReader:
    BANANA_BOT_ADDRESS = "0xdb5889e35e379ef0498aae126fc2cce1fbd23216"

    def __init__(self, tx_hash):
        self.tx_hash = tx_hash

    def get_swapped_tokens(self, logs, is_eth_first_token, wallet_address, tokens_amount):
        eth_amount = PriceOfTransactionService.get_internal_transactions(self.tx_hash, self.BANANA_BOT_ADDRESS, wallet_address)
        return TokensSwapped(eth_amount=eth_amount, token_amount=tokens_amount, is_buying=True)
