from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.path == "/produtos/":
            self.wfile.write(b"<h1>Produtos</h1>")
        else:
            self.wfile.write(b"<h1>AgroFeira</h1>")

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
