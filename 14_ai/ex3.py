# 파인 튜닝한 텍스트 분류 모델 불러오기

import os
from transformers import pipeline

# ===========================================================
#  1. 모델 불러오기
#  - 파인 튜닝하고 저장한 급식 리뷰 감정 분류 모델을 불러와서 사용
#  - 새로운 문장을 넣으면 부정 / 긍정 과 확신 정도(score)를 출력
#  - 내가 만든 모델을 허깅페이스에 올려서 공유할 수도 있음
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(BASE_DIR, "model", "my_sentiment_model")

# 모델 이름 대신 내 폴더 경로를 넣음 (허깅페이스에서 내려받지 않고 내 PC의 파일을 사용)
classifier = pipeline("text-classification", model=save_dir)


# ===========================================================
#  2. 문장 분류하기
#  - 학습에 사용하지 않은 새로운 문장으로 확인
#  - 결과 : label(부정 / 긍정) + score(확률, 0~1)
# ===========================================================

# 분류할 문장 (긍정, 부정이 섞여 있음)
sentences = [
    "오늘 급식 정말 끝내주게 맛있었어요",
    "된장찌개가 너무 짰어요",
    "치킨이 바삭바삭하고 간도 적당했어요",
    "스파게티 면이 안 익었어요"
]

for sentence in sentences:
    result = classifier(sentence)[0]    # {'label': '긍정', 'score': 0.98} 형태의 결과 중 첫 번째
    print(f"{result['label']} ({result['score']:.2f}) : {sentence}")    # 예) 긍정 (0.98) : 문장
