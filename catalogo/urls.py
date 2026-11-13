from . import views_painel



urrlpartens: [
                path(
    "painel/pedidos/",
    views_painel.PainelPedidosView.as_view(),
    name="painel_pedidos",
),

path(
    "painel/pedidos/<uuid:codigo>/",
    views_painel.PainelPedidoDetailView.as_view(),
    name="painel_pedido",
),

]
