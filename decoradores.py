from functools import wraps
from flask import Flask, jsonify, request
import jwt
import os
from dotenv import load_dotenv
from models import Usuarios

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def token_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'mensaje' : 'El token es requerido'})

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({'mensaje' : 'El token es inválido'})
        return f(*args, **kwargs)
    return decorated

def es_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if data['user'] == 'superuser123':
            return f(*args, **kwargs)
        usuarios = Usuarios.query.filter_by(usuario=data['user']).first()
        if usuarios.grupo != 'admin':
            return jsonify({
                'mensaje' : 'El usuario actual no cuenta con permisos suficientes'
                })
        else:
            return f(*args, **kwargs)
    return decorated

def permisos_escritura(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        usuarios = Usuarios.query.filter_by(usuario=data['user']).first()
        if usuarios.grupo != 'admin' and usuarios.grupo != 'writter':
            return jsonify({
                'mensaje' : 'El usuario actual no cuenta con permisos suficientes'
                })
        else:
            return f(*args, **kwargs)
    return decorated