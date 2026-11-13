import time


class TempoDeRespostaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        inicio = time.perf_counter()
        resposta = self.get_response(request)
        milissegundos = (time.perf_counter() - inicio) * 1000
        resposta["X-Tempo-Resposta"] = f"{milissegundos:.1f} ms"
        return resposta
