# from flask import Flask,render_template
# app=Flask("__name__")
# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/login")
# def login():
#     return render_template("login.html")

# if __name__=="__main__":
#     app.run(debug=True,port=5000)

# from flask import Flask, render_template
# from flask_mysqldb import MySQL

# app = Flask(__name__)

# # MySQL Configuration
# app.config['MYSQL_HOST'] = '127.0.0.1:3306'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '902165'
# app.config['MYSQL_DB'] = 'classroom'

# mysql = MySQL(app)

# @app.route("/")
# def index():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM student")
#     data = cur.fetchall()
#     cur.close()
#     return  render_template("index.html", data=data)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host=" 127.0.0.1",
    user="root",
    password="902165",
    database="qa_assistant"
)

cursor = db.cursor()

@app.route("/")
def home():
    cursor.execute("SELECT DATABASE();")
    dbname = cursor.fetchone()
    print("Connected Database:", dbname)
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    feature = request.form["feature"]

    test_case = f"Check if {feature} works correctly with valid and invalid inputs."
    
    cursor.execute(
        "INSERT INTO test_cases (feature_name, test_case) VALUES (%s, %s)",
        (feature, test_case)
    )

    db.commit()
    return redirect("/dashboard")


@app.route("/add_bug", methods=["POST"])
def add_bug():
    title = request.form["title"]
    desc = request.form["description"]

    if "crash" in desc.lower():
        priority = "high"
    elif "slow" in desc.lower():
        priority = "medium"
    else:
        priority = "low"

    cursor.execute(
        "INSERT INTO bugs (title, description, priority) VALUES (%s, %s, %s)",
        (title, desc, priority)
    )

    db.commit()
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    # ✅ Corrected SELECT Queries
    cursor.execute("SELECT * FROM test_cases")
    tests = cursor.fetchall()

    cursor.execute("SELECT * FROM bugs")
    bugs = cursor.fetchall()

    return render_template("dashboard.html", tests=tests, bugs=bugs)


if __name__ == "__main__":
    app.run(debug=True)