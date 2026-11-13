from django.db import models

from .querysets import ProdutoQuerySet


class Categoria(models.Model):
    nome = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Unidade(models.Model):
    nome = models.CharField(max_length=30)
    sigla = models.CharField(max_length=10)
    fracionavel = models.BooleanField(default=False)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Produtor(models.Model):
    nome = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    comunidade = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    caf = models.CharField("CAF", max_length=20, unique=True)
    cooperativa = models.CharField(max_length=120, blank=True)
    formas_pagamento = models.CharField(max_length=80)
    chave_pix = models.CharField(max_length=80)
    pedido_minimo_centavos = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["nome"]
        verbose_name_plural = "produtores"

    def __str__(self):
        return self.nome


class Propriedade(models.Model):
    MANEJOS = [
        ("convencional", "convencional"),
        ("transicao", "em transição agroecológica"),
        ("agroecologico", "agroecológico"),
        ("organico", "orgânico certificado"),
    ]

    produtor = models.ForeignKey(
        Produtor, on_delete=models.CASCADE, related_name="propriedades"
    )
    nome = models.CharField(max_length=80)
    comunidade = models.CharField(max_length=80)
    referencia = models.CharField("referência de acesso", max_length=200, blank=True)
    distancia_sede_km = models.PositiveIntegerField("distância da sede (km)")
    area_total_ha = models.DecimalField(
        "área total (ha)", max_digits=6, decimal_places=1
    )
    area_saf_ha = models.DecimalField(
        "área em agrofloresta (ha)", max_digits=6, decimal_places=1, default=0
    )
    manejo = models.CharField(max_length=15, choices=MANEJOS)
    fonte_agua = models.CharField("fonte de água", max_length=60)
    casa_de_farinha = models.BooleanField(default=False)
    camara_fria = models.BooleanField("câmara fria", default=False)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    variedade = models.CharField(max_length=60, blank=True)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="produtos"
    )
    produtor = models.ForeignKey(
        Produtor, on_delete=models.PROTECT, related_name="produtos"
    )
    propriedade = models.ForeignKey(
        Propriedade, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="produtos",
    )
    unidade = models.ForeignKey(
        Unidade, on_delete=models.PROTECT, related_name="produtos"
    )
    preco_centavos = models.PositiveIntegerField()
    estoque = models.PositiveIntegerField(default=0)
    destaque = models.BooleanField(default=False)
    conservacao = models.CharField("conservação", max_length=120, blank=True)
    validade = models.DateField(null=True, blank=True)

    objects = ProdutoQuerySet.as_manager()

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class JanelaSafra(models.Model):
    MESES = [
        (1, "janeiro"), (2, "fevereiro"), (3, "março"), (4, "abril"),
        (5, "maio"), (6, "junho"), (7, "julho"), (8, "agosto"),
        (9, "setembro"), (10, "outubro"), (11, "novembro"), (12, "dezembro"),
    ]
    SITUACOES = [
        ("pico", "pico de safra"),
        ("disponivel", "disponível"),
        ("entressafra", "entressafra"),
        ("fora", "fora de safra"),
    ]

    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name="safras"
    )
    mes_inicio = models.PositiveIntegerField("mês inicial", choices=MESES)
    mes_fim = models.PositiveIntegerField("mês final", choices=MESES)
    situacao = models.CharField("situação", max_length=12, choices=SITUACOES)

    class Meta:
        ordering = ["mes_inicio"]
        verbose_name = "janela de safra"
        verbose_name_plural = "janelas de safra"

    def __str__(self):
        inicio = self.get_mes_inicio_display()
        fim = self.get_mes_fim_display()
        return f"{inicio} a {fim}: {self.get_situacao_display()}"
