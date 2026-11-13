from django import template

register = template.Library()


@register.filter
def reais(centavos):
    """Recebe um valor inteiro em centavos e devolve o texto 'R$ 1.234,56'."""
    try:
        centavos = int(centavos)
    except (TypeError, ValueError):
        return ""
    sinal = "-" if centavos < 0 else ""
    inteiro, resto = divmod(abs(centavos), 100)
    milhares = f"{inteiro:,}".replace(",", ".")
    return f"{sinal}R$ {milhares},{resto:02d}"
