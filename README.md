# 해외 뉴스 요약

해외의 뉴스를 크롤링해 한국어로 요약한 뒤 결과를 디스코드 봇으로 사용자에게 출력하는 프로그램입니다. 현재는 cnn의 daily기사만을 일정 시간마다 크롤링해 요약합니다. 작동 순서는 아래와 같습니다.

1. 매일 00시 01분부터 1시간마다 당일의 뉴스를 크롤링한다.
2. runpod의 serverless로 배포된 Gemma2 9B 모델이 뉴스를 요약한다.
3. 요약된 결과를 Discord bot 채널에서 새로운 스레드를 생성한 뒤 전달한다.


# 예시

![image](https://github.com/user-attachments/assets/80913782-02f5-4e37-8906-fe4f718b7df1)

---

![image](https://github.com/user-attachments/assets/a7c879c4-0919-465e-8bc5-3aa89831abf6)


# 사용 방법
1. 자신만의 디스코드 서버를 개설한다.
2. 서버 토큰을 발급받은 뒤 `.env`파일을 생성해 `DISCORD_TOKEN`값을 설정한다.
3. Runpod의 Serverless환경에 AI모델을 배포한 뒤 `RUNPOD_BASE_URL`과 `RUNPOD_API_KEY`를 `.env`파일에 설정한다.
  3.1. Runpod이 아닌 로컬 환경으로 AI모델을 사용한다면 `llm.py`파일의 `vllm_endpoint`를 수정해주세요.
4. 스레드가 생성될 채널의 id값을 가져와 `.env`파일의 `CHANNEL_ID`를 설정한다.
5. `bot.py`를 실행시킨다.
