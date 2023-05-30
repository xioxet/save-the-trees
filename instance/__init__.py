import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='stt_user',
    password='MySql123!',
    port='3306',
    database='stt_db',
)

mycursor = mydb.cursor()