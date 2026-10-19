# 파일 처리

import os

# 이 파일이 있는 폴더 기준으로 경로 만들기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

FILE_PATH = os.path.join(BASE_DIR, "test.txt")
print(FILE_PATH)

# ===========================================================
#  1. 파일 열기
#  - 형식) open(파일경로, 모드, encoding="utf-8")
#
#  [파일 열기 모드]
#  - r(read)   : (  ) 모드, 파일이 없으면 오류 발생
#  - w(write)  : (  ) 모드, 파일이 없으면 새로 만들고
#                이미 있으면 기존 내용을 모두 삭제한 후 새로 작성
#  - a(append) : (  ) 모드, 기존 내용을 유지한 채 뒤에 내용을 추가
#
#  - 한글이 깨지지 않도록 encoding="utf-8"을 함께 지정한다.
#  - 파일을 다 사용하면 반드시 (  )로 닫아준다.
# ===========================================================


# ===========================================================
#  2. 파일 쓰기
#  - 형식) f.write("문자열")
#  - write()는 줄바꿈을 자동으로 해주지 않으므로 ( )를 직접 넣어야 한다.
# ===========================================================

# f = ( )(FILE_PATH, "w", encoding="utf-8")     # 파일 오픈
# f.( )("hello python\n")                       # 파일 쓰기
# f.( )("안녕 파이썬\n")
# f.( )()                                       # 반드시 닫아주기


# ===========================================================
#  3. with문 사용하기
#  - 형식) with open(경로, 모드, encoding="utf-8") as f:
#              read/write
#  - with 블록을 벗어나면 파일이 자동으로 닫힌다. (close() 불필요)
#  - 실수로 close()를 빼먹는 것을 막아주므로 with문 사용을 권장
# ===========================================================

# ( ) open(FILE_PATH, "w", encoding="utf-8") as f:
#     f.write("hello python2\n")
#     f.write("안녕 파이썬2\n")


# ===========================================================
#  4. 파일 읽기
#  - read()      : 전체를 하나의 ( 문자열 )로 읽기
#  - readlines() : 한 줄씩 읽어 ( 리스트 )에 담기 (각 줄 끝에 \n 포함)
#  - for문       : 파일 객체를 반복하며 한 줄씩 읽기 (가장 많이 쓰임)
# ===========================================================

# with open(FILE_PATH, "r", encoding="utf-8") as f:
#     content = f.( )()                  # 전체를 하나의 문자열로
#     print(content)

# with open(FILE_PATH, "r", encoding="utf-8") as f:
#     lines = f.( )()               # 한 줄씩 읽어 리스트에 담음 (각 줄 끝에 \n 포함)
#     print(lines)

# with open(FILE_PATH, "r", encoding="utf-8") as f:
#     for line in f:                      # 파일 객체의 반복자 이용 (가장 많이 쓰임)
#         print(line.( )())             # 줄바꿈 제거


# ===========================================================
#  5. 쓰기 모드 비교
#  - w 모드: 파일 없으면 새로 생성, 있으면 내용 삭제하고 새로 씀
#  - a 모드: 파일 없으면 새로 생성, 있으면 기존 내용 뒤에 추가
# ===========================================================

# 실행 결과 예상해보기
# with open(FILE_PATH, "w", encoding="utf-8") as f:
#     f.write("첫 번째 줄\n")

# with open(FILE_PATH, "w", encoding="utf-8") as f:
#     f.write("두번째 줄\n")

# with open(FILE_PATH, "r", encoding="utf-8") as f:
#     print(f.read())

# with open(FILE_PATH, "a", encoding="utf-8") as f:
#     f.write("세번째 줄\n")

# with open(FILE_PATH, "r", encoding="utf-8") as f:
#     print(f.read())


# ===========================================================
#  6. 파일이 없을 때 예외 처리
#  - r 모드로 없는 파일을 열면 FileNotFoundError 예외가 발생한다.
#  - try-except로 예외 처리하기
# ===========================================================

# with open(os.path.join(BASE_DIR, "hello.txt"), "r", encoding="utf-8") as f:
#     print(f.read())
