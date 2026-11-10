# 파인 튜닝한 텍스트 생성 모델 불러오기

import os
from transformers import pipeline

# ===========================================================
#  1. 모델 불러오기
#  - 파인 튜닝하고 저장한 텍스트 생성 모델을 불러와서 사용
#  - 문장의 앞부분을 넣으면 모델이 뒷부분을 이어서 만들어냄
#  - 내가 만든 모델을 허깅페이스에 올려서 공유할 수도 있음
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(BASE_DIR, "model", "my_text_generation_model")

# 모델 이름 대신 내 폴더 경로를 넣음 (허깅페이스에서 내려받지 않고 내 PC의 파일을 사용)
generator = pipeline("text-generation", model=save_dir)


# ===========================================================
#  2. 문장 이어서 만들기
#  - generator(문장앞부분) 은 결과를 리스트로 돌려주므로 [0] 으로 첫 번째 결과를 꺼냄
#  - 결과의 generated_text : 넣은 문장 + 모델이 이어서 만든 문장
#  - do_sample=False : 매번 가장 확률이 높은 글자만 골라서 같은 입력에는 같은 결과가 나오게 함
#  - max_new_tokens=40 : 최대 40토큰까지만 만들기
# ===========================================================

# 문장의 앞부분 (학습 데이터와 같은 것도 있고, 조금 다르게 바꾼 것도 있음)
prompts = [
    "한국디지털미디어고등학교의 줄임말은",
    "디미고는 경기도",
    "디미고에는 학과가",
    "디미고 학생은",
    "디미고의 교훈은",
    "디미고는 서울",
    "디미고에서는 해킹",
]

for prompt in prompts:
    result = generator(prompt, max_new_tokens=40, do_sample=False)[0]
    print(result["generated_text"])     # 예) 디미고는 경기도 안산시에 있어요.
