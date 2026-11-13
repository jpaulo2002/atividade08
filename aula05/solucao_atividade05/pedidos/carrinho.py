from decimal import ROUND_HALF_UP, Decimal

from catalogo.models import Produto

CHAVE = "carrinho"


def ler(sessao):
    """O carrinho como está na sessão: {'<id do produto>': '<quantidade>'}."""
    return sessao.get(CHAVE, {})


def adicionar(sessao, produto, quantidade):
    carrinho = sessao.setdefault(CHAVE, {})
    atual = Decimal(carrinho.get(str(produto.pk), "0"))
    carrinho[str(produto.pk)] = str(atual + quantidade)
    sessao.modified = True


def esvaziar(sessao):
    sessao.pop(CHAVE, None)


def subtotal_centavos(preco_centavos, quantidade):
    """Preço vezes quantidade, arredondado para o centavo."""
    valor = preco_centavos * quantidade
    return int(valor.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def itens(sessao):
    """Os itens do carrinho da sessão, com produto e preço lidos do banco."""
    return detalhar(ler(sessao))


def detalhar(carrinho):
    """Transforma {'<id>': '<quantidade>'} em itens, lendo tudo do banco."""
    produtos = {
        p.pk: p
        for p in Produto.objects.filter(pk__in=[int(pk) for pk in carrinho])
        .select_related("produtor", "unidade")
    }
    resultado = []
    for pk, texto in carrinho.items():
        produto = produtos.get(int(pk))
        if produto is None:  # o produto saiu do catálogo depois de entrar no carrinho
            continue
        quantidade = Decimal(texto)
        resultado.append({
            "produto": produto,
            "quantidade": quantidade,
            "subtotal_centavos": subtotal_centavos(produto.preco_centavos, quantidade),
        })
    return resultado


def total_centavos(itens):
    return sum(item["subtotal_centavos"] for item in itens)
