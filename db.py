import mysql.connector
import bcrypt

def connect():
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="hp13hp13",
            database="aivest"
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

        sql = "SELECT * FROM users WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        usuario = mycursor.fetchone()
        if usuario:
            return {"erro": "Email já cadastrado"}

        # Gera o hash da senha
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        # Insere o novo usuário na tabela "usuarios"
        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        val = (nome, email, hashed_senha)
        mycursor.execute(sql, val)
        usuario_id = mycursor.lastrowid
        print(
            "\033[32mINFO\033[37m:     Novo usuário cadastrado com sucesso. ID:", usuario_id)

        # Confirma a transação
        mydb.commit()

        return {"id": usuario_id, "nome": nome, "email": email, "token": "True"} #"preferencias": preferencias[2]


    except mysql.connector.Error as error:
        print("\033[31mERRO\033[37m:     Ao cadastrar novo usuário:", error)
        return False

# Função para logar um usuário existente


def login(mydb, email, senha):
    try:
        # Cria um cursor
        mycursor = mydb.cursor(buffered=True)

        # Seleciona o usuário correspondente ao email informado
        sql = "SELECT * FROM users WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        usuario = mycursor.fetchone()
        if usuario:
            # Verifica se a senha informada é igual à senha armazenada no banco de dados
            if bcrypt.checkpw(senha.encode('utf-8'), usuario[3].encode('utf-8')):
                # Seleciona as preferências do usuário na tabela "preferencias"
                print(usuario)
                sql = "SELECT * FROM preferences WHERE userid = %s"
                val = (usuario[0],)
                mycursor.execute(sql, val)
                preferencias = mycursor.fetchone()
                print(preferencias)
                # descarta os resultados da consulta anterior
                mycursor.fetchall()

                return {"id": usuario[0], "name": usuario[1], "email": usuario[2], "token": "True"} #"preferencias": preferencias[2]
            else:
                print("\033[31mERRO\033[37m:     Senha incorreta.")
                return {"erro": "Senha incorreta"}#, "erro": error}
        else:
            print("\033[31mERRO\033[37m:     Email incorreto.")
            return {"erro": "Email incorreto"}#, "erro": error}

    except mysql.connector.Error as error:
        print("\033[31mERRO\033[37m:     Erro interno:", error)
        return {"erro": "Erro interno", "erro": error}


def preferences():
        # Cria um registro de preferências padrão para o novo usuário na tabela "preferencias"
    sql = "INSERT INTO preferences (usuario_id, preferencia_1, lista_preferencias) VALUES (%s, %s, %s)"
    val = (usuario_id, "Preferência 1",
            "Preferência 1, Preferência 2, Preferência 3")
    mycursor.execute(sql, val)
    preferencias_id = mycursor.lastrowid
    print(
        "\033[32mINFO\033[37m:     Novas preferências cadastradas com sucesso. ID:", preferencias_id)
