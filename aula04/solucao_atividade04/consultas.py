from django.db.models import Count, F, Max, Min, Sum

from catalogo.models import Categoria, Produto, Produtor, Unidade

# 1. Os produtos de até R$ 10,00, do mais barato para o mais caro.
c1 = Produto.objects.filter(preco_centavos__lte=1000).order_by("preco_centavos")
print(1, [p.nome for p in c1])

# 2. Os produtos com "pimenta" no nome, sem diferenciar maiúsculas.
c2 = Produto.objects.filter(nome__icontains="pimenta")
print(2, [p.nome for p in c2])

# 3. Os produtos dos produtores da Colônia do Uraim.
c3 = Produto.objects.filter(produtor__comunidade="Colônia do Uraim")
print(3, [p.nome for p in c3])

# 4. Os produtos vendidos em unidade fracionável.
c4 = Produto.objects.filter(unidade__fracionavel=True)
print(4, [p.nome for p in c4])

# 5. Os produtores independentes (sem cooperativa).
c5 = Produtor.objects.filter(cooperativa="")
print(5, [p.nome for p in c5])

# 6. Cada categoria com quantos produtos tem, da que tem mais para a que tem menos.
c6 = Categoria.objects.annotate(n=Count("produtos")).order_by("-n", "nome")
print(6, [(c.nome, c.n) for c in c6])

# 7. O menor e o maior preço do catálogo.
c7 = Produto.objects.aggregate(menor=Min("preco_centavos"), maior=Max("preco_centavos"))
print(7, c7)

# 8. O valor de todo o estoque da feira, em centavos (preço vezes estoque, somado).
c8 = Produto.objects.aggregate(total=Sum(F("preco_centavos") * F("estoque")))
print(8, c8)

# 9. Os produtos que NÃO estão disponíveis em fevereiro.
c9 = Produto.objects.exclude(pk__in=Produto.objects.disponiveis_em(2))
print(9, [p.nome for p in c9])

# 10. Os produtos de produtores da Colônia do Uraim disponíveis em novembro, por preço.
c10 = (Produto.objects.disponiveis_em(11)
       .filter(produtor__comunidade="Colônia do Uraim").order_by("preco_centavos"))
print(10, [p.nome for p in c10])
