from django.contrib import admin

from .models import ItemPedido, Pedido, PontoRetirada


@admin.register(PontoRetirada)
class PontoRetiradaAdmin(admin.ModelAdmin):
    list_display = ["nome", "endereco", "horario"]


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["comprador", "ponto_retirada", "situacao", "criado_em"]
    list_filter = ["situacao", "ponto_retirada"]
    inlines = [ItemPedidoInline]
