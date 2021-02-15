from .api import http, websocket


def setup_routes(app):
    app.router.add_route('GET', f'/', http.http_response.test)
    app.router.add_route('GET', f'/test_get', http.get_api.test_get.test_json)
    app.router.add_route('POST', f'/test_post', http.post_api.test_post.test_json)
    app.router.add_route('POST', f'/action', http.post_api.bot_action.action)
