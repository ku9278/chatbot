# Chatbot (음성 기반 챗봇)

이 프로젝트는 OpenAI GPT와 음성 인식(STT), 음성 합성(TTS)을 활용한 음성 기반 챗봇입니다. 
사용자는 마이크로 질문을 입력하고, 챗봇의 답변을 음성으로 들을 수 있습니다.

---

## 주요 기능

- **음성 인식(STT)**: 마이크로 질문을 입력받아 텍스트로 변환
- **GPT 기반 답변**: OpenAI GPT 모델을 사용해 자연스러운 답변 생성
- **음성 합성(TTS)**: 챗봇의 답변을 음성(mp3)으로 변환 후 재생
- **대화 요약**: 대화가 길어지면 자동으로 요약
- **토큰 관리**: 대화의 토큰 수를 관리하여 효율적인 대화 유지

---

## 설치 방법

1. **필수 패키지 설치**
    ```bash
    pip install -r requirements.txt
    ```

2. **OpenAI API 키 설정**
    - 프로젝트 루트에 `.env` 파일을 만들고 아래와 같이 작성하세요.
      ```
      OPENAI_API_KEY=your_openai_api_key
      ```

---

## 사용 방법

1. **실행**
    ```bash
    python chatbot.py
    ```

2. **대화 흐름**
    - `입력:` 프롬프트에서 Enter를 누르면 음성 입력이 시작됩니다.
    - 마이크에 질문을 말하면 챗봇이 답변을 음성으로 들려줍니다.
    - `0`을 입력하면 프로그램이 종료됩니다.

---

## 참고

- OpenAI GPT 및 TTS API 사용
- 자연어 처리: [openai](https://github.com/openai/openai-python)
- 음성 인식: [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- 음성 재생: [playsound](https://pypi.org/project/playsound/)
