import csv
import psycopg2
import json

with open('../config.json', 'r') as arquivo:
    config = json.load(arquivo)

if config["test"]:
    db_config = "db_test"
else:
    db_config = "db_prod"

# Conecta ao banco de dados PostgreSQL
conn = psycopg2.connect(
    host= config[db_config]["host"],
    user= config[db_config]["user"],
    password= config[db_config]["password"],
    database= config[db_config]["database"]
)


with conn.cursor() as cur:
    # Seleciona o usuário correspondente ao email informado
    sql = "select preferenceslist from preferences where preferenceid = 3"
    cur.execute(sql)
    usuario = cur.fetchone()

    print(usuario)

# Confirma as alterações no banco de dados
conn.commit()

# Fecha a conexão com o banco de dados
conn.close()
