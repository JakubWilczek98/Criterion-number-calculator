import pandas as pd
import numpy as np
import mysql.connector as msql
from mysql.connector import Error

class Case_2:
    
    def __init__(self, temperatura_sciany, selected_temp, selected_material, selected_velosity, wymiar_charakterystyczny, rodzaj_oplywu, mycursor):
            #Dane wejsciowe      
            self.temperatura_sciany = temperatura_sciany #zmienna wejsciowa!
            self.selected_temp = selected_temp
            self.selected_material = selected_material #zmienna wejsciowa!
            self.selected_velosity = selected_velosity #zmienna wejsciowa!
            self.wymiar_charakterystyczny = wymiar_charakterystyczny #zmienna wejsciowa!
            self.rodzaj_oplywu = rodzaj_oplywu
            self.mycursor = mycursor

    def l_reynoldsa(self):
        self.mycursor.execute("SELECT wspl_lepkosci_dynamicznej FROM {} WHERE temperatura = {}".format(self.selected_material, self.selected_temp))
        myresult = self.mycursor.fetchall()            
        wspl_lepkosci_dynamicznej = [i[0] for i in myresult][0] *10**-6
        self.l_reynoldsa = (self.selected_velosity*self.wymiar_charakterystyczny)/wspl_lepkosci_dynamicznej  
        return round(self.l_reynoldsa,3)

    def prf_prw(self):
        if self.selected_material == "dry_air":
            self.mycursor.execute("SELECT liczba_prandtla FROM {} WHERE temperatura = {}".format(self.selected_material, self.selected_temp))
            myresult = self.mycursor.fetchall()   
            self.prf = [i[0] for i in myresult][0]
            self.eps_prf_prw = 1
        elif self.selected_material == "water":
            self.mycursor.execute("SELECT liczba_prandtla FROM {} WHERE temperatura = {}".format(self.selected_material, self.selected_temp))
            myresult = self.mycursor.fetchall()   
            prf = [i[0] for i in myresult][0]
            self.mycursor.execute("SELECT wspl_rozszerzalnosci FROM {} WHERE temperatura = {}".format(self.selected_material, self.temperatura_sciany))
            myresult = self.mycursor.fetchall()   
            self.prw = [i[0] for i in myresult][0]
            self.eps_prf_prw = prf/prw
        return self.eps_prf_prw, self.prf

    def stale(self):
        if self.rodzaj_oplywu == "plyta":
            if self.l_reynoldsa <= 10**5:
                C = 0.76 
                m = 0.50
            else:
                C = 0.037
                m = 0.80
        elif self.rodzaj_oplywu == "walec":
            if self.l_reynoldsa >= 10 and self.l_reynoldsa <= 1000:
                C = 0.59
                m = 0.47
            else:
                C = 0.21
                m = 0.62 
        self.C = C
        self.m = m
        return self.C, self.m
    
    def l_nusselta(self):
        if self.rodzaj_oplywu == "plyta":
            self.l_nusselta = self.C*(self.l_reynoldsa)**self.m*(self.prf)**0.43*(self.eps_prf_prw)**0.25

        elif self.rodzaj_oplywu == "walec":
            self.l_nusselta = self.C*(self.l_reynoldsa)**self.m*(self.prf)**0.38*(self.eps_prf_prw)**0.25

        return round(self.l_nusselta,3)

'''
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
        
            case = Case_2(temperatura_sciany, selected_temp, selected_material, selected_velosity, wymiar_charakterystyczny, rodzaj_oplywu, mycursor)
            
            l_reynoldsa = case.l_reynoldsa()
            print(l_reynoldsa)
            case.stale()
            case.prf_prw()
            l_nusselta = case.l_nusselta()
            print(l_nusselta)
           
        
    except Error as e:
        print("Connection error", e)
        
'''