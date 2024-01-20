from flask import Flask
from flask import render_template
from pathlib import Path

from . import crud
from . import utils


app = Flask(__name__)


@app.route("/config")
def index():

    # para propósito de testes:
    # se o db existir, apaga deleta.
    db_file = "db/dados.db"
    if (Path(db_file).is_file):
        Path(db_file).unlink()
    ###############

    # armazena a mensagem de retorno
    mensagem = ''


    #######################
    # CRIAÇAO DAS TABELAS #
    #######################

    # chamada das funções que criam as tabelas no db
    flag_criacao_tabelas = False
    for q in crud.criar_tabelas_query_lista:
        flag_criacao_tabelas = crud.criar_tabelas(q)

    # chamada das funções que inserem os tipos/categorias de usuários
    tipo_usuarios = [
        'paciente',
        'profissional',
        'administrador'
    ]

    flag_tipos_usuario = False
    for tipo in tipo_usuarios:
        flag_tipos_usuario = crud.inserir_tipos_de_usuarios(tipo)

    # Caso haja algum problema com a criação das tabelas
    # a mensagem não será exibida
    if (flag_criacao_tabelas):
        mensagem += '<p>Tabelas criadas com sucesso</p>'

    # Caso haja algum problema com a inserção dos tipos/categorias
    # de usuários a mensagem não será exibida
    if (flag_tipos_usuario):
        mensagem += '<p>Categorias de usuários criadas com sucesso</p>'


    ########################
    # CADASTRO DE USUÁRIOS #
    ########################

    # exemplos de usuário:
    # Esses valores serão inseridos pelo usuário no futuro.
    lista_usuarios = [
        # tipo_de_usuario, nome, email,
        [1, 'João Silva', 'joao@email.com'],
        [1, 'Maria do Socorro Alves', 'maria@email.com'],
        [1, 'Cleide Santos', 'cleide@email.com'],
        [2, 'Aparecida das Dores', 'aparecida@email.com'],
        [3, 'Pedro Souza', 'pedro@email.com']
    ]

    flag = False
    for usuario in lista_usuarios:
        flag = crud.inserir_usuarios(usuario[0], usuario[1], usuario[2])

    if (flag):
        mensagem += '<p>Usuários cadastrados com sucesso</p>'
    else:
        mensagem += '<p>Erro ao cadastrar usuários</p>'


    ######################################
    # APENAS PARA FINS DE TESTES:        #
    # INSERÇÃO DOS DADOS VITAIS DE MARIA #
    ######################################

    # exemplos de dados:
    # Esses valores serão inseridos pelo usuário no futuro.
    email_usuario = 'maria@email.com'

    dados_vitais = [
        '10x8',
        '98%',
        '50bpm',
        'ap:mv+ sem ra',
        crud.get_usuario_by_email(email_usuario)
    ]

    flag = crud.inserir_dados_vitais(dados_vitais[0], dados_vitais[1],
                                     dados_vitais[2], dados_vitais[3],
                                     dados_vitais[4])

    if (flag):
        mensagem += '<p>Dados vitais do usuário ' + email_usuario + \
            ' foram cadastrados com sucesso</p>'
    else:
        mensagem += '<p>Erro ao cadastrar os dados vitais do usuário \
            ' + email_usuario + '</p>'
    
    mensagem += '<p><a href="/lista/usuarios">Ir para lista de usuários</a></p>'

    mensagem = '<div>' + mensagem + '</div>'

    return mensagem


@app.route('/lista/usuarios')
def lista_usuarios():
    return render_template('lista_usuarios.html', lista_usuarios=crud.get_usuarios())


@app.route('/perfil-usuario/<id>')
def perfil_usuario(id):
    return render_template('perfil_usuario.html', perfil=crud.get_perfil_by_usuario_id(id))
