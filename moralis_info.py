from moralis import evm_api

MORALIS_API_KEY = "DYEG2TcEdh2jxVFOzsTezn1m6APIVEMsjS1XlUVxSHnXqqIDLeUme7esL68d9Ua3"


def get_current_price(token_address, chain):
    params = {
        "address": token_address,
        "chain": chain
    }
    try:
        data = evm_api.token.get_token_price(
            api_key=MORALIS_API_KEY,
            params=params,
        )
        if data["usdPrice"] == None:
            return 0
        return data["usdPrice"]
    except:
        return 0
