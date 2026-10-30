# Open API 모듈
# - 나이스 급식 API 호출 담당

import os
import pprint
import requests
from dotenv import load_dotenv

# ===========================================================
#  1. 준비하기
#  - .env 파일에서 NEIS_API_KEY 불러오기
#  - 상수 데이터 설정
# ===========================================================

load_dotenv()
NEIS_API_KEY = os.getenv("NEIS_API_KEY")

SC_CODE = "J10"             # 시도교육청구분코드
SCHUL_CODE = "7530560"      # 행정표준코드    

# ===========================================================
#  2. Open API 호출
# ===========================================================

def get_food_info(mlsv_ymd, sc_code=SC_CODE, schul_code=SCHUL_CODE):
    try:
        url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
        params = {
            "KEY": NEIS_API_KEY,
            "Type": "json",
            "pIndex": "1",
            "pSize": "100",
            "ATPT_OFCDC_SC_CODE": sc_code,
            "SD_SCHUL_CODE": schul_code,
            "MLSV_YMD": mlsv_ymd,
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        # pprint.pprint(data)

        rows = []

        # 응답코드 확인 (급식이 없는 날은 INFO-200)
        if "RESULT" in data:
            result = data["RESULT"]
            if result["CODE"] == "INFO-200":
                return rows
            raise Exception((result["CODE"], result["MESSAGE"]))

        for row in data["mealServiceDietInfo"][1]["row"]:
            dish = row["DDISH_NM"].replace("<br/>", "\n")
            rows.append(
                (row["MLSV_YMD"],           # 일자
                 row["MMEAL_SC_NM"],        # 구분
                 dish,                      # 메뉴
                 row["CAL_INFO"])           # 칼로리
            )
        
        return rows

    except Exception as e:
        print(f"Open API 오류 발생: {e}")
        raise
