from flask import Flask, render_template, request, abort, jsonify
from db.db import db
from db.models.history import History
import config

app = Flask(__name__, template_folder="../frontend/build", static_folder="../frontend/build/static")
app.config.from_prefixed_env()
db.init_app(app)

@app.get("/")
def index():
    return render_template('index.html')

@app.get('/temperature/now')
def get_temp_now():
    # TODO: handle errors
    entry = db.session.execute(db.select(History, History.bathroom).order_by(History.time.desc())).scalars()
    # print(entry.to_dict())
    for obj in entry:
        print(obj)
    return ''

@app.get('/temperature/history/<room>/<int:limit>')
def get_history(room, limit):
    # TODO: inplement
    abort(501)

@app.post('/temperature')
def new_temp():
    # TODO: handle errors
    entry = History(**request.get_json())
    db.session.add(entry)
    db.session.commit()
    return '', 201
