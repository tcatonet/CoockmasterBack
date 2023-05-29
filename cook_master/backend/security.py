# BRAIZET Rémi
# Version 3.0

import logging
import jwt
from functools import wraps
from flask import request, jsonify, current_app, abort, make_response

from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from resources.user import User


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)


def authenticate():
    # creates dictionary of form data
    auth = request.form
    
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="Login required !!"'})
    
    user = User.query.filter_by(email=auth.get('email')).first()
    
    if not user:
        # returns 401 if user does not exist
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'})
    
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           current_app.config['SECRET_KEY'])
        
        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'})