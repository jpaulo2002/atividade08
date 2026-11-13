from django.http import Http404
from django.shortcuts import redirect, render

from .dados import PRODUTORES, PRODUTOS


def home(request):
    destaques = [p for p in PRODUTOS if p["destaque"]]
    contexto = {"destaques": destaques, "total": len(PRODUTOS)}
    return render(request, "catalogo/home.html", contexto)


def produtos(request):
    busca = request.GET.get("q", "")
    lista = PRODUTOS
    if busca:
        lista = [p for p in PRODUTOS if busca.lower() in p["nome"].lower()]
    contexto = {"produtos": lista, "busca": busca}
    return render(request, "catalogo/produto_lista.html", contexto)


def produto(request, slug):
    for p in PRODUTOS:
        if p["slug"] == slug:
            return render(request, "catalogo/produto_detalhe.html", {"produto": p})
    raise Http404("Nenhum produto com esse endereço.")


def catalogo_antigo(request):
    return redirect("catalogo:produtos", permanent=True)


def produtores(request):
    busca = request.GET.get("q", "")
    lista = PRODUTORES
    if busca:
        termo = busca.lower()
        lista = [pr for pr in PRODUTORES
                 if termo in pr["nome"].lower() or termo in pr["comunidade"].lower()]
    contexto = {"produtores": lista, "busca": busca}
    return render(request, "catalogo/produtor_lista.html", contexto)


def produtor(request, slug):
    for pr in PRODUTORES:
        if pr["slug"] == slug:
            dele = [p for p in PRODUTOS if p["produtor"]["slug"] == slug]
            contexto = {"produtor": pr, "produtos": dele}
            return render(request, "catalogo/produtor_detalhe.html", contexto)
    raise Http404("Nenhum produtor com esse endereço.")
