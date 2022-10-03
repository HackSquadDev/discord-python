FROM python:3

WORKDIR /app

COPY . .

RUN pip install .

CMD ["python", "bot.py"]
