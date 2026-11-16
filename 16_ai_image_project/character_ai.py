# AI 모듈
# - 파인 튜닝한 이미지 분류 모델로 이미지를 뽀로로 / 크롱 / 포비로 분류

import os
from transformers import pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# ===========================================================
#  1. 준비하기
# ===========================================================
classifier = None      # 모델은 처음 사용할 때 한 번만 불러옴

MIN_SCORE = 0.6


# ===========================================================
#  2. 이미지 분류
#  - 모델을 불러오는 데 몇 초 걸리므로 처음 한 번만 불러서 계속 사용
# ===========================================================

def classify(image):
    global classifier
    if classifier is None:
        classifier = pipeline("image-classification", model=MODEL_DIR)
    result = classifier(image, top_k=1)[0]
    return result["label"], result["score"]
