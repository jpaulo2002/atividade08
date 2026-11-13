# ✅ Solução da Atividade 4 — "Consultas sem desperdício"

> **Esta pasta é a SOLUÇÃO da Atividade 4**, publicada pelo professor **depois do prazo** dela. Serve para duas coisas: conferir o que você fez, e dar um ponto de partida para a **Apostila 5** a quem não terminou a Apostila 4 ou a Atividade 4.
>
> Copiar esta solução agora **não vale nota** na Atividade 4 — o prazo dela já passou. Vale para você seguir o semestre sem ficar para trás.

## O que tem aqui

O projeto inteiro, do jeito que ele fica ao fim da Apostila 4 **mais** a Atividade 4:

| Arquivo | O que é |
|---|---|
| `catalogo/views.py` | as views `produtos` (busca, filtros, ordem e páginas), `produto` e `produtor` |
| `catalogo/querysets.py` | o `QuerySet` do catálogo, com a consulta de safra |
| `consultas.py` | as dez consultas da Parte C |
| `templates/`, `catalogo/templates/`, `static/css/agrofeira.css` | as páginas da Apostila 4 |
| `catalogo/`, `pedidos/`, `agrofeira/`, `servidor20/` | o que já vinha das aulas anteriores |

O que a Atividade 4 pedia, e onde está:

- **Parte A** — `produtos` em `catalogo/views.py`: filtros `q`, `categoria` e `produtor`, ordem (`nome`, `preco`, `-preco`; valor desconhecido cai em `nome`), `Paginator` com 12 por página, e `page` fora do intervalo levado à última página. O `?page=` some dos links de página para os filtros não se perderem.
- **Parte B** — `produto` e `produtor`: `get_object_or_404`, `select_related` nas relações de um e `prefetch_related` nas de muitos, para o perfil do produtor não fazer uma consulta por produto.
- **Parte C** — `consultas.py`: as dez consultas, cada uma com o seu `print`.
- **Parte D e respostas curtas** — são texto do PDF; a tabela antes/depois você mede no seu projeto.

## Como usar esta solução para começar a Apostila 5

Só faça isto se o **seu** projeto não chegou ao fim da Apostila 4 e da Atividade 4 funcionando. Se chegou, siga direto para a Apostila 5.

1. Abra o codespace do seu repositório `agrofeira-servidor-<seu-usuário>`.
2. No terminal, na **raiz** do seu repositório (o comando `pwd` mostra `/workspaces/agrofeira-servidor-<seu-usuário>`), rode este comando — é uma linha só:

```bash
curl -fsSL https://github.com/fab-araujo/2026.2-DWM-BSI-PGM/archive/refs/heads/main.tar.gz | tar xz --strip-components=3 --exclude=README.md 2026.2-DWM-BSI-PGM-main/aula04/solucao_atividade04
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

4. Confira: suba o servidor (`python manage.py runserver 0.0.0.0:8000`) e abra `/produtos/`, `/produtores/` e `/admin/`.
5. Salve no seu repositório pelo painel **Controle do Código-Fonte** (mensagem, **Confirmação**, **Sincronizar alterações**) e comece a Apostila 5 pela Seção 1.

---

*Os nomes de produtores, sítios e compradores usados nos dados são fictícios; a geografia é real.*
