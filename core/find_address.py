from datetime import datetime

from services.ApiService import ApiService
from services.EthTrackerService import EthTrackerService

data = ApiService.get_addresses_bought_token_desc_api("0xe0c8b298db4cffe05d1bea0bb1ba414522b33c1b")
correct_data = []
for tx in data:
    if int(tx["timeStamp"]) < 1691980012 or int(tx["timeStamp"]) > 1692210412:
        continue
    correct_data.append(tx)
correct_data.reverse()
print(len(correct_data))
for tx in correct_data:
    time = datetime.fromtimestamp(int(tx["timeStamp"]))
    from_address = tx[EthTrackerService.FROM_FIELD]
    to_address = tx[EthTrackerService.TO_FIELD]
    print(f"Time: {time},  From: {from_address}, To: {to_address}")

for tx in correct_data:
    from_address = tx[EthTrackerService.FROM_FIELD]
    print("get for address: " + from_address)
    transactions = EthTrackerService.get_erc_20_transactions(from_address, None, searching_token="NCDToken")
    if 10 <= len(transactions["NCDToken"]) <= 16:
        print("GOOD: " + from_address)


# transactions = EthTrackerService.get_erc_20_transactions("0x009756a2ec87af8948695d5b450f5d8836421a8e", None, searching_token="NCDToken")
# print(len(transactions["NCDToken"]))