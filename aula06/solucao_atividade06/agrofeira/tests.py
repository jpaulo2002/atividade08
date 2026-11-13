from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

SESSAO = "django.contrib.sessions.middleware.SessionMiddleware"
MENSAGENS = "django.contrib.messages.middleware.MessageMiddleware"


class OrdemDoMiddlewareTests(TestCase):
    @override_settings(MIDDLEWARE=[SESSAO, MENSAGENS])
    def test_sessao_antes_das_mensagens_funciona(self):
        resposta = self.client.get("/produtos/")
        self.assertEqual(resposta.status_code, 200)

    @override_settings(MIDDLEWARE=[MENSAGENS, SESSAO])
    def test_mensagens_antes_da_sessao_quebra(self):
        with self.assertRaises(ImproperlyConfigured):
            self.client.get("/produtos/")


@override_settings(MIDDLEWARE=["agrofeira.middleware.TempoDeRespostaMiddleware"])
class TempoDeRespostaTests(TestCase):
    def test_a_resposta_traz_o_cabecalho_com_o_tempo(self):
        resposta = self.client.get("/produtos/")
        self.assertIn("X-Tempo-Resposta", resposta.headers)
        self.assertTrue(resposta["X-Tempo-Resposta"].endswith(" ms"))

    def test_o_cabecalho_aparece_tambem_no_404(self):
        resposta = self.client.get("/nao-existe/")
        self.assertEqual(resposta.status_code, 404)
        self.assertIn("X-Tempo-Resposta", resposta.headers)


class TempoDeRespostaLigadoTests(TestCase):
    def test_o_middleware_esta_ligado_no_settings(self):
        resposta = self.client.get("/produtos/")
        self.assertIn("X-Tempo-Resposta", resposta.headers)
