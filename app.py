from flask import Flask

from api_subscriptions import api_subscriptions
from database import db_session

app = Flask(__name__)
app.register_blueprint(api_subscriptions)


@app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()
