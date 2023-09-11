import os

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")

# Change this to use your own RPC URL
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
# AggregatorV3Interface ABI
abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
# Feed address
# addr = web3.to_checksum_address('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
# print(addr)
addr = '0x89c7926c7c15fD5BFDB1edcFf7E7fC8283B578F6'

# Set up contract instance
contract = web3.eth.contract(address=addr, abi=abi)

#  Valid roundId must be known. They are NOT incremental.
# invalidRoundId = 18446744073709562300
validRoundId = 18446744073709554177

historicalData = contract.functions.getRoundData(validRoundId).call()
print(historicalData)