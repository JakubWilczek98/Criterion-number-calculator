import pandas as pd
import numpy as np
import mysql.connector as msql
from mysql.connector import Error

def l_reynoldsa(selected_material,selected_temp,selected_velosity, wymiar_charakterystyczny):
    mycursor.execute("SELECT wspl_lepkosci_dynamicznej FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
    myresult = mycursor.fetchall()            
    wspl_lepkosci_dynamicznej = [i[0] for i in myresult][0] *10**-6
    return (selected_velosity*wymiar_charakterystyczny)/wspl_lepkosci_dynamicznej

def prf_prw(selected_material, selected_temp, temperatura_sciany):
    if selected_material == "dry_air":
        mycursor.execute("SELECT liczba_prandtla FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
        myresult = mycursor.fetchall()   
        prf = [i[0] for i in myresult][0]
        eps_prf_prw = 1
    elif selected_material == "water":
        mycursor.execute("SELECT liczba_prandtla FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
        myresult = mycursor.fetchall()   
        prf = [i[0] for i in myresult][0]
        mycursor.execute("SELECT wspl_rozszerzalnosci FROM {} WHERE temperatura = {}".format(selected_material, temperatura_sciany))
        myresult = mycursor.fetchall()   
        prw = [i[0] for i in myresult][0]
        eps_prf_prw = prf/prw
    return eps_prf_prw, prf

def stale(l_reynoldsa, rodzaj_oplywu):
    if rodzaj_oplywu == "plyta":
        if l_reynoldsa <= 10**5:
            C = 0.76 
            m = 0.50
        else:
            C = 0.037
            m = 0.80
    elif rodzaj_oplywu == "walec":
        if l_reynoldsa >= 10 and l_reynoldsa <= 1000:
            C = 0.59
            m = 0.47
        else:
            C = 0.21
            m = 0.62
    return C, m

if __name__ == "__main__":
    
    #Dane wejsciowe:
    selected_temp = -21
    selected_material = 'dry_air'
    selected_velosity = 22.2
    wymiar_charakterystyczny = 25 #Dlugosc w kierunku przeplywu dla plyty lub srednica walca dla walca
    rodzaj_oplywu = 'plyta' #plyta lub walec
    temperatura_sciany = 0 #zmienna wejsciowa!   
        
    try:
        mydb = msql.connect(host='localhost', 
                            user='root',
                            password = '',
                            database="materials"
                            )
        if mydb.is_connected():
            mycursor = mydb.cursor()
            print("We are connected to database")  
            
            #Liczba Reynoldsa
            l_reynoldsa = l_reynoldsa(selected_material,selected_temp,selected_velosity, wymiar_charakterystyczny)
            print("Liczba reynoldsa: ")
            print(l_reynoldsa)
            
            #Prf and Prw
            eps_prf_prw, prf = prf_prw(selected_material, selected_temp, temperatura_sciany)
            print("Prf: ")
            print(prf)
            
            #Stale
            C, m = stale(l_reynoldsa, rodzaj_oplywu)
            
            if rodzaj_oplywu == "plyta":
                l_nusselta = C * (l_reynoldsa)**m*(prf)**0.43*(eps_prf_prw)**0.25
                print('l_nusselta:')
                print(l_nusselta)
            elif rodzaj_oplywu == "walec":
                l_nusselta = C * (l_reynoldsa)**m*(prf)**0.38*(eps_prf_prw)**0.25
                print('l_nusselta:')
                print(l_nusselta)
    
    except Error as e:
        print("Connection error", e)