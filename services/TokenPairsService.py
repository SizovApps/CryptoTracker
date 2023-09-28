from services.Web3Service import Web3Service

token_pair_by_token_contract = dict()


class TokenPairsService:

    @staticmethod
    def get_token_pair(token_contract_address):
        if token_contract_address in token_pair_by_token_contract:
            return token_pair_by_token_contract[token_contract_address]

        uniswap_v2_pair = Web3Service.get_uniswap_v2_pair(token_contract_address)
        if uniswap_v2_pair is not None:
            token_pair_by_token_contract[token_contract_address] = uniswap_v2_pair
            return uniswap_v2_pair

        uniswap_v3_pair = Web3Service.get_uniswap_v3_pair(token_contract_address)
        if uniswap_v2_pair is not None:
            token_pair_by_token_contract[token_contract_address] = uniswap_v3_pair
        return uniswap_v3_pair
