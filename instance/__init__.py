import mysql.connector
from getpass import getpass

pass_verify = False

if pass_verify:
    password = getpass("Database password:")
else:
    password = "password"
mydb = mysql.connector.connect(
    host='localhost',
    user='stt_user',
    password=password,
    port='3306',
    database='stt_db',
)

mycursor = mydb.cursor()
print(mycursor)