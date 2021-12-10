import math
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

mydb = mysql.connector.connect(
    host='mysql.agh.edu.pl',
    user='awilcze',
    password='***** ***',
    database='awilcze'
)

mycursor = mydb.cursor()

#mycursor.execute('SHOW TABLES')
mycursor.execute('SELECT PLACA_POD FROM PRACOWNICY WHERE PLACA_POD = 2666')

myresult = mycursor.fetchall()

oczekiwana = [i[0] for i in myresult][0]
print(oczekiwana)

print(myresult)

#for x in myresult:
 #   print(x)