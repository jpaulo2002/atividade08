from django.db.models import Count, Q
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from pedidos.models import Pedido, ItemPedido

from pedidos.carrinho import subtotal_centavos


class PainelPedidosView(ProdutorLogado, ListView):
    model = Pedido
    template_name = "catalogo/painel/pedidos.html"
    context_object_name = "pedidos"

    def get_queryset(self):
        produtor = self.request.user.produtor

        return (
            Pedido.objects.filter(
                itens__produto__produtor=produtor
            )
            .annotate(
                meus_itens=Count(
                    "itens",
                    filter=Q(itens__produto__produtor=produtor)
                )
            )
            .distinct()
            .order_by("-criado_em")
        )



class PainelPedidoDetailView(ProdutorLogado, DetailView):
    model = Pedido
    template_name = "catalogo/painel/pedido.html"
    context_object_name = "pedido"

    slug_field = "codigo"
    slug_url_kwarg = "codigo"

    def get_queryset(self):
        produtor = self.request.user.produtor

        return (
            Pedido.objects.filter(
                itens__produto__produtor=produtor
            )
            .distinct()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        produtor = self.request.user.produtor

        itens_produtor = ItemPedido.objects.filter(
            pedido=self.object,
            produto__produtor=produtor
        )

        itens = []
        total_centavos = 0

        for item in itens_produtor:
            subtotal = subtotal_centavos(
                item.preco_unitario_centavos,
                item.quantidade
            )

            itens.append({
                "item": item,
                "subtotal": subtotal,
            })

            total_centavos += subtotal

        context["itens"] = itens
        context["total_centavos"] = total_centavos

        return context