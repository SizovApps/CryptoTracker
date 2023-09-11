from model.TokensSwapped import TokensSwapped
from services.DexHandlerService import dexHandlerService


def test_buy_uniswap_2():
    tokens_swapped = dexHandlerService.factory_handler(
        "0xdf11152e3b73ad1ad336fc280d7679ebd583e009a6373401c497848460440337", "PEPE")
    correct_tokens_swapped = TokensSwapped(eth_amount=0.08, token_amount=29120577178958282625840728036, is_buying=True)
    assert tokens_swapped.eth_amount == correct_tokens_swapped.eth_amount
    assert tokens_swapped.token_amount == correct_tokens_swapped.token_amount
    assert tokens_swapped.is_buying == correct_tokens_swapped.is_buying


def test_sell_uniswap_2():
    tokens_swapped = dexHandlerService.factory_handler(
        "0x2e453fe451e8532d690a50fbd5ae98274c07112d0475ef4ae0490e957d4db1ad", "PEPE")
    correct_tokens_swapped = TokensSwapped(eth_amount=0.009233611988356095, token_amount=3471836484887159547936399684,
                                           is_buying=False)
    assert tokens_swapped.eth_amount == correct_tokens_swapped.eth_amount
    assert tokens_swapped.token_amount == correct_tokens_swapped.token_amount
    assert tokens_swapped.is_buying == correct_tokens_swapped.is_buying


def test_buy_uniswap_3():
    tokens_swapped = dexHandlerService.factory_handler(
        "0x18eb6b4ccf05f12dae967671fecb957b7525e1f2c1d3690650018556f95e6374", "SHIC")
    correct_tokens_swapped = TokensSwapped(eth_amount=0.001, token_amount=215275110463510010550, is_buying=True)
    assert tokens_swapped.eth_amount == correct_tokens_swapped.eth_amount
    assert tokens_swapped.token_amount == correct_tokens_swapped.token_amount
    assert tokens_swapped.is_buying == correct_tokens_swapped.is_buying


def test_sell_uniswap_3():
    tokens_swapped = dexHandlerService.factory_handler(
        "0x4f524ab801ee9708dcbfb088577a9e840a80de6413abb3b60f94907b4ef3beb1", "SHIC")
    correct_tokens_swapped = TokensSwapped(eth_amount=2.541280159944008709, token_amount=555469020763, is_buying=False)
    assert tokens_swapped.eth_amount == correct_tokens_swapped.eth_amount
    assert tokens_swapped.token_amount == correct_tokens_swapped.token_amount
    assert tokens_swapped.is_buying == correct_tokens_swapped.is_buying


def test_buy_banana_gun():
    tokens_swapped = dexHandlerService.factory_handler(
        "0x4596ff645a3783df3b285e846c02238cca91e39f840bb713baae8e96207a034c", "BRETT")
    correct_tokens_swapped = TokensSwapped(eth_amount=0.031100657982904871, token_amount=2000000000000000, is_buying=True)
    assert tokens_swapped.eth_amount == correct_tokens_swapped.eth_amount
    assert tokens_swapped.token_amount == correct_tokens_swapped.token_amount
    assert tokens_swapped.is_buying == correct_tokens_swapped.is_buying
