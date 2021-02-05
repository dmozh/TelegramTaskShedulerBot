import base64
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from .routes import setup_routes


# for gunicorn launch
DEV = True
if DEV:
    from dev import server
    from network import send_request, TypeRequest
    import credentials as crs
    r = send_request(host=f"{crs.BASE_URL}{crs.API_TOKEN}",
                     api_url=f"/setWebhook",
                     request_type=TypeRequest.GET,
                     query_params={"url": f"{server.dev_server.url}/action"}
                     )
# simple create app
# async def create_app():
#     app = web.Application()
#     setup_routes(app)
#     return app

# create app for using ws
async def create_app():
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    setup_routes(app)
    app.wslist = []
    return app
