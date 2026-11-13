from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("carrinho/", views.ver_carrinho, name="carrinho"),
    path("carrinho/esvaziar/", views.esvaziar, name="esvaziar"),
    path("checkout/", views.checkout, name="checkout"),
    path("pedido/<uuid:codigo>/", views.pedido, name="pedido"),
]
