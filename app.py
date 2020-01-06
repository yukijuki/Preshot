from flask import Flask, request, redirect, session, send_from_directory, jsonify, render_template, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "super-secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.debug = True
db = SQLAlchemy(app)


# Define Models

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), unique=True)
    industry = db.Column(db.String(80))
    password = db.Column(db.String(80))
    signed_up_at = db.Column(db.DateTime())

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    filename = db.Column(db.String(255), nullable=False, unique=True, default="default.jpg")
    link = db.Column(db.String(255), nullable=False)
    faculty = db.Column(db.String(80), nullable=False)
    firm = db.Column(db.String(80), nullable=False)
    industry = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(80), nullable=False)
    lab = db.Column(db.String(80), nullable=False)
    club = db.Column(db.String(80), nullable=False)
    wagamanchi = db.Column(db.String(255), nullable=False)
    ask_clicks = db.Column(db.Integer, default=0)

class Ask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(80))
    employee_name = db.Column(db.String(80))
    industry = db.Column(db.String(80))
    position = db.Column(db.String(80))
    created_at = db.Column(db.DateTime())

#----------------------------------------------------------------
# db.drop_all()
# db.create_all()
# db.session.commit()
#User login

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        print(data)

        """
        data = {
            "email":"Str",
            "password" = 6,
        }
        """
        session["Email"] = data["email"]

        student = Student.query.filter_by(email=data["email"]).first()
        print(student)
        if student is None:
            newuser = Student(
            email = data["email"], 
            password = data["password"], 
            signed_up_at=datetime.datetime.now()
            )
            db.session.add(newuser)
            db.session.commit()
            #"account created"
            return redirect(url_for('profile'))
        
        else:
            if student.password == data["password"]:
                return redirect(url_for('home'))

            else:  
                #"password is wrong"
                return redirect(request.url)

    return render_template("register.html")

@app.route("/profile", methods=["Get", "POST"])
def profile():
    email = None
    if session.get("Email", None) is not None:
        email = session.get("Email")
    else:
        redirect(url_for('register'))

    print(email)
    student = Student.query.filter_by(email=email).first()

    if  request.method == "POST":
        data = request.get_json()
        print("check")
        print(data)

        """
        data = {
            "email": "Str",
            "name": "Str",
            "industry" = "Str",
        }
        """
        student.password = data["password"]
        student.name = data["name"]
        student.industry = data["industry"]
        db.session.commit()

        response = make_response(jsonify(data, 200))
        return response

        

    return render_template("profile.html", data = student)

'''
@app.route("/login", methods=["GET"])
def login():
    if request.method == "GET":
        data = request.form

        print(data)
        """
        data = {
            "email":"Str",
            "password":"int"
        }
        """

        student = Student.query.filter_by(email=data["email"]).first()

        if student is None:
            return jsonify({"message": "need to sign up first"}) #render_template("register.html", message = "email not found")

        else:
            if student.password == data["password"]:
                return jsonify({"message": "you made it"}) #render_template("home.html", title="Login", form=form)

            else:
                return jsonify({"message": "password is wrong"}) #render_template("login.html", message = "password is wrong")
    return render_template("login.html")
'''

@app.route("/home", methods=["GET"])
def home():
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
    # def sort():
    #     return employees, common

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

    return render_template("home.html", data = response)


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
        position=data["position"], 
        created_at=datetime.datetime.now())

    db.session.add(asklog)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)