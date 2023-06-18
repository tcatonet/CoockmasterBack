# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import jwt

from flask import Blueprint, current_app, abort, request
from functools import wraps
from utils.validation import send_confirmation_mail
from config import mail
from flask_jwt import jwt_required

from models.user import User

app_verification = Blueprint('verication', __name__)
mail_resend = Blueprint('resend', __name__)
ADMIN=100
 
@app_verification.route("/verification/<token>")
def verification(token=''):

    if len(token) < 36:
        abort(503, 'Invalid token')

    user = User.find_by_registration_token(token)
    
    if not user:
        abort(503, 'unprocessable verification')

    user.patch_in_db(dict(verified=''))
    response_message = dict(message='Registration comlpete !\nyou can safely close this windows now.')
    response = current_app.response_class(response=json.dumps(dict(message='user deleted')), status=204,
                                          mimetype='application/json')
    return response
 

@mail_resend.route("/resend")
@jwt_required()
def resend(): 
    current_user = request.args.get('email')
    current_user = current_user.replace("'", "")
    if not current_user:
        abort(404, 'user not found')

    user = User.find_by_email(current_user) 
    
    if not user:
        abort(503, 'unprocessable verification')

    if user.verified == '':
        abort(409, 'you are already verified, you can safely close this windows')
        
    msg = send_confirmation_mail(user.email, request.url_root, user.verified)
    try: 
        mail.send(msg)  
    except ConnectionRefusedError:
        abort(503, dict(message='could not send a new mail'))
    else:
        response = current_app.response_class(response=json.dumps(dict(message='mail sent')), status=204, mimetype='application/json')
        return response 
   
 
def token_required(f): 
   @wraps(f)
   def decorator(*args, **kwargs): 
       token = None 
       if 'x-access-tokens' in request.headers:  
           token = request.headers['x-access-tokens']
  
       if not token:
            abort(405, 'missing token')

       try: 
           data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
           user = User.query.filter_by(id=data['public_id']).first()
           if not user:
            abort(401, 'invalid token')
       except:
            abort(401, 'invalid token') 

       return f(user=user, *args, **kwargs)
   return decorator


def admin_token_required(f): 
   @wraps(f)
   def decorator(*args, **kwargs): 
       token = None 
       if 'x-access-tokens' in request.headers:  
           token = request.headers['x-access-tokens']
  
       if not token:
            abort(405, 'missing token')

       try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.filter_by(id=data['public_id']).first()
            if not user:
                abort(401, 'invalid token')

            if user.level != ADMIN:
                abort(403, 'Forbidden action')            
       except:
            abort(401, 'invalid token '+ str(user.level)+" "+ str(user.email)) 

       return f(user=user, *args, **kwargs)
   return decorator