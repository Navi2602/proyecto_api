from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String, unique=True, nullable=False)
    curp = db.Column(db.String, nullable=False)
    cp = db.Column(db.Integer, unique=False, nullable=False)
    rfc = db.Column(db.String, unique=True, nullable=False)
    tel = db.Column(db.Integer, unique=True, nullable=False)
    fecha = db.Column(db.Integer, unique=False, nullable=False)
    grupo = db.Column(db.String, unique=False, nullable=False)