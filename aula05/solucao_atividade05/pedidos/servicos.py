from collections import defaultdict

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.template.defaultfilters import floatformat

from catalogo.templatetags.moeda import reais

from . import carrinho as cesta
from catalogo.models import Produto

from .models import ItemPedido, Pedido


def validar_quantidade(produto, quantidade):
    """Recusa a quantidade que não vale para o produto.

    Quem pede e quem recusa é o servidor: o navegador só ajuda.
    """
    if quantidade <= 0:
        raise ValidationError(
            f"{produto.nome}: a quantidade tem que ser maior que zero."
        )
    if not produto.unidade.fracionavel and quantidade != quantidade.to_integral_value():
        raise ValidationError(
            f"{produto.nome} é vendido por {produto.unidade.nome} inteiro: "
            "não aceita quantidade quebrada."
        )
    if quantidade > produto.estoque:
        em_estoque = floatformat(produto.estoque, "-3")
        raise ValidationError(
            f"Estoque de {produto.nome}: {em_estoque} {produto.unidade.sigla}. "
            f"Você pediu {floatformat(quantidade, '-3')}."
        )


def validar_pedido_minimo(itens):
    """Soma os subtotais por produtor e compara com o pedido mínimo de cada um."""
    totais = defaultdict(int)
    for item in itens:
        totais[item["produto"].produtor] += item["subtotal_centavos"]
    for produtor, total in totais.items():
        faltam = produtor.pedido_minimo_centavos - total
        if faltam > 0:
            raise ValidationError(
                f"{produtor.nome}: o pedido mínimo é {reais(produtor.pedido_minimo_centavos)} "
                f"e faltam {reais(faltam)}."
            )


def criar_pedido(carrinho, dados):
    """Grava o pedido, os itens e a baixa do estoque: tudo, ou nada."""
    if not carrinho:
        raise ValidationError("O carrinho está vazio.")
    itens = cesta.detalhar(carrinho)
    if len(itens) != len(carrinho):
        raise ValidationError(
            "Um produto do carrinho saiu do catálogo. Esvazie o carrinho e monte o pedido de novo."
        )
    for item in itens:
        validar_quantidade(item["produto"], item["quantidade"])
    validar_pedido_minimo(itens)

    with transaction.atomic():
        pedido = Pedido.objects.create(
            comprador=dados["comprador"],
            telefone=dados["telefone"],
            ponto_retirada=dados["ponto_retirada"],
        )
        for item in itens:
            produto, quantidade = item["produto"], item["quantidade"]
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                nome_produto=produto.nome,
                nome_produtor=produto.produtor.nome,
                nome_unidade=produto.unidade.nome,
                preco_unitario_centavos=produto.preco_centavos,
                quantidade=quantidade,
            )
            baixou = Produto.objects.filter(pk=produto.pk, estoque__gte=quantidade).update(
                estoque=F("estoque") - quantidade
            )
            if not baixou:
                raise ValidationError(f"Estoque insuficiente de {produto.nome}.")
    return pedido
