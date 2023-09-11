from core.make_info_for_addresses import make_info_for_addresses
from model.Wallet import Wallet
from services.EthTrackerService import EthTrackerService
from services.InternalTransactionService import InternalTransactionService
from services.WriterService import WriterService

WALLETS_INTERACTED_ADDRESSES = []


def get_best_wallets_for_token(token_address, token_name, max_best_addresses, max_transactions_to_check, swap_factory, start_time=None, end_time=None):
    WriterService.write_header_wallets_stats(token_name)
    all_transactions = EthTrackerService.get_transaction_of_token(token_address, token_name, max_transactions_to_check, swap_factory, start_time, end_time)
    wallets_interacted_with_token = []
    for buyer_transaction in all_transactions:
        if buyer_transaction.buyer_address in WALLETS_INTERACTED_ADDRESSES:
            continue
        wallet = Wallet(buyer_transaction.buyer_address)
        wallet.set_erc20_transactions(buyer_transaction.erc20_transaction)
        InternalTransactionService.set_internal_transactions(wallet)
        wallet.count_profit()
        wallets_interacted_with_token.append(wallet)
        WALLETS_INTERACTED_ADDRESSES.append(wallet.address)

    wallets_interacted_with_token.sort(key=lambda x: x.pnl, reverse=True)
    print(f"Wallets interacted with token: {wallets_interacted_with_token}")

    for wallet in wallets_interacted_with_token:
        WriterService.write_wallet(wallet, token_name)

    if max_best_addresses >= len(wallets_interacted_with_token):
        result_wallets = make_result_addresses(wallets_interacted_with_token)
        make_info_for_addresses(token_name, None, result_wallets, swap_factory)
    else:
        result_wallets = make_result_addresses(wallets_interacted_with_token[:max_best_addresses])
        make_info_for_addresses(token_name, None, result_wallets, swap_factory)


def make_result_addresses(result_wallets):
    result_addresses = []
    for wallet in result_wallets:
        result_addresses.append(wallet.address)
    return result_addresses
