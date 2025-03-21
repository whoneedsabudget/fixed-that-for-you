import http.server
import socketserver
import threading
import time
import unittest

from src.linkparser import LinkParser

PORT = 8000


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = """
        <html>
          <body>
            <a href="https://www.example.com/e2e/story">
              <span>Click here</span>
            </a>
          </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))


class TestLinkParserE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = MyHandler
        cls.httpd = socketserver.TCPServer(("", PORT), handler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.server_thread.join()

    def test_apple_e2e(self):
        # Use local server to simulate apple.news page content
        url = "https://apple.news/any"
        parser = LinkParser(url)
        # Override URL to point to our local server providing test HTML
        parser.url = "http://localhost:8000"
        result = parser.fix()
        expected = "https://archive.today/newest/https://www.example.com/e2e/story"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
