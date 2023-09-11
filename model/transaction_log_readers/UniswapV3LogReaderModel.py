
class UniswapV3LogReaderModel:
    def __init__(self, amount0, amount1, sqrtPriceX96, liquidity, tick):
        self.amount0 = amount0
        self.amount1 = amount1
        self.sqrtPriceX96 = sqrtPriceX96
        self.liquidity = liquidity
        self.tick = tick