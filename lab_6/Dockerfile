FROM python:latest

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "run.py"]