# ✅ Solução da Atividade 2 — "Os produtores da feira"

> **Esta pasta é a SOLUÇÃO da Atividade 2**, publicada pelo professor **depois do prazo** dela. Serve para duas coisas: conferir o que você fez, e dar um ponto de partida para a **Apostila 3** a quem não terminou a Apostila 2 ou a Atividade 2.
>
> Copiar esta solução agora **não vale nota** na Atividade 2 — o prazo dela já passou. Vale para você seguir o semestre sem ficar para trás.

## O que tem aqui

O projeto inteiro, do jeito que ele fica ao fim da Apostila 2 **mais** a Atividade 2:

| Arquivo | O que é |
|---|---|
| `manage.py`, `agrofeira/` | o projeto, com `templates/` e `static/` configurados no `settings.py` |
| `catalogo/` | a aplicação: `dados.py`, as views, as rotas, os templates, o filtro `reais` |
| `templates/base.html` | o layout, já com **Produtores** no menu |
| `static/css/agrofeira.css` | a folha de estilos |
| `servidor20/servidor.py` | o servidor de vinte linhas da Atividade 1 |

O que a Atividade 2 pedia, e onde está:

- `catalogo/urls.py` — as rotas `produtores/` (nome `produtores`) e `produtores/<slug:slug>/` (nome `produtor`).
- `catalogo/views.py` — a view `produtores`, com a busca por nome **ou** comunidade, sem diferenciar maiúsculas; e a view `produtor`, que procura pelo slug, junta os produtos daquele produtor e levanta `Http404` quando não acha.
- `catalogo/templates/catalogo/produtor_lista.html` — a lista, com o formulário de busca, a frase com `pluralize:"es"` e o `{% empty %}`.
- `catalogo/templates/catalogo/produtor_detalhe.html` — o perfil, com a trilha e os produtos pelo `{% include %}` do cartão.
- `templates/base.html` e `catalogo/templates/catalogo/produto_detalhe.html` — o link **Produtores** no menu e o nome do produtor como link.

## Como usar esta solução para começar a Apostila 3

Só faça isto se o **seu** projeto não chegou ao fim da Apostila 2 e da Atividade 2 funcionando. Se chegou, siga direto para a Apostila 3 — não misture as duas coisas.

1. Abra o codespace do seu repositório `agrofeira-servidor-<seu-usuário>`.
2. No terminal, na **raiz** do seu repositório (o comando `pwd` mostra `/workspaces/agrofeira-servidor-<seu-usuário>`), rode este comando — é uma linha só:

```bash
curl -fsSL https://github.com/fab-araujo/2026.2-DWM-BSI-PGM/archive/refs/heads/main.tar.gz | tar xz --strip-components=3 --exclude=README.md 2026.2-DWM-BSI-PGM-main/aula02/solucao_atividade02
```

   Ele baixa o repositório da disciplina e extrai **só o conteúdo desta pasta** na raiz do seu repositório. Arquivos com os mesmos nomes que você já tinha são **substituídos**; arquivos seus com outros nomes ficam.

3. Confira: suba o servidor (`python manage.py runserver 0.0.0.0:8000`) e abra `/produtos/`, `/produtores/` e `/produtores/dona-graca-do-mel/`.
4. Salve no seu repositório pelo painel **Controle do Código-Fonte** (mensagem, **Confirmação**, **Sincronizar alterações**) e comece a Apostila 3 pela Seção 1.

---

*Os nomes de produtores e sítios usados nos dados são fictícios; a geografia é real.*
