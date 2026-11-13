# ✅ Solução da Atividade 1 — "O servidor de vinte linhas"

> **Esta pasta é a SOLUÇÃO da Atividade 1**, publicada pelo professor **depois do prazo** dela. Serve para duas coisas: conferir o que você fez, e dar um ponto de partida para a **Apostila 2** a quem não terminou a Atividade 1.
>
> Copiar esta solução agora **não vale nota** na Atividade 1 — o prazo dela já passou. Vale para você seguir o semestre sem ficar para trás.

## O que tem aqui

| Arquivo | O que resolve |
|---|---|
| `servidor20/servidor.py` | Parte B: o servidor de vinte linhas com a rota nova `/produtores/`, que lê `dados/produtores.json` a partir do endereço do próprio script. |
| `manage.py`, `agrofeira/`, `catalogo/` | Parte C: o projeto Django `agrofeira` com a aplicação `catalogo` e a view `home` em `/`. |

Os pontos da Parte C que mais deram trabalho, e onde estão:

- `agrofeira/settings.py` — `'catalogo'` em `INSTALLED_APPS`; `ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.app.github.dev']`; e já com `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Belem'` (o ajuste que a Apostila 2 pede logo no começo).
- `agrofeira/urls.py` — `path('', include('catalogo.urls'))`.
- `catalogo/urls.py` — o arquivo que **não** nasce sozinho: `app_name = "catalogo"` e a rota `""` com o nome `home`.
- `catalogo/views.py` — a view `home`, devolvendo `HttpResponse("<h1>AgroFeira Paragominas</h1>")`.

## Como usar esta solução para começar a Apostila 2

Só faça isto se o **seu** repositório ainda não tem o projeto Django funcionando. Se ele já tem, siga direto para a Apostila 2 — não misture as duas coisas.

1. Tenha o seu repositório `agrofeira-servidor-<seu-usuário>`, criado a partir do modelo da disciplina (Parte A da Atividade 1), e abra o codespace dele.
2. No terminal, na **raiz** do seu repositório (o comando `pwd` mostra `/workspaces/agrofeira-servidor-<seu-usuário>`), rode este comando — é uma linha só:

```bash
curl -fsSL https://github.com/fab-araujo/2026.2-DWM-BSI-PGM/archive/refs/heads/main.tar.gz | tar xz --strip-components=3 --exclude=README.md 2026.2-DWM-BSI-PGM-main/aula01/solucao_atividade01
```

   Ele baixa o repositório da disciplina e extrai **só o conteúdo desta pasta** na raiz do seu repositório: `manage.py`, `agrofeira/`, `catalogo/` e `servidor20/`. (Este README não é copiado, para não substituir o seu.) Se você já tinha arquivos com esses mesmos nomes, eles são substituídos.

3. Confira:

```bash
ls
python manage.py runserver 0.0.0.0:8000
```

   O `ls` tem que mostrar `manage.py`, `agrofeira`, `catalogo` e `servidor20` ao lado de `dados`. Com o servidor no ar, a porta 8000 aberta no navegador mostra **AgroFeira Paragominas**. O aviso vermelho de migrações não aplicadas é esperado.

4. Salve no seu repositório pelo painel **Controle do Código-Fonte** (mensagem, **Confirmação**, **Sincronizar alterações**) e comece a Apostila 2 pela Seção 1.

## O que o relatório da Atividade 1 deveria dizer

Para você comparar com o que escreveu.

**Captura 2 — os cabeçalhos que só o Django envia.** Quem os acrescenta é o `SecurityMiddleware` e o `XFrameOptionsMiddleware`, ligados por padrão em todo projeto novo:

- `X-Frame-Options: DENY` — proíbe que outro site mostre esta página dentro de um `<iframe>`. Protege contra *clickjacking*: o site do atacante esconde a sua página, transparente, por baixo de um botão dele, e o clique do visitante vai parar na sua página sem ele perceber.
- `X-Content-Type-Options: nosniff` — manda o navegador obedecer ao `Content-Type` declarado, sem tentar adivinhar o tipo pelo conteúdo. Impede, por exemplo, que um arquivo enviado como texto seja executado como script.
- `Referrer-Policy: same-origin` — o navegador só envia o cabeçalho `Referer` (de qual página o visitante veio) em pedidos para o **mesmo** site; para outros sites, não conta de onde vem.
- `Cross-Origin-Opener-Policy: same-origin` — isola a janela da página de janelas abertas por sites de outra origem, que não conseguem manipulá-la.

**Captura 3 — sem `'localhost'` em `ALLOWED_HOSTS`.** A resposta é **400 Bad Request**, com o erro `DisallowedHost: Invalid HTTP_HOST header: 'localhost:8000'`. O Django confere o cabeçalho `Host` de todo pedido contra a lista `ALLOWED_HOSTS` e recusa o que não está nela, porque um `Host` forjado pode fazer o próprio site montar links apontando para o domínio de um atacante (num e-mail de redefinição de senha, por exemplo). E o `Host` que chega é `localhost:8000`, não o endereço público: o proxy do Codespaces recebe o pedido do navegador e o repassa ao seu servidor como uma conexão local — o endereço público só vai no cabeçalho `X-Forwarded-Host`, que o Django ignora por padrão. Por isso a correção é ter `'localhost'` na lista.

---

*Os nomes de produtores e sítios usados nos dados são fictícios; a geografia é real.*
