from flask import Flask, render_template, request, abort
from sqlalchemy.orm import scoped_session
from db import SessionLocal
from models.temperature_status import TemperatureStatus


app = Flask(__name__, template_folder="../frontend/build", static_folder="../frontend/build/static")
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
    
    return TemperatureStatus.get_now(db_session)


@app.post('/api/temperature')
def new_temp():
    # TODO: handle errors
    try:
        entry = TemperatureStatus(**request.get_json())
        db_session.add(entry)
        db_session.commit()
        return '', 201
    except Exception as error:
        print(error)
        abort(400, error)


@app.errorhandler(400)
def error400(error):
    return error, 400

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()