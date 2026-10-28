# streamlit 기초

import time
import pandas as pd
import streamlit as st

# ===========================================================
#  0. Streamlit이란?
#  - 파이썬만으로 웹앱을 만들 수 있는 오픈소스 프레임워크 (https://streamlit.io/)
#  - HTML, CSS, JavaScript를 몰라도 데이터 앱을 빠르게 제작 가능
#  - 데이터 분석, 시각화, AI 모델 데모 화면에 많이 사용
#
#  [특징]
#  - 위에서 아래로 실행되는 스크립트가 곧 화면이 됨
#  - 위젯(버튼, 슬라이더 등)을 조작하면 스크립트 전체가 처음부터 다시 실행됨
#  - 코드를 저장하면 브라우저에서 자동으로 새로고침(Rerun) 가능
#
#  [설치와 실행방법]
#  - 설치) pip install streamlit
#  - 실행) streamlit run 파일명.py
#  - 접속) http://localhost:8501
# ===========================================================


# ===========================================================
#  1. 텍스트 출력하기
#  - st.title()    : 제목
#  - st.header()   : 헤더
#  - st.subheader(): 서브헤더
#  - st.text()     : 일반 텍스트
#  - st.markdown() : 마크다운 문법
#  - st.write()    : 만능 출력 (문자열, 숫자, 표, 차트 등 자동 판단)
# ===========================================================

st.title("Streamlit 기본 문법")

# st.divider()    # 구분선

# st.header("1. 텍스트 출력")
# st.subheader("서브헤더")

# st.text("텍스트")
# st.markdown("마크다운, **굵게**, *기울임*")
# st.write(1234, [1, 2, 3])
# st.text("1234")

# st.divider()    # 구분선


# ===========================================================
#  2. 데이터 출력하기
#  - st.dataframe(): 정렬/스크롤이 되는 표
#  - st.table()    : 고정된 표
#  - st.json()     : JSON 출력
# ===========================================================

# st.header("2. 데이터 출력")

# df = pd.DataFrame({
#     "이름": ["홍길동", "김철수", "이영희"],
#     "국어": [90, 80, 70],
#     "영어": [85, 95, 75],
# })

# st.dataframe(df)
# st.table(df)
# st.json(df.to_dict())

# st.divider()


# ===========================================================
#  3. 차트 그리기
#  - st.line_chart() : 선 그래프
#  - st.bar_chart()  : 막대 그래프
# ===========================================================

# st.header("3. 차트")

# chart_df = df.set_index("이름")

# st.bar_chart(chart_df)
# st.line_chart(chart_df)

# st.divider()


# ===========================================================
#  4. 입력 위젯
#  - 위젯의 반환값을 변수에 저장해서 사용
#  - st.text_input()  : 한 줄 입력
#  - st.number_input(): 숫자 입력
#  - st.slider()      : 슬라이더
#  - st.selectbox()   : 선택 상자
#  - st.radio()       : 라디오 버튼
#  - st.checkbox()    : 체크박스
#  - st.date_input()  : 날짜 선택
#  - st.button()      : 버튼 (클릭한 순간만 True)
# ===========================================================

# st.header("4. 입력 위젯")

# name = st.text_input("이름을 입력하세요")
# age = st.number_input("나이", min_value=1, max_value=100, value=17)

# grade = st.selectbox("학년", ["1학년", "2학년", "3학년"])
# gender = st.radio("성별", ["남", "여"], horizontal=True)
# agree = st.checkbox("동의합니다")

# score = st.slider("점수", 0, 100, 50)
# birth = st.date_input("날짜 선택")

# if st.button("확인"):
#     st.write(f"{name} / {age}세 / {grade} / {gender} / {score}점 / 동의: {agree} / {birth}")

# st.divider()


# ===========================================================
#  5. 상태 메시지
#  - st.success() / st.info() / st.warning() / st.error()
#  - st.spinner()  : 작업 중 로딩 표시
# ===========================================================

# st.header("5. 상태 메시지")

# st.success("성공 메시지")
# st.info("안내 메시지")
# st.warning("경고 메시지")
# st.error("에러 메시지")

# if st.button("시간 걸리는 작업 실행"):
#     with st.spinner("처리 중..."):
#         time.sleep(2)
#     st.success("완료!")

# st.divider()


# ===========================================================
#  6. 세션 상태 (st.session_state)
#  - 위젯 조작 시 스크립트가 처음부터 다시 실행되므로
#    일반 변수는 값이 초기화됨
#  - 값을 유지하려면 st.session_state에 저장
# ===========================================================

# st.header("6. 세션 상태")

# count = 0

# if st.button("카운트 증가"):
#     count += 1

# st.write(f"버튼 클릭 횟수: {count}")


# if "count" not in st.session_state:
#     st.session_state.count = 0

# if st.button("카운트 증가"):
#     st.session_state.count += 1

# st.write(f"버튼 클릭 횟수: {st.session_state.count}")
