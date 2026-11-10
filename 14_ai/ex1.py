# 허깅페이스 텍스트 모델 사용하기
# - 텍스트 분류, 빈칸 채우기, 텍스트 생성

import os
from dotenv import load_dotenv
from transformers import pipeline

# ===========================================================
#  1. 허깅페이스(Hugging Face)란?
#  - 학습이 끝난 AI 모델을 공개하고 공유하는 사이트 (https://huggingface.co/)
#  - 다른 사람이 데이터를 학습시켜 만든 모델을 가져다 쓸 수 있음
#
#  [파이프라인 방식]
#  - 공개된 모델을 내 PC로 다운받아 실행 (최초 1회 다운로드, 이후 캐시 사용)
#  - 로컬에서 실행되므로 모델이 크면 오래 걸림, 토큰 없어도 실행은 됨
#  - 무료(공개) 모델과 접근 권한 승인이 필요한 Gated 모델이 있음
#
#  [API 호출 방식]
#  - 허깅페이스 서버에서 모델을 실행하고 결과만 받아옴
#  - 내 PC가 느려도 큰 모델 사용 가능, 토큰 필요
#  - 현재는 일반 무료 계정에 제공되는 무료 크레딧 제공 안함
#
#  [설치]
#  - pip install transformers torch
#  - Token 발급 : 모델을 내려받아 실행만 할 경우 Read 유형 발급
# ===========================================================

# ===========================================================
#  2. 텍스트 분류(Text Classification)란?
#  - 문장을 읽고 미리 정해진 범주(label) 중 하나로 분류하는 작업
#  - 예) 감정 분석(긍정/부정), 스팸 메일 판별, 뉴스 주제 분류
#  - 결과는 label(분류 이름) + score(확률, 0~1)로 나옴
# ===========================================================

# ===========================================================
#  3. 파이프라인 방식
#  - pipeline("작업이름", model="모델이름") 으로 모델을 불러옴
#  - 작업이름 : text-classification
#  - 모델이름 : 허깅페이스 > Models > Tasks에서 검색
#  - Use this model 버튼 클릭 > Libraries의 Transformers > pipeline 코드
# ===========================================================

load_dotenv()
token = os.getenv("HF_TOKEN")
print(token)

# print("1. 파이프라인 : 감정 분석")

# classifier = pipeline(
#     "text-classification",
#     model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
#     token=token
# )

# sentences = [
#     "I love this movie. It was fantastic!",
#     "The food was cold and the service was terrible.",
# ]

# for sentence in sentences:
#     result = classifier(sentence)[0]
#     print(f"{result['label']} ({result['score']:.2f}) : {sentence}")


# print()
# print("2. 파이프라인 : 빈칸 채우기")

# unmasker = pipeline(
#     "fill-mask",
#     model="distilbert/distilbert-base-uncased",
#     token=token
# )

# result = unmasker("Python is a popular [MASK] language.")

# for item in result:
#     print(f"{item['token_str']} ({item['score']:.2f}) : {item['sequence']}")


# print()
# print("3. 파이프라인 : 텍스트 생성")

# pipe = pipeline(
#     "text-generation", 
#     model="Qwen/Qwen2.5-0.5B-Instruct",
#     token=token
# )


# # [role 지정]
# # - system : 모델의 성격, 말투, 규칙을 정하는 지시문 (맨 앞에 한번만 넣음)
# # - user : 모델에게 하는 질문이나 요청
# # - assistant : 모델이 한 답변

# messages = [
#     {"role": "system", "content": "너는 친절한 파이썬 선생님이야. 짧은 한 문장으로 답해줘."},
#     {"role": "user", "content": "리스트와 튜플의 차이가 뭐야?"}
# ]

# result = pipe(messages, max_new_tokens=100)

# print(result[0]["generated_text"][-1]["content"])   # 마지막 메시지 = 모델의 답변


# # 모델은 이전 대화를 기억하지 못함
# # 이어서 대화하려면 지난 user와 assistant 메시지를 매번 목록에 다시 넣어 보내기
# messages = [
#     {"role": "system", "content": "너는 친절한 파이썬 선생님이야. 짧은 한 문장으로 답해줘."},
#     {"role": "user", "content": "리스트가 뭐야?"},
#     {"role": "assistant", "content": "여러 값을 순서대로 담는 자료형이에요."},  # 이전 답변
#     {"role": "user", "content": "튜플이랑은 뭐가 달라?"},                      # 앞 대화를 이어서 질문
# ]

# result = pipe(messages, max_new_tokens=100)

# print(result[0]["generated_text"][-1]["content"])   # 마지막 메시지 = 모델의 답변


# # 위 방식을 코드로 구현
# # - 질문할 때마다 user 메시지를 목록에 추가하고, 모델의 답변도 assistant 로 목록에 추가
# # - 다음 질문 때 지금까지의 대화 전체가 모델에 전달되어 앞 내용을 기억하는 것처럼 동작

# chat = [
#     {"role": "system", "content": "너는 친절한 파이썬 선생님이야. 모든 질문에 짧은 한 문장으로 답해줘."},
# ]

# while True:
#     question = input("질문 : ").strip()
#     if question.lower() == "exit":
#         break

#     chat.append({"role": "user", "content": question})              # 질문 추가

#     result = pipe(chat, max_new_tokens=100)
#     answer = result[0]["generated_text"][-1]["content"]             # 마지막 메시지 = 모델의 답변

#     chat.append({"role": "assistant", "content": answer})           # 답변도 추가 (다음 질문 때 함께 전달)
#     print(f"답변 : {answer}\n")
