# BRAIZET Rémi
# Version 3.1

import os
import logging
import secrets

from dotenv import load_dotenv
from distutils.util import strtobool
from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_talisman import Talisman
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

"""
    Initial Configuration of our api
    configuring prod mode if needed
    handling secrets and database location
    
    This is the "mini factory" of our application
"""

if not os.path.exists('custom.env') and not os.path.exists('production.env') and not os.path.exists('develop.env'):
    logging.critical('No environnement file found ! provide either develop, custom or production .env file')
    exit(1)

for env_file in ['custom.env', 'production.env', 'develop.env']:
    if os.path.exists(env_file):
        load_dotenv(env_file)
        break


if os.environ.get('FLASK_ENV') == 'production':
    production = True
else:
    production = False
    
app = Flask(__name__)
#app = APIFlask(__name__, spec_path='/spec')
cors = CORS(app)


app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = bool(strtobool(os.environ.get('MAIL_USE_TLS', 'False')))
app.config['MAIL_USE_SSL'] = bool(strtobool(os.environ.get('MAIL_USE_SSL', 'False')))
app.config['SPEC_FORMAT'] = 'yaml'
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

mail = Mail(app)
docs = FlaskApiSpec(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JSON_AS_ASCII'] = False

host = os.environ.get('FLASK_HOST')
port = os.environ.get('FLASK_PORT')
debug = os.environ.get('DEBUG')

PROD_HOST = '0.0.0.0'
PROD_PORT = 5000

if production == 'True':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.secret_key = secrets.token_urlsafe(16)
    Talisman(app, content_security_policy=None, force_https=True)
    
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.secret_key = 'secret'



