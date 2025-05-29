import os
from dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr
from playsound import playsound

class Chatbot():
    MAX_TOKENS_HISTORY = 3000

    def __init__(self, NLP_model = "gpt-4o-mini", max_tokens = 1000, temperature = 1, TTS_model = "tts-1", voice = "alloy"):
        # NLP - openai api
        self.client = OpenAI()
        self.NLP_model = NLP_model
        self.messages = [{"role": "system", "content": "너의 대답은 음성으로 사용자에게 전달된다"}]
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.tokens = 0 # 저장된 대화의 토큰

        # STT
        self.speech_recognizer = sr.Recognizer()

        # TTS - openai api
        self.TTS_model = TTS_model
        self.voice = voice

    
    def get_answer(self, query: str, summarize = False) -> str:
        # 질문 저장
        self.messages.append({"role": "user", "content": query})

        response = self.client.chat.completions.create(
            model = self.NLP_model,
            messages = self.messages,
            max_tokens = self.max_tokens,
            temperature = self.temperature
        )
        answer = response.choices[0].message.content

        # 답변 저장 및 토큰 계산
        if summarize:
            self.messages = [{"role": "system", "content": "이전 대화 요약: " + answer}]
            self.tokens = response.usage.completion_tokens
        else:
            self.messages.append({"role": "assistant", "content": answer})
            self.tokens = response.usage.total_tokens
        
        return answer


    def summarize_history(self):
        query = "지금까지의 대화를 요약해줘"
        self.get_answer(query, summarize = True)
        # get_answer에서 self.messages와 self.tokens가 업데이트 된다.

    
    def speech_recognize(self) -> str:
        while True:
            # 음성 입력
            print("\033[F음성 인식중...")
            with sr.Microphone() as source:
                audio = self.speech_recognizer.listen(source)
            
            # 음성을 텍스트로 변환
            try:
                text = self.speech_recognizer.recognize_google(audio, language='ko-KR')
                return text
            except sr.UnknownValueError:
                print("\033[F음성을 인식하지 못했습니다. 다시 시도하세요.")
                print("")
                continue
            except sr.RequestError as e:
                print("\033[FGoogle Web Speech API 서비스에 문제가 발생했습니다.")
                print("프로그램을 종료합니다.")
                exit(1)

    
    def speak_answer(self, answer: str):
        print("\033[F대답 중...    ")
        speech_file_path = "./tmp/answer.mp3"

        response = self.client.audio.speech.create(
            model = self.TTS_model,
            voice = self.voice,
            input = answer
        )

        # mp3 파일 생성 (stream_to_file 안됨)
        with open(speech_file_path, "wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)

        # mp3 파일 재생
        playsound(speech_file_path)
        print("\033[F대답 완료     ")
        
        # mp3 파일 삭제
        if os.path.exists(speech_file_path):
            os.remove(speech_file_path)


    def start_chat(self):
        print("--대화 시작--")
        print("음성 입력: Enter / 종료: 0 ")

        while(True):
            cmd = input("입력: ")
            if cmd == "0": break
            
            # 음성 입력 받기
            query = self.speech_recognize()
            # 질문 제공 후 답변 받기
            answer = self.get_answer(query)
            # 답변을 음성으로 출력
            self.speak_answer(answer)

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