from django.db import models
from django.db.models import F, Q


class ProdutoQuerySet(models.QuerySet):
    def disponiveis_em(self, mes):
        no_mesmo_ano = Q(safras__mes_inicio__lte=mes, safras__mes_fim__gte=mes)
        virando_o_ano = Q(safras__mes_inicio__gt=F("safras__mes_fim")) & (
            Q(safras__mes_inicio__lte=mes) | Q(safras__mes_fim__gte=mes)
        )
        return self.filter(
            no_mesmo_ano | virando_o_ano,
            safras__situacao__in=["pico", "disponivel"],
        ).distinct()
