import mysql.connector

# konwekcja swobodna w przestrzeni nieograniczonej

mydb = mysql.connector.connect(
    host='mysql.agh.edu.pl',
    user='awilcze1',
    password='***',
    database='awilcze1'
)

mycursor = mydb.cursor()


material = 'dry_air'
temp_plynu = 30
temp_powierzchni = 170
temp_charakterystyczna = round((temp_powierzchni + temp_plynu)/2)
wymiar_charakterystyczny = 0.1
predkosc_charakterystyczna = 10

if material == 'water':
    selection = 'SELECT wspl_przew_ciepla, wspl_lepkosci_kinematycznej, liczba_prandtla, wspl_rozszerzalnosci FROM {} WHERE temperatura = {}'.format(material, temp_charakterystyczna)
elif material == 'dry_air':
    selection = 'SELECT wspl_przew_ciepla, wspl_lepkosci_kinematycznej, liczba_prandtla FROM {} WHERE temperatura = {}'.format(material, temp_charakterystyczna)


mycursor.execute(selection)
myresult = mycursor.fetchall()


przysp_ziemskie = 9.81
wsp_przewodzenia_ciepla = ([i[0] for i in myresult][0])/10**2
wsp_lepkosci_kinematycznej = ([i[1] for i in myresult][0])/10**6

if material == 'water':
    wsp_rozszerzalnosci = ([i[3] for i in myresult][0])/10**4
elif material == 'dry_air':
    wsp_rozszerzalnosci = 1/373

liczba_Prandtla = [i[2] for i in myresult][0]
liczba_Reynoldsa = (predkosc_charakterystyczna * wymiar_charakterystyczny)/wsp_lepkosci_kinematycznej
liczba_Grashofa = ((wsp_rozszerzalnosci * przysp_ziemskie * wymiar_charakterystyczny**3)/wsp_lepkosci_kinematycznej**2)*(temp_powierzchni - temp_plynu)
liczba_Rayleigha = liczba_Grashofa * liczba_Prandtla

if liczba_Rayleigha < 0.001:
    C = 0.5
    n = 0
elif liczba_Rayleigha >= 0.001 and liczba_Rayleigha < 500:
    C = 1.18
    n = 1/8
elif liczba_Rayleigha >= 500 and liczba_Rayleigha < 20*10**6:
    C = 0.54
    n = 1/4
elif liczba_Rayleigha > 20*10**6 and liczba_Rayleigha < 10**13:
    C = 0.135
    n = 1/3

liczba_Nusselta = C * (liczba_Rayleigha)**(n)
###
liczba_Froudea = predkosc_charakterystyczna**2/(przysp_ziemskie * wymiar_charakterystyczny)

liczba_Galileusza = liczba_Reynoldsa**2/liczba_Froudea

#liczba_Galileusza2 = (przysp_ziemskie * wymiar_charakterystyczny**3)/wsp_lepkosci_kinematycznej**2

liczba_Archimedesa = liczba_Galileusza * wsp_rozszerzalnosci * (temp_powierzchni - temp_plynu)

print('liczba Prandlta:', liczba_Prandtla, '\nliczba Reynoldsa:', liczba_Reynoldsa, '\nliczba Grashofa:', liczba_Grashofa,
      '\nliczba Rayleigha:', liczba_Rayleigha, '\nliczba Nusselta:', liczba_Nusselta)

print('liczba Galileusza:', liczba_Galileusza, '\nliczba Archimedesa:', liczba_Archimedesa)
#print(myresult)
