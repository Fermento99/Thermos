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

@app.get('/api/temperature')
def get_temperature():
    # TODO: handle errors
    args = request.args
    if 'room' in args.keys():
        try: 
            if 'limit' in args.keys():
                return History.get_history(room=args['room'], limit=int(args['limit']))
            else:
                return History.get_history(room=args['room'], limit=12)
        except Exception as error:
            print(error)
            abort(400, error)
    
    return History.get_now()


@app.post('/api/temperature')
def new_temp():
    # TODO: handle errors
    try:
        entry = History(**request.get_json())
        db.session.add(entry)
        db.session.commit()
        return '', 201
    except Exception as error:
        print(error)
        abort(400, error)


@app.errorhandler(400)
def error400(error):
    return error, 400
