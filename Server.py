from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading

USE_HTTPS = False
LISTEN_ON_PORT = 4444
LISTEN_ON_RANGE = '0.0.0.0'
KEYFILE =  './key.pem'
CERTFILE = './cert.pem'

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        # Check if value exists before printing it
        if 'foo' in self.server.SHARED_DICT:
            self.wfile.write(str(self.server.SHARED_DICT['foo']).encode())
        else:
            self.wfile.write(b'Value not found')

    def do_POST(self):
        # Exmple for writing to dictionary
        self.server.SHARED_DICT['foo'] = 42

        self.send_response(200)
        self.end_headers()
        self.wfile.write(str(self.server.SHARED_DICT['foo']).encode())

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