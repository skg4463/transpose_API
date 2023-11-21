import requests
import csv
from datetime import datetime, timedelta
import time
import logging

"""
transpose.io 를 통한 SQL query code
custom endpoint = https://api.transpose.io/endpoint/dex_liquidity_by_account?end_date={end_date}&start_date={start_date}
api key = M3POVCPgTamflczQHxcqlhBlX6ciBBvg

"""

# 로깅 설정: 터미널에 로그 출력
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_data(start_date, end_date):
    headers = {
        'X-API-KEY': 'M3POVCPgTamflczQHxcqlhBlX6ciBBvg',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(
            f'https://api.transpose.io/endpoint/dex_liquidity_by_account?end_date={end_date}&start_date={start_date}',
            headers=headers,
            json={'options': {}},
        )

        if response.status_code == 200:
            logging.info(f"Data fetched successfully for dates {start_date} to {end_date}")
            return response.json()
        else:
            logging.error(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return None


def save_to_csv(data, filename):
    if data and 'results' in data:
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # 파일이 비어있으면 헤더 작성
                if file.tell() == 0:
                    writer.writerow(data['results'][0].keys())  # 헤더 작성
                # 각 데이터 행을 파일에 쓰기
                for row in data['results']:
                    writer.writerow(row.values())
            logging.info(f"Data saved to {filename}")
        except IOError as e:
            logging.error(f"IOError occurred while saving to {filename}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error occurred while saving to {filename}: {e}")


# 시작 날짜와 종료 날짜 설정
start_date = datetime(2022, 1, 1)
end_date = start_date + timedelta(hours=48)  # 시간 간격

# 파일 이름 설정
filename = 'uniswap_data.csv'

# 48시간 간격으로 데이터 요청 및 저장
while end_date <= datetime(2022, 12, 31):
    data = fetch_data(start_date.strftime("%Y-%m-%dT%H:%M:%SZ"), end_date.strftime("%Y-%m-%dT%H:%M:%SZ"))
    if data:
        # print(data)
        save_to_csv(data, filename)

    # 다음 48시간 간격으로 날짜 업데이트.
    start_date += timedelta(hours=48)
    end_date += timedelta(hours=48)

    # API 요청 제한을 고려하여 대기
    time.sleep(1)  # 초당 1회 요청 제한에 맞춰 대기
    logging.info("Waiting for next request cycle 1s")
