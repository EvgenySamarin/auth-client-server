"""
Flask configuration. Currently, stubs and fakes

IN CASE OF PUBLICATION TO A PUBLIC REPOSITORY, THIS FILE MUST BE HIDDEN
"""

# alchemy_config for different database connection types
# PostgreSQL =  postgresgl://user:password@localhost/mydatabase
# MySQL = mysql://user:password@localhost/mydatabase
# Oracle = oracle://user:password@127.0.0.1:1521/mydatabase
# SQLite = sqlite://user:password@127.0.0.1:1521/mydatabase
SQLALCHEMY_DATABASE_URI = 'sqlite:///flsite.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
SECRET_KEY = '86548a1a-aee2-11ed-9522-ee0f590d2416'