# ✅ Solução da Atividade 6 — "A suíte que prova as regras"

> **Esta pasta é a SOLUÇÃO da Atividade 6**, publicada pelo professor **depois do prazo** dela. Serve para duas coisas: conferir o que você fez, e dar um ponto de partida para a **Apostila 8** a quem não terminou a Apostila 6 ou a Atividade 6.
>
> Copiar esta solução agora **não vale nota** na Atividade 6 — o prazo dela já passou. Vale para você seguir o semestre sem ficar para trás.

## O que tem aqui

O projeto inteiro, do jeito que ele fica ao fim da Apostila 6 **mais** a Atividade 6:

| Arquivo | O que é |
|---|---|
| `pedidos/tests.py` | a suíte da apostila (subtotal, quantidade, formulário, pedido mínimo, transação de brinquedo, carrinho) e as classes da Parte A: as regras do `criar_pedido`, a transação do `criar_pedido` e as páginas do fechamento |
| `catalogo/tests.py` | os testes do `disponiveis_em` e das páginas, e o da safra que atravessa o ano (Parte B) |
| `agrofeira/middleware.py` | o `TempoDeRespostaMiddleware`, ligado como primeira linha do `MIDDLEWARE` |
| `agrofeira/tests.py` | a ordem do `MIDDLEWARE` (apostila) e os testes do middleware, isolado e ligado (Parte C) |
| `pedidos/`, `catalogo/`, `agrofeira/settings.py`, `templates/`, `static/`, `servidor20/` | o que já vinha das aulas anteriores |

Fica de fora, porque não é código: a tabela de sabotagens (Parte D) e a página de texto (Parte E). A pasta `padroes/` da Seção 12 da Apostila 6 também não vem aqui: são exemplos soltos de Python, que não fazem parte do projeto.

## Como usar esta solução para começar a Apostila 8

Só faça isto se o **seu** projeto não chegou ao fim da Apostila 6 e da Atividade 6 funcionando. Se chegou, siga direto para a Apostila 8.

1. Abra o codespace do seu repositório `agrofeira-servidor-<seu-usuário>`.
2. No terminal, na **raiz** do seu repositório (o comando `pwd` mostra `/workspaces/agrofeira-servidor-<seu-usuário>`), rode este comando — é uma linha só:

```bash
curl -fsSL https://github.com/fab-araujo/2026.2-DWM-BSI-PGM/archive/refs/heads/main.tar.gz | tar xz --strip-components=3 --exclude=README.md 2026.2-DWM-BSI-PGM-main/aula06/solucao_atividade06
```

   Ele extrai **só o conteúdo desta pasta** na raiz do seu repositório. Arquivos com os mesmos nomes que você já tinha são **substituídos**; arquivos seus com outros nomes ficam.

3. Instale o que o projeto pede e recrie o banco a partir do que veio, um comando de cada vez:

```bash
pip install -r requirements.txt
rm -f db.sqlite3
python manage.py migrate
python manage.py loaddata catalogo pedidos
python manage.py createsuperuser
```

4. Confira: rode `python manage.py test` (tem que terminar em `OK`), suba o servidor (`python manage.py runserver 0.0.0.0:8000`) e abra `/produtos/`, `/carrinho/` e `/admin/`.
5. Salve no seu repositório pelo painel **Controle do Código-Fonte** (mensagem, **Confirmação**, **Sincronizar alterações**) e comece a Apostila 8 pela Seção 1.

---

*Os nomes de produtores, sítios e compradores usados nos dados são fictícios; a geografia é real.*
