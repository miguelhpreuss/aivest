# https://dbdiagram.io/d/644171546b31947051ef68f3

import mysql.connector
import json

with open('config.json', 'r') as arquivo:
    config = json.load(arquivo)

if config["test"]:
    db_config = "db_test"
else:
    db_config = "db_prod"


mydb = mysql.connector.connect(
    host= config[db_config]["host"],
    user= config[db_config]["user"],
    password= config[db_config]["password"],
    database= config[db_config]["database"]
)

mycursor = mydb.cursor()

with open('bd.sql', 'r') as file:
    sql_script = file.read()

mycursor.execute(sql_script, multi=True)
mydb.commit()

mydb.close()
