import mysql.connector

mydb = mysql.connector.connect(
    host="sql9.freemysqlhosting.net",
    user="sql9610501",
    password="wfzWNvg9yw",
    database="sql9610501"
)

mycursor = mydb.cursor()

with open('bd.sql', 'r') as file:
    sql_script = file.read()

mycursor.execute(sql_script, multi=True)
mydb.commit()

mydb.close()
