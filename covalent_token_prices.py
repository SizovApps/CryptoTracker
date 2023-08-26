import requests
from requests.auth import HTTPBasicAuth

API_KEY = "cqt_rQF73HYHy3cRC6ddKmYV7PwhRYb9"
address = "0x94746C1d8f9506D6B92C30ff92BD6f9D6aA66d2c"
BASE_URL = "https://api.covalenthq.com/v1/eth-mainnet/address/"
ETHER_VALUE = 10**18

# url = "https://api.covalenthq.com/v1/eth-mainnet/address/0x94746C1d8f9506D6B92C30ff92BD6f9D6aA66d2c/transfers_v2/"

# https://api.etherscan.io/api?module=account&action=txlistinternal
# &address=0x94746C1d8f9506D6B92C30ff92BD6f9D6aA66d2c&apikey=1MXH1BG14R8689DHRDUDTF3UKSUWUK6AQC&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc

tokens = dict()

def get_transactions_for_token(address, contract_address):
    get_transactions_url = BASE_URL + f"{address}/transfers_v2/"

    headers = {
        "accept": "application/json",
    }
    basic = HTTPBasicAuth(API_KEY, '')
    params = dict()
    params['contract-address'] = contract_address
    response = requests.get(get_transactions_url, headers=headers, auth=basic, params=params)

    json = response.json()
    data = json['data']['items']
    data = reversed(data)


    for item in data:
        print(item)
        from_address = item["from_address"]
        to_address = item["to_address"]
        value = item["value"]
        transfers = item["transfers"]
        contract_name = transfers[0]["contract_name"]
        transfer_type = transfers[0]["transfer_type"]
        update_info_of_token(contract_name, value, transfer_type)
        print("From address: ", from_address)
        print("To address: ", to_address)
        print("Value: ", value)
        print("contract_name: ", contract_name)

        print("-------------")


def update_info_of_token(contract_name, value, transfer_type):
    value = float(value) / ETHER_VALUE
    if contract_name in tokens:
        if transfer_type == "IN":
            tokens[contract_name] = [tokens[contract_name][0] + value]
        else:
            tokens[contract_name] = [tokens[contract_name][0] - value]
    else:
        if transfer_type == "IN":
            tokens[contract_name] = [value]
        else:
            tokens[contract_name] = [value]