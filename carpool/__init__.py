import os
from carpool.schedule import automaticDelete
from flask import (
            Flask,session)
from carpool.db1 import connector
from carpool.auth import login_required
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    from . import auth
    app.register_blueprint(auth.bp)
    # a simple page that says hello
    from . import AfterLogin
    app.register_blueprint(AfterLogin.bp)

    from . import transaction
    app.register_blueprint(transaction.bp)
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=automaticDelete, trigger="interval", seconds=60)
    scheduler.start()
    atexit.register(lambda:scheduler.shutdown(wait=False))

    @app.route('/hello')
    @login_required
    def hello():
        try:
            c, conn = connector()
            #print(session['username'])
            return("okay")
        except Exception as e:
            return(str(e))
    return app
