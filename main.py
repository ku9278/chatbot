import os
from dotenv import load_dotenv
from openai import OpenAI

class Chatbot():
    MAX_TOKENS_HISTORY = 3000

    def __init__(self, model = "gpt-4o-mini", max_tokens = 1000, temperature = 1):
        self.client = OpenAI()
        self.model = model
        self.messages = [] # 연속적인 대화를 위한 대화 저장
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.tokens = 0 # 저장된 대화의 토큰

    
    def get_answer(self, query: str) -> str:
        # 질문 저장
        self.messages.append({"role": "user", "content": query})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        answer = response.choices[0].message.content

        # 답변 저장 및 토큰 계산
        self.messages.append({"role": "assistant", "content": answer})
        self.tokens = response.usage.total_tokens
        
        return answer


    def summarize_history(self):
        query = "지금까지의 대화를 요약해줘"
        summary = self.get_response(query)
        self.messages = [{"role": "system", "content": "이전 대화 요약: " + summary}]
        self.tokens = 0


    def start_chat(self):
        print("--대화 시작--")
        while(True):
            query = input("입력: ")
            if query == "0": break
            print(self.get_answer(query))

            # 저장된 대화의 토큰이 일정 수준을 넘으면 대화를 요약한다
            if (self.tokens > self.MAX_TOKENS_HISTORY): self.summarize_history()

        self.end_chat()


    def end_chat(self):
        print("--대화 종료--")
        self.client.close()


def main():
    chatbot = Chatbot()
    chatbot.start_chat()


if __name__=='__main__':
    load_dotenv()
    main()