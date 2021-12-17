import pandas as pd
import numpy as np
import mysql.connector as msql
from mysql.connector import Error
  
    
def l_reynoldsa(selected_material,selected_temp,selected_velosity, wymiar_charakterystyczny):
    mycursor.execute("SELECT wspl_lepkosci_dynamicznej FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
    myresult = mycursor.fetchall()            
    wspl_lepkosci_dynamicznej = [i[0] for i in myresult][0] *10**-6
    return (selected_velosity*wymiar_charakterystyczny)/wspl_lepkosci_dynamicznej

def l_prandtla(selected_material, selected_temp):  
    mycursor.execute("SELECT wspl_lepkosci_kinematycznej, wspl_dyf_cieplnej FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
    myresult = mycursor.fetchall()            
    wspl_lepkosci_kinematycznej = [i[0] for i in myresult][0]*10**-6
    wspl_dyf_cieplnej = [i[1] for i in myresult][0]*10**-6
    return wspl_lepkosci_kinematycznej/wspl_dyf_cieplnej

def l_prandtla_cp(selected_material, selected_temp):
    mycursor.execute("SELECT wspl_lepkosci_dynamicznej, cieplo_wlasciwe, wspl_przew_ciepla FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
    myresult = mycursor.fetchall()            
    wspl_lepkosci_dynamicznej = [i[0] for i in myresult][0]*10**-6
    cieplo_wlasciwe = [i[1] for i in myresult][0]*10**3
    wspl_przew_ciepla = [i[2] for i in myresult][0]*10**-2
    return (cieplo_wlasciwe*wspl_lepkosci_dynamicznej)/(wspl_przew_ciepla)
    
def l_grashofa(selected_material, selected_temp, temperatura_wlot, temperatura_sciany):
    g = 9.81
    if selected_material == "dry_air":
        beta = 1/373
    elif selected_material == "water":
        mycursor.execute("SELECT wspl_rozszerzalnosci FROM {} WHERE temperatura = {}".format(selected_material, abs(temperatura_wlot-temperatura_sciany)))
        myresult = mycursor.fetchall()
        beta = [i[0] for i in myresult][0]*10**-4
    mycursor.execute("SELECT wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}".format(selected_material, selected_temp))
    myresult = mycursor.fetchall()   
    wspl_lepkosci_kinematycznej = [i[0] for i in myresult][0]*10**-6
    return (g*wymiar_charakterystyczny**3*beta*abs(temperatura_wlot-temperatura_sciany)/wspl_lepkosci_kinematycznej**2)


def rozbieg_hydrauliczny(l_reynoldsa, wymiar_charakterystyczny, dlugosc):
    L_do_w_charakterystyczny = round(dlugosc/wymiar_charakterystyczny)
    if l_reynoldsa <=2300:   
        if L_do_w_charakterystyczny <=1:
            eps_L = 1.9
        elif (L_do_w_charakterystyczny > 1 and L_do_w_charakterystyczny <=5):
            eps_L = 1.44
        elif (L_do_w_charakterystyczny > 5 and L_do_w_charakterystyczny <=10):
            eps_L = 1.28
        elif L_do_w_charakterystyczny > 10 and L_do_w_charakterystyczny <=20:
            eps_L = 1.19
        elif L_do_w_charakterystyczny > 20 and L_do_w_charakterystyczny <=30:
            eps_L = 1.05
        elif L_do_w_charakterystyczny > 30 and L_do_w_charakterystyczny <=40:
            eps_L = 1.02
        elif L_do_w_charakterystyczny > 40:
            eps_L = 1
    else:
        if L_do_w_charakterystyczny <=1:
            eps_L = 1.65
        elif (L_do_w_charakterystyczny > 1 and L_do_w_charakterystyczny <=5):
            eps_L = 1.34
        elif (L_do_w_charakterystyczny > 5 and L_do_w_charakterystyczny <=10):
            eps_L = 1.23
        elif L_do_w_charakterystyczny > 10 and L_do_w_charakterystyczny <=20:
            eps_L = 1.13
        elif L_do_w_charakterystyczny > 20 and L_do_w_charakterystyczny <=30:
            eps_L = 1.07
        elif L_do_w_charakterystyczny > 30 and L_do_w_charakterystyczny <=40:
            eps_L = 1.03
        elif L_do_w_charakterystyczny > 40:
            eps_L = 1
    return eps_L
    
    
def prf_prw(selected_material, temperatura_wlot, temperatura_sciany):
    if selected_material == "dry_air":
        mycursor.execute("SELECT liczba_prandtla FROM {} WHERE temperatura = {}".format(selected_material, temperatura_wlot))
        myresult = mycursor.fetchall()   
        prf = [i[0] for i in myresult][0]
        eps_prf_prw = 1
    elif selected_material == "water":
        mycursor.execute("SELECT liczba_prandtla FROM {} WHERE temperatura = {}".format(selected_material, temperatura_wlot))
        myresult = mycursor.fetchall()   
        prf = [i[0] for i in myresult][0]
        mycursor.execute("SELECT wspl_rozszerzalnosci FROM {} WHERE temperatura = {}".format(selected_material, temperatura_sciany))
        myresult = mycursor.fetchall()   
        prw = [i[0] for i in myresult][0]
        eps_prf_prw = prf/prw
    return eps_prf_prw, prf


def nif_niw(selected_material, temperatura_wlot, temperatura_sciany):
    mycursor.execute("SELECT gestosc, wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}".format(selected_material, temperatura_wlot))
    myresult = mycursor.fetchall()   
    gestosc_f = [i[0] for i in myresult][0]
    wspl_lepkosci_kinematycznej_f = [i[1] for i in myresult][0]
    
    mycursor.execute("SELECT gestosc, wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}".format(selected_material, temperatura_sciany))
    myresult = mycursor.fetchall()   
    gestosc_w = [i[0] for i in myresult][0]
    wspl_lepkosci_kinematycznej_w = [i[1] for i in myresult][0]
    
    nif = gestosc_f * wspl_lepkosci_kinematycznej_f
    niw = gestosc_w * wspl_lepkosci_kinematycznej_w
    return nif, niw

if __name__ == "__main__":
    
    #Dane wejsciowe
    temperatura_wlot = 155 #zmienna wejsciowa!
    temperatura_wylot = 265  #zmienna wejsciowa! 
    temperatura_sciany = 270 #zmienna wejsciowa!
    selected_temp = (temperatura_wlot+temperatura_wylot)/2 
    selected_material = 'dry_air' #zmienna wejsciowa!
    selected_velosity = 4 #zmienna wejsciowa!
    wymiar_charakterystyczny = 9*10**-3 #zmienna wejsciowa!
    dlugosc = 1.6 #dlugosc    
    
    
    try:
        mydb = msql.connect(host='localhost', 
                            user='root',
                            password = '',
                            database="materials"
                            )
        if mydb.is_connected():
            mycursor = mydb.cursor()
            print("We are connected to database")  
            '''
            print(l_reynoldsa(selected_material, selected_temp, selected_velosity, wymiar_charakterystyczny))
            print(l_prandtla(selected_material, selected_temp))
            print(l_prandtla_cp(selected_material, selected_temp))
            '''
            
           
            eps_prf_prw, prf = prf_prw(selected_material, temperatura_wlot, temperatura_sciany)
            
            l_reynoldsa = l_reynoldsa(selected_material, selected_temp, selected_velosity, wymiar_charakterystyczny)
            
            eps_L = rozbieg_hydrauliczny(l_reynoldsa, wymiar_charakterystyczny, dlugosc)
            
            l_grashofa = l_grashofa(selected_material, selected_temp, temperatura_wlot, temperatura_sciany)
            
            
            print("Liczba reynoldsa: ")
            print(l_reynoldsa)
            print("Liczba grashofa: ")
            print(l_grashofa)
            print("Prf: ")
            print(prf)
            print("eps_L: ")
            print(prf)
            l_prandtla = l_prandtla(selected_material, selected_temp)
            print("Liczba prandtla:")
            print(l_prandtla)
            
            
            
            
            if l_reynoldsa <= 2300:
            
                #-----------------------Laminarny------------------------------ Re<=2300
                 
                l_nusselta = 0.15*(l_reynoldsa)**0.33*(prf)**0.43*(l_grashofa)**0.1*(eps_prf_prw)*0.25*eps_L
                print('l_nusselta:')
                print(l_nusselta)
            
            elif l_reynoldsa > 2300 and l_reynoldsa <= 10000:   
                       
                #-----------------------Przejsciowy------------------------------
        
                nif , niw = nif_niw(selected_material, temperatura_wlot, temperatura_sciany)
                l_nusselta = 0.037*(1+(wymiar_charakterystyczny/dlugosc)**(2/3))*((l_reynoldsa)**0.75-180)*l_prandtla**0.42*(nif/niw)**0.14
                print('l_nusselta:')
                print(l_nusselta)
            
            elif l_reynoldsa > 10000 and l_reynoldsa < 50000:
    
    
                #-----------------------Turbuletny------------------------------ Re>=10000
                
                l_nusselta = 0.021*(l_reynoldsa)**0.8*((prf)**0.43)*((eps_prf_prw)**0.25)*eps_L
                print('l_nusselta:')
                print(l_nusselta)
                
    except Error as e:
        print("Connection error", e)
    
    
    
    