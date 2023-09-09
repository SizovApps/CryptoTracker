from model.Wallet import *
from services.EthTrackerService import EthTrackerService
from services.InternalTransactionService import InternalTransactionService
from services.WriterService import WriterService

NO_DEFINED_VALUE = 100000000000

checked_addresses = []


def get_profit(address, token_name, start_time):
    account_eth_balance = EthTrackerService.get_account_balance(address)
    print("Текущий баланс ETH: ", account_eth_balance)

    wallet = Wallet(address)
    if wallet.address in checked_addresses:
        return None
    try:
        wallet.set_erc20_transactions(EthTrackerService.get_erc_20_transactions(address, start_time))
    except RuntimeError as error:
        print(error)
        print(error.args)

    InternalTransactionService.set_internal_transactions(wallet)

    wallet.count_profit()
    checked_addresses.append(wallet.address)
    WriterService.write_wallet(wallet, token_name)
    return wallet


def make_info_for_addresses(token_name, start_time, addresses):
    WriterService.write_header_wallets_stats(token_name)

    wallets = []
    for address in addresses:
        wallet = get_profit(address, token_name, start_time)
        if wallet is not None:
            wallets.append(wallet)

    wallets_by_win_rate = EthTrackerService.get_best_wallets_by_win_rate(wallets)
    WriterService.write_best_by_win_rate(wallets, token_name)
    for wallet in wallets_by_win_rate:
        print(f"{wallet.address}, winRate: {wallet.win_rate}, pnl: {wallet.pnl}, Count of wins: {wallet.count_of_profit},  Count of loses: {wallet.count_of_loss}")
