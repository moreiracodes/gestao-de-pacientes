'''
    crud.py: Este módulo contém funções que precisam interagir
    com o banco de dados.
    
    C reate
    R ead
    U pdate
    D elete

'''

# Criar db e Conectar db

import sqlite3

# Se as tabelas não existirem crie-as.
criar_tabelas_query_lista = [
    """
        CREATE TABLE IF NOT EXISTS usuarios (
        id          integer         primary key autoincrement,
        nome        varchar(50)     not null,
        tipo_id     integer         not null,
        email       varchar(50)     not null
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS usuarios_tipos (
        id          integer         primary key autoincrement,
        tipo        varchar(50)     not null
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS dados_vitais (
        id                      integer         primary key autoincrement,
        pressao_arterial        varchar(10)     not null,
        saturacao_O2            integer         not null,
        frequencia_cardiaca     integer         not null,
        ausculta_pulmonar       varchar(50)     not null,
        usuario_id              integer         not null
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS ventilacao_mecanica_invasiva (
        id                          integer         primary key autoincrement,
        modo_respiratorio           varchar(20)     not null,
        fiO2                        float           not null,
        peep                        float           not null,
        pressao_pico_inspiratoria   float           null,
        pressao_inspiratoria        float           null,
        volume_corrente             float           not null,
        tempo_inspiratorio          float           null,
        tempo_expiratorio           float           null,
        relacao_ie                  float           null,
        usuario_id                  integer         not null
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS ventilacao_nao_invasiva (
        id                  integer          primary key    autoincrement,
        bipap               varchar(3)       null,
        cpap                varchar(3)       null,
        ipap                float            null,
        epap                float            null,
        presao_suporte      float            null,
        usuario_id          integer         not null
        )
        """,
]

# bipap e cpap está como varchar, porque o usuario vai indicar
# qual deles o paciente faz uso
# responde com sim ou não.


def conectar_banco_de_dados():
    '''
        Cria a conexão e o cursor do banco de dados

        retorna uma tupla (conexao, cursor)
    '''
    db_file = "db/dados.db"

    conexao = sqlite3.connect(db_file)
    cursor = conexao.cursor()

    return (conexao, cursor)


def escrever_banco_de_dados(query, parametros=None,
                            banco=conectar_banco_de_dados):
    try:
        conexao, cursor = banco()
        if (parametros):

            cursor.execute(query, (parametros))

        else:
            cursor.execute(query)

        conexao.commit()
        cursor.close()
        conexao.close()

        return True

    except Exception as e:
        print()
        print(f'Erro ao processar query: \n {query}\n \
              com os parametros \n {parametros}: {e}')
        print()
        return False


def ler_banco_de_dados(query,
                       banco=conectar_banco_de_dados):
    try:
        conexao, cursor = banco()

        # resultado vai armazenar uma lista com as linhas do resultado
        # do select na tabela
        # exemplo:
        # resultado de 'select * from usuarios where id=1':
        # a tabela usuario tem os campos [id, nome, tipo_id, email], entao
        # resultado = [1, 'João Silva', 'joao@email.com']

        resultado_objeto = cursor.execute(query)
        resultado_lista = []
        for row in resultado_objeto:
            resultado_lista.append(row)
        cursor.close()
        conexao.close()

        return resultado_lista

    except Exception as e:
        print()
        print(f'Erro ao processar query: \n {query}\n{e}')
        print()
        return False


def criar_tabelas(query):
    '''
        Por limitação do sqlite que não cria as todas em uma só query,
        foi necessária a definicão dessa função que recebe
        conectar [function]: função que retorna (conexão, cursor)
        query [string]: a query de definição da tabela

        return [bool]
    '''
    try:
        return escrever_banco_de_dados(query)

    except Exception as e:
        print()
        print(f'Erro ao criar tabelas: \n {query}\n{e}')
        print()
        return False


def inserir_tipos_de_usuarios(tipo_usuario):

    query = """
                INSERT INTO usuarios_tipos (tipo)
                VALUES
                (?);
            """

    try:
        return escrever_banco_de_dados(query, (tipo_usuario,))

    except Exception as err:
        print()
        print(f'Erro ao inserir tipo de usuário: {err}')
        print()
        return False


def inserir_usuarios(tipo_usuarios_id, nome, email):

    # Aqui seria o lugar ideal para validar
    # se os campos nome e email

    query = """
                INSERT INTO usuarios (nome, tipo_id, email)
                VALUES
                (?, ?, ?);
            """
    try:
        return escrever_banco_de_dados(query, (nome, tipo_usuarios_id, email))

    except Exception as err:
        print()
        print(f'Erro ao inserir usuário: {err}')
        print()


def get_usuarios():
    query = "select * from usuarios"
    linha_tabela = ler_banco_de_dados(query)
    # print(linha_tabela)
    return linha_tabela


def get_usuario_by_email(email):
    query = "select * from usuarios where email='" + email + "'"
    linha_tabela = ler_banco_de_dados(query)
    id = linha_tabela[0][0]
    return id


def get_perfil_by_usuario_id(usuario_id):
    query = '''
                SELECT u.nome, u.email,
                    ut.tipo,
                    dv.pressao_arterial,
                    dv.saturacao_O2,
                    dv.frequencia_cardiaca,
                    dv.ausculta_pulmonar
                FROM usuarios AS u
                
                LEFT JOIN usuarios_tipos AS ut
                ON u.tipo_id=ut.id

                LEFT JOIN dados_vitais AS dv
                ON u.id=dv.usuario_id

                WHERE u.id={0}

            '''.format(usuario_id)
    linha_tabela = ler_banco_de_dados(query)
    print(linha_tabela)
    return linha_tabela


def inserir_dados_vitais(pressao_arterial, saturacao_O2, frequencia_cardiaca,
                         ausculta_pulmonar, usuario_id):

    # Aqui seria o lugar ideal para validar
    # se os dados recebidos

    query = """
            INSERT INTO dados_vitais (pressao_arterial, saturacao_O2,
            frequencia_cardiaca, ausculta_pulmonar, usuario_id)
            VALUES
            (?, ?, ?, ?, ?);
        """

    try:
        return escrever_banco_de_dados(query,
                                       (pressao_arterial, saturacao_O2,
                                        frequencia_cardiaca, ausculta_pulmonar,
                                        usuario_id))

    except Exception as err:
        print()
        print(f'Erro ao inserir dados vitais: {err}')
        print()
