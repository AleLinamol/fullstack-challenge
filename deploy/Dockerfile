FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY deploy/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/agent /app/backend/agent
COPY backend/orchestrator /app/backend/orchestrator
COPY deploy/start.py /app/deploy/start.py
RUN useradd --create-home appuser
USER appuser
CMD ["python", "deploy/start.py"]
