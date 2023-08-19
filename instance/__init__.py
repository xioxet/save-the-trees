import mysql.connector
from getpass import getpass

pass_verify = False

if pass_verify:
    password = getpass("Database password:")
else:
    password = "MySql123!"
while True:
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password,
            port='3306',
            database='stt_db',
        )
    except mysql.connector.errors.ProgrammingError as err:
        print("Wrong password")
        if not pass_verify:
            raise err
        else:
            password = getpass("Database password:")
    else:
        mycursor = mydb.cursor()
        break
print(mycursor)