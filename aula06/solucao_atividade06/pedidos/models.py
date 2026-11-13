import uuid

from django.db import models

from catalogo.models import Produto, Produtor


class PontoRetirada(models.Model):
    nome = models.CharField(max_length=80)
    endereco = models.CharField("endereço", max_length=200)
    horario = models.CharField("horário", max_length=80)
    produtores = models.ManyToManyField(
        Produtor, related_name="pontos_retirada", blank=True
    )

    class Meta:
        ordering = ["nome"]
        verbose_name = "ponto de retirada"
        verbose_name_plural = "pontos de retirada"

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    SITUACOES = [
        ("recebido", "recebido"),
        ("separado", "separado"),
        ("entregue", "entregue"),
        ("cancelado", "cancelado"),
    ]

    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    comprador = models.CharField(max_length=80)
    telefone = models.CharField(max_length=20)
    ponto_retirada = models.ForeignKey(
        PontoRetirada, on_delete=models.PROTECT, related_name="pedidos"
    )
    situacao = models.CharField(
        "situação", max_length=10, choices=SITUACOES, default="recebido"
    )
    criado_em = models.DateTimeField("feito em", auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Pedido {self.pk} - {self.comprador}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="itens"
    )
    produto = models.ForeignKey(
        Produto, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="itens_pedido",
    )
    nome_produto = models.CharField(max_length=80)
    nome_produtor = models.CharField(max_length=80)
    nome_unidade = models.CharField(max_length=30)
    preco_unitario_centavos = models.PositiveIntegerField()
    quantidade = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        verbose_name = "item do pedido"
        verbose_name_plural = "itens do pedido"

    def __str__(self):
        return f"{self.quantidade} x {self.nome_produto}"
