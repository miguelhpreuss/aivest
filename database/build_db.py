# https://dbdiagram.io/d/644171546b31947051ef68f3

import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="hp13hp13",
    database="aivest"
)

mycursor = mydb.cursor()

with open('bd.sql', 'r') as file:
    sql_script = file.read()

mycursor.execute(sql_script, multi=True)
mydb.commit()

mydb.close()
