# Open API + DB + Web 연동 프로젝트 실습

# ===========================================================
#  [모듈 구성]
#  - app.py : 메인 모듈 (웹 화면)
#  - meal_api.py : Open API 호출
#  - meal_db.py : DB 처리
# ===========================================================

# ===========================================================
#  [실행 순서]
#  - 일자 선택 -> [급식 조회하기] 버튼
#  - 먼저 DB 조회, DB에 없으면 API 호출 후 DB 저장
#  - 화면에 급식 정보 출력
# ===========================================================

import streamlit as st
import pandas as pd
from datetime import date

import meal_db
from meal_api import get_food_info

try:
    st.title("🍚 급식 조회 앱")
    COLUMNS = ["일자", "구분", "메뉴", "칼로리"]

    selected = st.date_input("조회일자", value=date.today())

    # DB 초기화
    if "init_db" not in st.session_state:
        st.session_state.init_db = True
        meal_db.init_db()

    if st.button("급식 조회하기"):
        ymd = selected.strftime("%Y%m%d")

        # DB에서 급식 정보 조회
        rows = meal_db.load_meals(ymd)

        if not rows:
            # DB에 없는 경우 API 호출
            rows = get_food_info(ymd)
            if not rows:
                st.info("해당 일자의 급식 정보가 없습니다.")
            else:
                meal_db.save_meal(rows)
                print(f"{ymd} 급식 {len(rows)}건을 DB에 저장했습니다.")

        # 급식 정보 출력
        if rows:        
            st.divider()
            df = pd.DataFrame(rows, columns=COLUMNS)
            st.dataframe(df, hide_index=True)

except Exception as e:
    st.error(f"급식 정보를 가져오지 못했습니다.")
    print(f"에러 메시지: {e}")
