import mysql.connector

def liczba_Prandtla(material, temp_charakterystyczna):
    selection = 'SELECT liczba_prandtla FROM {} WHERE temperatura = {}'.format(material, temp_charakterystyczna)
    mycursor.execute(selection)
    myresult = mycursor.fetchall()
    return [i[0] for i in myresult][0]

def liczba_Reynoldsa(material, predkosc_charakterystyczna, wymiar_charakterystyczny):
    selection = 'SELECT wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}'.format(material, temp_charakterystyczna)
    mycursor.execute(selection)
    myresult = mycursor.fetchall()
    wsp_lepkosci_kinematycznej = ([i[0] for i in myresult][0])/10**6
    return (predkosc_charakterystyczna * wymiar_charakterystyczny)/wsp_lepkosci_kinematycznej

def liczba_Grashofa(material, temp_charakterystyczna, przysp_ziemskie, temp_powierzchni, temp_plynu):
    if material == 'water':
        selection = 'SELECT wspl_lepkosci_kinematycznej, wspl_rozszerzalnosci FROM {} WHERE temperatura = {}'.format(material, temp_charakterystyczna)
        mycursor.execute(selection)
        myresult = mycursor.fetchall()
        wsp_lepkosci_kinematycznej = ([i[0] for i in myresult][0])/10**6
        wsp_rozszerzalnosci = ([i[1] for i in myresult][0])/10**4
    elif material == 'dry_air':
        selection = 'SELECT wspl_lepkosci_kinematycznej FROM {} WHERE temperatura = {}'.format(material, temp_charakterystyczna)
        mycursor.execute(selection)
        myresult = mycursor.fetchall()
        wsp_lepkosci_kinematycznej = ([i[0] for i in myresult][0])/10**6
        wsp_rozszerzalnosci = 1/373
    return ((wsp_rozszerzalnosci * przysp_ziemskie * wymiar_charakterystyczny**3)/wsp_lepkosci_kinematycznej**2)*(temp_powierzchni - temp_plynu)

def liczba_Rayleigha(liczba_Prandtla, liczba_Grashofa):
    return liczba_Grashofa * liczba_Prandtla

def liczba_Nusselta(liczba_Rayleigha):
    if liczba_Rayleigha < 0.001:
        C = 0.5
        n = 0
    elif liczba_Rayleigha >= 0.001 and liczba_Rayleigha < 500:
        C = 1.18
        n = 1 / 8
    elif liczba_Rayleigha >= 500 and liczba_Rayleigha < 20 * 10 ** 6:
        C = 0.54
        n = 1 / 4
    elif liczba_Rayleigha > 20 * 10 ** 6 and liczba_Rayleigha < 10 ** 13:
        C = 0.135
        n = 1 / 3
    return C * (liczba_Rayleigha)**(n)

# dane wejściowe
material = 'dry_air'
temp_plynu = 30
temp_powierzchni = 170
temp_charakterystyczna = round((temp_powierzchni + temp_plynu)/2)
wymiar_charakterystyczny = 0.1
predkosc_charakterystyczna = 10
przysp_ziemskie = 9.81

# łączenie się z bazą danych
mydb = mysql.connector.connect(
    host='mysql.agh.edu.pl',
    user='awilcze1',
    password='***',
    database='awilcze1'
)

mycursor = mydb.cursor()

# wyznaczone wartości liczb kryterialnych
liczba_Prandtla = liczba_Prandtla(material, temp_charakterystyczna)
liczba_Reynoldsa = liczba_Reynoldsa(material, predkosc_charakterystyczna, wymiar_charakterystyczny)
liczba_Grashofa = liczba_Grashofa(material, temp_charakterystyczna, przysp_ziemskie, temp_powierzchni, temp_plynu)
liczba_Rayleigha = liczba_Rayleigha(liczba_Prandtla, liczba_Grashofa)
liczba_Nusselta = liczba_Nusselta(liczba_Rayleigha)

print('liczba Prandlta:', liczba_Prandtla,
      '\nliczba Reynoldsa:', liczba_Reynoldsa,
      '\nliczba Grashofa:', liczba_Grashofa,
      '\nliczba Rayleigha:', liczba_Rayleigha,
      '\nliczba Nusselta:', liczba_Nusselta
      )
