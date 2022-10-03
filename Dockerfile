FROM python:3

WORKDIR /app/hacksquad_bot
RUN pip install --no-cache-dir .

COPY . ./

CMD ["python", "bot.py"]
