FROM ubuntu:18.04
COPY . ./app
WORKDIR /app
RUN apt-get -y upgrade && apt-get -y update && apt-get -y install python3 && apt-get -y install python3-pip
#RUN apt-get -y install build-essential libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip && apt-get -y install wget && apt-get -y install git
ENV REDIS_HOST="redis"
ENV REDIS_PORT="6379"
ENV REDIS_DB="0"
ENV API_TOKEN="1521318440:AAEj_EFh5daUFizzmyXfBTXEpLxKkd_IwH0"
ENV BASE_URL="https://api.telegram.org/bot"
ENV PRODUCTION="1"

RUN pip3 install -r requirements.txt
CMD ["gunicorn", "app.app:create_app", "--bind localhost:8080", "--worker-class aiohttp.GunicornWebWorker", "--preload"]