from http.server import BaseHTTPRequestHandler
from pathlib import Path

class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Function entrypoint serving CampusMind static client."""
    def do_GET(self):
        html_path = Path(__file__).parent / "index.html"
        content = html_path.read_bytes() if html_path.exists() else b"<h1>CampusMind</h1>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

def app(environ, start_response):
    """WSGI application callable fallback for Vercel Python runtime."""
    html_path = Path(__file__).parent / "index.html"
    content = html_path.read_bytes() if html_path.exists() else b"<h1>CampusMind</h1>"
    start_response("200 OK", [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(content)))
    ])
    return [content]

application = app
