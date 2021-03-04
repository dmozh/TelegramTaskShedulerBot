import os

PRODUCTION = os.getenv("PRODUCTION")
HOST = ''
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
#
if PRODUCTION:
    HOST = os.getenv("HOST")
    API_TOKEN = os.getenv("API_TOKEN")
    BASE_URL = os.getenv("BASE_URL")

else:
    print('fu')