from http.server import BaseHTTPRequestHandler, HTTPServer

produtos = [
    "Farinha d'água do Uraim — lata",
    "Açaí grosso — rasa",
    "Pimenta-do-reino preta — maço",
    "Mel de abelha uruçu — pote",
]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.enviar(200, "<h1>AgroFeira Paragominas</h1>")
        elif self.path == "/produtos/":
            itens = "".join(f"<li>{p}</li>" for p in produtos)
            self.enviar(200, f"<h1>Produtos</h1><ul>{itens}</ul>")
        else:
            self.enviar(404, "<h1>Não encontrado</h1>")

    def enviar(self, status, corpo):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(corpo.encode("utf-8"))

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
