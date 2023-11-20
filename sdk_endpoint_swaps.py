import time
import logging
from transpose import Transpose
from transpose.src.util.errors import TransposeRateLimit


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Transpose 객체 초기화
api = Transpose(api_key='M3POVCPgTamflczQHxcqlhBlX6ciBBvg', debug=True)


def fetch_swaps():
    swaps = []  # swaps 변수 초기화
    try:
        time.sleep(1)
        logging.debug("Starting API call to fetch swaps")
        swaps = api.token.swaps_by_contract_address(
            contract_address='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
            direction="all",
            occurred_after='2023-01-16T00:00:00',
            occurred_before='2023-01-17T00:00:00',
            order='asc',
            limit=100
        )
        time.sleep(1)
        logging.debug(f"API call successful, retrieved {len(swaps)} swaps")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return swaps  # swaps 반환


swaps = fetch_swaps()

# 결과 처리
target_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
for swap in swaps:
    if swap.from_token == target_address or swap.to_token == target_address and swap.exchange_name == 'uniswap':
        print('blockNum:', swap.block_number)
        print(swap.exchange_name)
        print(swap.timestamp)
        print(swap.transaction_hash)
        print(swap)
