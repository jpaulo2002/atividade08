# ✅ Solução da Atividade 3 — "As tabelas da feira"

> **Esta pasta é a SOLUÇÃO da Atividade 3**, publicada pelo professor **depois do prazo** dela. Serve para duas coisas: conferir o que você fez, e dar um ponto de partida para a **Apostila 4** a quem não terminou a Apostila 3 ou a Atividade 3.
>
> Copiar esta solução agora **não vale nota** na Atividade 3 — o prazo dela já passou. Vale para você seguir o semestre sem ficar para trás.

## O que tem aqui

O projeto inteiro, do jeito que ele fica ao fim da Apostila 3 **mais** a Atividade 3:

| Arquivo | O que é |
|---|---|
| `catalogo/models.py`, `catalogo/migrations/` | os seis modelos do catálogo e as quatro migrações da apostila |
| `catalogo/fixtures/catalogo.json` | a fixture do catálogo |
| `catalogo/views.py`, `catalogo/admin.py` | as views lendo do banco e o admin do catálogo |
| `pedidos/` | a aplicação da Atividade 3: modelos, migração, fixture e admin |
| `agrofeira/settings.py` | com `'pedidos'` em `INSTALLED_APPS` e `CSRF_TRUSTED_ORIGINS` |
| `templates/`, `static/`, `servidor20/` | o que já vinha das aulas anteriores |

O que a Atividade 3 pedia, e onde está:

- `pedidos/models.py` — `PontoRetirada`, `Pedido` e `ItemPedido`, com os nomes de campo da tabela da atividade.
  - Centavos em `PositiveIntegerField`; quantidade em `DecimalField` com três casas; `criado_em` com `auto_now_add=True`; situação com `choices` e `recebido` como padrão.
  - `produtores` é um `ManyToManyField` em `PontoRetirada`, com `related_name="pontos_retirada"` e `blank=True` (regra 6).
- As regras de remoção:
  - `Pedido.ponto_retirada` com `PROTECT`: um ponto com pedidos não some (regra 2).
  - `ItemPedido.pedido` com `CASCADE`: apagar o pedido leva os itens (regra 3).
  - `ItemPedido.produto` com `SET_NULL`: o produto pode sair do catálogo, e o retrato congelado guarda o histórico (regra 2).
- `pedidos/admin.py` — pontos e pedidos registrados, com colunas e filtros; os itens dentro do pedido, num `TabularInline` com `extra = 0`.

## As respostas curtas esperadas no PDF

1. **Regras de remoção** — as três da lista acima, com o motivo de cada uma. `PROTECT` em `ItemPedido.produto` também vale (produto já vendido não se apaga). `CASCADE` em `Pedido.ponto_retirada` ou em `ItemPedido.produto` apagaria histórico.
2. **A tabela a mais** — `pedidos_pontoretirada_produtores`, com `id`, `pontoretirada_id` e `produtor_id`. É a tabela de pares do muitos-para-muitos: cada linha diz "este produtor entrega neste ponto".
3. **O preço diferente** — o item guarda o preço do dia da compra (R$ 28,00); o catálogo mostra o de hoje (R$ 30,00). O pedido é histórico e não pode mudar quando o produto muda.
4. **A quantidade** — `DecimalField`, que guarda o número exato. `FloatField` usa ponto flutuante e erra contas simples (`0.1 + 0.2` dá `0.30000000000000004`).

## Como usar esta solução para começar a Apostila 4

Só faça isto se o **seu** projeto não chegou ao fim da Apostila 3 e da Atividade 3 funcionando. Se chegou, siga direto para a Apostila 4.

1. Abra o codespace do seu repositório `agrofeira-servidor-<seu-usuário>`.
2. No terminal, na **raiz** do seu repositório (o comando `pwd` mostra `/workspaces/agrofeira-servidor-<seu-usuário>`), rode este comando — é uma linha só:

```bash
curl -fsSL https://github.com/fab-araujo/2026.2-DWM-BSI-PGM/archive/refs/heads/main.tar.gz | tar xz --strip-components=3 --exclude=README.md 2026.2-DWM-BSI-PGM-main/aula03/solucao_atividade03
```

   Ele extrai **só o conteúdo desta pasta** na raiz do seu repositório. Arquivos com os mesmos nomes que você já tinha são **substituídos**; arquivos seus com outros nomes ficam.

3. Recrie o banco a partir do que veio, um comando de cada vez:

```bash
rm -f db.sqlite3
python manage.py migrate
python manage.py loaddata catalogo pedidos
python manage.py createsuperuser
```

4. Confira: suba o servidor (`python manage.py runserver 0.0.0.0:8000`) e abra `/produtos/`, `/produtores/` e `/admin/`.
5. Salve no seu repositório pelo painel **Controle do Código-Fonte** (mensagem, **Confirmação**, **Sincronizar alterações**) e comece a Apostila 4 pela Seção 1.

---

*Os nomes de produtores, sítios e compradores usados nos dados são fictícios; a geografia é real.*
