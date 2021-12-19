from flask import Flask, render_template,request, flash, redirect,  url_for

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
    return render_template("case_2.html")

@app.route("/case_3")

def case_3():
    return render_template("case_3.html")

@app.route("/case_4")

def case_4():
    return render_template("case_4.html")

@app.route("/case_1_result", methods = ["POST", "GET"])
def case_1_result():
    output = request.form.to_dict()
    temp1 = float(output["temp1"]) 
    temp2 = float(output["temp2"])
    temp3 = float(output["temp2"])
    material = request.form.get('comp_select')
    velosity = float(output["velo"])
    wymiar = float(output["wymiar"])
    dlugosc = float(output["dlugosc"])
    
    
    return render_template("case_1.html", 
                           temp1 = temp1,
                           data=[{'name':'powietrze'}, {'name':'woda'}]) 

if __name__ == '__main__':
    app.run(debug = True, port=5001)