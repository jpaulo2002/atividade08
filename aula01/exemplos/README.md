# Aula 1 — exemplos mostrados em sala

- `servidor20/v1_ingenuo.py` — tentativa ingênua: responde qualquer caminho com o mesmo texto.
- `servidor20/v2_le_caminho.py` — lê `self.path`, ainda sem recusar o que não existe.
- `servidor20/servidor.py` — a versão final: duas rotas (`/` e `/produtos/`) e 404 para o resto.
- `django_demo/` — o projeto Django criado em aula (`django-admin startproject agrofeira .` e `manage.py startapp catalogo`), com a view `home` em `/`.

Material de consulta pra quando você travar — não pra copiar. O seu trabalho vai na raiz do seu próprio repositório (`servidor20/` e `agrofeira/`+`catalogo/`, criados do zero com os comandos da Atividade 1), não aqui dentro. Copiar estes arquivos pra lá até "funciona", mas você não aprende `INSTALLED_APPS`, `include()` ou `ALLOWED_HOSTS` — e o relatório da Atividade 1 pede que você explique o que fez.