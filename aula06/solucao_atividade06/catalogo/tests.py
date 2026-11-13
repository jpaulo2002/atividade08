from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalogo.models import Categoria, JanelaSafra, Produto, Produtor, Unidade


class CatalogoBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        categoria = Categoria.objects.create(nome="Frutas", slug="frutas")
        unidade = Unidade.objects.create(nome="quilo", sigla="kg", fracionavel=True)
        produtor = Produtor.objects.create(nome="Família Oliveira", slug="familia-oliveira", caf="B1")
        cls.cupuacu = Produto.objects.create(
            nome="Cupuaçu", slug="cupuacu", categoria=categoria, produtor=produtor,
            unidade=unidade, preco_centavos=1200, estoque=Decimal("20"),
        )
        cls.banana = Produto.objects.create(
            nome="Banana", slug="banana", categoria=categoria, produtor=produtor,
            unidade=unidade, preco_centavos=500, estoque=Decimal("30"),
        )


class DisponiveisEmTests(CatalogoBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # a safra do cupuaçu vai de março a agosto
        JanelaSafra.objects.create(
            produto=cls.cupuacu, mes_inicio=3, mes_fim=8, situacao="pico"
        )
        # a banana dá o ano inteiro
        JanelaSafra.objects.create(
            produto=cls.banana, mes_inicio=1, mes_fim=12, situacao="disponivel"
        )

    def test_dentro_da_janela_inclusive_nos_extremos(self):
        for mes in (3, 5, 8):
            with self.subTest(mes=mes):
                self.assertIn(self.cupuacu, Produto.objects.disponiveis_em(mes))

    def test_fora_da_janela(self):
        for mes in (1, 2, 9, 12):
            with self.subTest(mes=mes):
                self.assertNotIn(self.cupuacu, Produto.objects.disponiveis_em(mes))

    def test_janela_do_ano_inteiro_vale_em_qualquer_mes(self):
        for mes in (1, 6, 12):
            with self.subTest(mes=mes):
                self.assertIn(self.banana, Produto.objects.disponiveis_em(mes))

    def test_entressafra_nao_conta_como_disponivel(self):
        JanelaSafra.objects.filter(produto=self.cupuacu).update(situacao="entressafra")
        self.assertNotIn(self.cupuacu, Produto.objects.disponiveis_em(5))


class PaginasTests(CatalogoBase):
    def test_home_responde_200(self):
        resposta = self.client.get(reverse("catalogo:home"))
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, "catalogo/home.html")

    def test_lista_mostra_os_produtos(self):
        resposta = self.client.get(reverse("catalogo:produtos"))
        self.assertContains(resposta, "Cupuaçu")
        self.assertContains(resposta, "Banana")

    def test_busca_filtra_a_lista(self):
        resposta = self.client.get(reverse("catalogo:produtos"), {"q": "cupu"})
        self.assertContains(resposta, "Cupuaçu")
        self.assertNotContains(resposta, "Banana")

    def test_pagina_do_produto(self):
        resposta = self.client.get(reverse("catalogo:produto", args=["cupuacu"]))
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context["produto"], self.cupuacu)

    def test_slug_inexistente_e_404(self):
        resposta = self.client.get(reverse("catalogo:produto", args=["nao-existe"]))
        self.assertEqual(resposta.status_code, 404)

    def test_endereco_antigo_redireciona_para_sempre(self):
        resposta = self.client.get("/catalogo/")
        self.assertRedirects(resposta, reverse("catalogo:produtos"), status_code=301)


class SafraQueAtravessaOAnoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        categoria = Categoria.objects.create(nome="Frutas", slug="frutas")
        unidade = Unidade.objects.create(nome="quilo", sigla="kg", fracionavel=True)
        produtor = Produtor.objects.create(nome="Família Oliveira", slug="familia-oliveira", caf="B1")
        base = dict(categoria=categoria, produtor=produtor, unidade=unidade, preco_centavos=100)
        cls.cupuacu = Produto.objects.create(nome="Cupuaçu", slug="cupuacu", **base)
        cls.natal = Produto.objects.create(nome="Panetone", slug="panetone", **base)
        JanelaSafra.objects.create(produto=cls.cupuacu, mes_inicio=11, mes_fim=2, situacao="pico")
        JanelaSafra.objects.create(produto=cls.natal, mes_inicio=12, mes_fim=12, situacao="pico")

    def test_novembro_a_fevereiro_vale_nos_quatro_meses(self):
        for mes in (11, 12, 1, 2):
            with self.subTest(mes=mes):
                self.assertIn(self.cupuacu, Produto.objects.disponiveis_em(mes))

    def test_novembro_a_fevereiro_nao_vale_no_resto_do_ano(self):
        for mes in (3, 6, 10):
            with self.subTest(mes=mes):
                self.assertNotIn(self.cupuacu, Produto.objects.disponiveis_em(mes))

    def test_janela_de_um_mes_so(self):
        self.assertIn(self.natal, Produto.objects.disponiveis_em(12))
        for mes in (11, 1):
            with self.subTest(mes=mes):
                self.assertNotIn(self.natal, Produto.objects.disponiveis_em(mes))
