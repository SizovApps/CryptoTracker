from model.Wallet import Wallet
from services.EthTrackerService import EthTrackerService
from services.InternalTransactionService import InternalTransactionService
from services.WriterService import WriterService

RESULTS_ADDRESSES = []


def get_best_wallets_for_token(token_address, token_name, max_best_addresses, start_time=None, end_time=None):
    WriterService.write_header_wallets_stats(token_name)
    all_transactions = EthTrackerService.get_transaction_of_token(token_address, start_time, end_time)
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
        if wallet.profit_in_dollar != 0:
            x = 0
        WriterService.write_wallet(wallet, token_name)
        # WriterService.write_full_stats(wallet.address, wallet.profit_in_dollar, wallet.profit_in_ETH,
        #                                wallet.full_enter, wallet.full_exit,
        #                                wallet.count_of_profit, wallet.count_of_loss, tokens=wallet.tokens)

    # WriterService.create_excel(token_name, results)

    # for i in range(max_best_addresses):
    #     wallet = results[i]
    #     print("Лучшие адрес: " + wallet.address)
    #     get_profit(wallet.address)
