# 모델 파인 튜닝하기 (이미지 분류 모델)

import os
import torch
from PIL import Image
from torchvision import transforms
from transformers import AutoImageProcessor, AutoModelForImageClassification

# ===========================================================
#  1. 패키지 목록
#  - torch : PyTorch 딥러닝 라이브러리
#  - Image : Pillow 라이브러리의 이미지 처리 모듈
#  - transforms : 이미지를 뒤집거나 회전해서 비슷한 사진을 만들어주는 도구 (torchvision 라이브러리)
#  - AutoImageProcessor : 이미지를 모델이 읽을 수 있는 숫자로 바꾸는 도구
#  - AutoModelForImageClassification : 이미지 한 장을 통째로 보고 범주 하나로 분류하는 모델
#  - 예시) 뽀로로 사진 → [AutoImageProcessor] → 숫자 → [AutoModelForImageClassification] → pororo
#
#  [설치]
#  - pip install transformers torch torchvision pillow
# ===========================================================

# ===========================================================
#  2. 우리가 만들 모델
#  - ViT 모델은 ImageNet 1000종류(동물, 물건 등)만 구분할 수 있음
#  - 뽀로로를 보여주면 강아지 or 인형 같은 엉뚱한 답을 함
#  - 이 모델을 추가 이미지로 파인 튜닝해서 뽀로로 / 크롱 / 포비를 구분하게 만들기
#
#  [순서]
#  1) 이미지 데이터 준비하기 (캐릭터마다 20장씩)
#  2) 기존 모델과 이미지 프로세서 불러오기
#  3) 모델 학습하기 (예측 -> 오차 -> 수정 반복)
#  4) 학습한 모델을 저장하고 다시 불러서 사용하기
# ===========================================================

# ===========================================================
#  3. 이미지 데이터 준비하기
#  - 폴더를 하나씩 열어서 사진을 읽고, 폴더 이름을 정답으로 사용
#  - 파일 이름 순서로 앞의 15장은 학습용, 뒤의 5장은 평가용
#  - 평가용은 학습에 쓰지 않고 정확도 확인에만 사용
#
#  [데이터 증강(augmentation)]
#  - 사진이 적을 때 학습용 사진을 뒤집고 돌려서 비슷한 사진을 더 만들어내는 방법
#  - 학습용 사진 1장마다 변형한 사진을 4장씩 추가 (캐릭터마다 15장 -> 75장)
#  - 평가용 사진은 증강하지 않음
#
#  [증강 규칙]
#  - 좌우 뒤집기, 15도 안쪽 회전, 일부 확대, 밝기 / 대비 변화
#  - 상하 뒤집기는 하지 않음 : 거꾸로 선 캐릭터는 실제로 입력될 일이 없음
# ===========================================================

# 이 파일이 있는 폴더 기준으로 경로 만들기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(BASE_DIR, "dataset")

class_names = ["pororo", "crong", "poby"]                   # 0: pororo, 1: crong, 2: poby

# 데이터 증강하기
augment = transforms.Compose([
    transforms.RandomHorizontalFlip(),                      # 좌우 뒤집기 (50% 확률)
    transforms.RandomRotation(15),                          # -15 ~ 15도 회전
    transforms.RandomResizedCrop(224, scale=(0.7, 1.0)),    # 원본 면적의 70~100% 영역을 무작위로 잘라 224×224로 변환
    transforms.ColorJitter(brightness=0.3, contrast=0.3),   # 밝기, 대비 변화
])

train_images, train_labels = [], []
test_images, test_labels = [], []

for label, name in enumerate(class_names):
    folder = os.path.join(dataset_dir, name)                # dataset/pororo
    files = sorted(os.listdir(folder))

    for i, file in enumerate(files):
        image = Image.open(os.path.join(folder, file)).convert("RGB")   # 흑백, 투명 사진도 RGB 로 통일

        if i < len(files) - 5:                              # 학습용 데이터
            train_images.append(image)                      # 원본
            train_labels.append(label)
            for _ in range(4):                              # 원본 1장당 증강본 4장 추가
                train_images.append(augment(image))
                train_labels.append(label)
        else:                                               # 평가용 데이터
            test_images.append(image)
            test_labels.append(label)

train_labels = torch.tensor(train_labels)
test_labels = torch.tensor(test_labels)

print(f"학습용 {len(train_images)}장 / 평가용 {len(test_images)}장")


# ===========================================================
#  4. 기존 모델 불러오기
#  - from_pretrained(모델이름) : 허깅페이스에서 이미 학습된 모델을 내려받아 불러옴
#    (최초 1회 다운로드, 이후에는 내 PC에 저장된 캐시 사용)
#  - AutoImageProcessor : 이미지를 모델이 읽을 수 있는 숫자로 바꾸는 도구
#  - AutoModelForImageClassification : 이미지 한 장을 통째로 보고 범주 하나로 분류하는 모델
#
#  - id2label : 분류할 종류가 3개라는 것을 모델에 알려줌
#  - ignore_mismatched_sizes=True : 기존 모델은 1000종류용이므로 마지막 층을 3종류용으로 새로 만듦
# ===========================================================

# model_name = "google/vit-base-patch16-224"

# processor = AutoImageProcessor.from_pretrained(model_name)
# model = AutoModelForImageClassification.from_pretrained(
#     model_name,
#     id2label={0: "pororo", 1: "crong", 2: "poby"},
#     ignore_mismatched_sizes=True,
# )


# ===========================================================
#  5. 데이터 변환하기
#  - 사진 목록을 모델에 넣을 수 있는 형태로 바꾸기
#  - 이미지 프로세서가 사진 -> 숫자 텐서로 바꿈
#    · 크기를 224x224 로 맞춤 (ViT 모델이 읽는 크기)
#    · 픽셀 값(0~255)을 모델이 학습한 범위(-1~1)로 맞춤
# ===========================================================

# # 이미지 -> 숫자 (224x224 크기로 변환)
# # return_tensors="pt" : 결과를 PyTorch 텐서로 받음
# train_inputs = processor(train_images, return_tensors="pt")
# test_inputs = processor(test_images, return_tensors="pt")


# ===========================================================
#  6. 정확도 확인하기
#  - predict : 사진들의 종류 번호를 예측
#  - accuracy : 예측한 번호가 정답과 얼마나 맞는지 비율로 계산
# ===========================================================

# def predict(inputs):
#     model.eval()                                            # 평가 모드
#     with torch.no_grad():                                   # 학습하지 않고 예측만 하기
#         logits = model(pixel_values=inputs["pixel_values"]).logits      # 모든 사진 숫자를 한 번에 모델에 넣고 분류 점수(logits)만 꺼내기
#     return logits.argmax(dim=1)                             # 점수가 높은 쪽을 선택


# def accuracy(inputs, labels):
#     return (predict(inputs) == labels).float().mean().item()


# print()
# print("[학습 전]")
# print(f"학습용 정확도 : {accuracy(train_inputs, train_labels):.0%}")
# print(f"평가용 정확도 : {accuracy(test_inputs, test_labels):.0%}")


# ===========================================================
#  7. 학습하기
#  - 학습용 데이터로 모델의 값(가중치)을 조금씩 고쳐서 정답을 더 잘 맞히게 만드는 과정
#  - 예측 -> 오차 -> 수정 반복
#    1) 예측 : 모델이 사진을 보고 각 종류별 점수를 계산
#    2) 오차 : 예측과 정답이 얼마나 다른지 계산 (loss, 작을수록 좋음)
#    3) 수정 : 오차가 줄어드는 방향으로 모델의 값을 조금 고침
#  - batch : 데이터를 작게 나눈 묶음. 한 묶음씩 학습 (여기서는 8장씩)
#  - epoch : 학습 데이터 전체를 한 번 학습하는 것 (여기서는 10번 반복)
#  - 옵티마이저(optimizer) : 모델의 값을 고쳐주는 도구 (AdamW)
#  - lr(learning rate, 학습률) : 한 번에 고치는 크기
#    (너무 크면 정답을 지나쳐 학습이 불안정하고, 너무 작으면 학습이 느림)
# ===========================================================

# ===========================================================
#  마지막 분류층만 학습하기 (본체 고정)
#  - ViT 본체(model.vit)는 이미 이미지를 잘 이해하므로 그대로 두기
#  - 새로 만든 마지막 층(model.classifier)만 우리 데이터로 학습
#  - requires_grad = False : 이 값은 수정하지 않음
# ===========================================================

# for parameter in model.vit.parameters():
#     parameter.requires_grad = False

# # 옵티마이저 생성 : model.classifier.parameters() = 학습으로 고쳐질 모델의 모든 값, lr = 학습률
# optimizer = torch.optim.AdamW(model.classifier.parameters(), lr=1e-3)

# print()
# print("[학습]")
# for epoch in range(1, 11):
#     model.train()                                           # 학습 모드
#     order = torch.randperm(len(train_labels))               # 순서 섞기

#     for i in range(0, len(order), 8):                       # 8장씩 묶어서 학습 (batch)
#         batch = order[i:i + 8]
#         # 정답(labels)를 함께 넣으면 모델이 예측 점수(logits)와 함께 오차(loss)도 계산해줌
#         outputs = model(
#             pixel_values=train_inputs["pixel_values"][batch],
#             labels=train_labels[batch],
#         )
#         loss = outputs.loss

#         optimizer.zero_grad()                               # 이전 기울기 지우기
#         loss.backward()                                     # 기울기 계산
#         optimizer.step()                                    # 값 고치기

#     print(f"epoch {epoch:2d} | loss = {loss.item():.3f}")
#     # -> 반복할수록 loss 가 줄어들면 학습이 잘 되고 있는 것

# print()
# print("[학습 후]")
# print(f"학습용 정확도 : {accuracy(train_inputs, train_labels):.0%}")
# print(f"평가용 정확도 : {accuracy(test_inputs, test_labels):.0%}")


# ===========================================================
#  8. 모델 저장하기
#  - 파인 튜닝한 모델은 지금 메모리에만 있어서 프로그램을 끄면 사라짐
#  - 파일로 저장해두면 다시 학습하지 않고 불러서 사용할 수 있음
#  - 모델과 이미지 프로세서 두개 파일을 저장
#  - 이미지 프로세서도 같이 저장해야 나중에 같은 방식으로 이미지를 변환할 수 있음
# ===========================================================

# save_dir = os.path.join(BASE_DIR, "model", "my_image_model")

# model.save_pretrained(save_dir)
# processor.save_pretrained(save_dir)
