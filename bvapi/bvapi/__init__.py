import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__version__ = '0.1.0'

DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_BASE = os.environ['DB_BASE']
AD_USER = os.environ['AD_USER']
AD_PASS = os.environ['AD_PASS']

configdb = {
    'postgres': {
        'driver': 'psycopg2',
        'host': DB_HOST,
        'port': DB_PORT,
        'database': DB_BASE,
        'user': DB_USER,
        'password': DB_PASS,
        'prefix': ''
    }
}

DB_URL = "{h}:{p}".format(h=DB_HOST,p=DB_PORT)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=DB_USER, pw=DB_PASS, url=DB_URL, db=DB_BASE)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desliga warning de obsolecencia

db = SQLAlchemy(app)
