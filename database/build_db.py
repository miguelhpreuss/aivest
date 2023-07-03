import psycopg2
import json

with open('../config.json', 'r') as arquivo:
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

cur = conn.cursor()

with open('bd_structure.sql', 'r') as file:
    sql_script = file.read()

cur.execute(sql_script)
conn.commit()

conn.close()