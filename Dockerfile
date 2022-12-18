FROM python:3.9-slim-buster

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

RUN chmod u+x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
