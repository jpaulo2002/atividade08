from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from catalogo.models import Produtor

SENHA = "feira2026"  # só para a aula; em produção cada pessoa escolhe a sua

USUARIOS = {
    "dona-raimunda-do-acai": "raimunda",
    "seu-tonico-da-farinha": "tonico",
    "irmaos-sousa": "sousa",
    "dona-graca-do-mel": "graca",
    "seu-benedito-da-pimenta": "benedito",
    "dona-socorro-do-cacau": "socorro",
    "familia-oliveira": "oliveira",
    "dona-francisca-das-polpas": "francisca",
}


class Command(BaseCommand):
    help = "Cria um usuário para cada produtor da fixture e liga os dois."

    def handle(self, *args, **opcoes):
        if not settings.DEBUG:
            raise CommandError("Contas com senha pública só existem em desenvolvimento (DEBUG = True).")
        for slug, nome in USUARIOS.items():
            produtor = Produtor.objects.filter(slug=slug).first()
            if produtor is None:
                self.stdout.write(f"pulado: não há produtor {slug}")
                continue
            usuario, criado = User.objects.get_or_create(username=nome)
            if criado:
                usuario.set_password(SENHA)
                usuario.save()
            produtor.usuario = usuario
            produtor.save()
            self.stdout.write(f"{'criado' if criado else 'já existia'}: {nome} → {produtor.nome}")
