FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGODB_URI mongodb://mongo:27017/Users

CMD [ "python", "app.py" ]

