from .views.routes import auth_blueprint
from .views.incident_views import incident_blueprint
import datetime, os
from flask import Flask
from flask_jwt_extended import JWTManager
app = Flask(__name__)
SECRET_KEY = os.getenv('SECRETE_KEY', "precious")
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=360)
jwt = JWTManager(app)
app.register_blueprint(auth_blueprint)
app.register_blueprint(incident_blueprint)

