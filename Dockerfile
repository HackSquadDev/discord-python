FROM python:3

RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "hacksquad_discordpy/main.py", "&"]