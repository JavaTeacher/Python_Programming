# 파인 튜닝한 이미지 분류 모델 불러오기

import os
from PIL import Image
from transformers import pipeline

# ===========================================================
#  1. 모델 불러오기
#  - 파인 튜닝하고 저장한 이미지 분류 모델을 불러와서 사용
#  - 새로운 이미지를 넣으면 이미지 분류와 확신 정도(score)를 출력
#  - 내가 만든 모델을 허깅페이스에 올려서 공유할 수도 있음
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(BASE_DIR, "model", "my_image_model")

# 모델 이름 대신 내 폴더 경로를 넣음 (허깅페이스에서 내려받지 않고 내 PC의 파일을 사용)
classifier = pipeline("image-classification", model=save_dir)

# 테스트 데이터
path = os.path.join(BASE_DIR, "images", "poby.jpg")

for result in classifier(Image.open(path).convert("RGB")):
    print(f"{result['label']} ({result['score']:.2f})")
