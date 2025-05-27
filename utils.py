import tiktoken

# GPT-4o-mini 전용 토큰 계산 함수
def get_token_Gpt4oMini(messages):
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    tokens_per_message = 3
    tokens_per_name = 1

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name

    num_tokens += 3  # assistant 응답 시작 부분 오버헤드
    return num_tokens