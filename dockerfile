FROM python:3.8.17

WORKDIR /api

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD python main.py

