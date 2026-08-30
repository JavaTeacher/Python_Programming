# 문자열 내장 함수

a = "Hello, Python"

# # dir() 함수: 객체가 가지고 있는 속성과 메소드 목록을 반환하는 파이썬 내장 함수
# print()                       # str 자료형이 제공하는 속성과 메소드 목록
# print()                      # int 자료형이 제공하는 속성과 메소드 목록
# print()                      # list 자료형이 제공하는 속성과 메소드 목록

# # len() 함수: 객체의 길이를 반환하는 파이썬 내장 함수
# print()                       # 문자열의 길이
# print()               # 리스트의 길이(요소의 개수)

# # 대소문자를 변환해주는 문자열 메소드
# print()                    # 대문자로 변환
# print()                    # 소문자로 변환
# print()               # 문자열의 첫 글자만 대문자로 변환
# print()                    # 각 단어의 첫 글자만 대문자로 변환

# # 문자열의 공백문자 or 특정문자를 제거하는 문자열 메소드
# a = "\t  python  \n"
# print()
# print()       # 왼쪽 공백문자 제거
# print()       # 오른쪽 공백문자 제거
# print()        # 양쪽 공백문자 제거

# a = "***python***"
# print()                # 왼쪽 특정문자 제거
# print()                # 오른쪽 특정문자 제거
# print()                 # 양쪽 특정문자 제거


# s = "Python is fun. I love Python."

# # 부분 문자열이 처음 등장하는 위치(인덱스)를 알려주는 문자열 메소드
# print()             # 인덱스 반환
# print()            # 인덱스 반환

# print()               # 인덱스 반환 ( 없으면 )
# print()            # 인덱스 반환 ( 없으면 )

# # 부분 문자열이 몇 번 나오는지 알려주는 문자열 메소드
# print()                 # 등장 횟수

# # 문자열 포함여부를 알려주는 멤버십 연산자
# print()                # 포함(True)
# print()                  # 미포함(False)

# # 특정 Prefix로 시작하고 있는지 알려주는 문자열 메소드
# print()       # True

# # 특정 Suffix로 끝나고 있는지 알려주는 문자열 메소드
# print()         # False

# # 이전 문자열을 새로운 문자열로 치환하는 문자열 메소드
# # 문제) replace는 원본 문자열을 바꿀까요? 새로운 문자열을 만들까요?
# print()     # 전체 치환
# print()  # 1개만 치환

# # 판별 문자열 메소드 (isXXX())
# print("123")              # 숫자이면 True
# print("abc")              # 알파벳이면 True
# print("abc123")           # 알파벳 + 숫자이면 True
# print(" \t \n")           # 공백문자이면 True
# print("hello")            # 소문자이면 True
# print("HELLO")            # 대문자이면 True

# # 구분자를 기준으로 문자열을 분리하는 문자열 메소드
# a = "apple,banana,kiwi"
# fruits = None                # ","를 기준으로 분리 (기본값 공백)
# print(fruits)                       # 리스트가 만들어짐

# # Iterable(반복가능) 객체안의 문자열을 결합하는 문자열 메소드
# print()             # ","로 연결하여 결합


# =========================================================
#  🔥 실습 문제
# =========================================================

# # 1️⃣ 문자열 양쪽 공백 제거 + 대문자 변환
# s = "  hello world  "
# result = s.______().______()
# print(result)                   # ✅ "HELLO WORLD" 출력

# # 2️⃣ 이메일 형식 체크
# email = "abcd@dimigo.hs.kr"
# print(___ ___ email)            # ✅ "@dimigo.hs.kr"이 포함되어 있으면 True

# # 3️⃣ 문자열에서 특정 단어가 몇 번 등장하나?
# sentence = "the quick brown fox jumps over the lazy dog"
# print(sentence._____("the"))    # ✅ 2 출력

# # 4️⃣ 공백문자를 기준으로 문자열을 리스트로 나누고, 다시 문자열로 결합하기
# data = "   kim   lee   park   choi   "
# names = data._____()
# print(names)                    # ✅ 리스트 출력
# print(___.____(names))          # ✅ "kim lee park choi" 출력
