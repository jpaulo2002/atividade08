from catalogo.models import Propriedade
import uuid

from django.contrib.auth.models import User
from django.urls import reverse

from pedidos.models import ItemPedido, Pedido, PontoRetirada



class PedidosBase(PainelBase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        produtor_ana = Produtor.objects.get(
            slug="sitio-da-ana"
        )

        produtor_bia = Produtor.objects.get(
            slug="sitio-da-bia"
        )

        cls.mamao = Produto.objects.create(
            nome="Mamão",
            slug="mamao",
            categoria=cls.categoria,
            produtor=produtor_ana,
            unidade=cls.unidade,
            preco_centavos=400,
            estoque=Decimal("30"),
        )

        cls.cupuacu = Produto.objects.create(
            nome="Cupuaçu",
            slug="cupuacu",
            categoria=cls.categoria,
            produtor=produtor_bia,
            unidade=cls.unidade,
            preco_centavos=1200,
            estoque=Decimal("20"),
        )

        ponto = PontoRetirada.objects.create(
            nome="Praça",
            endereco="Centro",
            horario="sáb 7h",
        )

        cls.pedido_misto = cls.novo_pedido(
            "Cris",
            ponto,
            [
                (cls.banana, 2),
                (cls.mamao, 3),
                (cls.cupuacu, 1),
            ],
        )

        cls.pedido_da_bia = cls.novo_pedido(
            "Dani",
            ponto,
            [
                (cls.cupuacu, 2),
            ],
        )

    @classmethod
    def novo_pedido(cls, comprador, ponto, linhas):

        pedido = Pedido.objects.create(
            comprador=comprador,
            telefone="9",
            ponto_retirada=ponto,
        )

        for produto, quantidade in linhas:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                nome_produto=produto.nome,
                nome_produtor=produto.produtor.nome,
                nome_unidade="quilo",
                preco_unitario_centavos=produto.preco_centavos,
                quantidade=Decimal(quantidade),
            )

        return pedido

class PainelPedidosTests(PedidosBase):

    def test_lista_so_tem_pedidos_do_produtor(self):
        self.client.force_login(self.ana)

        resposta = self.client.get(
            reverse("painel_pedidos")
        )

        self.assertContains(resposta, "Cris")
        self.assertNotContains(resposta, "Dani")

    def test_lista_tem_um_pedido_e_dois_itens(self):
        self.client.force_login(self.ana)

        resposta = self.client.get(
            reverse("painel_pedidos")
        )

        pedidos = resposta.context["pedidos"]

        self.assertEqual(pedidos.count(), 1)

        pedido = pedidos[0]

        self.assertEqual(pedido.meus_itens, 2)

    def test_detalhe_so_mostra_itens_do_produtor(self):
        self.client.force_login(self.ana)

        resposta = self.client.get(
            reverse(
                "painel_pedido",
                kwargs={"codigo": self.pedido_misto.codigo},
            )
        )

        self.assertContains(resposta, "Banana")
        self.assertContains(resposta, "Mamão")
        self.assertNotContains(resposta, "Cupuaçu")

        self.assertEqual(
            resposta.context["total_centavos"],
            2200,
        )

    def test_pedido_alheio_e_inexistente_dao_404(self):
        self.client.force_login(self.ana)

        for codigo in [
            self.pedido_da_bia.codigo,
            uuid.uuid4(),
        ]:
            with self.subTest(codigo=codigo):

                resposta = self.client.get(
                    reverse(
                        "painel_pedido",
                        kwargs={"codigo": codigo},
                    )
                )

                self.assertEqual(resposta.status_code, 404)

    def test_sem_login_redireciona_para_entrada(self):
        urls = [
            reverse("painel_pedidos"),
            reverse(
                "painel_pedido",
                kwargs={"codigo": self.pedido_misto.codigo},
            ),
        ]

        for url in urls:
            with self.subTest(url=url):

                resposta = self.client.get(url)

                self.assertRedirects(
                    resposta,
                    f"/contas/entrar/?next={url}",
                )

    def test_usuario_sem_produtor_recebe_403(self):
        sem_produtor = User.objects.create_user(
            username="sem_produtor",
            password="teste123",
        )

        self.client.force_login(sem_produtor)

        urls = [
            reverse("painel_pedidos"),
            reverse(
                "painel_pedido",
                kwargs={"codigo": self.pedido_misto.codigo},
            ),
        ]

        for url in urls:
            with self.subTest(url=url):

                resposta = self.client.get(url)

                self.assertEqual(resposta.status_code, 403)

def test_cadastro_produto_usa_produtor_logado(self):
    self.client.force_login(self.ana)

    dados = self.dados_do_produto(
        nome="Mamão",
        slug="mamao",
    )

    dados["produtor"] = self.produtor_bia.pk

    resposta = self.client.post(
        reverse("painel_produto_novo"),
        dados,
    )

    self.assertRedirects(
        resposta,
        reverse("painel"),
    )

    produto = Produto.objects.get(slug="mamao")

    self.assertEqual(
        produto.produtor,
        self.produtor_ana,
    )

    self.assertNotEqual(
        produto.produtor,
        self.produtor_bia,
    )


def test_editar_produto_inexistente_retorna_404(self):
    self.client.force_login(self.ana)

    resposta = self.client.get(
        reverse(
            "painel_produto_editar",
            kwargs={"pk": 99999},
        )
    )

    self.assertEqual(
        resposta.status_code,
        404,
    )

    self.client.logout()

    resposta = self.client.get(
        reverse(
            "painel_produto_editar",
            kwargs={"pk": 99999},
        )
    )

    self.assertRedirects(
        resposta,
        "/contas/entrar/?next=/painel/produtos/99999/editar/",
    )