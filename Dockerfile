FROM python:3

WORKDIR /app/hacksquad_bot
COPY . .

RUN pip install --no-cache-dir .

CMD ["python", "bot.py"]
