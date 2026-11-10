# 허깅페이스 이미지 분류 모델 사용하기

import os
from dotenv import load_dotenv

from PIL import Image
from transformers import pipeline

# ===========================================================
#  1. 이미지 분류(Image Classification)란?
#  - 사진 한 장을 보고 어떤 종류인지 맞히는 것 (예: 강아지 / 고양이 / 자동차)
#  - 결과는 label(종류 이름) + score(확률, 0~1)로 나옴
#  - 텍스트 감정 분류와 사용법이 같고, 입력이 문장 대신 이미지일 뿐임
#
#  [설치]
#  - pip install transformers pillow
# ===========================================================

# ===========================================================
#  2. 파이프라인 방식
#  - pipeline("작업이름", model="모델이름")으로 모델을 불러옴
#  - 작업이름 : image-classification
#  - 모델이름 : 허깅페이스 > Models > Tasks에서 검색
#
#  [사용 모델]
#  - ViT(Vision Transformer)
#    · 글(문장)을 단어 단위로 읽는 트랜스포머를 이미지에 적용한 모델 (2020년 구글 발표)
#    · 퍼즐 조각을 하나씩 보는 게 아니라, 조각들의 관계를 함께 보고 그림을 맞히는 것
#    · 동작 순서
#      1) 이미지를 작은 정사각형 조각(patch)으로 자름  (예: 224x224 이미지 -> 16x16 조각 196개)
#      2) 각 조각을 숫자 목록(벡터)으로 바꾸고, 조각의 위치 정보를 더함
#      3) 조각들끼리 서로 어떤 관계인지 파악 (예: 귀 조각 + 눈 조각 + 코 조각 -> 강아지 얼굴)
#      4) 이미지 전체를 요약한 값으로 종류별 확률을 계산
#    · 모델 이름 읽기 : google/vit-base-patch16-224
#      - base : 모델 크기 (small < base < large)
#      - patch16 : 조각 크기 16x16 픽셀
#      - 224 : 입력 이미지 크기 224x224 (다른 크기의 사진은 자동으로 크기를 맞춤)
#    · ImageNet의 1000가지 종류를 구분하도록 학습되어 있음 (https://deeplearning.cms.waikato.ac.nz/user-guide/class-maps/IMAGENET/)
# ===========================================================

load_dotenv()
token = os.getenv("HF_TOKEN")

# print("1. 파이프라인 : 이미지 분류")

# classifier = pipeline(
#     "image-classification",
#     model="google/vit-base-patch16-224",
#     token=token
# )

# results = classifier("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/hub/parrots.png")
# for result in results:
#     print(f"{result['label']} ({result['score']:.2f})")
# print()


# # 강아지 사진 분류하기
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# image = Image.open(os.path.join(BASE_DIR, "images", "dog.jpg"))   # 분류하고 싶은 이미지 파일 경로
# results = classifier(image, top_k=3)    # 확률이 높은 3개만 보기

# for result in results:
#     print(f"{result['label']} ({result['score']:.2f})")
# print()


# # 고양이 사진 분류하기
# image = Image.open(os.path.join(BASE_DIR, "images", "cat.jpg"))
# results = classifier(image, top_k=3)

# for result in results:
#     print(f"{result['label']} ({result['score']:.2f})")
# print()


# # 뽀로로, 크롱, 포비 사진은?
# image = Image.open(os.path.join(BASE_DIR, "images", "pororo.jpg"))
# results = classifier(image, top_k=3)    # 확률이 높은 3개만 보기

# for result in results:
#     print(f"{result['label']} ({result['score']:.2f})")
# print()
