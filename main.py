from flask import Flask, render_template, request, flash, redirect,  url_for


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
    return render_template("case_3.html", data=[{'name':'powietrze'}, {'name':'woda'}])

@app.route("/case_4")

def case_4():
    return render_template("case_4.html", data=[{'name':'powietrze'}, {'name':'woda'}])

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

    return render_template("case_3.html",
                           temp1=temp1,
                           temp3=temp3,
                           )


@app.route("/case_4_result", methods=["POST", "GET"])
def case_4_result():
    output = request.form.to_dict()
    temp1 = float(output["temp1"])
    temp3 = float(output["temp3"])
    material = request.form.get('material')
    velosity = float(output["velo"])
    wymiar = float(output["wymiar"])

    return render_template("case_4.html",
                           temp1=temp1,
                           temp3=temp3,
                           )


if __name__ == '__main__':
    app.run(debug=True, port=5001)