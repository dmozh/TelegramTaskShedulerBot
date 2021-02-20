import os

PRODUCTION = os.getenv("PRODUCTION")
HOST = ''
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")

if PRODUCTION:
    import http.client

    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")

    HOST = conn.getresponse().read().decode()

    API_TOKEN = os.getenv("API_TOKEN")
    BASE_URL = os.getenv("BASE_URL")

else:
    # from dev import server

    # HOST = server.dev_server.url

    API_TOKEN = "1521318440:AAEj_EFh5daUFizzmyXfBTXEpLxKkd_IwH0"
    BASE_URL = "https://api.telegram.org/bot"


