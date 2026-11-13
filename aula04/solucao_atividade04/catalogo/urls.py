from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.home, name="home"),
    path("produtos/", views.produtos, name="produtos"),
    path("produtos/<slug:slug>/", views.produto, name="produto"),
    path("catalogo/", views.catalogo_antigo),
    path("produtores/", views.produtores, name="produtores"),
    path("produtores/<slug:slug>/", views.produtor, name="produtor"),
]
