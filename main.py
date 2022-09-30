import sqlite3
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from validaciones import validar_rfc, validar_telefono, validar_fecha, validar_cp, validar_curp
import os
from dotenv import load_dotenv
from functools import wraps
from models import Usuarios
from decoradores import token_requerido, es_admin, permisos_escritura

#Variables de entorno
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    """Función para crear todas las tablas"""
    db.create_all()


@app.route('/generar_token', methods=['POST'])
def login():
    """Servicio para generar el token."""
    if request.json['usuario'] and request.json['api_key'] == app.config['SECRET_KEY'] and  request.json['password'] == 'password':
        token = jwt.encode({
            'user' : request.json['usuario'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=600)},
            app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    
    return jsonify({'error':'No se puede verificar'})

@app.route('/usuarios/crear', methods=['POST'])
@token_requerido
@es_admin
def crear_usuario():
    """Servicio para crear un usuario"""

    validar_rfc(request.json['rfc'])
    validar_telefono(request.json['tel'])
    validar_fecha(request.json['fecha'])
    validar_cp(request.json['cp'])
    validar_curp(request.json['curp'])

    usuario_data = Usuarios(
        usuario= request.json['usuario'],
        curp = request.json['curp'],
        cp = request.json['cp'],
        rfc = request.json['rfc'],
        tel = request.json['tel'],
        fecha = request.json['fecha'],
        grupo = request.json['grupo']
        )

    db.session.add(usuario_data)
    db.session.commit()
    return jsonify({'exito': 'datos capturados correctamente'})

@app.route("/usuario/<int:_id>", methods=["GET"])
@token_requerido
def consultar_usuario(_id):
    """Servicio para consultar un solo usuario."""
    try:
        usuarios = Usuarios.query.get(_id)

        output = []

        user_data = {}
        user_data['usuario'] = usuarios.usuario
        user_data['curp'] = usuarios.curp
        user_data['cp'] = usuarios.cp
        user_data['rfc'] = usuarios.rfc
        user_data['tel'] = usuarios.tel
        user_data['grupo'] = usuarios.grupo

        output.append(user_data)
        return jsonify({'usuarios': output})
    except:
        return jsonify({'mensaje': f'El usuario con id {_id} no existe.'})


@app.route("/usuarios", methods=["GET"])
@token_requerido
def consultar_usuarios():
    """Servicio para consultar todos los usuarios."""
    try:
        usuarios = Usuarios.query.all()

        output = []

        for _usuario in usuarios:
            user_data = {}
            user_data['usuario'] = _usuario.usuario
            user_data['curp'] = _usuario.curp
            user_data['cp'] = _usuario.cp
            user_data['rfc'] = _usuario.rfc
            user_data['tel'] = _usuario.tel
            user_data['grupo'] = _usuario.grupo

            output.append(user_data)
        return jsonify({'usuarios': output})
    except:
        return jsonify({'mensaje': 'Actualmente no hay usuarios en la base de datos.'})

@app.route("/usuario/<int:_id>/actualizar", methods=["PUT"])
@token_requerido
@permisos_escritura
def actualizar_usuario(_id):
    """Servicio para actualizar un usuario."""

    validar_rfc(request.json['rfc'])
    validar_telefono(request.json['tel'])
    validar_fecha(request.json['fecha'])
    validar_cp(request.json['cp'])
    validar_curp(request.json['curp'])

    try:
        db.session.query(Usuarios).filter(Usuarios.id==_id).update(request.json)
        db.session.commit()
        return jsonify({'exito': 'usuario actualizado correctamente'})
    except:
        return jsonify({'mensaje': f'El usuario con id {_id} no existe.'})

@app.route("/usuario/<int:_id>/eliminar", methods=["GET"])
@token_requerido
@es_admin
def eliminar_usuario(_id):
    """Servicio para eliminar un usuario."""

    try:
        db.session.query(Usuarios).filter(Usuarios.id==_id).delete()
        db.session.commit() 
        return jsonify({'exito': 'usuario eliminado correctamente'})
    except:
        return jsonify({'mensaje': f'El usuario con id {_id} no existe.'})

if __name__ == '__main__':
    app.run(debug=True)