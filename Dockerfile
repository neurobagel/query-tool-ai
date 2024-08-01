FROM ollama/ollama:latest

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

COPY ./app/ /app/

COPY ./entrypoint.sh ./

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]