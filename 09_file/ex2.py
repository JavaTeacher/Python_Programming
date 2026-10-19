# JSON 처리 (JavaScript Object Notation)

import os
import json

# ===========================================================
#  1. JSON이란?
#  - 자바스크립트 객체 표기법을 기반으로 만들어진 경량의 데이터 교환 형식
#  - 서버와 클라이언트가 서로 데이터를 주고 받을 때 많이 사용 (https://www.json.org/)
#  
#  [데이터 구조]
#  - 객체(Object): { }로 표현하고, Key와 Value 쌍으로 저장 (예) {"name": "홍길동", "age": 17}
#  - 배열(Array) : [ ]로 표현하고, 순서가 있는 값의 목록을 저장 (예) ["사과", "바나나", "키위"]
#
#  [작성규칙]
#  - 키는 반드시 큰따옴표(")로 감싸기 (작은 따옴표는 안됨)
#  - 마지막 항목 뒤에는 콤마(,)를 붙이면 안됨
#  - 주석 작성 불가
#
#  [json 모듈 함수]
#  1) 직렬화
#  - dumps(객체) : 파이썬 (  ) -> JSON 형식 (  ) (s는 string)
#  - dump(객체, f) : 파이썬 (  ) -> JSON 형식 (  )
#
#  2) 역직렬화
#  - loads(문자열) : JSON 형식 ( ) -> 파이썬 (  )
#  - load(f) : JSON 형식 (  ) -> 파이썬 (  )
# ===========================================================


# ===========================================================
#  2. 파이썬 객체 <-> JSON 형식 문자열 변환
#  - json.dumps(데이터, ensure_ascii=False, indent=4)
#  - json.loads(f)
#  - ensure_ascii=False: 한글이 \uXXXX 형태로 바뀌지 않고 그대로 출력
#  - indent=4: 사람이 읽기 좋게 들여쓰기
# ===========================================================

data = {
    "name": "뽀로로",
    "age": 17,
    "scores": [100, 90],
    "subjects": ["파이썬", "컴구"],
}

# 직렬화) 파이썬 객체 -> JSON 형식 문자열
# json_str = json.( )(data, ensure_ascii=False, indent=4)
# print(json_str, type(json_str))

# 역직렬화) JSON 형식 문자열 -> 파이썬 객체
# parsed = json.( )(json_str)
# print( )
# print( )                      # 100 출력
# print( )                      # 컴구 출력


# ===========================================================
#  3. 파이썬 객체 <-> JSON 형식 파일 변환
#  - json.dump(데이터, f, ensure_ascii=False, indent=4)
#  - json.load(f)
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "score.json")

# 직렬화) 파이썬 객체 -> JSON 형식 파일
# with open(FILE_PATH, "w", encoding="utf-8") as f:
#     json.( )(data, f, ensure_ascii=False, indent=4)

# 역직렬화) JSON 형식 파일 -> 파이썬 객체
# try:
#     with open(FILE_PATH, "r", encoding="utf-8") as f:
#         score = json.( )(f)
# except FileNotFoundError:
#     print("파일을 찾을 수 없습니다.")

# print( )


# ===========================================================
#  4. 리스트 목록 데이터 변환
# ===========================================================
students = [
    {"id": 1, "name": "뽀로로", "scores": {"kor": 100, "mat": 100, "eng": 100}},
    {"id": 2, "name": "크롱", "scores": {"kor": 90, "mat": 90, "eng": 90}},
]

# 직렬화) 파이썬 객체 -> JSON 형식 문자열
# json_str = json.( )(students, ensure_ascii=False, indent=4)
# print( )

# 역직렬화) JSON 형식 문자열 -> 파이썬 객체
# parsed = json.( )(json_str)
# print( )
