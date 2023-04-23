import csv
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

# Prepara o cursor para executar os comandos SQL
cursor = mydb.cursor()

# Abre o arquivo CSV
with open("acoes.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # Itera pelas linhas do arquivo CSV e insere os dados na tabela "stocks"
    for row in reader:
        stock = row["stock"]
        shortname = row["shortname"]
        longname = row["longname"]
        sector = row["sector"]
        industry = row["industry"]
        
        # Insere os dados na tabela "stocks"
        sql = "INSERT INTO Stocks (Symbol, ShortName, LongName, Sector, Industry) VALUES (%s, %s, %s, %s, %s)"
        val = (stock, shortname, longname, sector, industry)
        cursor.execute(sql, val)

# Confirma as alterações no banco de dados
mydb.commit()

# Fecha a conexão com o banco de dados
mydb.close()
