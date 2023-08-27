import datetime

from core.make_info_for_addresses import get_profit_last_month
from model.Wallet import Wallet
from services.EthTrackerService import EthTrackerService
from services.TransactionsService import set_internal_transactions
from services.WriterService import WriterService

RESULTS = []
RESULTS_ADDRESSES = []
TOKEN_NAME = "HARAM"
TOKEN_ADDRESS = "0xc961da88bb5e8ee2ba7dfd4c62a875ef80f7202f"
MAX_BEST_ADDRESSES = 10

START_TIME = datetime.datetime(2023, 8, 12, 23, 0, 0)
# START_TIME = None
END_TIME = None

WriterService.write_header_wallets_stats(TOKEN_NAME)
all_transactions = EthTrackerService.get_transaction_of_token(TOKEN_ADDRESS, START_TIME, END_TIME)
wallets = []
for buyer_transaction in all_transactions:
    if buyer_transaction.buyer_address in RESULTS_ADDRESSES:
        continue
    wallet = Wallet(buyer_transaction.buyer_address)
    wallet.set_erc20_transactions(buyer_transaction.erc20_transaction)
    set_internal_transactions(wallet)
    wallet.count_profit()
    RESULTS.append(wallet)
    RESULTS_ADDRESSES.append(wallet.address)

RESULTS.sort(key=lambda x: x.pnl, reverse=True)
print(RESULTS)

for wallet in RESULTS:
    WriterService.write_full_stats(wallet, TOKEN_NAME)

WriterService.create_excel(TOKEN_NAME, RESULTS)


for i in range(MAX_BEST_ADDRESSES):
    wallet = RESULTS[i]
    print("Лучшие адрес: " + wallet.address)
    get_profit_last_month(wallet.address)


