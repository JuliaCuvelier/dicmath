import tempfile

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create and configure the app
app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{tempfile.gettempdir()}/dicmath.db',
)
app.config.from_pyfile('config.py', silent=True)

# Create and configure the database
db = SQLAlchemy(app)

from dicmath import models

with app.app_context():
    db.drop_all()
    db.create_all()

# Import routing
from dicmath import views
