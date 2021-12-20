import mysql.connector
from case_3 import Case_3

if __name__ == '__main__':
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

    case = Case_3(material=material, temp_plynu=temp_plynu, temp_powierzchni=temp_powierzchni,
                  predkosc_charakterystyczna=predkosc_charakterystyczna, wymiar_charakterystyczny=wymiar_charakterystyczny,
                  mycursor=mycursor
                  )

    # wyznaczone wartości liczb kryterialnych
    liczba_Prandtla = case.liczba_Prandtla()
    liczba_Reynoldsa = case.liczba_Reynoldsa()
    liczba_Grashofa = case.liczba_Grashofa()
    liczba_Rayleigha = case.liczba_Rayleigha()
    liczba_Nusselta = case.liczba_Nusselta()

    print('liczba Prandlta:', liczba_Prandtla,
          '\nliczba Reynoldsa:', liczba_Reynoldsa,
          '\nliczba Grashofa:', liczba_Grashofa,
          '\nliczba Rayleigha:', liczba_Rayleigha,
          '\nliczba Nusselta:', liczba_Nusselta
          )