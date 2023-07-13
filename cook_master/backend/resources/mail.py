# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import copy
import logging
import ssl
import json

from argparse import Namespace 
from resources.verification import token_required, generate_token
from utils.validation import send_confirmation_creation_account
from flask import abort
from flask_restful import Resource, reqparse
from config import mail
from flask import abort, current_app

from models.user import User


class Mail(Resource):
    """ mailing endpoint. """
    
    code = Namespace(name='code', default="", dest="code", action='store', type=int, case_sensitive=False)

    @staticmethod
    def __required__(arg_namespace):
        local_args_namespace = copy.deepcopy(arg_namespace)
        edit = vars(local_args_namespace)
        edit['required'] = True
        return local_args_namespace
    

    @token_required    
    def post(self, user):
        """
        Finds a user by its email and deletes it.
    
        :param email: the email of the user.
        :type email: str
        :return: success or failure.
        :rtype: application/json response.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.code)))

        try:
            data = parser.parse_args()
        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
            
        if data['code'] == user.code:
            response = current_app.response_class(response=json.dumps({'refresh_token': generate_token(user=user).decode("utf-8")}), status=200,mimetype='application/json')
            msg = send_confirmation_creation_account(user.email)
            keys_to_patch = dict()
            keys_to_patch['email_validate'] = True
            keys_to_patch['level'] = 10

            user.patch_in_db(keys_to_patch)
            user = User.find_by_email(email=user.email)
            if not user:
                abort(404, dict(message='User could not be found'))

            try: 
                user.patch_in_db(keys_to_patch) 
                mail.send(msg)
            except ConnectionRefusedError as e:
                current_app.logger.warning('Could not send delete account email')
                current_app.logger.warning(e)
            except ssl.SSLError as e:  
                current_app.logger.warning(e)

            return response  
            
        else:
            res = "Wrong code "+str(self.code) + "  |" +  str(user.code)
            response = current_app.response_class(response=res, status=404,mimetype='application/json')
            return response 
