# AI 모듈
# - 파인 튜닝한 모델로 급식 리뷰를 긍정 / 부정으로 분류

import os
from transformers import pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# ===========================================================
#  1. 준비하기
# ===========================================================
classifier = None      # 모델은 처음 사용할 때 한 번만 불러옴


# ===========================================================
#  2. 리뷰 분류
#  - classify() : 리뷰 한 건을 분류해서 (분류, 확률) 로 돌려줌
#  - 모델을 불러오는 데 몇 초 걸리므로 처음 한 번만 불러서 계속 사용
# ===========================================================

def classify(text):
    global classifier
    if classifier is None:
        classifier = pipeline("text-classification", model=MODEL_DIR)

    result = classifier(text)[0]
    return result["label"], result["score"]      # 예) ("긍정", 0.81)
