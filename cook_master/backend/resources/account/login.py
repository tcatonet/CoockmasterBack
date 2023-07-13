# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import jwt
import logging

from datetime import datetime, timedelta

from flask import request, make_response, jsonify, current_app, abort
from werkzeug.security import check_password_hash
from flask_restful import Resource

from resources.account.user import User


class Login(Resource):
    @staticmethod
    def post():
        auth = request.get_json()
        
        if not auth or not auth.get('email') or not auth.get('password'):
            return make_response(str(auth), 408, {'WWW-Authenticate': 'Basic realm ="Login required !!"', 'message': str(auth)})
        
        user = User.query.filter_by(email=auth.get('email')).first()
 
        if not user:
            return make_response('Could not verify' + str(auth.get('email')), 409, {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'})
        
        if check_password_hash(user.password, auth.get('password')):
            token = jwt.encode({'public_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, current_app.config['SECRET_KEY'])

            return make_response(jsonify({'token': token.decode('UTF-8'), 'level': user.level}), 200)
        return make_response((user.password), 404, {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'})
    


    @staticmethod
    def patch():
        auth = request.get_json()

        return make_response(jsonify({}), 200)
