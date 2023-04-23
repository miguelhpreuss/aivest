import csv
import mysql.connector

# Faz a conexão com o banco de dados
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="hp13hp13",
    database="aivest"
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
