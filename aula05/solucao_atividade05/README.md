# ✅ Solução da Atividade 5 — "O fechamento do pedido"

> **Esta pasta é a SOLUÇÃO da Atividade 5**, publicada pelo professor **depois do prazo** dela. Serve para duas coisas: conferir o que você fez, e dar um ponto de partida para a **Apostila 6** a quem não terminou a Apostila 5 ou a Atividade 5.
>
> Copiar esta solução agora **não vale nota** na Atividade 5 — o prazo dela já passou. Vale para você seguir o semestre sem ficar para trás.

## O que tem aqui

O projeto inteiro, do jeito que ele fica ao fim da Apostila 5 **mais** a Atividade 5:

| Arquivo | O que é |
|---|---|
| `pedidos/forms.py` | `AdicionarAoCarrinhoForm` (Apostila 5) e `FechamentoForm` (Atividade 5, Parte A) |
| `pedidos/servicos.py` | `validar_quantidade`, `validar_pedido_minimo` e `criar_pedido` (Parte B) |
| `pedidos/views.py`, `pedidos/urls.py` | carrinho, esvaziar, `checkout` e `pedido/<uuid:codigo>/` (Parte C) |
| `pedidos/templates/pedidos/` | `carrinho.html`, `checkout.html` e `pedido.html` |
| `pedidos/models.py`, `pedidos/migrations/` | com o `codigo` (UUID) do pedido |
| `agrofeira/settings.py` | com `MESSAGE_STORAGE` na sessão |
| `catalogo/`, `templates/`, `static/`, `servidor20/` | o que já vinha das aulas anteriores |

Não há testes nesta pasta: a **Apostila 6** é quem ensina a escrevê-los.

## Como usar esta solução para começar a Apostila 6

Só faça isto se o **seu** projeto não chegou ao fim da Apostila 5 e da Atividade 5 funcionando. Se chegou, siga direto para a Apostila 6.

1. Abra o codespace do seu repositório `agrofeira-servidor-<seu-usuário>`.
2. No terminal, na **raiz** do seu repositório (o comando `pwd` mostra `/workspaces/agrofeira-servidor-<seu-usuário>`), rode este comando — é uma linha só:

```bash
curl -fsSL https://github.com/fab-araujo/2026.2-DWM-BSI-PGM/archive/refs/heads/main.tar.gz | tar xz --strip-components=3 --exclude=README.md 2026.2-DWM-BSI-PGM-main/aula05/solucao_atividade05
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

4. Confira: suba o servidor (`python manage.py runserver 0.0.0.0:8000`) e abra `/produtos/`, `/carrinho/` e `/admin/`.
5. Salve no seu repositório pelo painel **Controle do Código-Fonte** (mensagem, **Confirmação**, **Sincronizar alterações**) e comece a Apostila 6 pela Seção 1.

---

*Os nomes de produtores, sítios e compradores usados nos dados são fictícios; a geografia é real.*
