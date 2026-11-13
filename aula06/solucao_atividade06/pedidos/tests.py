from decimal import Decimal
from unittest import mock

from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import TestCase
from django.urls import reverse

from catalogo.models import Categoria, Produto, Produtor, Unidade
from pedidos import servicos
from pedidos.forms import AdicionarAoCarrinhoForm
from pedidos.models import ItemPedido, Pedido, PontoRetirada


class BaseDeTeste(TestCase):
    """Os dados que todas as classes de teste do app usam."""

    @classmethod
    def setUpTestData(cls):
        categoria = Categoria.objects.create(nome="Hortaliças", slug="hortalicas")
        maco = Unidade.objects.create(nome="maço", sigla="maço", fracionavel=False)
        quilo = Unidade.objects.create(nome="quilo", sigla="kg", fracionavel=True)
        sousa = Produtor.objects.create(
            nome="Irmãos Sousa", slug="irmaos-sousa", caf="A1",
            pedido_minimo_centavos=1000,
        )
        tonico = Produtor.objects.create(
            nome="Seu Tonico", slug="seu-tonico", caf="A2",
            pedido_minimo_centavos=2000,
        )
        cls.jambu = Produto.objects.create(
            nome="Jambu", slug="jambu", categoria=categoria, produtor=sousa,
            unidade=maco, preco_centavos=400, estoque=Decimal("50"),
        )
        cls.cheiro = Produto.objects.create(
            nome="Cheiro-verde", slug="cheiro-verde", categoria=categoria,
            produtor=sousa, unidade=maco, preco_centavos=300, estoque=Decimal("40"),
        )
        cls.farinha = Produto.objects.create(
            nome="Farinha seca", slug="farinha-seca", categoria=categoria,
            produtor=tonico, unidade=quilo, preco_centavos=1000,
            estoque=Decimal("60"),
        )
        cls.ponto = PontoRetirada.objects.create(
            nome="Feira do Centro", endereco="Praça central", horario="sábado, 7h"
        )
        cls.dados = {
            "comprador": "Maria", "telefone": "(91) 90000-0000",
            "ponto_retirada": cls.ponto,
        }


class ValidarQuantidadeTests(BaseDeTeste):
    def test_aceita_inteiro_em_unidade_inteira(self):
        servicos.validar_quantidade(self.jambu, Decimal("2"))  # não levanta nada

    def test_aceita_quebrado_em_unidade_fracionavel(self):
        servicos.validar_quantidade(self.farinha, Decimal("1.5"))

    def test_recusa_quebrado_em_unidade_inteira(self):
        with self.assertRaises(ValidationError):
            servicos.validar_quantidade(self.jambu, Decimal("1.5"))

    def test_recusa_zero_e_negativo(self):
        for quantidade in ("0", "-1"):
            with self.subTest(quantidade=quantidade):
                with self.assertRaises(ValidationError):
                    servicos.validar_quantidade(self.jambu, Decimal(quantidade))

    def test_aceita_exatamente_o_estoque(self):
        servicos.validar_quantidade(self.jambu, Decimal("50"))

    def test_recusa_mais_do_que_o_estoque(self):
        with self.assertRaises(ValidationError):
            servicos.validar_quantidade(self.jambu, Decimal("51"))


class CriarPedidoTests(BaseDeTeste):
    def test_pedido_abaixo_do_minimo_do_produtor_e_recusado(self):
        # 2 maços de jambu = R$ 8,00, e o mínimo dos Irmãos Sousa é R$ 10,00
        with self.assertRaises(ValidationError) as contexto:
            servicos.criar_pedido({str(self.jambu.pk): "2"}, self.dados)
        mensagem = contexto.exception.messages[0]
        self.assertIn("Irmãos Sousa", mensagem)
        self.assertIn("2,00", mensagem)  # faltam R$ 2,00
        self.assertEqual(Pedido.objects.count(), 0)

    def test_o_minimo_soma_os_itens_do_mesmo_produtor(self):
        # 2 jambus (R$ 8,00) + 1 cheiro-verde (R$ 3,00) = R$ 11,00 dos Irmãos Sousa
        carrinho = {str(self.jambu.pk): "2", str(self.cheiro.pk): "1"}
        pedido = servicos.criar_pedido(carrinho, self.dados)
        self.assertEqual(pedido.itens.count(), 2)


def criar_duas_categorias():
    """Função de brinquedo, só para ensaiar a transação: grava as duas categorias, ou nenhuma."""
    with transaction.atomic():
        Categoria.objects.create(nome="Frutas", slug="frutas")
        Categoria.objects.create(nome="Raízes", slug="raizes")


class TransacaoDeBrinquedoTests(TestCase):
    def test_falha_na_segunda_nao_deixa_a_primeira(self):
        cria_de_verdade = Categoria.objects.create
        chamadas = []

        def cria_a_primeira_e_falha_na_segunda(**campos):
            chamadas.append(campos)
            if len(chamadas) == 2:
                raise RuntimeError("falha plantada")
            return cria_de_verdade(**campos)

        with mock.patch.object(
            Categoria.objects, "create", side_effect=cria_a_primeira_e_falha_na_segunda
        ):
            with self.assertRaises(RuntimeError):
                criar_duas_categorias()

        self.assertEqual(Categoria.objects.count(), 0)


class CarrinhoPaginasTests(BaseDeTeste):
    def test_pagina_do_produto_traz_o_formulario(self):
        resposta = self.client.get(reverse("catalogo:produto", args=["jambu"]))
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, "catalogo/produto_detalhe.html")
        self.assertIn("form", resposta.context)

    def test_slug_inexistente_e_404(self):
        resposta = self.client.get(reverse("catalogo:produto", args=["nao-existe"]))
        self.assertEqual(resposta.status_code, 404)

    def test_adicionar_redireciona_para_o_carrinho_e_guarda_na_sessao(self):
        resposta = self.client.post(
            reverse("catalogo:produto", args=["jambu"]), {"quantidade": "2"}
        )
        self.assertRedirects(resposta, reverse("pedidos:carrinho"))
        self.assertEqual(self.client.session["carrinho"], {str(self.jambu.pk): "2"})

    def test_a_mensagem_aparece_na_pagina_seguinte(self):
        resposta = self.client.post(
            reverse("catalogo:produto", args=["jambu"]), {"quantidade": "2"}, follow=True
        )
        self.assertContains(resposta, "Jambu entrou no carrinho.")

    def test_quantidade_quebrada_volta_com_erro_e_nao_guarda(self):
        resposta = self.client.post(
            reverse("catalogo:produto", args=["jambu"]), {"quantidade": "1.5"}
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "quantidade quebrada")
        self.assertNotIn("carrinho", self.client.session)

    def test_o_preco_forjado_no_envio_nao_muda_o_subtotal(self):
        self.client.post(
            reverse("catalogo:produto", args=["jambu"]), {"quantidade": "2", "preco": "1"}
        )
        resposta = self.client.get(reverse("pedidos:carrinho"))
        self.assertContains(resposta, "R$ 8,00")  # 2 x R$ 4,00, do banco

    def test_carrinho_vazio_mostra_o_aviso(self):
        resposta = self.client.get(reverse("pedidos:carrinho"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Seu carrinho está vazio.")

    def test_esvaziar_so_aceita_post(self):
        resposta = self.client.get(reverse("pedidos:esvaziar"))
        self.assertEqual(resposta.status_code, 405)

    def test_sem_token_csrf_o_envio_e_recusado(self):
        cliente = self.client_class(enforce_csrf_checks=True)
        resposta = cliente.post(reverse("catalogo:produto", args=["jambu"]), {"quantidade": "1"})
        self.assertEqual(resposta.status_code, 403)


class CriarPedidoRegrasTests(BaseDeTeste):
    def test_carrinho_vazio_e_recusado(self):
        with self.assertRaises(ValidationError):
            servicos.criar_pedido({}, self.dados)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_quantidade_quebrada_em_unidade_inteira_e_zero_sao_recusadas(self):
        for quantidade in ("1.5", "0"):
            with self.subTest(quantidade=quantidade):
                with self.assertRaises(ValidationError):
                    servicos.criar_pedido({str(self.jambu.pk): quantidade}, self.dados)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_estoque_insuficiente_e_recusado(self):
        with self.assertRaises(ValidationError):
            servicos.criar_pedido({str(self.jambu.pk): "51"}, self.dados)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_produto_que_sumiu_e_recusado(self):
        pk = self.cheiro.pk
        self.cheiro.delete()
        carrinho = {str(self.jambu.pk): "3", str(pk): "2"}
        with self.assertRaises(ValidationError):
            servicos.criar_pedido(carrinho, self.dados)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_o_item_guarda_o_retrato_do_banco(self):
        carrinho = {str(self.jambu.pk): "3", str(self.farinha.pk): "3"}
        pedido = servicos.criar_pedido(carrinho, self.dados)
        item = pedido.itens.get(nome_produto="Jambu")
        self.assertEqual(item.preco_unitario_centavos, 400)
        self.assertEqual(item.nome_produtor, "Irmãos Sousa")
        self.assertEqual(item.nome_unidade, "maço")
        self.jambu.preco_centavos = 900  # o produtor reajusta depois
        self.jambu.save()
        item.refresh_from_db()
        self.assertEqual(item.preco_unitario_centavos, 400)

    def test_a_baixa_do_estoque(self):
        carrinho = {str(self.jambu.pk): "3", str(self.farinha.pk): "3"}
        servicos.criar_pedido(carrinho, self.dados)
        self.jambu.refresh_from_db()
        self.farinha.refresh_from_db()
        self.assertEqual(self.jambu.estoque, Decimal("47"))
        self.assertEqual(self.farinha.estoque, Decimal("57"))


class TransacaoDoPedidoTests(BaseDeTeste):
    def test_falha_no_meio_nao_deixa_pedido_pela_metade(self):
        carrinho = {str(self.jambu.pk): "3", str(self.farinha.pk): "3"}
        cria_de_verdade = ItemPedido.objects.create
        chamadas = []

        def cria_o_primeiro_e_falha_no_segundo(**campos):
            chamadas.append(campos)
            if len(chamadas) == 2:
                raise RuntimeError("falha plantada")
            return cria_de_verdade(**campos)

        with mock.patch.object(
            ItemPedido.objects, "create", side_effect=cria_o_primeiro_e_falha_no_segundo
        ):
            with self.assertRaises(RuntimeError):
                servicos.criar_pedido(carrinho, self.dados)

        self.assertEqual(Pedido.objects.count(), 0)
        self.assertEqual(ItemPedido.objects.count(), 0)
        self.jambu.refresh_from_db()
        self.assertEqual(self.jambu.estoque, Decimal("50"))


class FechamentoPaginasTests(BaseDeTeste):
    def guardar_no_carrinho(self, carrinho):
        sessao = self.client.session
        sessao["carrinho"] = carrinho
        sessao.save()

    def envio(self, **extra):
        return {"comprador": "Maria", "telefone": "(91) 90000-0000",
                "ponto_retirada": self.ponto.pk, **extra}

    def test_checkout_com_carrinho_vazio_volta_para_o_carrinho(self):
        resposta = self.client.get(reverse("pedidos:checkout"))
        self.assertRedirects(resposta, reverse("pedidos:carrinho"))

    def test_checkout_mostra_o_formulario(self):
        self.guardar_no_carrinho({str(self.jambu.pk): "3"})
        resposta = self.client.get(reverse("pedidos:checkout"))
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, "pedidos/checkout.html")

    def test_pedido_valido_redireciona_para_a_confirmacao_e_esvazia_o_carrinho(self):
        self.guardar_no_carrinho({str(self.jambu.pk): "3", str(self.farinha.pk): "3"})
        resposta = self.client.post(reverse("pedidos:checkout"), self.envio())
        pedido = Pedido.objects.get()
        self.assertRedirects(resposta, reverse("pedidos:pedido", args=[pedido.codigo]))
        self.assertNotIn("carrinho", self.client.session)

    def test_abaixo_do_minimo_mostra_o_erro_e_nao_grava(self):
        self.guardar_no_carrinho({str(self.jambu.pk): "2"})
        resposta = self.client.post(reverse("pedidos:checkout"), self.envio())
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "faltam R$ 2,00")
        self.assertEqual(Pedido.objects.count(), 0)

    def test_preco_forjado_no_envio_e_ignorado(self):
        self.guardar_no_carrinho({str(self.jambu.pk): "3", str(self.farinha.pk): "3"})
        self.client.post(reverse("pedidos:checkout"), self.envio(preco="1"))
        item = ItemPedido.objects.get(nome_produto="Jambu")
        self.assertEqual(item.preco_unitario_centavos, 400)

    def test_codigo_inexistente_e_404(self):
        resposta = self.client.get(
            reverse("pedidos:pedido", args=["00000000-0000-0000-0000-000000000000"])
        )
        self.assertEqual(resposta.status_code, 404)

    def test_sem_token_csrf_o_envio_e_recusado(self):
        cliente = self.client_class(enforce_csrf_checks=True)
        resposta = cliente.post(reverse("pedidos:checkout"), {})
        self.assertEqual(resposta.status_code, 403)
