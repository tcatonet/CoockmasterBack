# BRAIZET Rémi
# Version 1.0

import jwt
import datetime

from flask_restful import Resource, reqparse
from functools import wraps
from flask import request

from models.user import User
from utils.messages import ErrorMessages, InfoMessages
from utils.success_payload_formatter import response_success, response_failure


class Authenticate(Resource):
    """Infrastructure' endpoint."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        'useremail',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        """
       Authentication

        :return: success or failure.
        :rtype: application/json response.
        """
        data = Authenticate.parser.parse_args()

        if api_data_filter_auth.check_data(data):

            user = User.find_by_email_and_password(data['useremail'], data['password'])
            response = None
            if user:
                token = generateToken(data['useremail'], data['password'])
                response = response = response_success(message={'global': InfoMessages.ACCOUNT_AUTHENTICATE_SUCCESS} , refresh_token=token.decode('utf-8'))

            else:
                response = response_failure(message={'global': ErrorMessages.ACCOUNT_AUTHENTICATE_ERROR})

        else:
            response = api_data_filter_auth.response_failure_check_data()


        return response


def generateToken(email, password):
    return jwt.encode({'email': email, 'password': password, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, "klhkhfsfidDhsFGdwVSZkopw", algorithm="HS256") 


def token_required2(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        print("coucou")
        try:
            token = None

            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']
                print("TOKEN")
                print(token)
            else:
                print(" MISSING_TOKEN 1")
                raise Exception(ErrorMessages.MISSING_TOKEN)

            if not token:
                print("MISSING_TOKEN 2")
                raise Exception(ErrorMessages.MISSING_TOKEN)

            try:
                data = jwt.decode(token, "klhkhfsfidDhsFGdwVSZkopw", algorithms=['HS256'])

            except:
                print("not valid")

                raise Exception(ErrorMessages.INVALID_TOKEN)

            current_email = data['email']
            current_password = data['password']
            print(current_email)
            print(current_password)
            user = UserModel.find_by_email_and_password(current_email, current_password)
            refresh_token=""

            if user:
                refresh_token = generateToken(current_email, current_password)
                refresh_token = refresh_token.decode('utf-8')
                print("refresh_token")
                print(refresh_token)
                print("refresh_token")

            else:
                print("not user")

                raise Exception(ErrorMessages.FOUND_ACCOUNT_ERROR)

            if not current_email:
                print("not current_email")

                raise Exception(ErrorMessages.INVALID_TOKEN)

            print("RETURN")
            print(current_email)
            print(current_password)
            print(refresh_token)

        except Exception as e:
            print("222")
            print(e)

            return {
                'message': str(e)
            }, 400

        return f(current_email=current_email, current_password=current_password, refresh_token=refresh_token, *args, **kwargs)
        

def token_required(request):
        try:
            token = None

            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']

            else:
                raise Exception(ErrorMessages.MISSING_TOKEN)

            if not token:
                raise Exception(ErrorMessages.MISSING_TOKEN)

            try:
                data = jwt.decode(token, "klhkhfsfidDhsFGdwVSZkopw", algorithms=['HS256'])

            except:
                raise Exception(ErrorMessages.INVALID_TOKEN)

            current_email = data['email']
            current_password = data['password']
            user = UserModel.find_by_email_and_password(current_email, current_password)
            refresh_token=""

            if user:
                refresh_token = generateToken(current_email, current_password)
                refresh_token = refresh_token.decode('utf-8')

            else:
                raise Exception(ErrorMessages.FOUND_ACCOUNT_ERROR)

            if not current_email:
                raise Exception(ErrorMessages.INVALID_TOKEN)

            payload = {
                "auth_success": True,
                "current_email": current_email,
                "current_password": current_password,
                "refresh_token": refresh_token
            }
            return payload


        except Exception as e:
            print("222")
            print(e)

            return {
                'auth_success': False,
                'message': str(e)
            }



def get_token_required(request):

        try:
            token = None
            request.query_string
            token = request.args['token']
            print(token)
            project_name = request.args['project_name']

            if not token:
                raise Exception(ErrorMessages.MISSING_TOKEN)


            if not project_name:
                raise Exception(ErrorMessages.MISSING_PROJECT_NAME)

            try:
                data = jwt.decode(token, "klhkhfsfidDhsFGdwVSZkopw", algorithms=['HS256'])

            except:
                raise Exception(ErrorMessages.INVALID_TOKEN)

            current_email = data['email']
            current_password = data['password']


            user = UserModel.find_by_email_and_password(current_email, current_password)
            refresh_token=""

            if user:
                refresh_token = generateToken(current_email, current_password)
                refresh_token = refresh_token.decode('utf-8')

            else:
                raise Exception(ErrorMessages.FOUND_ACCOUNT_ERROR)

            if not current_email:
                raise Exception(ErrorMessages.INVALID_TOKEN)


            payload = {
                "auth_success": True,
                "current_email": current_email,
                "current_password": current_password,
                "refresh_token": refresh_token,
                "project_name": project_name
            }
            return payload

        except Exception as e:

            return {
                'auth_success': False,
                'message': str(e)
            }
