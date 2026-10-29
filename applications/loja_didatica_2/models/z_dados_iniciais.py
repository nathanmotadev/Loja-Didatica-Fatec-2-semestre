# -*- coding: utf-8 -*-
# =============================================================================
#  MODEL — carga inicial (executa uma única vez, quando não há grupos no banco)
#  O prefixo "z_" garante que este arquivo rode depois de db.py e regras.py.
# =============================================================================

USUARIOS_DEMO = [
    # (papel,          nome,           e-mail,                senha)
    ('administrador', 'Administrador', 'admin@loja.com',     'admin123'),
    ('operador',      'Olívia',        'operador@loja.com',  'operador123'),
    ('vendedor',      'Vicente',       'vendedor@loja.com',  'vendedor123'),
    ('cliente',       'Clara',         'cliente@loja.com',   'cliente123'),
]

# (código, nome, categoria, preço, estoque inicial, prazo em dias úteis, descrição)
PRODUTOS_DEMO = [
    ('SHP-10001', 'Shape Maple 8.0"', 'Shapes', 249.90, 18, 5,
     'Shape de 7 camadas de maple canadense, concave médio, para street e transição.'),
    ('SHP-10002', 'Shape Maple 8.25"', 'Shapes', 259.90, 14, 5,
     'Shape de 7 camadas de maple, um pouco mais largo, com mais estabilidade nas manobras.'),
    ('RDA-10001', 'Rodas 52 mm 99A (jogo com 4)', 'Rodas', 149.90, 30, 5,
     'Rodas de poliuretano duras, ideais para street e skatepark.'),
    ('RDA-10002', 'Rodas 56 mm 95A (jogo com 4)', 'Rodas', 159.90, 20, 5,
     'Rodas mais macias, ótimas para pisos irregulares e para cruzar a cidade.'),
    ('TRK-10001', 'Trucks de Alumínio 139 mm (par)', 'Trucks', 289.90, 10, 7,
     'Par de trucks com pivô reforçado e bushings 90A.'),
    ('TRK-10002', 'Trucks de Alumínio 149 mm (par)', 'Trucks', 319.90, 8, 7,
     'Par de trucks para shapes de 8.25" a 8.5", com eixo de aço.'),
    ('CAL-10001', 'Tênis Skate Canvas', 'Calçados', 299.90, 16, 7,
     'Tênis de lona com sola vulcanizada e reforço na biqueira.'),
    ('CAL-10002', 'Tênis Skate Camurça', 'Calçados', 399.90, 0, 7,
     'Tênis de camurça com palmilha acolchoada e costura reforçada.'),
    ('PRD-10001', 'Camiseta Skateroom', 'Vestuário', 79.90, 40, 5,
     'Algodão penteado com a estampa do emblema Skateroom Fatec.'),
    ('PRD-10002', 'Moletom com Capuz', 'Vestuário', 189.90, 15, 7,
     'Moletom flanelado com capuz e bolso canguru. Tamanhos P ao GG.'),
    ('PRD-10003', 'Boné Skateroom', 'Vestuário', 59.90, 25, 5,
     'Aba curva, ajuste traseiro e bordado do emblema.'),
    ('PRD-10006', 'Mochila Skate', 'Acessórios', 199.90, 12, 10,
     'Impermeável, com compartimento acolchoado para notebook.'),
]


def carga_inicial():
    grupos = {}
    for papel in PAPEIS:
        grupos[papel] = auth.add_group(papel, PAPEL_DESCRICAO[papel])

    usuarios = {}
    for papel, nome, email, senha in USUARIOS_DEMO:
        uid = db.auth_user.insert(first_name=nome, last_name='Demo', email=email,
                                  password=db.auth_user.password.validate(senha)[0],
                                  telefone='(11) 99999-0000')
        auth.add_membership(grupos[papel], uid)
        usuarios[papel] = uid
    # o administrador também pode operar e vender
    auth.add_membership(grupos['operador'], usuarios['administrador'])
    auth.add_membership(grupos['vendedor'], usuarios['administrador'])

    categorias = {}
    for nome, desc in [('Shapes', 'Shapes de maple para street e transição'),
                       ('Rodas', 'Rodas de poliuretano em várias durezas'),
                       ('Trucks', 'Trucks de alumínio e acessórios'),
                       ('Calçados', 'Tênis para skate'),
                       ('Vestuário', 'Camisetas, moletons e bonés'),
                       ('Acessórios', 'Mochilas e itens para o dia a dia')]:
        categorias[nome] = db.categoria.insert(nome=nome, descricao=desc)

    for codigo, nome, cat, preco, estoque, prazo, desc in PRODUTOS_DEMO:
        imagem = codigo + '.jpg'
        if not os.path.exists(caminho_imagem(imagem)):
            imagem = ''
        pid = db.produto.insert(codigo=codigo, nome=nome, descricao=desc,
                                categoria=categorias[cat], preco=preco, estoque=0,
                                prazo_dias=prazo, imagem=imagem, ativo=True,
                                vendedor=usuarios['vendedor'])
        if estoque:
            registrar_movimento(pid, 'entrada', estoque, motivo='Estoque inicial')
    db.commit()


if db(db.auth_group).isempty():
    carga_inicial()
