import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# CSV 파일 읽기
df = pd.read_csv('uniswap_data.csv', parse_dates=['timestamp'])

# 'liquidity_delta'를 실수로 변환
df['liquidity_delta'] = pd.to_numeric(df['liquidity_delta'], errors='coerce')
df['pool_balance'] = pd.to_numeric(df['pool_balance'], errors='coerce')

# 'liquidity_delta'가 양수이면 'liquidity_add', 음수이면 'liquidity_remove'로 분류
df['liquidity_type'] = df['liquidity_delta'].apply(lambda x: 'liquidity_add' if x > 0 else 'liquidity_remove')

# 유동성 추가 및 제거 데이터 분리
liquidity_add = df[df['liquidity_type'] == 'liquidity_add']
liquidity_remove = df[df['liquidity_type'] == 'liquidity_remove']

# 3시간 단위로 리샘플링
resampled_add = liquidity_add.resample('24H', on='timestamp').agg({'liquidity_delta': 'sum'})
resampled_remove = liquidity_remove.resample('24H', on='timestamp').agg({'liquidity_delta': 'sum'})
resampled_balance = df.resample('24H', on='timestamp').agg({'pool_balance': 'mean'})

# 그래프 그리기
fig, ax1 = plt.subplots(figsize=(12, 6))

# x축 눈금 및 레이블 설정
ax1.xaxis.set_major_locator(mdates.MonthLocator())  # 매월로 눈금 설정
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # '년-월' 형식으로 날짜 형식 지정

color = 'tab:green'
ax1.set_xlabel('Time')
ax1.set_ylabel('Liquidity Delta', color=color)
ax1.plot(resampled_add.index, resampled_add['liquidity_delta'], label='Liquidity Add', color='green', linewidth=0.5)
ax1.plot(resampled_remove.index, -resampled_remove['liquidity_delta'], label='Liquidity Remove', color='red', linewidth=0.5)  # 음수값을 양수로 변환하여 표시
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='upper left')

ax2 = ax1.twinx()  # 같은 x축을 공유하는 두 번째 y축 생성
color = 'tab:blue'
ax2.set_ylabel('Pool Balance', color=color)
ax2.plot(resampled_balance.index, resampled_balance['pool_balance'], label='Pool Balance', color=color, linewidth=0.5)
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc='upper right')

plt.title('Liquidity Additions, Removals, and Pool Balance Over Time')
plt.show()
