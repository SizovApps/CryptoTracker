import os

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")

# Change this to use your own RPC URL
web3 = Web3(Web3.HTTPProvider(INFURA_URL))


class Web3Service:

    @staticmethod
    def is_contract(address):
        address = web3.to_checksum_address(address)
        code = web3.eth.get_code(address)
        if code.hex() != '0x':
            return True
        return False

