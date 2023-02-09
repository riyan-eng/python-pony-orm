from flask import Flask, render_template, redirect, request,make_response, jsonify
from pony.flask import Pony
from pony.orm import Database, Required, Optional
from http import HTTPStatus

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
  respon={
    "data": datas,
    "message": "ok"
  }
  return jsonify(respon), HTTPStatus.OK

@app.route("/create", methods=["POST"])
def create():
  bodyJson = request.json
  print(bodyJson)
  
  query = f"insert into task(name, description) values('{bodyJson['name']}', '{bodyJson['desc']}')"
  db.execute(query)
  respon = {
    "data": "berhasil memasukkan data",
    "message": "ok"
  }
  return jsonify(respon), HTTPStatus.CREATED

@app.route("/detail/<id>")
def detail(id):
  try:
    query=f"select name, description from public.task where id={id}"
    data = []
    for d in db.execute(query):
      data.append({
        "name": d[0],
        "desc": d[1]
      })
    
    if not data:
      respon={
        "data": "no data",
        "message": "bad"
      }
      return jsonify(respon), HTTPStatus.BAD_REQUEST
    
    respon = {
      "data": data[0],
      "message": "ok"
    }
    return jsonify(respon), HTTPStatus.OK
  
  except Exception as err:
    respon={
      "data": str(err),
      "message": "bad"
    }
    return jsonify(respon), HTTPStatus.BAD_GATEWAY
    

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