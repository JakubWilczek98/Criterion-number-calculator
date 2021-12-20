import mysql.connector as msql
from mysql.connector import Error
from flask import Flask, render_template, request, flash, redirect,  url_for
from case_3 import Case_3
from case_4 import Case_4


app = Flask(__name__)


@app.route("/")
@app.route("/home")


def home():
    return render_template("index.html")

@app.route("/case_1")

def case_1():
    return render_template("case_1.html", data=[{'name':'powietrze'}, {'name':'woda'}])

@app.route("/case_2")

def case_2():
    return render_template("case_2.html",
                           data=[{'name':'powietrze'}, {'name':'woda'}], data1=[{'name':'Oplyw walca'}, {'name':'Oplyw plyty'}])

@app.route("/case_3")

def case_3():
    return render_template("case_3.html", data=[{'name':'dry_air'}, {'name':'water'}])

@app.route("/case_4")

def case_4():
    return render_template("case_4.html", data=[{'name':'dry_air'}, {'name':'water'}])

@app.route("/case_1_result", methods = ["POST", "GET"])
def case_1_result():
    output = request.form.to_dict()
    temp1 = float(output["temp1"]) 
    temp2 = float(output["temp2"])
    temp3 = float(output["temp3"])
    material = request.form.get('material')
    velosity = float(output["velo"])
    wymiar = float(output["wymiar"])
    dlugosc = float(output["dlugosc"])

    
    
    return render_template("case_1.html", 
                           temp1 = temp1, material = material,
                           data=[{'name':'powietrze'}, {'name':'woda'}]) 

@app.route("/case_2_result", methods = ["POST", "GET"])
def case_2_result():
    output = request.form.to_dict()
    temp1 = float(output["temp1"]) 
    temp3 = float(output["temp3"])
    material = request.form.get('material')
    velosity = float(output["velo"])
    wymiar = float(output["wymiar"])
    rodzaj = request.form.get('rodzaj')

    
    return render_template("case_2.html", 
                           temp1 = temp1, rodzaj = rodzaj, 
                           data=[{'name':'powietrze'}, {'name':'woda'}], data1=[{'name':'Oplyw walca'}, {'name':'Oplyw plyty'}])


@app.route("/case_3_result", methods=["POST", "GET"])
def case_3_result():
    output = request.form.to_dict()
    temp1 = float(output["temp1"])
    temp3 = float(output["temp3"])
    material = request.form.get('material')
    velosity = float(output["velo"])
    wymiar = float(output["wymiar"])

    try:
        mydb = msql.connect(host='mysql.agh.edu.pl',
                            user='awilcze1',
                            password='***',
                            database='awilcze1',
                            )
        if mydb.is_connected():
            mycursor = mydb.cursor()
            print('We are connected to database')

            case = Case_3(material=material,
                          temp_plynu=temp1,
                          temp_powierzchni=temp3,
                          predkosc_charakterystyczna=velosity,
                          wymiar_charakterystyczny=wymiar,
                          mycursor=mycursor
                          )

            liczba_Prandtla = case.liczba_Prandtla()
            liczba_Reynoldsa = case.liczba_Reynoldsa()
            liczba_Grashofa = case.liczba_Grashofa()
            liczba_Rayleigha = case.liczba_Rayleigha()
            liczba_Nusselta = case.liczba_Nusselta()

    except Error as e:
        print('Connection error', e)

    return render_template("case_3.html",
                           liczba_Prandtla=liczba_Prandtla,
                           liczba_Reynoldsa=liczba_Reynoldsa,
                           liczba_Grashofa=liczba_Grashofa,
                           liczba_Rayleigha=liczba_Rayleigha,
                           liczba_Nusselta=liczba_Nusselta,
                           )


@app.route("/case_4_result", methods=["POST", "GET"])
def case_4_result():
    output = request.form.to_dict()
    temp1 = float(output["temp1"])
    temp3 = float(output["temp3"])
    material = request.form.get('material')
    velosity = float(output["velo"])
    wymiar = float(output["wymiar"])

    try:
        mydb = msql.connect(host='mysql.agh.edu.pl',
                            user='awilcze1',
                            password='***',
                            database='awilcze1',
                            )
        if mydb.is_connected():
            mycursor = mydb.cursor()
            print('We are connected to database')

            case = Case_3(material=material,
                          temp_plynu=temp1,
                          temp_powierzchni=temp3,
                          predkosc_charakterystyczna=velosity,
                          wymiar_charakterystyczny=wymiar,
                          mycursor=mycursor
                          )

            liczba_Prandtla = case.liczba_Prandtla()
            liczba_Reynoldsa = case.liczba_Reynoldsa()
            liczba_Grashofa = case.liczba_Grashofa()
            liczba_Rayleigha = case.liczba_Rayleigha()
            liczba_Nusselta = case.liczba_Nusselta()

    except Error as e:
        print('Connection error', e)

    return render_template("case_3.html",
                           liczba_Prandtla=liczba_Prandtla,
                           liczba_Reynoldsa=liczba_Reynoldsa,
                           liczba_Grashofa=liczba_Grashofa,
                           liczba_Rayleigha=liczba_Rayleigha,
                           liczba_Nusselta=liczba_Nusselta,
                           )


if __name__ == '__main__':
    app.run(debug=True, port=5001)
