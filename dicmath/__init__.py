from flask import Flask

# Create the app
app = Flask(__name__, instance_relative_config=True)

# Configure the app
app.config.from_mapping(
    SECRET_KEY='dev',
)
app.config.from_pyfile('config.py', silent=True)

# Import routing
from dicmath import views
