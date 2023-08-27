from eth_waller_tracking import EthTracker
from model.Wallet import *
from services.TransactionsService import set_internal_transactions
from writer import write_wallet, write_header_wallets_stats, create_excel

NO_DEFINED_VALUE = 100000000000

checked_addresses = []


def get_profit_last_month(address, token_name, start_time):
    account_eth_balance = EthTracker.get_account_balance(address)
    print("Текущий баланс ETH: ", account_eth_balance)

    wallet = Wallet(address, account_eth_balance)
    if wallet.address in checked_addresses:
        return None
    try:
        wallet.set_erc20_transactions(EthTracker.get_erc_20_transactions(address, start_time))
    except RuntimeError as error:
        print(error)
        print(error.args)

    set_internal_transactions(wallet)

    wallet.count_profit()
    checked_addresses.append(wallet.address)
    write_wallet(wallet, token_name)
    return wallet


def make_info_for_addresses(token_name, start_time, addresses):
    write_header_wallets_stats(token_name)

    results = []
    for address in addresses:
        wallet = get_profit_last_month(address, token_name, start_time)
        if wallet is not None:
            results.append(wallet)

    create_excel(token_name, results)
