# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import copy
import logging
import ssl
import json
import random
import string

from argparse import Namespace 
from resources.verification import token_required, generate_token
from utils.validation import send_confirmation_creation_account
from flask import abort
from flask_restful import Resource, reqparse
from config import mail
from flask import abort, current_app

from models.user import User

from utils.validation import send_retrieve_password_mail
from werkzeug.security import generate_password_hash


class RetrievePassword(Resource):
    """ mailing endpoint. """
    
    email = Namespace(name='email', default="", dest="email", action='store', type=str)

    @staticmethod
    def __required__(arg_namespace):
        local_args_namespace = copy.deepcopy(arg_namespace)
        edit = vars(local_args_namespace)
        edit['required'] = True
        return local_args_namespace

    def post(self): 
        """
        Finds a user by its email and deletes it.
    
        :param email: the email of the user.
        :type email: str
        :return: success or failure.
        :rtype: application/json response.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.email)))

        try:
            data = parser.parse_args()
        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')

        else:
            user = User.find_by_email(email=data['email'])

            if user:
                password=self.generate_password()
                msg = send_retrieve_password_mail(user.email, password)

                try:
                    mail.send(msg) 
                    keys_to_patch = dict()
                    keys_to_patch['password'] = generate_password_hash(password)
                    user.patch_in_db(keys_to_patch) 

                except ConnectionRefusedError as e:
                    current_app.logger.warning('Could not send reset password email')
                    current_app.logger.warning(e)
                except ssl.SSLError as e:
                    current_app.logger.warning(e)

            response = current_app.response_class(response=json.dumps({}), status=200,
                                                mimetype='application/json')
            return response

    

    def generate_password(self):
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits
        special_characters = string.punctuation

        password_characters = []

        # Ajouter une lettre minuscule
        password_characters.append(random.choice(lowercase_letters))

        # Ajouter une lettre majuscule
        password_characters.append(random.choice(uppercase_letters))

        # Ajouter un chiffre
        password_characters.append(random.choice(digits))

        # Ajouter un caractère spécial
        password_characters.append(random.choice(special_characters))

        # Générer le reste des caractères aléatoirement
        for _ in range(6):
            password_characters.append(random.choice(lowercase_letters + uppercase_letters + digits + special_characters))

        # Mélanger les caractères
        random.shuffle(password_characters)

        # Générer le mot de passe final 
        password = ''.join(password_characters)

        return password