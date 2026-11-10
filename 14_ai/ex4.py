# 모델 파인 튜닝하기 (텍스트 생성 모델)

import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ===========================================================
#  1. 패키지 목록
#  - torch : PyTorch 딥러닝 라이브러리
#  - AutoTokenizer : 문장을 모델이 읽을 수 있는 숫자로 바꾸는 도구
#  - AutoModelForCausalLM : 앞 글자들을 보고 다음 글자를 이어서 만들어내는 텍스트 생성 모델
#  - 예시) "디미고는" → [AutoTokenizer] → 숫자 → [AutoModelForCausalLM] → "경기도 안산시에 있어요."
#
#  [설치]
#  - pip install transformers torch
# ===========================================================

# ===========================================================
#  2. 우리가 만들 모델
#  - 현재 모델은 한국디지털미디어고에 대해 잘 모름
#  - 디미고 관련 문장 50개로 파인 튜닝해서 디미고에 대한 문장을 이어서 쓰게 만들기
#  - 문장 50개를 학습용 40개 / 평가용 10개로 나누어서 학습 전후를 비교
#
#  [텍스트 분류와 다른 점]
#  - 분류 : 문장 하나 -> 정답 하나(긍정/부정)를 맞히도록 학습
#  - 생성 : 문장의 앞부분 -> 바로 다음 글자(토큰)를 맞히도록 학습
#  - 따라서 별도의 정답(label)이 필요 없고, 문장 자체가 정답이 됨
#    (예: "디미고는 경기도 안산시에 있어요."를 보고 "디미고는" 다음에 "경기도"가 나오도록 학습)
#
#  [순서]
#  1) 학습 데이터 준비하고 학습용 / 평가용으로 나누기
#  2) 기존 모델과 토크나이저 불러오기
#  3) 모델 학습하기 (예측 -> 오차 -> 수정 반복)
#  4) 학습한 모델을 저장하고 다시 불러서 사용하기
# ===========================================================

# ===========================================================
#  3. 학습용 / 평가용 데이터 나누기
#  - data/dimigo.json : 디미고 관련 단문 50개
#  - 학습용 데이터 (train) : 모델이 공부하는 데이터
#  - 평가용 데이터 (test)  : 모델이 한 번도 못 본 데이터. 시험 문제 역할
#  - 5번째마다 평가용(test)으로 따로 빼고, 나머지는 학습용(train)으로 사용
#
#  [주의]
#  - 평가용 데이터는 학습에 절대 사용하지 않음
#  - 같은 내용을 다르게 쓴 문장이 학습용에 있으면 평가 정확도가 높게 나올 수 있음
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "data", "dimigo.json"), encoding="utf-8") as f:
    sentences = json.load(f)

# 5번째마다 평가용, 나머지는 학습용
train_sentences = [s for i, s in enumerate(sentences) if i % 5 != 4]
test_sentences = [s for i, s in enumerate(sentences) if i % 5 == 4]

print(f"학습용 {len(train_sentences)}개 / 평가용 {len(test_sentences)}개")


# ===========================================================
#  4. 기존 모델 불러오기
#  - from_pretrained(모델이름) : 허깅페이스에서 이미 학습된 모델을 내려받아 불러옴
#    (최초 1회 다운로드, 이후에는 내 PC에 저장된 캐시 사용)
#  - AutoTokenizer : 문장을 모델이 읽을 수 있는 숫자로 바꾸는 도구
#  - AutoModelForCausalLM : 다음 글자를 이어서 만들어내는 텍스트 생성 모델
#
#  - dtype=torch.float32 : 학습할 때는 숫자를 정밀하게(32비트) 다뤄야 함
# ===========================================================

# model_name = "Qwen/Qwen2.5-0.5B-Instruct"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name, dtype=torch.float32)


# ===========================================================
#  5. 데이터 변환하기
#  - 문장 목록을 모델에 넣을 수 있는 형태로 바꾸기
#  - 모델이 문장 끝을 알 수 있도록 문장 끝에 종료 토큰(eos)을 붙임
#
#  - 문장 -> 숫자 텐서 (input_ids), 정답(labels)은 입력 숫자를 그대로 복사해서 사용
#    모델이 알아서 한 칸씩 밀어서 "앞 글자 -> 다음 글자" 로 비교해줌
#  - padding=True : 가장 긴 문장에 맞춰 짧은 문장을 채워서 길이를 같게 만듦
#  - 채워 넣은 칸(padding)은 정답이 아니므로 오차 계산에서 제외
# ===========================================================

# def make_dataset(sentences):
#     texts = [sentence + tokenizer.eos_token for sentence in sentences]      # 문장 끝에 종료 토큰 붙이기

#     # return_tensors="pt" : 결과를 PyTorch 텐서로 받음
#     inputs = tokenizer(texts, padding=True, return_tensors="pt")            # 문장 -> 숫자

#     # inputs["input_ids"] : 모델에 넣을 토큰값
#     # inputs["attention_mask"] : 실제 토큰과 패딩의 위치 구분 (패딩은 0으로 표시)
#     labels = inputs["input_ids"].clone()                                    # 텐서 복사 (원본 유지)
#     labels[inputs["attention_mask"] == 0] = -100                            # 패딩으로 채워 넣은 칸은 오차 계산 제외
#     return inputs, labels


# # 학습용, 평가용 데이터를 각각 숫자로 변환
# train_inputs, train_labels = make_dataset(train_sentences)
# test_inputs, test_labels = make_dataset(test_sentences)

# # 한 번에 처리할 문장 수 (한꺼번에 처리하면 메모리를 많이 쓰므로 나눠서 처리)
# batch_size = 10


# ===========================================================
#  6. 정확도 확인하기
#  - 다음 토큰 정확도 : 앞 토큰들을 보고 예측한 다음 토큰이 실제 다음 토큰과 같은 비율
#  - 문장 전체를 모델에 넣고 위치마다 "다음 토큰"을 예측한 값과 정답을 비교
#    (예: 디미고는 -> 경기도 / 디미고는 경기도 -> 안산시에 / ...)
#
#  - generate : 입력한 문장 뒤에 이어질 글자를 모델이 만들어냄
#  - do_sample=False : 매번 가장 확률이 높은 글자만 골라서 같은 입력에는 같은 결과가 나오게 함
#  - max_new_tokens=40 : 최대 40토큰까지만 만들기
# ===========================================================

# def accuracy(inputs, labels):
#     model.eval()                                                            # 평가 모드
#     correct, total = 0, 0
#     with torch.no_grad():                                                   # 학습하지 않고 예측만 하기
#         for i in range(0, len(labels), batch_size):
#             logits = model(
#                 input_ids=inputs["input_ids"][i:i + batch_size],
#                 attention_mask=inputs["attention_mask"][i:i + batch_size],
#             ).logits                                                        # 위치마다 다음 토큰의 분류 점수
#             predicted = logits[:, :-1].argmax(dim=-1)                       # 각 위치에서 예측한 다음 토큰
#             answer = labels[i:i + batch_size][:, 1:]                        # 실제 다음 토큰 (한 칸씩 밀어서 비교)
#             mask = answer != -100                                           # 패딩 칸은 제외
#             correct += (predicted[mask] == answer[mask]).sum().item()
#             total += mask.sum().item()
#     return correct / total


# def generate(prompt):
#     model.eval()                                                        # 평가 모드
#     prompt_inputs = tokenizer(prompt, return_tensors="pt")              # 입력 문장을 숫자 텐서로 변환
#     with torch.no_grad():                                               # 학습하지 않기
#         # 디미고는 경기도 -> 디미고는 경기도 안산 -> 디미고는 경기도 안산에 -> 디미고는 경기도 안산에 있습니다.
#         output = model.generate(                                        # 입력 뒤에 이어지는 토큰 생성
#             **prompt_inputs,
#             max_new_tokens=40,                                          # 새로 생성할 토큰 수 제한
#             do_sample=False,
#             pad_token_id=tokenizer.pad_token_id,
#         )
#     return tokenizer.decode(output[0], skip_special_tokens=True)


# # 평가용 문장의 앞부분(두 단어)만 주고 뒷부분을 만들게 하기 (학습에 쓰지 않은 문장)
# prompts = [" ".join(sentence.split()[:2]) for sentence in test_sentences]


# def show_generated():
#     for prompt, sentence in zip(prompts, test_sentences):
#         print(f"{prompt} -> {generate(prompt)}")
#         print(f"    (원래 문장) {sentence}")


# print()
# print("[학습 전]")
# print(f"학습용 정확도 : {accuracy(train_inputs, train_labels):.0%}")
# print(f"평가용 정확도 : {accuracy(test_inputs, test_labels):.0%}")
# show_generated()


# ===========================================================
#  7. 학습하기
#  - 학습용 데이터로 모델의 값(가중치)을 조금씩 고쳐서 문장을 더 잘 이어서 쓰게 만드는 과정
#  - 예측 -> 오차 -> 수정 반복
#    1) 예측 : 모델이 앞 글자들을 보고 다음 글자를 예측
#    2) 오차 : 예측과 실제 다음 글자가 얼마나 다른지 계산 (loss, 작을수록 좋음)
#    3) 수정 : 오차가 줄어드는 방향으로 모델의 값을 조금 고침
#  - batch : 데이터를 작게 나눈 묶음. 한 묶음씩 학습 (여기서는 10문장씩)
#  - epoch : 학습 데이터 전체를 한 번 학습하는 것 (여기서는 10번 반복)
#  - 옵티마이저(optimizer) : 모델의 값을 고쳐주는 도구 (AdamW)
#  - lr(learning rate, 학습률) : 한 번에 고치는 크기
#    (너무 크면 기존에 알던 내용을 잊어버리고, 너무 작으면 학습이 느림)
#  - 학습은 학습용 데이터로만 하고, 평가용 데이터는 정확도 확인에만 사용
# ===========================================================

# # 단어 사전(embedding) 가중치는 고정하고 나머지만 학습
# model.get_input_embeddings().weight.requires_grad = False

# # 학습할 모델의 가중치 준비
# trainable = [p for p in model.parameters() if p.requires_grad]

# # 옵티마이저 생성 : 학습으로 고쳐질 모델의 값만 전달, lr = 학습률
# optimizer = torch.optim.AdamW(trainable, lr=2e-5)

# print()
# print("[학습]")
# for epoch in range(1, 11):
#     model.train()                                   # 학습 모드
#     order = torch.randperm(len(train_labels))       # 순서 섞기
#     total_loss = 0

#     for i in range(0, len(order), batch_size):
#         batch = order[i:i + batch_size]
#         # 정답(labels)를 함께 넣으면 모델이 오차(loss)도 계산해줌
#         outputs = model(
#             input_ids=train_inputs["input_ids"][batch],
#             attention_mask=train_inputs["attention_mask"][batch],
#             labels=train_labels[batch],
#         )
#         loss = outputs.loss                         # 오차 (텐서)

#         optimizer.zero_grad()                       # 이전 기울기 지우기
#         loss.backward()                             # 기울기 계산
#         optimizer.step()                            # 값 고치기

#         total_loss += loss.item()

#     print(f"epoch {epoch:2d} | loss = {total_loss / (len(order) / batch_size):.3f}")
#     # -> 반복할수록 loss 가 줄어들면 학습이 잘 되고 있는 것

# print()
# print("[학습 후]")
# print(f"학습용 정확도 : {accuracy(train_inputs, train_labels):.0%}")      # 공부한 문장으로 본 시험
# print(f"평가용 정확도 : {accuracy(test_inputs, test_labels):.0%}")        # 처음 보는 문장으로 본 시험
# show_generated()


# ===========================================================
#  8. 모델 저장하기
#  - 파인 튜닝한 모델은 지금 메모리에만 있어서 프로그램을 끄면 사라짐
#  - 파일로 저장해두면 다시 학습하지 않고 불러서 사용할 수 있음
#  - 모델과 토크나이저 두개 파일을 저장
#  - 모델 : 학습으로 고쳐진 값(가중치) + 설정
#  - 토크나이저 : 모델이 학습한 숫자 규칙을 저장
# ===========================================================

# save_dir = os.path.join(BASE_DIR, "model", "my_text_generation_model")

# model.save_pretrained(save_dir)         # 학습한 모델 저장 (고쳐진 가중치 + 설정)
# tokenizer.save_pretrained(save_dir)     # 토크나이저 저장 (모델과 같은 폴더에)
