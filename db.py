# https://www.freemysqlhosting.net/

import mysql.connector
import bcrypt


def connect():
    try:
        mydb = mysql.connector.connect(
            host="sql9.freemysqlhosting.net",
            user="sql9610501",
            password="wfzWNvg9yw",
            database="sql9610501"
        )
        print(
            f"\033[32mINFO\033[37m:     Conexão bem sucedida com o Banco de Dados: {mydb._host}")
        return mydb
    except mysql.connector.Error as error:
        print(f"\033[31mERRO\033[37m:     Ao conectar ao banco de dados:", error)
        return {"msg": "Ao Conectar ao banco de dados", "erro": error}


# Função para cadastrar um novo usuário
def signup(mydb, nome, email, senha):
    try:
        # Cria um cursor
        mycursor = mydb.cursor()

        # Gera o hash da senha
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        # Insere o novo usuário na tabela "usuarios"
        sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        val = (nome, email, hashed_senha)
        mycursor.execute(sql, val)
        usuario_id = mycursor.lastrowid
        print(
            "\033[32mINFO\033[37m:     Novo usuário cadastrado com sucesso. ID:", usuario_id)

        # Cria um registro de preferências padrão para o novo usuário na tabela "preferencias"
        sql = "INSERT INTO preferencias (usuario_id, preferencia_1, lista_preferencias) VALUES (%s, %s, %s)"
        val = (usuario_id, "Preferência 1",
               "Preferência 1, Preferência 2, Preferência 3")
        mycursor.execute(sql, val)
        preferencias_id = mycursor.lastrowid
        print(
            "\033[32mINFO\033[37m:     Novas preferências cadastradas com sucesso. ID:", preferencias_id)

        # Confirma a transação
        mydb.commit()

        return {"msg": "Sucesso ao cadastrar"}

    except mysql.connector.Error as error:
        print("\033[31mERRO\033[37m:     Ao cadastrar novo usuário:", error)
        return False

# Função para logar um usuário existente


def login(mydb, email, senha):
    try:
        # Cria um cursor
        mycursor = mydb.cursor()

        # Seleciona o usuário correspondente ao email informado
        sql = "SELECT * FROM usuarios WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        usuario = mycursor.fetchone()

        if usuario:
            # Verifica se a senha informada é igual à senha armazenada no banco de dados
            if bcrypt.checkpw(senha.encode('utf-8'), usuario[3].encode('utf-8')):
                # Seleciona as preferências do usuário na tabela "preferencias"
                sql = "SELECT * FROM preferencias WHERE usuario_id = %s"
                val = (usuario[0],)
                mycursor.execute(sql, val)
                preferencias = mycursor.fetchone()

                return {"id": usuario[0], "nome": usuario[1], "email": usuario[2], "preferencias": preferencias[2]}
            else:
                print("\033[31mERRO\033[37m:     Senha incorreta.")
                return {"msg": "Senha incorreta", "erro": error}
        else:
            print("\033[31mERRO\033[37m:     Email incorreto.")
            return {"msg": "Email incorreto", "erro": error}

    except mysql.connector.Error as error:
        print("\033[31mERRO\033[37m:     Erro ao buscar usuário:", error)
        return {"msg": "Erro ao buscar usuário", "erro": error}
