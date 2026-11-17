# AI + DB + Web 연동 프로젝트 실습 : 이미지 파일 분류
# - 이미지 파일 선택 -> AI가 분류 -> DB에 분류 결과 저장 -> 이미지 검색

# ===========================================================
# [모듈 구성]
# - app.py : 메인 모듈 (웹 화면)
# - character_ai.py : 이미지 분류 모델
# - character_db.py : 분류 결과 DB 처리
# ===========================================================

import os
from datetime import datetime

import pandas as pd
import streamlit as st
from PIL import Image

import character_ai as ai
import character_db as db

# ===========================================================
#  1. 준비하기
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CAPTURE_DIR = os.path.join(DATA_DIR, "captures")

characters = {"pororo": "뽀로로", "crong": "크롱", "poby": "포비"}

try:
    st.title("🐧 이미지 파일 분류")

    # DB 초기화
    if "init_db" not in st.session_state:
        st.session_state.init_db = True
        db.init_db()


# ===========================================================
#  2. 이미지 파일 선택 -> 분류 -> DB 저장
# ===========================================================

    uploaded = st.file_uploader("분류할 이미지 파일을 선택하세요.", type=["jpg", "jpeg", "png"])

    if uploaded is None:
        st.info("이미지 파일을 선택하세요.")
    else:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, width=400)

        with st.spinner("분류하는 중..."):
            label, score = ai.classify(image)        # 확률이 가장 높은 결과

        st.subheader(f"분류 결과 : {characters[label]} ({score:.0%})")

        if st.button("DB 저장하기"):
            file = f"{label}_{datetime.now():%Y%m%d_%H%M%S}.jpg"
            image.save(os.path.join(CAPTURE_DIR, file))

            db.save_detection(label, score, file)
            st.success("저장했습니다.")


# ===========================================================
#  3. 이미지 검색
#  - 분류(전체 / 뽀로로 / 크롱 / 포비)를 고르면 DB 에서 검색해서 사진과 분류 결과를 보여줌
# ===========================================================

    st.divider()
    st.header("이미지 검색")

    choices = {"전체": None}
    for eng, kor in characters.items():
        choices[kor] = eng

    choice = st.radio("분류", list(choices), horizontal=True)

    rows = db.load_detections(name=choices[choice])

    if rows:
        df = pd.DataFrame(
            rows,
            columns=["번호", "캐릭터", "확률", "사진"]
        )

        # on_select="rerun" : 행을 선택하면 화면 코드를 다시 실행하고, 선택한 행 번호를 event로 돌려줌
        event = st.dataframe(df, width="stretch", hide_index=True, on_select="rerun", selection_mode="single-row")

        if st.button("사진 보기"):
            selected = event.selection.rows         # 선택한 행의 위치 목록

            if not selected:
                st.warning("사진을 볼 행을 선택하세요.")
            else:
                row = df.iloc[selected[0]]
                st.image(os.path.join(CAPTURE_DIR, row["사진"]), width=200)

except Exception as e:
    st.error("실행 중 오류가 발생했습니다.")
    print(f"에러 메시지: {e}")
