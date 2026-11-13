"""Os dados da AgroFeira Paragominas, ainda numa lista Python.

Arquivo fornecido no encontro 2: baixe para catalogo/dados.py e NAO edite.
Os nomes de campo (nome, slug, preco_centavos, produtor, unidade...) sao
os mesmos que os modelos do banco de dados vao ter. Por isso, quando os
dados sairem daqui e forem para o banco, os templates nao mudam.

Dinheiro em centavos inteiros: 2200 quer dizer R$ 22,00.
Nomes de produtores e sitios sao ficticios; a geografia e real.
"""

# ---------------------------------------------------------------- categorias
ACAI_E_FRUTOS = {"nome": "Açaí e frutos da floresta", "slug": "acai-e-frutos-da-floresta"}
POLPAS = {"nome": "Polpas congeladas", "slug": "polpas-congeladas"}
MANDIOCA = {"nome": "Derivados da mandioca", "slug": "derivados-da-mandioca"}
ESPECIARIAS = {"nome": "Especiarias", "slug": "especiarias"}
CACAU = {"nome": "Cacau e chocolate", "slug": "cacau-e-chocolate"}
MEL = {"nome": "Mel e derivados da colmeia", "slug": "mel-e-derivados-da-colmeia"}
HORTALICAS = {"nome": "Hortaliças e temperos verdes", "slug": "hortalicas-e-temperos-verdes"}
FRUTAS = {"nome": "Frutas frescas", "slug": "frutas-frescas"}

CATEGORIAS = [ACAI_E_FRUTOS, POLPAS, MANDIOCA, ESPECIARIAS, CACAU, MEL, HORTALICAS, FRUTAS]

# ---------------------------------------------------------------- unidades
# fracionavel=True: aceita quantidade quebrada (1,5 kg). As outras, nao.
QUILO = {"nome": "quilo", "sigla": "kg", "fracionavel": True}
LITRO = {"nome": "litro", "sigla": "L", "fracionavel": True}
GRAMA = {"nome": "grama", "sigla": "g", "fracionavel": True}
SACA = {"nome": "saca de 60 kg", "sigla": "saca", "fracionavel": False}
LATA = {"nome": "lata de 18 litros", "sigla": "lata", "fracionavel": False}
RASA = {"nome": "rasa", "sigla": "rasa", "fracionavel": False}
MACO = {"nome": "maço", "sigla": "maço", "fracionavel": False}
DUZIA = {"nome": "dúzia", "sigla": "dz", "fracionavel": False}
POTE = {"nome": "pote", "sigla": "pote", "fracionavel": False}
VIDRO = {"nome": "vidro", "sigla": "vidro", "fracionavel": False}
BANDEJA = {"nome": "bandeja", "sigla": "bdj", "fracionavel": False}
BARRA = {"nome": "barra", "sigla": "barra", "fracionavel": False}
CACHO = {"nome": "cacho", "sigla": "cacho", "fracionavel": False}
CENTO = {"nome": "cento", "sigla": "cento", "fracionavel": False}

UNIDADES = [QUILO, LITRO, GRAMA, SACA, LATA, RASA, MACO, DUZIA, POTE, VIDRO,
            BANDEJA, BARRA, CACHO, CENTO]

# ---------------------------------------------------------------- produtores
RAIMUNDA = {
    "nome": "Dona Raimunda do Açaí",
    "slug": "dona-raimunda-do-acai",
    "comunidade": "Sítio Recanto do Açaí — Rio Capim",
    "cooperativa": "Cooperativa Mista do Rio Capim",
    "caf": "PA0412.2025.00137",
    "formas_pagamento": "Pix, dinheiro",
    "chave_pix": "raimunda.acai@exemplo.com",
    "pedido_minimo_centavos": 3000,
    "descricao": "Bate o açaí de madrugada, no mesmo dia da colheita. Três gerações no mesmo açaizal de várzea.",
}
TONICO = {
    "nome": "Seu Tonico da Farinha",
    "slug": "seu-tonico-da-farinha",
    "comunidade": "Colônia do Uraim",
    "cooperativa": "",
    "caf": "PA0412.2024.00981",
    "formas_pagamento": "Pix, dinheiro, cartão",
    "chave_pix": "(91) 90000-0101",
    "pedido_minimo_centavos": 2000,
    "descricao": "Casa de farinha própria. Farinha d'água de puba, torrada no forno de lenha.",
}
IRMAOS_SOUSA = {
    "nome": "Irmãos Sousa",
    "slug": "irmaos-sousa",
    "comunidade": "Chácara Dois Irmãos — Vila de Cumaru",
    "cooperativa": "",
    "caf": "PA0412.2025.00455",
    "formas_pagamento": "Pix, dinheiro",
    "chave_pix": "irmaossousa@exemplo.com",
    "pedido_minimo_centavos": 1000,
    "descricao": "Hortaliças e temperos colhidos na véspera da feira, sem agrotóxico.",
}
GRACA = {
    "nome": "Dona Graça do Mel",
    "slug": "dona-graca-do-mel",
    "comunidade": "Sítio Água Fria — PA-125",
    "cooperativa": "Associação dos Meliponicultores de Paragominas",
    "caf": "PA0412.2023.01220",
    "formas_pagamento": "Pix",
    "chave_pix": "(91) 90000-0202",
    "pedido_minimo_centavos": 3500,
    "descricao": "Cria abelha sem ferrão (uruçu) e abelha africanizada, em caixas espalhadas pelo quintal agroflorestal.",
}
BENEDITO = {
    "nome": "Seu Benedito da Pimenta",
    "slug": "seu-benedito-da-pimenta",
    "comunidade": "Sítio Nova Aliança — Ramal do Uraim",
    "cooperativa": "Cooperativa Agrícola do Uraim",
    "caf": "PA0412.2024.00310",
    "formas_pagamento": "Pix, dinheiro",
    "chave_pix": "benedito.pimenta@exemplo.com",
    "pedido_minimo_centavos": 5000,
    "descricao": "Pimenta-do-reino secada ao sol no terreiro. Vende a saca para quem revende e o quilo para quem cozinha.",
}
SOCORRO = {
    "nome": "Dona Socorro do Cacau",
    "slug": "dona-socorro-do-cacau",
    "comunidade": "Sítio Boa Esperança — Rio Uraim",
    "cooperativa": "Cooperativa Agrícola do Uraim",
    "caf": "PA0412.2025.00702",
    "formas_pagamento": "Pix, cartão",
    "chave_pix": "(91) 90000-0303",
    "pedido_minimo_centavos": 2500,
    "descricao": "Cacau de sombra, fermentado no cocho de madeira. Faz o chocolate em casa, em barras de 100 g.",
}
OLIVEIRA = {
    "nome": "Família Oliveira",
    "slug": "familia-oliveira",
    "comunidade": "Fazenda Santa Luzia — BR-010, km 210",
    "cooperativa": "",
    "caf": "PA0412.2023.00056",
    "formas_pagamento": "Pix, dinheiro, cartão",
    "chave_pix": "familiaoliveira@exemplo.com",
    "pedido_minimo_centavos": 2000,
    "descricao": "Pomar familiar à beira da BR-010: banana, laranja e maracujá o ano inteiro.",
}
FRANCISCA = {
    "nome": "Dona Francisca das Polpas",
    "slug": "dona-francisca-das-polpas",
    "comunidade": "Colônia do Uraim",
    "cooperativa": "Cooperativa Mista do Rio Capim",
    "caf": "PA0412.2024.01133",
    "formas_pagamento": "Pix",
    "chave_pix": "(91) 90000-0404",
    "pedido_minimo_centavos": 4000,
    "descricao": "Despolpa e congela a fruta no mesmo dia. Entrega em caixa térmica.",
}

PRODUTORES = [RAIMUNDA, TONICO, IRMAOS_SOUSA, GRACA, BENEDITO, SOCORRO, OLIVEIRA, FRANCISCA]

# ---------------------------------------------------------------- produtos
PRODUTOS = [
    {"nome": "Açaí médio", "slug": "acai-medio", "variedade": "médio (tipo B)",
     "categoria": ACAI_E_FRUTOS, "produtor": RAIMUNDA, "unidade": LITRO,
     "preco_centavos": 2200, "estoque": 40, "destaque": False,
     "conservacao": "Geladeira, consumir em até 2 dias.",
     "descricao": "Açaí batido na hora, consistência média. Bom para tomar com farinha e peixe."},
    {"nome": "Açaí grosso", "slug": "acai-grosso", "variedade": "grosso (tipo A)",
     "categoria": ACAI_E_FRUTOS, "produtor": RAIMUNDA, "unidade": LITRO,
     "preco_centavos": 3000, "estoque": 25, "destaque": True,
     "conservacao": "Geladeira, consumir em até 2 dias.",
     "descricao": "O mais encorpado da casa: pouca água, muito fruto."},
    {"nome": "Açaí em fruto", "slug": "acai-em-fruto", "variedade": "fruto in natura",
     "categoria": ACAI_E_FRUTOS, "produtor": RAIMUNDA, "unidade": RASA,
     "preco_centavos": 12000, "estoque": 6, "destaque": False,
     "conservacao": "Bater em até 24 horas depois da colheita.",
     "descricao": "A rasa de açaí colhido de madrugada, para quem bate em casa."},
    {"nome": "Farinha d'água", "slug": "farinha-dagua", "variedade": "d'água, grossa",
     "categoria": MANDIOCA, "produtor": TONICO, "unidade": LATA,
     "preco_centavos": 15000, "estoque": 12, "destaque": True,
     "conservacao": "Local seco, em recipiente fechado.",
     "descricao": "Farinha de puba torrada no forno de lenha. Crocante, amarelinha."},
    {"nome": "Farinha seca", "slug": "farinha-seca", "variedade": "seca, fina",
     "categoria": MANDIOCA, "produtor": TONICO, "unidade": QUILO,
     "preco_centavos": 1000, "estoque": 60, "destaque": False,
     "conservacao": "Local seco, em recipiente fechado.",
     "descricao": "Farinha branca e fina, boa para farofa."},
    {"nome": "Tucupi", "slug": "tucupi", "variedade": "fervido",
     "categoria": MANDIOCA, "produtor": TONICO, "unidade": LITRO,
     "preco_centavos": 800, "estoque": 30, "destaque": False,
     "conservacao": "Geladeira, até 7 dias.",
     "descricao": "Caldo da mandioca-brava já fervido e temperado, pronto para o pato."},
    {"nome": "Goma de tapioca", "slug": "goma-de-tapioca", "variedade": "hidratada",
     "categoria": MANDIOCA, "produtor": TONICO, "unidade": QUILO,
     "preco_centavos": 1200, "estoque": 20, "destaque": False,
     "conservacao": "Geladeira, até 5 dias.",
     "descricao": "Goma fresca, é só peneirar e levar à frigideira."},
    {"nome": "Jambu", "slug": "jambu", "variedade": "folha e flor",
     "categoria": HORTALICAS, "produtor": IRMAOS_SOUSA, "unidade": MACO,
     "preco_centavos": 400, "estoque": 50, "destaque": False,
     "conservacao": "Geladeira, embrulhado em pano úmido.",
     "descricao": "O maço que faz a boca tremer. Colhido na véspera."},
    {"nome": "Cheiro-verde", "slug": "cheiro-verde", "variedade": "cebolinha e coentro",
     "categoria": HORTALICAS, "produtor": IRMAOS_SOUSA, "unidade": MACO,
     "preco_centavos": 300, "estoque": 80, "destaque": False,
     "conservacao": "Geladeira, até 5 dias.",
     "descricao": "Cebolinha e coentro no mesmo maço, do jeito da feira."},
    {"nome": "Chicória-do-pará", "slug": "chicoria-do-para", "variedade": "folha larga",
     "categoria": HORTALICAS, "produtor": IRMAOS_SOUSA, "unidade": MACO,
     "preco_centavos": 350, "estoque": 40, "destaque": False,
     "conservacao": "Geladeira, até 5 dias.",
     "descricao": "Também chamada de coentrão. Indispensável no tacacá."},
    {"nome": "Pimenta-de-cheiro", "slug": "pimenta-de-cheiro", "variedade": "amarela e vermelha",
     "categoria": HORTALICAS, "produtor": IRMAOS_SOUSA, "unidade": BANDEJA,
     "preco_centavos": 500, "estoque": 35, "destaque": False,
     "conservacao": "Geladeira, até 10 dias.",
     "descricao": "Perfume forte, ardência leve."},
    {"nome": "Mel de uruçu", "slug": "mel-de-urucu", "variedade": "abelha sem ferrão",
     "categoria": MEL, "produtor": GRACA, "unidade": POTE,
     "preco_centavos": 6000, "estoque": 15, "destaque": True,
     "conservacao": "Geladeira, depois de aberto.",
     "descricao": "Mel mais líquido e ácido que o comum. Pote de 500 g."},
    {"nome": "Mel de abelha africanizada", "slug": "mel-de-abelha-africanizada", "variedade": "florada silvestre",
     "categoria": MEL, "produtor": GRACA, "unidade": VIDRO,
     "preco_centavos": 3500, "estoque": 25, "destaque": False,
     "conservacao": "Temperatura ambiente.",
     "descricao": "Vidro de 700 g. Cristaliza no frio, e isso é sinal de mel puro."},
    {"nome": "Pólen apícola", "slug": "polen-apicola", "variedade": "desidratado",
     "categoria": MEL, "produtor": GRACA, "unidade": GRAMA,
     "preco_centavos": 30, "estoque": 2000, "destaque": False,
     "conservacao": "Geladeira, em pote fechado.",
     "descricao": "Vendido a granel, pesado na hora."},
    {"nome": "Pimenta-do-reino preta", "slug": "pimenta-do-reino-preta", "variedade": "preta, em grão",
     "categoria": ESPECIARIAS, "produtor": BENEDITO, "unidade": SACA,
     "preco_centavos": 150000, "estoque": 8, "destaque": False,
     "conservacao": "Local seco e arejado.",
     "descricao": "A saca de 60 kg, para quem revende ou tem restaurante."},
    {"nome": "Pimenta-do-reino branca", "slug": "pimenta-do-reino-branca", "variedade": "branca, em grão",
     "categoria": ESPECIARIAS, "produtor": BENEDITO, "unidade": QUILO,
     "preco_centavos": 4500, "estoque": 30, "destaque": False,
     "conservacao": "Local seco, em recipiente fechado.",
     "descricao": "Grão descascado na água, sabor mais suave que a preta."},
    {"nome": "Amêndoa de cacau", "slug": "amendoa-de-cacau", "variedade": "fermentada e seca",
     "categoria": CACAU, "produtor": SOCORRO, "unidade": QUILO,
     "preco_centavos": 5000, "estoque": 40, "destaque": False,
     "conservacao": "Local seco e arejado.",
     "descricao": "Fermentada seis dias no cocho e seca ao sol."},
    {"nome": "Chocolate 70%", "slug": "chocolate-70", "variedade": "barra de 100 g",
     "categoria": CACAU, "produtor": SOCORRO, "unidade": BARRA,
     "preco_centavos": 1800, "estoque": 45, "destaque": False,
     "conservacao": "Local fresco, longe do sol.",
     "descricao": "Feito em casa com o cacau do sítio e açúcar, nada mais."},
    {"nome": "Nibs de cacau", "slug": "nibs-de-cacau", "variedade": "torrado",
     "categoria": CACAU, "produtor": SOCORRO, "unidade": POTE,
     "preco_centavos": 2500, "estoque": 20, "destaque": False,
     "conservacao": "Local seco, em pote fechado.",
     "descricao": "Pedacinhos de amêndoa torrada. Vai bem no açaí."},
    {"nome": "Banana-prata", "slug": "banana-prata", "variedade": "prata",
     "categoria": FRUTAS, "produtor": OLIVEIRA, "unidade": CACHO,
     "preco_centavos": 2500, "estoque": 18, "destaque": False,
     "conservacao": "Temperatura ambiente.",
     "descricao": "O cacho inteiro, colhido ainda verde para amadurecer em casa."},
    {"nome": "Laranja", "slug": "laranja", "variedade": "pera",
     "categoria": FRUTAS, "produtor": OLIVEIRA, "unidade": CENTO,
     "preco_centavos": 4000, "estoque": 10, "destaque": False,
     "conservacao": "Temperatura ambiente.",
     "descricao": "O cento de laranja-pera, boa de suco."},
    {"nome": "Maracujá", "slug": "maracuja", "variedade": "azedo",
     "categoria": FRUTAS, "produtor": OLIVEIRA, "unidade": DUZIA,
     "preco_centavos": 1200, "estoque": 30, "destaque": False,
     "conservacao": "Temperatura ambiente.",
     "descricao": "A dúzia do maracujá amarelo, casca enrugada é sinal de maduro."},
    {"nome": "Polpa de cupuaçu", "slug": "polpa-de-cupuacu", "variedade": "congelada",
     "categoria": POLPAS, "produtor": FRANCISCA, "unidade": QUILO,
     "preco_centavos": 2200, "estoque": 35, "destaque": False,
     "conservacao": "Congelador, até 6 meses.",
     "descricao": "Pacotes de 1 kg, sem açúcar e sem conservante."},
    {"nome": "Polpa de bacuri", "slug": "polpa-de-bacuri", "variedade": "congelada",
     "categoria": POLPAS, "produtor": FRANCISCA, "unidade": QUILO,
     "preco_centavos": 3500, "estoque": 15, "destaque": False,
     "conservacao": "Congelador, até 6 meses.",
     "descricao": "Bacuri é fruta de safra curta; a polpa guarda o ano inteiro."},
]
