from flask import Flask, render_template, redirect, request
from pony.flask import Pony
from pony.orm import Database, Required, Optional

db = Database()

class Task(db.Entity):
  name = Required(str)
  description = Optional(str)

db.bind(provider="postgres", user="postgres", password="riyan", host="localhost", database="pony")
db.generate_mapping(create_tables=True)
app = Flask(__name__)
Pony(app)

@app.route("/")
def index():
  query = "select * from public.task"
  datas = []
  for d in db.execute(query):
    datas.append({
      "id": d[0],
      "name": d[1],
      "desc": d[2]
    })
  return render_template("index.html", datas=datas)

@app.route("/create", methods=["POST"])
def create():
  name_req = request.form.get("name")
  desc_req = request.form.get("desc")
  
  query = f"insert into task(name, description) values('{name_req}', '{desc_req}')"
  db.execute(query)
  return redirect("/")

@app.route("/detail/<id>")
def detail(id):
  query=f"select name, description from public.task where id={id}"
  data = []
  for d in db.execute(query):
    data.append({
      "name": d[0],
      "desc": d[1]
    })
  return render_template("detail.html", data=data[0])

@app.route("/update/<id>")
def update(id):
  return render_template("update.html")

@app.route("/update/<id>", methods=["POST"])
def update_post(id):
  return "help me"

@app.route("/delete/<id>")
def delete(id):
  query = f"delete from public.task where id={id}"
  db.execute(query)
  return redirect("/")