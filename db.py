import psycopg2
import bcrypt
import json


def connect():
    try:
        with open('config.json', 'r') as arquivo:
            config = json.load(arquivo)

        if config["test"]:
            db_config = "db_test"
        else:
            db_config = "db_prod"

        conn = psycopg2.connect(
            host=config[db_config]["host"],
            user=config[db_config]["user"],
            password=config[db_config]["password"],
            database=config[db_config]["database"]
        )

        print(
            f"\033[32mINFO\033[37m:     Conexão bem sucedida com o Banco de Dados: {conn.get_dsn_parameters()['host']}")
        return conn

    except psycopg2.Error as error:
        print(f"\033[31mERRO\033[37m:     Ao conectar ao banco de dados:", error)
        return {"msg": "Ao Conectar ao banco de dados", "erro": error}
    
def user(conn, id):
    try:
        # Cria um cursor
        with conn.cursor() as cur:

            # Seleciona o usuário correspondente ao email informado
            sql = "SELECT * FROM users WHERE userid = %s"
            val = (id,)
            cur.execute(sql, val)
            usuario = cur.fetchone()
            return {"id": usuario[0], "name": usuario[1], "email": usuario[2], "token": "True"}

    except Exception as e:
        print("\033[31mERRO\033[37m:     Erro interno:", e)
        return {"erro": "Erro interno", "erro": str(e)}


def signup(conn, nome, email, senha):
    try:
        # Cria um cursor
        cur = conn.cursor()

        sql = "SELECT * FROM users WHERE email = %s"
        val = (email,)
        cur.execute(sql, val)
        usuario = cur.fetchone()
        if usuario:
            return {"erro": "Email já cadastrado"}

        # Gera o hash da senha
        hashed_senha = bcrypt.hashpw(senha.encode(
            'utf-8'), bcrypt.gensalt()).decode("utf-8")

        # Insere o novo usuário na tabela "usuarios"
        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING userid"
        val = (nome, email, hashed_senha)
        cur.execute(sql, val)
        usuario_id = cur.fetchone()[0]
        print(
            "\033[32mINFO\033[37m:     Novo usuário cadastrado com sucesso. ID:", usuario_id)

        # Confirma a transação
        conn.commit()

        return {"id": usuario_id, "nome": nome, "email": email, "token": "True"}

    except psycopg2.Error as error:
        print("\033[31mERRO\033[37m:     Ao cadastrar novo usuário:", error)
        return False


# Função para logar um usuário existente


def login(conn, email, senha):
    try:
        # Cria um cursor
        with conn.cursor() as cur:

            # Seleciona o usuário correspondente ao email informado
            sql = "SELECT * FROM users WHERE email = %s"
            val = (email,)
            cur.execute(sql, val)
            usuario = cur.fetchone()

            if usuario:
                # Verifica se a senha informada é igual à senha armazenada no banco de dados
                if bcrypt.checkpw(senha.encode('utf-8'), usuario[3].encode('utf-8')):
                    # "preferencias": preferencias[2]
                    return {"id": usuario[0], "name": usuario[1], "email": usuario[2], "token": "True"}
                else:
                    print("\033[31mERRO\033[37m:     Senha incorreta.")
                    return {"erro": "Senha incorreta"}  # , "erro": error}
            else:
                print("\033[31mERRO\033[37m:     Email incorreto.")
                return {"erro": "Email incorreto"}  # , "erro": error}

        conn.commit()
    except Exception as e:
        print("\033[31mERRO\033[37m:     Erro interno:", e)
        return {"erro": "Erro interno", "erro": str(e)}


def savepref(conn, stock, userid, data):
    try:
        # Cria um cursor
        cur = conn.cursor()

        # Buscar id da ação
        sql = "SELECT stockid FROM stocks WHERE symbol = %s"
        val = (stock,)
        cur.execute(sql, val)
        stockid = cur.fetchone()

        if stockid:  # Se encontrar o stockid
            stockid = stockid[0]
            sql = "SELECT preferenceslist FROM preferences WHERE stockid = %s AND userid = %s"
            val = (stockid, userid,)
            cur.execute(sql, val)
            preference = cur.fetchone()

            if preference:  # se encontrar as preferencias
                sql = "UPDATE preferences SET preferenceslist = %s WHERE userid = %s AND stockid = %s RETURNING preferenceid"
                val = (data, userid, stockid)
                cur.execute(sql, val)
                preferenceid = cur.fetchone()[0]
                conn.commit()
                print(
                    "\033[32mINFO\033[37m:     Preferência atualizada com sucesso. ID:", preferenceid)
                return {"info": "Preferência atualizada com sucesso"}

            else:  # se não encontrar as preferencias
                sql = "INSERT INTO preferences (userid, stockid, preferenceslist) VALUES (%s, %s, %s) RETURNING preferenceid"
                val = (userid, stockid, data)
                cur.execute(sql, val)
                preferenceid = cur.fetchone()[0]
                conn.commit()
                print(
                    "\033[32mINFO\033[37m:     Nova preferência cadastrada com sucesso. ID:", preferenceid)
                return {"info": "Nova preferência cadastrada com sucesso"}

        else:  # se não encontrar a ação
            print("\033[32mERRO\033[37m:     Dados da ação não encontrada")
            return {"erro": "Dados da ação não encontrada"}
    except psycopg2.Error as error:
        print("\033[31mERRO\033[37m:     Ao cadastrar preferências:", error)
        return False


def getpref(conn, stock, userid):
    try:
        # Cria um cursor
        cur = conn.cursor()

        # Buscar id da ação
        sql = "SELECT stockid FROM stocks WHERE symbol = %s"
        val = (stock,)
        cur.execute(sql, val)
        stockid = cur.fetchone()

        if stockid:  # Se encontrar o stockid
            stockid = stockid[0]
            sql = "SELECT preferenceslist FROM preferences WHERE stockid = %s AND userid = %s"
            val = (stockid, userid,)
            print(val)
            cur.execute(sql, val)
            preference = cur.fetchone()

            if preference:  # se encontrar as preferencias
                return {"pref": preference[0]}

            else:  # se não encontrar as preferencias
                return {"erro": "Não encontrado a preferencia para essa ação"}

        else:  # se não encontrar a ação
            print("\033[32mERRO\033[37m:     Dados da ação não encontrada")
            return {"erro": "Dados da ação não encontrada"}
    except psycopg2.Error as error:
        print("\033[31mERRO\033[37m:     Ao buscar preferências:", error)
        return False
