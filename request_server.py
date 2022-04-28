import json
import logging
from http.server import BaseHTTPRequestHandler
from request_handler import RequestHandler


class Request(BaseHTTPRequestHandler):
    logger = logging.getLogger('Request')

    def __init__(self, handler: RequestHandler):
        super.__init__()
        self.handler = handler

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        data = {'result': 'ok'}
        self.start_scan()
        self.wfile.write(json.dumps(data).encode())

    def start_scan(self):
        self.handler.start_scan()

    def log_message(self, format, *args):
        """Log an arbitrary message.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client ip and current date/time are prefixed to
        every message.

        """

        self.logger.info("%s - %s" % (self.address_string(), format % args))
