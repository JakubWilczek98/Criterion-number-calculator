import pandas as pd
import numpy as np
import mysql.connector as msql
from mysql.connector import Error
 
class Case_1:
        def __init__(self, temperatura_wlot, temperatura_wylot, temperatura_sciany, selected_material, selected_velosity, wymiar_charakterystyczny, dlugosc, mycursor):
            #Dane wejsciowe
            self.temperatura_wlot = temperatura_wlot #zmienna wejsciowa!
            self.temperatura_wylot = temperatura_wylot #zmienna wejsciowa! 
            self.temperatura_sciany = temperatura_sciany #zmienna wejsciowa!
            self.selected_temp = (temperatura_wlot+temperatura_wylot)/2 
            self.selected_material = selected_material #zmienna wejsciowa!
            self.selected_velosity = selected_velosity #zmienna wejsciowa!
            self.wymiar_charakterystyczny = wymiar_charakterystyczny #zmienna wejsciowa!
            self.dlugosc = dlugosc #dlugosc
            self.mycursor = mycursor
            
        def l_reynoldsa(self):
            self.mycursor.execute("SELECT wspl_lepkosci_dynamicznej FROM {} WHERE temperatura = {}".format(self.selected_material, self.selected_temp))
            myresult = self.mycursor.fetchall()            
            wspl_lepkosci_dynamicznej = [i[0] for i in myresult][0] *10**-6
            self.l_reynoldsa = (self.selected_velosity*self.wymiar_charakterystyczny)/wspl_lepkosci_dynamicznej  
            return round(self.l_reynoldsa,3)

        def l_prandtla(self):  
            self.mycursor.execute("SELECT wspl_lepkosci_kinematycznej, wspl_dyf_cieplnej FROM {} WHERE temperatura = {}".format(self.selected_material, self.selected_temp))
            myresult = self.mycursor.fetchall()            
            wspl_lepkosci_kinematycznej = [i[0] for i in myresult][0]*10**-6
            wspl_dyf_cieplnej = [i[1] for i in myresult][0]*10**-6          
            self.l_prandtla = wspl_lepkosci_kinematycznej/wspl_dyf_cieplnej
            return round(self.l_prandtla,3)

        def l_prandtla_cp(self):
            self.mycursor.execute("SELECT wspl_lepkosci_dynamicznej, cieplo_wlasciwe, wspl_przew_ciepla FROM {} WHERE temperatura = {}".format(self.selected_material, self.selected_temp))
            myresult = self.mycursor.fetchall()            
            wspl_lepkosci_dynamicznej = [i[0] for i in myresult][0]*10**-6
            cieplo_wlasciwe = [i[1] for i in myresult][0]*10**3
            wspl_przew_ciepla = [i[2] for i in myresult][0]*10**-2
            self.l_prandtla_cp = (cieplo_wlasciwe*wspl_lepkosci_dynamicznej)/(wspl_przew_ciepla)
            return self.l_prandtla_cp
    
        def l_grashofa(self):
            g = 9.81
            if self.selected_material == "dry_air":
                beta = 1/373
            elif self.selected_material == "water":
                self.mycursor.execute("SELECT wspl_rozszerzalnosci FROM {} WHERE temperatura = {}".format(self.selected_material, abs(self.selected_temp-self.temperatura_sciany)))
                myresult = self.mycursor.fetchall()
                beta = [i[0] for i in myresult][0]*10**-4
            self.mycursor.execute("SELECT wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}".format(self.selected_material, self.selected_temp))
            myresult = self.mycursor.fetchall()   
            wspl_lepkosci_kinematycznej = [i[0] for i in myresult][0]*10**-6
            self.l_grashofa = (g*self.wymiar_charakterystyczny**3*beta*abs(self.selected_temp-self.temperatura_sciany)/wspl_lepkosci_kinematycznej**2)
            return round(self.l_grashofa)

        def rozbieg_hydrauliczny(self):
            L_do_w_charakterystyczny = round(self.dlugosc/self.wymiar_charakterystyczny)
            if self.l_reynoldsa <=2300:   
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
            self.eps_L = eps_L
            return self.eps_L
        
        def prf_prw(self):
            if self.selected_material == "dry_air":
                self.mycursor.execute("SELECT liczba_prandtla FROM {} WHERE temperatura = {}".format(self.selected_material, self.selected_temp))
                myresult = self.mycursor.fetchall()   
                self.prf = [i[0] for i in myresult][0]
                self.eps_prf_prw = 1
            elif self.selected_material == "water":
                self.mycursor.execute("SELECT liczba_prandtla FROM {} WHERE temperatura = {}".format(self.selected_material, self.selected_temp))
                myresult = self.mycursor.fetchall()   
                self.prf = [i[0] for i in myresult][0]
                self.mycursor.execute("SELECT wspl_rozszerzalnosci FROM {} WHERE temperatura = {}".format(self.selected_material, self.temperatura_sciany))
                myresult = self.mycursor.fetchall()   
                prw = [i[0] for i in myresult][0]
                self.eps_prf_prw = self.prf/prw
            return self.eps_prf_prw, self.prf

        def etaf_etaw(self):
            self.mycursor.execute("SELECT gestosc, wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}".format(self.selected_material, self.temperatura_wlot))
            myresult = self.mycursor.fetchall()   
            gestosc_f = [i[0] for i in myresult][0]
            wspl_lepkosci_kinematycznej_f = [i[1] for i in myresult][0]
            
            self.mycursor.execute("SELECT gestosc, wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}".format(self.selected_material, self.temperatura_sciany))
            myresult = self.mycursor.fetchall()   
            gestosc_w = [i[0] for i in myresult][0]
            wspl_lepkosci_kinematycznej_w = [i[1] for i in myresult][0]
            self.etaf = gestosc_f * wspl_lepkosci_kinematycznej_f
            self.etaw = gestosc_w * wspl_lepkosci_kinematycznej_w
            return self.etaf, self.etaw

        def l_nusselta(self):
            #-----------------------Laminarny------------------------------ Re<=2300
            if self.l_reynoldsa <= 2300:
                   
                self.l_nusselta = 0.15*(self.l_reynoldsa)**0.33*(self.prf)**0.43*((self.l_grashofa)**0.1)*((self.eps_prf_prw)**0.25)*self.eps_L
                
            #-----------------------Przejsciowy------------------------------
            elif self.l_reynoldsa > 2300 and self.l_reynoldsa <= 10000:   
                
                self.l_nusselta = 0.037*(1+(self.wymiar_charakterystyczny/self.dlugosc)**(2/3))*((self.l_reynoldsa)**0.75-180)*self.l_prandtla**0.42*(self.etaf/self.etaw)**0.14
            
            #-----------------------Turbuletny------------------------------ Re>=10000
            elif self.l_reynoldsa > 10000 and self.l_reynoldsa < 50000:
        
                self.l_nusselta = 0.021*(self.l_reynoldsa)**0.8*((self.prf)**0.43)*((self.eps_prf_prw)**0.25)*self.eps_L
   
            return round(self.l_nusselta,3)
    

    
    
    
    