import datetime

from eth_waller_tracking import *
from eth_waller_tracking import EthTracker
from model.Wallet import *
from services.transactions_service import set_internal_transactions
from writer import write_wallet, write_header_wallets_stats, create_excel

NO_DEFINED_VALUE = 100000000000

RESULTS = []
results_addresses = []


def get_profit_last_month(address, token_name):
    account_eth_balance = EthTracker.get_account_balance(address)
    print("Текущий баланс ETH: ", account_eth_balance)

    wallet = Wallet(address, account_eth_balance)
    if wallet.address in results_addresses:
        return None
    try:
        wallet.set_erc20_transactions(EthTracker.get_erc_20_transactions(address, datetime.datetime(2023, 5, 15, 0, 0, 0, 0)))
    except RuntimeError as error:
        print(error)
        print(error.args)

    set_internal_transactions(wallet)

    result, profit, percent = wallet.count_profit()
    if result:
        print("Good wallet: ", wallet.address)
    results_addresses.append(wallet.address)
    write_wallet(wallet, token_name)
    return wallet


def make_info_for_addresses(token_name, start_time, wallet_address):
    write_header_wallets_stats(token_name)
    # check = get_first_addresses("0xfcaf0e4498e78d65526a507360f755178b804ba8", START_TIME)
    check = [wallet_address]

    results = []
    for address in check:
        wallet = get_profit_last_month(address, token_name)
        if wallet is not None:
            results.append(wallet)

    create_excel(token_name, results)


make_info_for_addresses("UBANK", None, "0x88d8aa93f789a789e27438ddfeff9f35dbfb130b")
