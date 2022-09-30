from stdnum.mx.rfc import (validate,InvalidComponent,InvalidFormat,
InvalidLength,InvalidChecksum)
from flask import Flask, jsonify, request, make_response
import re
import datetime
from curp import CURP, CURPValueError

def validar_rfc(rfc):
    try:
        validate( rfc, validate_check_digits=True)
    except (InvalidComponent,InvalidFormat,InvalidLength,InvalidChecksum):
        return jsonify({'mensaje': 'RFC incorrecto'})

def validar_telefono(tel):
    regex_telefono = r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-|.]?){6,7}$"
    result = re.match(regex_telefono, tel)
    if result == None:
        return jsonify({'mensaje':'Número telefónico no válido'})

def validar_fecha(date_text):
        try:
            datetime.datetime.strptime(date_text, '%d-%m-%Y')
        except ValueError:
            return jsonify({'mensaje':'Formato de fecha incorrecto'})

def validar_cp(cp):
    if cp.isdigit() and len(cp) == 5:
        pass
    else:
        return jsonify({'error': 'Código Postal erroneo'})

def validar_curp(curp):
    try:
        c = CURP(curp)
    except Exception as e:
        return jsonify({'mensaje':'Formato de CURP incorrecto'})