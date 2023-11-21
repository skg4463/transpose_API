import time
import logging
from transpose import Transpose
import csv

"""
blockNum: 16415674
uniswap
2023-01-16T00:08:11Z
0x8a53347d44a49214534da135f01bb0a844fb41e055bb86448afdca56f9ae2873
<Swap:  from_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  to_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  
quantity_in="400000000"  quantity_out="256784456981887482">

"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Transpose 객체 초기화
api = Transpose(api_key='M3POVCPgTamflczQHxcqlhBlX6ciBBvg', debug=True)

WETH = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'  # WETH
USDC = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'  # USDC


def save_swaps_to_csv(swaps, filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # CSV 헤더 작성
        if file.tell() == 0:
            writer.writerow(['blockNum', 'timestamp', 'TxHash', 'origin', 'SENDER', 'from_token', 'to_token', 'quantity_in', 'quantity_out'])

        # swaps 데이터 작성
        for swap in swaps:
            if swap.from_token == WETH or swap.to_token == WETH and swap.exchange_name == 'uniswap':
                if swap.pair_contract_address == '0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640':
                    if swap.from_token == WETH:
                        from_token = 'WETH'
                        to_token = 'USDC'
                        quantity_in = swap.quantity_in / (10 ** 18)
                        quantity_out = swap.quantity_out / (10 ** 6)
                    else:
                        from_token = 'USDC'
                        to_token = 'WETH'
                        quantity_in = swap.quantity_in / (10 ** 6)
                        quantity_out = swap.quantity_out / (10 ** 18)
                    writer.writerow([swap.block_number, swap.timestamp, swap.transaction_hash, swap.origin, swap.sender, from_token, to_token, quantity_in, quantity_out])


def fetch_swaps():
    swaps = []  # swaps 변수 초기화
    try:
        time.sleep(1)
        logging.debug("Starting API call to fetch swaps")
        swaps = api.token.swaps_by_contract_address(
            contract_address='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',  # USDC
            direction="all",
            occurred_after='2022-01-01T00:00:00',
            occurred_before='2022-12-13T00:00:00',
            order='asc',
            limit=1000
        )
        time.sleep(1)
        logging.debug(f"API call successful, retrieved {len(swaps)} swaps")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return swaps  # swaps 반환


swaps = fetch_swaps()
save_swaps_to_csv(swaps, 'swaps.csv')

# 결과 처리

# for swap in swaps:
#     if swap.from_token == WETH or swap.to_token == WETH and swap.exchange_name == 'uniswap':
#         if swap.pair_contract_address == '0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640':
#             print('blockNum:', swap.block_number, ', contract_address:', swap.pair_contract_address, 'timsstamp:', swap.timestamp)
#             print('TxHash:', swap.transaction_hash, 'origin:', swap.origin, 'SENDER:', swap.sender)
#             if swap.from_token == WETH:
#                 print('WETH', swap. quantity_in / (10**18), ' -> USDC', swap.quantity_out / (10**6))
#             else:
#                 print('USDC', swap. quantity_in / (10**6), ' -> WETH', swap.quantity_out / (10**18))
#             # print(swap)
#             print('-------------------')

'''
swap.origin : 진짜 발송자 <- 비교식별자에 이거도 비교연산
swap.sender : router나 bot 가능 // 공격 판별을 위해 이거 사용
(attacker list.csv) 사용
'''