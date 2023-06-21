# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging
import re
import ssl
import jwt
import random
from datetime import datetime, timedelta

from argparse import Namespace
from flask import abort, current_app, request
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from utils.validation import valid_email_regex, valid_phone_regex, send_confirmation_mail, send_update_password_mail, send_update_email_mail, send_delete_account_mail
from config import mail
from resources.verification import token_required
from models.user import User
from models.ecommerce import Basket


class UserRegister(Resource):

    """ Users' endpoint. """
    
    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    email = Namespace(name='email', default="", dest="email", action='store', type=str, case_sensitive=True)
    password = Namespace(name='password', default="", dest="password", action='store', type=str, case_sensitive=True)
    username = Namespace(name='username', default="", dest="username", action='store', type=str, case_sensitive=True)
    firstname = Namespace(name='firstname', default="", dest="firstname", action='store', type=str, case_sensitive=True)
    lastname = Namespace(name='lastname', default="", dest="lastname", action='store', type=str, case_sensitive=True)
    phone = Namespace(name='phone', default="", dest="phone", action='store', type=str, case_sensitive=False)
    code = Namespace(name='code', default="", dest="code", action='store', type=int, case_sensitive=False)


    @staticmethod
    def __required__(arg_namespace):
        local_args_namespace = copy.deepcopy(arg_namespace)
        edit = vars(local_args_namespace)
        edit['required'] = True
        return local_args_namespace


    @staticmethod
    def __optional__(arg_namespace):
        local_args_namespace = copy.deepcopy(arg_namespace)
        edit = vars(local_args_namespace)
        edit['required'] = False
        return local_args_namespace
    

    @token_required
    def get(self, user): 
        """
            Find an user by email

            :param email: email of the user (every users emails are unique)
            :type email: str
            
            if no email is provided, return the current number of users
            :return: user data.
            :rtype: application/json.
        """


        user = User.find_by_email(email=user.email)
        if user:
            response = current_app.response_class(response=json.dumps(user.json()), status=200,
                                                      mimetype='application/json')
            return response
        
        else:    
            abort(404, 'user not found')

 
    def post(self):
        """
            Creates a new item using the provided name, price and store_id.
            :param username: username.
            :type username: str
            :param email: user's email.
            :type email: str
            :param password: the user's password.
            :type password: str
            # :param level: user subscription level.
            # :type level: int
            :param phone: phone.
            :type phone: str
            :param firstname: firstname.
            :type firstname: str
            :param lastname: lastname.
            :type lastname: str
            :return: success or failure message.
            :rtype: application/json response.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.email)))
        parser.add_argument(**vars(self.__required__(self.username)))
        parser.add_argument(**vars(self.__required__(self.password)))
        parser.add_argument(**vars(self.__optional__(self.firstname)))
        parser.add_argument(**vars(self.__optional__(self.lastname)))
        parser.add_argument(**vars(self.__optional__(self.phone)))
        
        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            if not re.match(valid_email_regex, data['email']):
                abort(400, 'invalid email')
            if data['phone'] != '' and not re.match(valid_phone_regex, data['phone']):
                abort(400, 'invalid phone number')
                
            if User.find_by_email(data['email']):
                abort(409, f'An user with the email |{data["email"]}| already exists')

            user = User(username=data['username'], email=data['email'], password=data['password'],
                        level=0, first_name=data['firstname'], last_name=data['lastname'], phone=data['phone'])
 
            try: 
                user.add_to_db()
            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred registering the user')

            try:
                basket_user = Basket(user_id=user.id) 
                basket_user.add_to_db()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the user basket')

            refresh_token = {
                'refresh_token': jwt.encode({'public_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
                }
            refresh_token = jwt.encode({'public_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
            user_json = user.json() 
            user_json['refresh_token'] = refresh_token.decode("utf-8") 
            response = current_app.response_class(response=json.dumps(user_json), status=201,
                                                mimetype='application/json')
            code = random.randint(10000,99999)
            msg = send_confirmation_mail(user.email, code)

            try:
                mail.send(msg)
                keys_to_patch = dict()
                keys_to_patch['code'] = code
                user.patch_in_db(keys_to_patch)

            except ConnectionRefusedError as e:
                current_app.logger.warning('Could not send verification email')
                current_app.logger.warning(e)
            except ssl.SSLError as e:
                current_app.logger.warning(e)
            return response

 
    @token_required 
    def delete(self, user):
        """
        Finds a user by its email and deletes it.
    
        :param email: the email of the user. 
        :type email: str 
        :return: success or failure.
        :rtype: application/json response.
        """ 

        try:
            user.remove_from_db()

        except Exception as e:
            logging.error(e)
            abort(422, 'An error occurred deleting the product')

        else:
            response = current_app.response_class(response=json.dumps(dict(message='user deleted')), status=204, mimetype='application/json')
            msg = send_delete_account_mail(user.email, request.url_root, user.verified)
            
            try:
                mail.send(msg)
            except ConnectionRefusedError as e:
                current_app.logger.warning('Could not send delete account email')
                current_app.logger.warning(e)
            except ssl.SSLError as e:
                current_app.logger.warning(e)
            return response


    @token_required 
    def patch(self, user):
        """
        Finds a user by its email and patches it.
        works for every field expect email
        
        :param any: any field you can specified during user creation.
                    if field is not empty or none, the value will be pacthed
        :type any: many
        :return: success or failure.
        :rtype: application/json response.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__optional__(self.email)))
        parser.add_argument(**vars(self.__optional__(self.username)))
        parser.add_argument(**vars(self.__optional__(self.password)))
        parser.add_argument(**vars(self.__optional__(self.firstname)))
        parser.add_argument(**vars(self.__optional__(self.lastname)))
        parser.add_argument(**vars(self.__optional__(self.phone)))
         
        try:
            data = parser.parse_args()
            del parser 

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
         
        else:
            if not re.match(valid_email_regex, data['email']):
                abort(4 00, 'invalid email')
            if data['phone'] != '' and not re.match(valid_phone_regex, data['phone']):
                abort(400, 'invalid phone number')

            if User.find_by_email(data['email']) and data['email'] != user.email:
                abort(409, f'An user with the email |{data["email"]}| already exists')

            if data['email']: 
                if data['email'] != user.email:
                    msg = send_update_email_mail(user.email, request.url_root, user.verified)
                    try:
                        mail.send(msg)
                    except ConnectionRefusedError as e:
                        current_app.logger.warning('Could not send email verification')
                        current_app.logger.warning(e)
                    except ssl.SSLError as e:
                        current_app.logger.warning(e)

            elif data['password']:
                if data['password'] != user.password:
                    pass
                    msg = send_update_password_mail(user.email, request.url_root, user.verified)
                    try:
                        mail.send(msg)
                    except ConnectionRefusedError as e:
                        current_app.logger.warning('Could not send password verification email')
                        current_app.logger.warning(e)
                    except ssl.SSLError as e:
                        current_app.logger.warning(e)

            data['password']=generate_password_hash(data['password'])

            keys_to_patch = dict()
            for key in data.keys():
                if data[key] and data[key] != '':
                    keys_to_patch[key] = data[key]

            user = User.find_by_email(email=user.email)

            if not user:
                abort(404, dict(message='User could not be found'))

            try:
                user.patch_in_db(keys_to_patch)

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred deleting the product')

            else:
                response = current_app.response_class(response=json.dumps(dict(message='user udpated')), status=204, mimetype='application/json')
                return response
