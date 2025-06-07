# ----------------------------
# Build Stage: 의존성 설치 및 빌드
# ----------------------------
FROM python:3.10-slim as builder

WORKDIR /app

# 시스템 의존성 설치 (Hugging Face 임베딩 모델용)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 가상 환경 설정
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Runtime Stage: 최종 실행 이미지
# ----------------------------
FROM python:3.10-slim

WORKDIR /app

# 시스템 의존성 (런타임용)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 가상 환경 복사
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 애플리케이션 코드 복사
COPY . .

# 비 root 사용자 생성
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Gunicorn 설정
ENV PORT=8000
ENV WORKERS_PER_CORE=2
ENV MAX_WORKERS=8
ENV TIMEOUT=120

# 헬스체크 엔드포인트
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:$PORT/health || exit 1

EXPOSE $PORT

# 프로덕션 실행 명령
CMD ["gunicorn", "main:app", \
    "--workers", "4", \
    "--worker-class", "uvicorn.workers.UvicornWorker", \
    "--bind", "0.0.0.0:${PORT}", \
    "--timeout", "${TIMEOUT}", \
    "--access-logfile", "-", \
    "--error-logfile", "-"]
