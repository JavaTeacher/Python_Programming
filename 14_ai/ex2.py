# 모델 파인 튜닝하기 (텍스트 분류 모델)

import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ===========================================================
#  1. 패키지 목록
#  - torch : PyTorch 딥러닝 라이브러리
#  - AutoTokenizer : 문장을 모델이 읽을 수 있는 숫자로 바꾸는 도구
#  - AutoModelForSequenceClassification : 문장 하나를 통째로 읽고 범주 하나로 분류하는 모델
#  - 예시) "국이 너무 짜요" → [AutoTokenizer] → 숫자 → [AutoModelForSequenceClassification] → 부정/긍정
#  
#  [설치]
#  - pip install transformers torch
# ===========================================================

# ===========================================================
#  2. 파인 튜닝(Fine-tuning)이란?
#  - 사전 학습(pre-trained)된 모델을 내 데이터로 조금 더 학습시켜서 내 목적에 맞게 고치는 것
#  - 처음부터 학습하는 것보다 데이터도 적게 필요하고 시간도 짧음
#
#  [비유]
#  - 한국어를 이미 잘하는 사람(기존 모델)에게 "급식 리뷰 긍정/부정 구분"만 따로 가르치는 것
#
#  [순서]
#  1) 데이터 준비하기
#  2) 기존 모델과 토크나이저 불러오기
#  3) 모델 학습하기 (예측 -> 오차 -> 수정 반복)
#  4) 학습한 모델을 저장하고 다시 불러서 사용하기
# ===========================================================

# ===========================================================
#  3. 우리가 만들 모델
#  - 한국어 급식 리뷰를 읽고 긍정(1) / 부정(0) 으로 분류
#  - KoELECTRA : 한국어 문장을 학습한 작은 모델 (영어 모델은 한국어를 구분하지 못함)
#  - 긍정, 부정 리뷰 각 50개씩 (학습용: 40개, 테스트용: 10개)
# ===========================================================

# ===========================================================
#  4. 데이터 준비하기
#  - (리뷰, 정답) 형태 -> 정답은 0(부정) 또는 1(긍정)
#  - 불러온 문장을 번갈아 배치
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "data", "positive.json"), encoding="utf-8") as f:
    positive = json.load(f)

with open(os.path.join(BASE_DIR, "data", "negative.json"), encoding="utf-8") as f:
    negative = json.load(f)

# 긍정, 부정을 번갈아 합치기
data = []
for good, bad in zip(positive, negative):
    data.append((good, 1))
    data.append((bad, 0))

print(data[:5])


# ===========================================================
#  5. 학습용 / 평가용 데이터 나누기
#  - 학습용 데이터 (train) : 모델이 공부하는 데이터
#  - 평가용 데이터 (test)  : 모델이 한 번도 못 본 데이터. 시험 문제 역할
#  - 5번째마다 평가용(test)으로 따로 빼고, 나머지는 학습용(train)으로 사용
#
#  [데이터를 나누는 이유]
#  - 학습에 쓴 문장으로 시험을 보면 모델이 답을 외웠는지, 진짜 이해했는지 알 수 없음
#  - 처음 보는 문장도 맞혀야 진짜 실력 (= 일반화)
#  - 학습 정확도는 높은데 평가 정확도가 낮으면 외우기만 한 것 (= 과적합)
#
#  [주의]
#  - 평가용 데이터는 학습에 절대 사용하지 않음
# ===========================================================

# # 5번째마다 평가용, 나머지는 학습용
# train_data = [d for i, d in enumerate(data) if i % 5 != 4]
# test_data = [d for i, d in enumerate(data) if i % 5 == 4]

# print(f"학습용 {len(train_data)}개 / 평가용 {len(test_data)}개")


# ===========================================================
#  6. 기존 모델 불러오기
#  - from_pretrained(모델이름) : 허깅페이스에서 이미 학습된 모델을 내려받아 불러옴
#    (최초 1회 다운로드, 이후에는 내 PC에 저장된 캐시 사용)
#  - AutoTokenizer : 문장을 모델이 읽을 수 있는 숫자로 바꾸는 도구
#  - AutoModelForSequenceClassification : 문장 하나를 통째로 읽고 범주 하나로 분류하는 모델
#  - id2label : 분류할 범주가 2개(부정, 긍정)라는 것을 모델에 알려줌
# ===========================================================

# model_name = "monologg/koelectra-small-v3-discriminator"        # 허깅페이스 모델 이름 (한국어 KoELECTRA small)

# tokenizer = AutoTokenizer.from_pretrained(model_name)           # 토크나이저 불러오기
# model = AutoModelForSequenceClassification.from_pretrained(     # KoELECTRA 본체 + 긍정/부정 분류용 층
#     model_name,
#     id2label={0: "부정", 1: "긍정"},         # 분류개수와 출력이름 지정
# )


# ===========================================================
#  7. 데이터 변환하기
#  - (문장, 정답) 목록을 모델에 넣을 수 있는 형태로 바꾸기
#  - 문장 -> 숫자 텐서, 정답 -> 정수 텐서로 바꿈
#  - 모델이 계산하는 데이터는 전부 텐서(Tensor)여야 함
#  - 텐서 : 숫자를 담은 다차원 배열로 PyTorch가 계산하는 데이터의 기본 단위임
# ===========================================================
# def make_dataset(data):
#     texts = [text for text, label in data]                  # 리뷰 문장만 모음
#     labels = torch.tensor([label for text, label in data])  # 정답(0/1)만 모아 텐서로 변환

#     # padding=True : 가장 긴 문장에 맞춰 짧은 문장을 채워서 길이를 같게 만듦
#     # return_tensors="pt" : 결과를 PyTorch 텐서로 받음
#     inputs = tokenizer(texts, padding=True, return_tensors="pt")    # 문장 -> 숫자
#     return inputs, labels


# # 학습용, 평가용 데이터를 각각 숫자로 변환
# train_inputs, train_labels = make_dataset(train_data)
# test_inputs, test_labels = make_dataset(test_data)


# ===========================================================
#  8. 정확도 확인하기
#  - predict : 문장들의 범주 번호(0: 부정 / 1: 긍정)를 예측
#  - accuracy : 예측한 번호가 정답과 얼마나 맞는지 비율로 계산
# ===========================================================

# def predict(inputs):
#     model.eval()                                    # 평가 모드
#     with torch.no_grad():                           # 학습하지 않고 예측만 하기
#         logits = model(**inputs).logits             # 문장 숫자를 모델에 넣고 분류 점수(logits)만 꺼내기
#     return logits.argmax(dim=1)                     # 점수가 높은 쪽을 선택


# def accuracy(inputs, labels):
#     return (predict(inputs) == labels).float().mean().item()


# print()
# print("[학습 전]")
# print(f"학습용 정확도 : {accuracy(train_inputs, train_labels):.0%}")
# print(f"평가용 정확도 : {accuracy(test_inputs, test_labels):.0%}")


# ===========================================================
#  9. 학습하기
#  - 학습용 데이터로 모델의 값(가중치)을 조금씩 고쳐서 정답을 더 잘 맞히게 만드는 과정
#  - 예측 -> 오차 -> 수정 반복
#    1) 예측 : 모델이 문장을 보고 부정 / 긍정 점수를 계산
#    2) 오차 : 예측과 정답이 얼마나 다른지 계산 (loss, 작을수록 좋음)
#    3) 수정 : 오차가 줄어드는 방향으로 모델의 값을 조금 고침
#  - epoch : 학습 데이터 전체를 한 번 학습하는 것
#  - 옵티마이저(optimizer) : 모델의 값을 고쳐주는 도구 (AdamW)
#  - lr(learning rate, 학습률) : 한 번에 고치는 크기
#    (너무 크면 정답을 지나쳐 학습이 불안정하고, 너무 작으면 학습이 느림)
# ===========================================================

# # 옵티마이저 생성 : model.parameters() = 학습으로 고쳐질 모델의 모든 값, lr = 학습률
# optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

# print()
# print("[학습]")
# for epoch in range(1, 31):                          # 30번 반복
#     model.train()                                   # 학습 모드
#     # 정답(labels)를 함께 넣으면 모델이 예측 점수(logits)와 함께 오차(loss)도 계산해줌
#     outputs = model(**train_inputs, labels=train_labels)
#     loss = outputs.loss                             # 오차 (텐서)

#     optimizer.zero_grad()                           # 이전 기울기 지우기
#     loss.backward()                                 # 기울기 계산
#     optimizer.step()                                # 값 고치기

#     print(f"epoch {epoch:2d} | loss = {loss.item():.3f}")
#     # -> 반복할수록 loss 가 줄어들면 학습이 잘 되고 있는 것

# print()
# print("[학습 후]")
# print(f"학습용 정확도 : {accuracy(train_inputs, train_labels):.0%}")    # 공부한 문장으로 본 시험
# print(f"평가용 정확도 : {accuracy(test_inputs, test_labels):.0%}")      # 처음 보는 문장으로 본 시험


# ===========================================================
#  10. 모델 저장하기
#  - 파인 튜닝한 모델은 지금 메모리에만 있어서 프로그램을 끄면 사라짐
#  - 파일로 저장해두면 다시 학습하지 않고 불러서 사용할 수 있음
#  - 모델과 토크나이저 두개 파일을 저장
#  - 모델 : 학습으로 고쳐진 값(가중치) + 설정(분류 개수, 부정 / 긍정 이름 등)
#  - 토크나이저 : 모델이 학습한 숫자 규칙을 저장
# ===========================================================

# save_dir = os.path.join(BASE_DIR, "model", "my_sentiment_model")

# model.save_pretrained(save_dir)         # 학습한 모델 저장 (고쳐진 가중치 + 설정)
# tokenizer.save_pretrained(save_dir)     # 토크나이저 저장 (모델과 같은 폴더에)
