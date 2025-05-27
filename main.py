import os
from dotenv import load_dotenv
from openai import OpenAI


class Chatbot():
    def __init__(self):
        self.client = OpenAI()
        self.messages = [] # 연속적인 대화를 위한 대화 저장

    
    def get_response(self, query: str) -> str:
        self.messages.append({"role": "user", "content": query}) # 질문 저장

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            max_tokens=1000,
            temperature=1
        )

        answer = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer}) # 답변 저장
        return answer


    def start_chat(self):
        print("--대화 시작--")
        while(True):
            query = input("입력: ")
            if query == "0":
                break
            print(self.get_response(query))
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