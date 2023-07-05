import mysql.connector
from getpass import getpass

mydb = mysql.connector.connect(
    host='localhost',
    user='stt_user',
    password=getpass(),
    port='3306',
    database='stt_db',
)

mycursor = mydb.cursor()
print(mycursor)