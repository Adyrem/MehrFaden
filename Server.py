from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading

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
    server = ThreadingSimpleServer(('0.0.0.0', 4444), Handler)
    # Implement HTTPS here once ssl is ready
    server.serve_forever()

if __name__ == '__main__':
    run()