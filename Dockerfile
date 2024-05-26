# Python 3.11을 기반으로 하는 Docker 이미지를 사용합니다.
FROM python:3.11.8-slim

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# 필요한 패키지를 설치합니다.
COPY requirements.txt .
RUN pip install -r requirements.txt

# 소스 코드를 복사합니다.
COPY . .

# 앱을 실행합니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]