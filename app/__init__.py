from flask import Flask
from .config import Config
from .routes import orders
from .models import db, Employee
from flask_login import LoginManager
from .routes import session

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)
db.init_app(app)

login = LoginManager(app)
login.login_view = 'session.login'

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))
