import math
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

# konwekcja swobodna w przestrzeni nieograniczonej

mydb = mysql.connector.connect(
    host='mysql.agh.edu.pl',
    user='awilcze1',
    password='***',
    database='awilcze1'
)

mycursor = mydb.cursor()

#mycursor.execute('SHOW TABLES')
def rounded(selected_material, selected_temp):
    if selected_material == 'dry_air' and selected_temp in range(-50, 1200):
        return round(selected_temp/10)*10
    elif selected_material == 'water' and selected_temp in range(0, 370):
        return round(selected_temp/10)*10

selected_material = 'water'
selected_temp = 14

selection = 'SELECT * FROM {} WHERE TEMPERATURA = {}'.format(selected_material, rounded(selected_material, selected_temp))
print(selection)
mycursor.execute(selection)

myresult = mycursor.fetchall()

oczekiwana = [i[0] for i in myresult][0]
print(oczekiwana)

print(myresult)
