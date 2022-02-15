from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('main.config')

db = SQLAlchemy(app)

import main.views