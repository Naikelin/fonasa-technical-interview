from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .routes import rest_api
from .models import db

load_dotenv('.env')

app = Flask(__name__)
app.config.from_object('api.config.BaseConfig')

db.init_app(app)
migrate = Migrate(app, db)
rest_api.init_app(app)
CORS(app)