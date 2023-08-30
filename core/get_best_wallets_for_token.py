from core.make_info_for_addresses import make_info_for_addresses
from model.Wallet import Wallet
from services.EthTrackerService import EthTrackerService
from services.InternalTransactionService import InternalTransactionService
from services.WriterService import WriterService

RESULTS_ADDRESSES = []


def get_best_wallets_for_token(token_address, token_name, max_best_addresses, start_time=None, end_time=None):
    WriterService.write_header_wallets_stats(token_name)
    all_transactions = EthTrackerService.get_transaction_of_token(token_address, token_name, start_time, end_time)
    results = []
    for buyer_transaction in all_transactions:
        if buyer_transaction.buyer_address in RESULTS_ADDRESSES:
            continue
        wallet = Wallet(buyer_transaction.buyer_address)
        wallet.set_erc20_transactions(buyer_transaction.erc20_transaction)
        InternalTransactionService.set_internal_transactions(wallet)
        wallet.count_profit()
        results.append(wallet)
        RESULTS_ADDRESSES.append(wallet.address)

    results.sort(key=lambda x: x.pnl, reverse=True)
    print(results)

    for wallet in results:
        WriterService.write_wallet(wallet, token_name)

    WriterService.create_excel(token_name, results)
    if max_best_addresses >= len(results):
        result_wallets = make_result_addresses(results)
        make_info_for_addresses(token_name, None, result_wallets)
    else:
        result_wallets = make_result_addresses(results[:max_best_addresses])
        make_info_for_addresses(token_name, None, result_wallets)


def make_result_addresses(result_wallets):
    result_addresses = []
    for wallet in result_wallets:
        result_addresses.append(wallet.address)
    return result_addresses
