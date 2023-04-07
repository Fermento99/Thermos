from flask import Flask, render_template, request, abort
from sqlalchemy.orm import scoped_session
from db import SessionLocal
from models.status import Status


app = Flask(__name__, template_folder="../frontend/build", static_folder="../frontend/build", static_url_path='')
db_session = scoped_session(SessionLocal)

@app.get("/")
def index():
    return render_template('index.html')

@app.get('/api/status')
def get_status():
    # TODO: handle errors
    args = request.args
    if 'room' in args.keys():
        try: 
            if 'limit' in args.keys():
                return Status.get_history(db_session, room=args['room'], limit=int(args['limit']))
            else:
                return Status.get_history(db_session, room=args['room'], limit=12)
        except Exception as error:
            print(error)
            abort(400, error)
    
    return Status.get_last_entry(db_session)


@app.errorhandler(400)
def error400(error):
    return error, 400

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()