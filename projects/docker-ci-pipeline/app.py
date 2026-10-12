from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            payload = {'status': 'ok'}
            self.send_response(200)
        elif self.path == '/':
            payload = {'service': 'sample-health-api', 'message': 'Hello from a container'}
            self.send_response(200)
        else:
            payload = {'error': 'not found'}
            self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8000), Handler).serve_forever()