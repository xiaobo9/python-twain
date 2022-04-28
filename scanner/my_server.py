import json
import logging
from http.server import BaseHTTPRequestHandler
from main_gui import MyTwain
from route_func import route, simple_router

logger = logging.getLogger('my_server')


class MyRequest(BaseHTTPRequestHandler):
    """
    接受 js 客户端调用，进行扫描动作
    """
    class_app: MyTwain | None

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        # 放着玩的
        self.app: MyTwain | None

    @classmethod
    def set_app(cls, app):
        cls.class_app = app

    def do_GET(self):
        api = simple_router(self.path)
        if api:
            api(self)
        else:
            self.error_404()

    @route(path=['/', '/index', '/index.html'])
    def index(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open("scanner/resources/index.html", "r", encoding="utf-8") as f:
            self.wfile.write(f.read().encode())

    @route(path='/favicon.ico')
    def favicon(self):
        self.send_response(200)
        self.send_header('Content-Type', 'image/jpeg')
        self.end_headers()

        with open("scanner/resources/favicon.ico", "rb") as f:
            self.wfile.write(f.read())

    @route(path='/api/scan')
    def api_scan(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        data = {'result': 'ok'}
        MyRequest.class_app.start_scan()
        self.wfile.write(json.dumps(data).encode())

    @route(path='/404.html')
    def error_404(self):
        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open("scanner/resources/404.html", "r", encoding="utf-8") as f:
            self.wfile.write(f.read().encode())
