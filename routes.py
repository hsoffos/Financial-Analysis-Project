from flask import render_template, request
from dbsetup import app, db
from peopledb import People
import templates


@app.route('/')
def home():
    return '<a href="/addperson"><button> Click Here </button></a>'


@app.route("/addperson")
def addperson():
    return render_template("index_landing.html")


@app.route("/personadd", methods=['POST'])
def personadd():
    pname = request.form["pname"]
    color = request.form["color"]
    entry = People(pname, color)
    db.session = People(pname, color)
    db.session.add(entry)
    db.session.commit()

    return render_template("index_landing.html")
