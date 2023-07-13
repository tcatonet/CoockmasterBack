# BRAIZET Rémi
# Version 8.8
# -*- coding: utf-8 -*-

import logging
import signal

from flask_restful import Api
from gevent import pywsgi
from config import app, docs
from flask_jwt import JWT
from sqlalchemy import text

from functools import partial
from resources.map import adv_mapping
from resources.map import app_mapping
from resources.online import app_online
from resources.mail import Mail
from resources.retrieve_password import RetrievePassword

from resources.account.user import UserRegister
from resources.account.adress import UserAdress

from resources.account.login import Login  
from resources.ecommerce.store import StoreProduct
from resources.ecommerce.product import ProductInStore
from resources.ecommerce.product_in_basket import ProductBasket
from resources.ecommerce.basket import UserBasket
from resources.ecommerce.order import UserOrder
from resources.ecommerce.product_categorie import StoreProductCategorie 
from resources.ecommerce.avis import UserAvis


from resources.event.event import UserEvent
from resources.event.room import CompanyRoom
from resources.event.prestataire import CompanyPrestataire
from resources.event.event_categorie import EventCatrgorie
from resources.event.event_subscription import EventSubscription

from resources.content.content_categorie import ContentCatrgorie
from resources.content.aggregate_content import AggregateContent
from resources.content.content import ContentText




from models.user import User  
from utils.global_config import ADMIN_LEVEL

from resources.verification import app_verification, mail_resend
from config import production, host, port, PROD_HOST, PROD_PORT, debug

# TODO might be needed here later on
from security import authenticate, identity

@app.before_first_request
def create_tables():
    from db import db
    db.init_app(app)
    db.create_all()

    user = User(username='admin', email='admin@admin.fr', password='admin',
                level=ADMIN_LEVEL, first_name='admin', last_name='admin', phone='0000000000')
    user.add_to_db()
 
# Adding /auth end point:
jwt = JWT(app, authenticate, identity)

 
# adding resources endpoints
api = Api(app) 

app.register_blueprint(app_online) 
app.register_blueprint(app_mapping)
app.register_blueprint(adv_mapping)  

app.register_blueprint(mail_resend) 
app.register_blueprint(app_verification)


api.add_resource(UserRegister, '/user')
api.add_resource(Mail, '/mail')
api.add_resource(RetrievePassword, '/password/retrieve')

api.add_resource(Login, '/login')  
api.add_resource(StoreProduct, '/store')
api.add_resource(StoreProductCategorie, '/product_catrgorie')
api.add_resource(ProductInStore, '/product') 
api.add_resource(ProductBasket, '/user_basket') 
api.add_resource(UserBasket, '/basket')
api.add_resource(UserOrder, '/user_order')
api.add_resource(UserAdress, '/user_adress')
api.add_resource(UserAvis, '/user_avis')

api.add_resource(CompanyRoom, '/company_room')
api.add_resource(CompanyPrestataire, '/company_prestataire')

api.add_resource(UserEvent, '/event')
api.add_resource(EventCatrgorie, '/event_catrgorie')
api.add_resource(EventSubscription, '/event/subscription')

api.add_resource(ContentCatrgorie, '/content/categorie')
api.add_resource(AggregateContent, '/content/aggregate')
api.add_resource(ContentText, '/content')


docs.register(UserRegister)

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
  