# BRAIZET Rémi
# Version 8.8
# -*- coding: utf-8 -*-

import logging
import signal

from flask_restful import Api
from gevent import pywsgi
from config import app
from flask_jwt import JWT
 
from functools import partial
from resources.map import adv_mapping
from resources.map import app_mapping
from resources.online import app_online
from resources.user import UserRegister
from resources.mail import Mail
from resources.login import Login
from resources.store import StoreProduct
from resources.product import ProductInStore
from resources.product_in_basket import ProductBasket
from resources.basket import UserBasket
from resources.order import UserOrder
from resources.adress import UserAdress
from resources.room import CompanyRoom
from resources.prestataire import CompanyPrestataire
from resources.categorie import EventCatrgorie
from resources.avis import UserAvis

from resources.verification import app_verification, mail_resend
from config import production, host, port, PROD_HOST, PROD_PORT, debug

# TODO might be needed here later on
from security import authenticate, identity


@app.before_first_request
def create_tables():
    from db import db 
    db.init_app(app)
    db.create_all()
 
 
# Adding /auth end point:
jwt = JWT(app, authenticate, identity)


# adding resources endpoints
api = Api(app) 
app.register_blueprint(app_online) 
app.register_blueprint(app_mapping)
app.register_blueprint(adv_mapping)  

app.register_blueprint(mail_resend) 
app.register_blueprint(app_verification) 

api.add_resource(UserRegister, '/register')
api.add_resource(Mail, '/mail')
api.add_resource(Login, '/login')
api.add_resource(StoreProduct, '/store')
api.add_resource(ProductInStore, '/product')
api.add_resource(ProductBasket, '/user_basket') 
api.add_resource(UserBasket, '/basket')
api.add_resource(UserOrder, '/user_order')
api.add_resource(UserAdress, '/user_adress')
api.add_resource(UserAvis, '/user_avis')
api.add_resource(CompanyRoom, '/company_room')
api.add_resource(CompanyPrestataire, '/company_prestataire')
api.add_resource(EventCatrgorie, '/event_catrgorie')

 
# we choose simply between dev and prod environment 
if production:
    logging.warning('starting production server !') 
 
    log = 'default' if debug else None 
  
    ssl_args = {} 
    import os
    if os.path.exists('server.key') and os.path.exists('server.crt'): 
        ssl_args = {'keyfile': 'server.key',
                    'certfile': 'server.crt'}
     
    listening_at = (PROD_HOST, PROD_PORT)
    server = pywsgi.WSGIServer(listening_at, application=app, log=log, **ssl_args)
  
    def signal_handler(sig, frame):  
        server.close() 
        app.logger.info('\nStopping server')
 
    signal.signal(signal.SIGINT, signal_handler)
 
    server.serve_forever()
    server.close()
else: 
    logging.warning('starting development server !')
      
    # Name is only set to main when file is explicitly run (not on imports):
    if __name__ == "__main__":
        app.run(host=host, port=port, debug=True) 
  