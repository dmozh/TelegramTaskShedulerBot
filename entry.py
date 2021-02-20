from aiohttp import web
import argparse
from app import create_app
from network import send_request, TypeRequest
import settings as crs

# for standalone launch
if not crs.PRODUCTION:
    parser = argparse.ArgumentParser(description="aiohttp server example")
    parser.add_argument('--path')
    parser.add_argument('--port')
    app = create_app()
    if __name__ == '__main__':
        r = send_request(host=f"{crs.BASE_URL}{crs.API_TOKEN}",
                         api_url=f"/setWebhook",
                         request_type=TypeRequest.GET,
                         query_params={"url": f"{crs.HOST}/action"}
                         )
        args = parser.parse_args()
        print(args.path, args.port)
        web.run_app(app, path=args.path, port=args.port)
