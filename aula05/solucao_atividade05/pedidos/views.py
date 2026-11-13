from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from . import carrinho, servicos
from .forms import FechamentoForm
from .models import Pedido


def ver_carrinho(request):
    itens = carrinho.itens(request.session)
    contexto = {"itens": itens, "total_centavos": carrinho.total_centavos(itens)}
    return render(request, "pedidos/carrinho.html", contexto)


@require_POST
def esvaziar(request):
    carrinho.esvaziar(request.session)
    messages.success(request, "Carrinho esvaziado.")
    return redirect("pedidos:carrinho")


def checkout(request):
    itens = carrinho.itens(request.session)
    if not itens:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect("pedidos:carrinho")
    if request.method == "POST":
        form = FechamentoForm(request.POST)
        if form.is_valid():
            try:
                pedido = servicos.criar_pedido(
                    carrinho.ler(request.session), form.cleaned_data
                )
            except ValidationError as erro:
                form.add_error(None, erro)
            else:
                carrinho.esvaziar(request.session)
                messages.success(request, "Pedido recebido!")
                return redirect("pedidos:pedido", codigo=pedido.codigo)
    else:
        form = FechamentoForm()
    contexto = {
        "form": form,
        "itens": itens,
        "total_centavos": carrinho.total_centavos(itens),
    }
    return render(request, "pedidos/checkout.html", contexto)


def pedido(request, codigo):
    p = get_object_or_404(Pedido.objects.select_related("ponto_retirada"), codigo=codigo)
    itens = [
        {
            "nome": i.nome_produto,
            "produtor": i.nome_produtor,
            "unidade": i.nome_unidade,
            "quantidade": i.quantidade,
            "preco_unitario_centavos": i.preco_unitario_centavos,
            "subtotal_centavos": carrinho.subtotal_centavos(
                i.preco_unitario_centavos, i.quantidade
            ),
        }
        for i in p.itens.all()
    ]
    contexto = {
        "pedido": p,
        "itens": itens,
        "total_centavos": sum(i["subtotal_centavos"] for i in itens),
    }
    return render(request, "pedidos/pedido.html", contexto)
