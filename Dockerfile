FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git && \
    git config --global user.email "agent@pipeline.local" && \
    git config --global user.name "AI Pipeline Agent"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
