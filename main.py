from flask import Flask
from pony.flask import Pony
from pony.orm import Database, Required, Optional

db = Database()

class Task(db.Entity):
  name = Required(str)
  desc = Optional(str)

db.bind(provider="postgres", user="postgres", password="riyan", host="localhost", database="pony")
db.generate_mapping(create_tables=True)
app = Flask(__name__)
Pony(app)

@app.route("/")
def index():
  return "help me"