from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import json
import urllib

USE_HTTPS = False
LISTEN_ON_PORT = 4444
LISTEN_ON_RANGE = '0.0.0.0'
KEYFILE =  './key.pem'
CERTFILE = './cert.pem'

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        parameters = urllib.parse.parse_qs(query)

        user = parameters["user"][0]
        key = parameters["key"][0]

        # Check if value exists before printing it
        if user in self.server.SHARED_DICT and key in self.server.SHARED_DICT[user]:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(self.server.SHARED_DICT[user][key]).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Key not found for user')

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(self.rfile.read(content_len))

        user = post_body['user']
        key = post_body['key']
        value = post_body['value']

        # Write value into dict
        # Also creates a new session if needed
        if user in self.server.SHARED_DICT:
            self.server.SHARED_DICT[user][key] = value
        else:
            self.server.SHARED_DICT[user] = {}
            self.server.SHARED_DICT[user][key] = value

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(post_body).encode())

# Shared value store between threads
# This does not implement any lock
# Values only persist while server is running
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    SHARED_DICT = {}

def run():
    server = ThreadingSimpleServer((LISTEN_ON_RANGE, LISTEN_ON_PORT), Handler)
    if USE_HTTPS:
        import ssl
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # Create keys for example with LetsEncrypt certbot
        context.load_cert_chain(keyfile=KEYFILE, certfile=CERTFILE)
        server.socket = context.wrap_socket(server.socket, server_side=True)
    server.serve_forever()

if __name__ == '__main__':
    run()