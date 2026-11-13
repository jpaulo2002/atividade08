from django import forms

from .models import Pedido
from .servicos import validar_quantidade


class AdicionarAoCarrinhoForm(forms.Form):
    quantidade = forms.DecimalField(max_digits=8, decimal_places=3)

    def __init__(self, *args, produto, **kwargs):
        super().__init__(*args, **kwargs)
        self.produto = produto
        passo = "0.001" if produto.unidade.fracionavel else "1"
        self.fields["quantidade"].widget.attrs.update({"min": passo, "step": passo})

    def clean_quantidade(self):
        quantidade = self.cleaned_data["quantidade"]
        if quantidade <= 0:
            raise forms.ValidationError("A quantidade tem que ser maior que zero.")
        return quantidade

    def clean(self):
        dados = super().clean()
        quantidade = dados.get("quantidade")
        if quantidade is not None:  # se o campo falhou, não há o que cruzar
            validar_quantidade(self.produto, quantidade)
        return dados


class FechamentoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["comprador", "telefone", "ponto_retirada"]
