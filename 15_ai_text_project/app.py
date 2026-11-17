# AI + DB + Web 연동 프로젝트 실습 : 급식 리뷰 분석
# - 나이스 급식 API 조회 -> 리뷰 작성 -> AI가 긍정 / 부정 분류 -> DB 리뷰 저장 -> DB 리뷰 검색

# ===========================================================
#  [모듈 구성]
#  - app.py : 메인 모듈 (웹 화면)
#  - meal_api.py : Open API 호출
#  - meal_db.py : 급식 DB 처리
#  - review_ai.py : 리뷰 긍정/부정 분류
#  - review_db.py : 리뷰 DB 처리
# ===========================================================

import streamlit as st
import pandas as pd
from datetime import date

import meal_db
import review_ai, review_db
from meal_api import get_food_info


# ===========================================================
#  1. 급식 조회
# ===========================================================

try:
    st.title("🍚 급식 조회 + 리뷰 분석 앱")
    COLUMNS = ["일자", "구분", "메뉴", "칼로리"]

    st.header("1. 급식 조회")
    selected = st.date_input("조회일자", value=date.today())

    # DB 초기화
    if "init_db" not in st.session_state:
        st.session_state.init_db = True
        meal_db.init_db()
        review_db.init_db()


    if st.button("급식 조회하기"):
        ymd = selected.strftime("%Y%m%d")
        st.session_state.ymd = ymd

        # DB에 없는 경우 API 호출 후 DB 저장
        if not meal_db.load_meals(ymd):
            api_rows = get_food_info(ymd)

            if api_rows:
                meal_db.save_meal(api_rows)
                print(f"{ymd} 급식 {len(api_rows)}건을 DB에 저장했습니다.")


    if "ymd" in st.session_state:
        ymd = st.session_state.ymd

        # 급식 정보 조회
        rows = meal_db.load_meals(ymd)

        if not rows:
            st.info("해당 일자의 급식 정보가 없습니다.")
        else:
            df = pd.DataFrame(rows, columns=COLUMNS)
            st.dataframe(df, hide_index=True)


# ===========================================================
#  2. 리뷰 작성
#  - st.form : 입력창과 저장 버튼을 묶어서, 저장 버튼을 눌렀을 때만 한 번에 처리
#  - clear_on_submit=True : 저장하면 입력창을 비움
#
#  [저장 버튼 클릭]
#  1) AI 가 긍정 / 부정과 확률을 계산
#  2) 리뷰, 분류, 확률을 DB에 저장
# ===========================================================

            st.divider()
            st.header("2. 리뷰 작성")

            with st.form("review_form", clear_on_submit=True):
                content = st.text_input("오늘 급식은 어땠나요?", placeholder="예) 돈가스가 바삭하고 맛있었어요")
                submitted = st.form_submit_button("저장")

            if submitted:
                content = content.strip()

                if not content:
                    st.warning("리뷰 내용을 입력해 주세요.")
                else:
                    with st.spinner("분류하는 중..."):
                        label, score = review_ai.classify(content)

                    # 리뷰 저장
                    review_db.save_review(ymd, content, label, score)
                    st.success(f"저장했습니다. AI 분류 : {label} ({score:.0%})")

            st.divider()


# ===========================================================
#  3. 리뷰 검색
#  - 분류(전체 / 긍정 / 부정)와 날짜 조건으로 DB 에서 검색
# ===========================================================

            st.header("3. 리뷰 검색")

            search_label = st.radio("분류", ["전체", "긍정", "부정"], horizontal=True)

            # 리뷰 조회
            review_rows = review_db.load_reviews(
                ymd,
                label=None if search_label == "전체" else search_label
            )

            # 리뷰 DataFrame
            review_df = pd.DataFrame(
                review_rows,
                columns=["번호", "일자", "리뷰", "분류", "확률", "작성시각"]
            )

            st.dataframe(review_df, width="stretch", hide_index=True)


except Exception as e:
    st.error(f"실행 중 오류가 발생했습니다.")
    print(f"에러 메시지: {e}")
