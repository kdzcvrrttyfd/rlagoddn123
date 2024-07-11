# 베이스 이미지 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 환경 변수 설정
ENV FLASK_ENV=production
ENV DATABASE_URI=mysql+mysqlconnector://username:password@hostname/databasename
ENV SECRET_KEY=your_secret_key
ENV FLASK_DEBUG=False

# 컨테이너가 사용할 포트 노출
EXPOSE 5000

# 애플리케이션 실행
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "run:app"]

