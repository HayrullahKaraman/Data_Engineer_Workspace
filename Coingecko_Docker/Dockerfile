FROM python:3.8.16-slim-bullseye
RUN mkdir /code
WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py app.py

CMD ["python", "-u","app.py"]