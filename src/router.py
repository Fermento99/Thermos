from flask import Flask, render_template, request, abort
from sqlalchemy.orm import scoped_session
from db import SessionLocal
from models.temperature_status import TemperatureStatus
from models.heating_status import HeatingStatus


app = Flask(__name__, template_folder="../frontend/build", static_folder="../frontend/build", static_url_path='')
db_session = scoped_session(SessionLocal)

@app.get("/")
def index():
    return render_template('index.html')

@app.get('/api/temperature')
def get_temperature():
    # TODO: handle errors
    args = request.args
    if 'room' in args.keys():
        try: 
            if 'limit' in args.keys():
                return TemperatureStatus.get_history(db_session, room=args['room'], limit=int(args['limit']))
            else:
                return TemperatureStatus.get_history(db_session, room=args['room'], limit=12)
        except Exception as error:
            print(error)
            abort(400, error)
    
    return TemperatureStatus.get_last_entry(db_session)

@app.get('/api/heating')
def get_heating():
    # TODO: handle errors
    args = request.args
    if 'room' in args.keys():
        try: 
            if 'limit' in args.keys():
                return HeatingStatus.get_history(db_session, room=args['room'], limit=int(args['limit']))
            else:
                return HeatingStatus.get_history(db_session, room=args['room'], limit=12)
        except Exception as error:
            print(error)
            abort(400, error)
    
    return HeatingStatus.get_last_entry(db_session)

@app.errorhandler(400)
def error400(error):
    return error, 400

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()