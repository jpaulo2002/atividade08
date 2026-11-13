from django.contrib import admin

from .models import Categoria, JanelaSafra, Produto, Produtor, Propriedade, Unidade


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nome", "slug"]
    prepopulated_fields = {"slug": ["nome"]}


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ["nome", "sigla", "fracionavel"]


@admin.register(Produtor)
class ProdutorAdmin(admin.ModelAdmin):
    list_display = ["nome", "comunidade", "cooperativa", "pedido_minimo_centavos"]
    search_fields = ["nome", "comunidade"]
    prepopulated_fields = {"slug": ["nome"]}


@admin.register(Propriedade)
class PropriedadeAdmin(admin.ModelAdmin):
    list_display = ["nome", "produtor", "comunidade", "area_total_ha", "manejo"]
    list_filter = ["manejo", "casa_de_farinha", "camara_fria"]


class JanelaSafraInline(admin.TabularInline):
    model = JanelaSafra
    extra = 1


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["nome", "produtor", "categoria", "preco_centavos", "estoque",
                    "destaque"]
    list_filter = ["categoria", "destaque"]
    search_fields = ["nome", "variedade", "produtor__nome"]
    prepopulated_fields = {"slug": ["nome"]}
    inlines = [JanelaSafraInline]
