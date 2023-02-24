from flask_sqlalchemy import SQLAlchemy

# create flask.SQLAlchemy instance to pass the base model metadata as table classes superclass
# to support flask framework conventions
database = SQLAlchemy()
