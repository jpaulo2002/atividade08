from django.shortcuts import get_object_or_404, redirect, render

from .models import Produto, Produtor


def home(request):
    destaques = Produto.objects.filter(destaque=True)
    contexto = {"destaques": destaques, "total": Produto.objects.count()}
    return render(request, "catalogo/home.html", contexto)


def produtos(request):
    busca = request.GET.get("q", "")
    lista = Produto.objects.all()
    if busca:
        lista = lista.filter(nome__icontains=busca)
    contexto = {"produtos": lista, "busca": busca}
    return render(request, "catalogo/produto_lista.html", contexto)


def produto(request, slug):
    p = get_object_or_404(Produto, slug=slug)
    return render(request, "catalogo/produto_detalhe.html", {"produto": p})


def catalogo_antigo(request):
    return redirect("catalogo:produtos", permanent=True)


def produtores(request):
    busca = request.GET.get("q", "")
    lista = Produtor.objects.all()
    if busca:
        lista = (lista.filter(nome__icontains=busca)
                 | lista.filter(comunidade__icontains=busca))
    contexto = {"produtores": lista, "busca": busca}
    return render(request, "catalogo/produtor_lista.html", contexto)


def produtor(request, slug):
    pr = get_object_or_404(Produtor, slug=slug)
    contexto = {"produtor": pr, "produtos": pr.produtos.all()}
    return render(request, "catalogo/produtor_detalhe.html", contexto)
