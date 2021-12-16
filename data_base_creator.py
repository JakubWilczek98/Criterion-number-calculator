import pandas as pd
import mysql.connector as msql
from mysql.connector import Error

csv_dry_air = pd.read_csv('dry_air_interpolated.csv', sep=',', header=None)
csv_water = pd.read_csv('water_interpolated.csv', sep=',', header=None)

try:
    conn = msql.connect(
        host='mysql.agh.edu.pl',
        user='awilcze1',
        password='***',
        database='awilcze1'
    )

    if conn.is_connected():
        cursor = conn.cursor()
        print("We are connected")
        cursor.execute('DROP TABLE IF EXISTS dry_air;')
        print('Creating table....')
        cursor.execute("CREATE TABLE dry_air (temperatura INT(3), gestosc FLOAT(4,3), cieplo_wlasciwe FLOAT(4,3), wspl_przew_ciepla FLOAT(3,2), wspl_dyf_cieplnej FLOAT(4,1), wspl_lepkosci_dynamicznej FLOAT(3,1), wspl_lepkosci_kinematycznej FLOAT(6,2), liczba_prandtla FLOAT(4,3))")
        print("dry_air table is created....")
        for i, row in csv_dry_air.iterrows():
            sql = "INSERT INTO awilcze1.dry_air VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # the connection is not autocommitted by default, so we must commit to save our changes
            conn.commit()
        cursor.execute('DROP TABLE IF EXISTS water;')
        print('Creating table....')
        cursor.execute("CREATE TABLE water (temperatura INT(2), cisnienie FLOAT(8,5), gestosc FLOAT(4,1), cieplo_wlasciwe FLOAT(8,3), wspl_przew_ciepla FLOAT(3,1), wspl_dyf_cieplnej FLOAT(3,1), wspl_lepkosci_dynamicznej FLOAT(5,1), wspl_lepkosci_kinematycznej FLOAT(4,3), wspl_rozszerzalnosci FLOAT(3,2) , napiecie_powierzchniowe FLOAT(4,1) ,liczba_prandtla FLOAT(4,2))")
        print("water table is created....")
        for i, row in csv_water.iterrows():
            sql = "INSERT INTO awilcze1.water VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # the connection is not autocommitted by default, so we must commit to save our changes
            conn.commit()
except Error as e:
    print("Connection error", e)
