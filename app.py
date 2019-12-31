from flask import Flask, request, redirect, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://App:fmg9akimbo@localhost/preshot"
app.config["SECRET_KEY"] = "super-secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.debug = True
db = SQLAlchemy(app)
# db.drop_all()
# db.create_all()

# Define Models

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.Integer(1))
    name = db.Column(db.String(80), unique=True)
    faculty = db.Column(db.String(80))
    club = db.Column(db.String(80))
    lab = db.Column(db.String(80))
    industry = db.Column(db.String(80))
    position = db.Column(db.String(80))
    signed_up_at = db.Column(db.DateTime())

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    filename = db.Column(db.String(255), unique=True)
    link = db.Column(db.String(255))
    faculty = db.Column(db.String(80))
    firm = db.Column(db.String(80))
    industry = db.Column(db.String(80))
    position = db.Column(db.String(80))
    lab = db.Column(db.String(80))
    club = db.Column(db.String(80))
    wagamanchi = db.Column(db.String(255))
    ask_clicks = db.Column(db.Integer)

class Ask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(80))
    employee_name = db.Column(db.String(80))
    club = db.Column(db.String(80))
    lab = db.Column(db.String(80))
    industry = db.Column(db.String(80))
    firm = db.Column(db.String(80))
    position = db.Column(db.String(80))
    created_at = db.Column(db.DateTime())

#----------------------------------------------------------------
#User login

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    """
    data = {
        "email":"Str",
        "password" = 6,
        "name": "Str",
        "faculty" = "Str",
        "club" = "Str",
        "lab" = "Str",
        "industry" = "Str",
        "position": "Str"
    }
    """

    newuser = Student(
        email = data["email"], 
        password = data["password"], 
        name = data["name"],
        faculty = data["faculty"],
        club = data["club"],
        lab = data["lab"],
        industry = data["industry"],
        position = data["position"],
        signed_up_at=datetime.datetime.now()
    )
    db.session.add(newuser)
    db.session.commit()

    return jsonify({"user": newuser})


@app.route("/login", methods=["GET"])
def login():
    data = request.get_json()
    """
    data = {
        "email":"Str",
        "pass":"int"
    }
    """

    user = Student.query.filter_by(email=data["email"]).first()

    if user is None:
        return jsonify({"message":"ユーザが見つかりません、先に登録してください。"})

    else:
        if user.password == data["password"]:
            return jsonify({"message":"Logined Succesfully"})

        else:
            return jsonify({"message":"パスワードが違います。"})


@app.route("/get_employees", methods=["GET"])
def get_employees():
    data = request.get_json()
    
    """
    data = {
        "faculty" = "Str",
        "firm" = "Str",
        "industry" = "Str",
        "position": "Str",
        "lab" = "Str",
        "club" = "Str",
    }
    """

    employees = Employee.query.all()

    #Sort with function
    def sort():
        return employees, common

    response = []

    for emplyee in employees:
        employee_data = {}
        employee_data["name"] = Employee.name
        employee_data["filename"] = Employee.filename
        employee_data["link"] = Employee.link
        employee_data["faculty"] = Employee.faculty
        employee_data["firm"] = Employee.firm
        employee_data["industry"] = Employee.industry
        employee_data["position"] = Employee.position
        employee_data["lab"] = Employee.lab
        employee_data["club"] = Employee.club
        employee_data["wagamanchi"] = Employee.wagamanchi
        employee_data["ask_clicks"] = Employee.ask_clicks
        response.append(employee_data)

    return jsonify({"list of employees": response})


@app.route("/ask_click", methods=["GET","Post"])
def ask_click():
    data = request.get_json()
    """
    data = {
        "email":"Str",
        "employee_name":"Str"
        "industry":"Str",
        "firm":"Str"
        "position":"Str",
        "lab":"Str"
        "club":"Str",
    }
    """
    employee = Employee.query.filter_by(name=data["employee_name"]).first()
    if employee.ask_clicks is None:
        employee.ask_clicks == 1
    else:
        employee.ask_clicks += 1
    asklog = Ask(
        email=data["email"], 
        employee_name=data["employee_name"], 
        industry=data["industry"], 
        firm=data["firm"], 
        position=data["position"], 
        lab=data["lab"], 
        club=data["club"], 
        created_at=datetime.datetime.now())

    db.session.add(asklog)
    db.session.commit()

    return jsonify({"images": "clicked"})

if __name__ == "__main__":
    app.run()