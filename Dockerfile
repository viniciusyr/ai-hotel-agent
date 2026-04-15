FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env.example README.md main.py ./
COPY agent ./agent
COPY config ./config
COPY knowledge ./knowledge
COPY llm ./llm
COPY stt ./stt
COPY telephony ./telephony
COPY tts ./tts

EXPOSE 8080

CMD ["python", "main.py"]
