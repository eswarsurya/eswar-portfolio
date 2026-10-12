import json
import threading
import unittest
from http.server import HTTPServer
from urllib.request import urlopen
from urllib.error import HTTPError
from app import Handler

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_health(self):
        with urlopen(self.base + '/health') as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read()), {'status': 'ok'})

    def test_unknown_path(self):
        with self.assertRaises(HTTPError) as ctx:
            urlopen(self.base + '/missing')
        self.assertEqual(ctx.exception.code, 404)

if __name__ == '__main__': unittest.main()