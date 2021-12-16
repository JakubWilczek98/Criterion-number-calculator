import pandas as pd
import numpy as np
import mysql.connector as msql
from mysql.connector import Error
  
    
def l_nusselta(selected_material, selected_temp, selected_length):
    
    return (wspl_dyf_cieplnej*wymiar_charakterystyczny)/wspl_przew_ciepla

def l_reynoldsa(selected_material,selected_temp,selected_velosity, wymiar_charakterystyczny):
    mycursor.execute("SELECT wspl_lepkosci_dynamicznej FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
    myresult = mycursor.fetchall()            
    wspl_lepkosci_dynamicznej = [i[0] for i in myresult][0] *10e-6
    return (selected_velosity*wymiar_charakterystyczny)/wspl_lepkosci_dynamicznej

def l_prandtla(selected_material, selected_temp):  
    mycursor.execute("SELECT wspl_lepkosci_kinematycznej, wspl_dyf_cieplnej FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
    myresult = mycursor.fetchall()            
    wspl_lepkosci_kinematycznej = [i[0] for i in myresult][0]*10e-6
    wspl_dyf_cieplnej = [i[1] for i in myresult][0]*10e-6
    return wspl_lepkosci_kinematycznej/wspl_dyf_cieplnej

def l_prandtla_cp(selected_material, selected_temp):
    mycursor.execute("SELECT wspl_lepkosci_dynamicznej, cieplo_wlasciwe, wspl_przew_ciepla FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
    myresult = mycursor.fetchall()            
    wspl_lepkosci_dynamicznej = [i[0] for i in myresult][0]*10e-6
    cieplo_wlasciwe = [i[1] for i in myresult][0]*10e2
    wspl_przew_ciepla = [i[2] for i in myresult][0]*10e-2
    return (cieplo_wlasciwe*wspl_lepkosci_dynamicznej)/(wspl_przew_ciepla)
    


if __name__ == "__main__":
    
    #Dane wejsciowe
    selected_temp = 1000
    selected_material = 'dry_air'
    wymiar_charakterystyczny = 60e-3
    selected_velosity = 5
    
    try:
        mydb = msql.connect(host='localhost', 
                            user='root',
                            password = '',
                            database="materials"
                            )
        if mydb.is_connected():
            mycursor = mydb.cursor()
            print("We are connected to database")  
            print(l_reynoldsa(selected_material, selected_temp, selected_velosity, wymiar_charakterystyczny))
            print(l_prandtla(selected_material, selected_temp))
            print(l_prandtla_cp(selected_material, selected_temp))
            
                  
            
            
            
        
    except Error as e:
        print("Connection error", e)
    
    
    
    