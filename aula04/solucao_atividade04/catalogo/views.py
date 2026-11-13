from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Categoria, Produto, Produtor


def home(request):
    mes = timezone.localdate().month
    destaques = (
        Produto.objects.disponiveis_em(mes)
        .filter(destaque=True)
        .select_related("categoria", "produtor", "unidade")
    )
    contexto = {"destaques": destaques, "total": Produto.objects.count()}
    return render(request, "catalogo/home.html", contexto)


ORDENS = {"nome": ["nome"], "preco": ["preco_centavos", "nome"], "-preco": ["-preco_centavos", "nome"]}


def produtos(request):
    busca = request.GET.get("q", "")
    categoria = request.GET.get("categoria", "")
    produtor = request.GET.get("produtor", "")
    ordem = request.GET.get("ordem", "nome")
    lista = Produto.objects.select_related("categoria", "produtor", "unidade")
    if busca:
        lista = lista.filter(nome__icontains=busca)
    if categoria:
        lista = lista.filter(categoria__slug=categoria)
    if produtor:
        lista = lista.filter(produtor__slug=produtor)
    lista = lista.order_by(*ORDENS.get(ordem, ["nome"]))
    pagina = Paginator(lista, 12).get_page(request.GET.get("page"))
    parametros = request.GET.copy()
    parametros.pop("page", None)
    parametros = parametros.urlencode()
    if parametros:
        parametros += "&"
    contexto = {
        "page_obj": pagina,
        "busca": busca,
        "categoria": categoria,
        "produtor": produtor,
        "ordem": ordem,
        "categorias": Categoria.objects.all(),
        "produtores": Produtor.objects.all(),
        "parametros": parametros,
    }
    return render(request, "catalogo/produto_lista.html", contexto)


def produto(request, slug):
    p = get_object_or_404(
        Produto.objects.select_related("categoria", "produtor", "unidade"), slug=slug
    )
    return render(request, "catalogo/produto_detalhe.html", {"produto": p})


def catalogo_antigo(request):
    return redirect("catalogo:produtos", permanent=True)


def produtores(request):
    busca = request.GET.get("q", "")
    lista = (
        Produtor.objects.annotate(num_produtos=Count("produtos"))
        .prefetch_related("propriedades")
        .order_by("nome")
    )
    if busca:
        lista = lista.filter(
            Q(nome__icontains=busca) | Q(comunidade__icontains=busca)
        )
    pagina = Paginator(lista, 4).get_page(request.GET.get("page"))
    parametros = request.GET.copy()
    parametros.pop("page", None)
    parametros = parametros.urlencode()
    if parametros:
        parametros += "&"
    contexto = {"page_obj": pagina, "busca": busca, "parametros": parametros}
    return render(request, "catalogo/produtor_lista.html", contexto)


def produtor(request, slug):
    pr = get_object_or_404(Produtor.objects.prefetch_related("propriedades"), slug=slug)
    produtos = pr.produtos.select_related("categoria", "unidade")
    contexto = {"produtor": pr, "produtos": produtos}
    return render(request, "catalogo/produtor_detalhe.html", contexto)
