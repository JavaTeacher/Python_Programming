# AI 모듈
# - 파인 튜닝한 모델로 급식 리뷰를 긍정 / 부정으로 분류

import os
import streamlit as st
from transformers import pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# ===========================================================
#  1. 준비하기
#  - @st.cache_resource : 모델을 처음 사용할 때 한 번만 불러오고,
#    이후에는 (재실행, 다른 세션에서도) 같은 객체를 재사용
# ===========================================================

@st.cache_resource(show_spinner="모델 불러오는 중...")
def get_classifier():
    return pipeline("text-classification", model=MODEL_DIR)


# ===========================================================
#  2. 리뷰 분류
#  - classify() : 리뷰 한 건을 분류해서 (분류, 확률) 로 돌려줌
# ===========================================================

def classify(text):
    result = get_classifier()(text)[0]
    return result["label"], result["score"]      # 예) ("긍정", 0.81)
