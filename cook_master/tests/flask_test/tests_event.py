import pprint
import logging
import datetime
import os
import pytest
import requests
import json

class Colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

URL = 'http://172.18.0.2:5000/'
TOKEN = ""
EMAIL_ADMIN = 'admin@admin.fr'

EMAIL = 'woyolan595@pixiil.com'
EMAIL2 = 'ofwyiqcq3z3@mail4k.com'
EMAIL3="rehoyi3174@carpetra.com"
EMAIL4="rehoyhi3174@carpetrah.com"
EMAIL5="rehoyhi3175@carpetrah.com"
EMAIL6="rehoyhi3176@carpetrah.com"
EMAIL7="rehoyhi3177@carpetrah.com"
EMAIL8="rehoyhi3178@carpetrah.com"
EMAIL9="rehoyhi3179@carpetrah.com"
EMAIL10="rehoyhi31710@carpetrah.com"
EMAIL11="rehoyhi31711@carpetrah.com"
EMAIL12="rehoyhi317122@carpetrah.com"
EMAIL13="rehoyhi317123@carpetrah.com"
EMAIL14="rehoyhi31714@carpetrah.com"
EMAIL15="rehoyhi31715@carpetrah.com"
EMAIL16="rehoyhi31716@carpetrah.com"
EMAIL17="rehoyhi31717@carpetrah.com"
EMAIL18="rehoyhi31718@carpetrah.com"
EMAIL19="rehoyhi31719@carpetrah.com"
EMAIL20="rehoyhi317120@carpetrah.com"
EMAIL21="rehoyhi317121@carpetrah.com"
EMAIL22="rehoyhi317121@carpetrah.com"
EMAIL23="rehoyhi31723@carpetrah.com"
EMAIL24="rehoyhi3171924@carpetrah.com"
EMAIL25="rehoyhi317125@carpetrah.com"
EMAIL26="rehoyhi317126@carpetrah.com"
EMAIL27="rehoyhi317127@carpetrah.com"


EMAIL28="rehoyhi31728@carpetrah.com"
EMAIL29="rehoyhi31729@carpetrah.com"
EMAIL30="rehoyhi317130@carpetrah.com"
EMAIL31="rehoyhi317131@carpetrah.com"
EMAIL32="rehoyhi317132@carpetrah.com"

class UnitLogger:
    def __init__(self, level=logging.ERROR):
        self.logger = logging.getLogger('Testing')

        # set log level
        self.logger.setLevel(level)

        # define file handler and set formatter
        time_now = datetime.datetime.now().strftime("day %m-%d time %H-%M-%S")
        if not os.path.exists('./logs/'):
            os.mkdir('./logs/')
            
        file_handler = logging.FileHandler(f'./logs/test-logs-{time_now}.log')
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)
        
        # add file handler to logger
        self.logger.addHandler(file_handler)
        
    def log_something(self):
        # Logs
        self.logger.debug('A debug message')
        self.logger.info('An info message')
        self.logger.warning('Something is not right.')
        self.logger.error('A Major error has happened.')
        self.logger.critical('Fatal error. Cannot continue')

    @staticmethod
    def log_test_results(self, rv):
        print(f'{Colors.BLUE}status code{Colors.ENDC}')
        pprint.pprint(rv.status_code)
        print(f'{Colors.GREEN}response message{Colors.ENDC}')
        pprint.pprint(rv.data.decode())


class TestEcommerceApplication:
    #pytest tests.py
    

    def test_create_room(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 201


    def test_get_all_room(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        x = requests.get("".join((URL,'company_room')),
                                json={},
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL27, 'password': 'bonjour'})


    def test_get_room(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.get("".join((URL,'company_room')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200
        
    def test_update_room(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'company_room')), 
                                    json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                    headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id = a.json()['id']
        x = requests.patch("".join((URL,'company_room')), 
                                json={'id': id, 'city': 'city22', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        assert x.status_code == 204


    def test_delete_room(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        
        a = requests.post("".join((URL,'company_room')), 
                                    json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                    headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id = a.json()['id']

        x = requests.delete("".join((URL,'company_room')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 204

    def test_create_prestataire(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'email':EMAIL, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 201


    def test_get_all_prestataire(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'email':EMAIL2, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL15, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL15, 'password': 'bonjour'})
        token = x.json()['token']
        x = requests.get("".join((URL,'company_prestataire')),
                                json={},
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_get_prestataire(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        x = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'email':EMAIL3, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL16, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL16, 'password': 'bonjour'})
        token = x.json()['token']
        x = requests.get("".join((URL,'company_prestataire')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_get_prestataire_with_admin_account(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        x = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'email':EMAIL3, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.get("".join((URL,'company_prestataire')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200
        


    def test_update_prestataire(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'email':EMAIL4, 'activite':'activite', 'description':'description'}, 
                                    headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id = a.json()['id']
        x = requests.patch("".join((URL,'company_prestataire')), 
                                json={'id': id,'lastname': 'lastname2', 'firstname':'firstname', 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        assert x.status_code == 204


    def test_delete_prestataire(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        
        a = requests.post("".join((URL,'company_prestataire')), 
                                    json={'lastname': 'lastname', 'firstname':'firstname', 'email':EMAIL5, 'activite':'activite', 'description':'description'}, 
                                    headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id = a.json()['id']

        x = requests.delete("".join((URL,'company_prestataire')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 204

    
    def test_create_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 201



    def test_get_all_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        x = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': False, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL2, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL2, 'password': 'bonjour'})
        token = x.json()['token']


        x = requests.get("".join((URL,'event_catrgorie')),
                                json={},
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_get_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        x = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']


        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL3, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL3, 'password': 'bonjour'})
        token = x.json()['token']



        x = requests.get("".join((URL,'event_catrgorie')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200
        

    def test_delete_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        
        a = requests.post("".join((URL,'event_catrgorie')), 
                                    json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                    headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id = a.json()['id']

        x = requests.delete("".join((URL,'event_catrgorie')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 203


    def test_create_event(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        catego = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idcatego = catego.json()['id']

        presta1 = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'email':EMAIL6, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta1 = presta1.json()['id']

        room = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom = room.json()['id']

        event = requests.post("".join((URL,'event')), 
                                json={'date_start': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'date_end': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'name': 'test_create_event', 'description':'test_create_event', 'categorie_id':idcatego, 'prestataire_id': [idpresta1], 'room_id': [idroom]}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        assert event.status_code == 201


    def test_create_event_with_presta_list(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        catego = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idcatego = catego.json()['id']

        presta1 = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'test_create_event_with_presta_list1', 'email':EMAIL7, 'firstname':'firstname', 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta1 = presta1.json()['id']

        presta2 = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'test_create_event_with_presta_list2', 'email':EMAIL8, 'firstname':'firstname', 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta2 = presta2.json()['id']
    
        room = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom = room.json()['id']

        event = requests.post("".join((URL,'event')), 
                                json={'date_start': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'date_end': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'name': 'test_create_event_with_presta_list', 'description':'test_create_event_with_presta_list', 'categorie_id':idcatego, 'prestataire_id': [idpresta1, idpresta2], 'room_id': [idroom]}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        assert event.status_code == 201


    def test_create_event_with_multiple_room(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        catego = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idcatego = catego.json()['id']

        presta1 = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'email':EMAIL9, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta1 = presta1.json()['id']

        room1 = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city1', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom1 = room1.json()['id']

        room2 = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city2', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom2 = room2.json()['id']

        event = requests.post("".join((URL,'event')), 
                                json={'date_start': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'date_end': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'name': 'test_create_event_with_multiple_room', 'description':'test_create_event', 'categorie_id':idcatego, 'prestataire_id': [idpresta1], 'room_id': [idroom1, idroom2]}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        assert event.status_code == 201


    def test_get_event(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        catego = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idcatego = catego.json()['id']

        presta = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'email':EMAIL10, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta = presta.json()['id']

        room = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom = room.json()['id']

        event = requests.post("".join((URL,'event')), 
                                json={'date_start': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'date_end': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'name': 'test_get_event', 'description':'test_get_event', 'categorie_id':idcatego, 'prestataire_id': [idpresta], 'room_id': [idroom]}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        event_id=event.json()['id']

        event = requests.get("".join((URL,'event')), 
                                json={'id': event_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert event.status_code == 200


    def test_delete_event(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        catego = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idcatego = catego.json()['id']

        presta = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'test_delete_event', 'firstname':'test_delete_event', 'email':EMAIL11, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta = presta.json()['id']

        room = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom = room.json()['id']

        event = requests.post("".join((URL,'event')),
                                json={'date_start': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'date_end': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'name': 'test_delete_event', 'description':'test_delete_event', 'categorie_id':idcatego, 'prestataire_id': [idpresta], 'room_id': [idroom]}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        event_id=event.json()['id']

        event = requests.get("".join((URL,'event')), 
                               json={'id': event_id}, 
                               headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        event_id=event.json()['id']

        event = requests.delete("".join((URL,'event')), 
                               json={'id': event_id}, 
                               headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        
        assert event.status_code == 204


    def test_patch_event(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        catego = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idcatego = catego.json()['id']

        presta = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'test_patch_event', 'firstname':'test_patch_event', 'email':EMAIL12, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta = presta.json()['id']

        presta2 = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'test_create_event_with_presta_list2', 'firstname':'firstname', 'email':EMAIL13, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta2 = presta2.json()['id']

        room = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom = room.json()['id']

        event = requests.post("".join((URL,'event')),
                                json={'date_start': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'date_end': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'name': 'test_patch_event', 'description':'test_patch_event', 'categorie_id':idcatego, 'prestataire_id': [idpresta], 'room_id': [idroom]}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        event_id=event.json()['id']

        event = requests.get("".join((URL,'event')), 
                               json={'id': event_id}, 
                               headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        event_id=event.json()['id']

        event = requests.patch("".join((URL,'event')), 
                               json={'id': event_id, 'prestataire_id':[idpresta, idpresta2], 'room_id': [idroom]}, 
                               headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        
        assert event.status_code == 201





    def test_subscribe_event(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        catego = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idcatego = catego.json()['id']

        presta1 = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'test_subscribe_event', 'firstname':'firstname', 'email':EMAIL6, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta1 = presta1.json()['id']

        room = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom = room.json()['id']

        event = requests.post("".join((URL,'event')), 
                                json={'date_start': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'date_end': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'name': 'test_subscribe_event', 'description':'test_subscribe_event', 'categorie_id':idcatego, 'prestataire_id': [idpresta1], 'room_id': [idroom], 'access': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idevent = event.json()['id']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL32, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL32, 'password': 'bonjour'})
        token = x.json()['token']

        event_sub = requests.post("".join((URL,'event/subscription')), 
                                json={'event_id': idevent}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        assert event_sub.status_code == 201


    def test_get_subscribe_event(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        catego = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idcatego = catego.json()['id']

        presta1 = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'test_get_subscribe_event', 'firstname':'firstname', 'email':EMAIL6, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta1 = presta1.json()['id']

        room = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom = room.json()['id']

        event = requests.post("".join((URL,'event')), 
                                json={'date_start': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'date_end': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'name': 'test_get_subscribe_event', 'description':'test_subscribe_event', 'categorie_id':idcatego, 'prestataire_id': [idpresta1], 'room_id': [idroom], 'access': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idevent = event.json()['id']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL31, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL31, 'password': 'bonjour'})
        token = x.json()['token']

        event_sub = requests.post("".join((URL,'event/subscription')), 
                                json={'event_id': idevent}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = event_sub.json()['id']

        event_sub = requests.get("".join((URL,'event/subscription')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert event_sub.status_code == 200


    def test_delete_subscribe_event(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        catego = requests.post("".join((URL,'event_catrgorie')), 
                                json={'room_mandatory': True, 'prestataire_mandatory': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idcatego = catego.json()['id']

        presta1 = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'test_delete_subscribe_event', 'firstname':'firstname', 'email':EMAIL6, 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        idpresta1 = presta1.json()['id']

        room = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress', 'capacity': 10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idroom = room.json()['id']

        event = requests.post("".join((URL,'event')), 
                                json={'date_start': str(datetime.datetime.now().strftime("%Y-%m-%d %H")),'date_end': str(datetime.datetime.now().strftime("%Y-%m-%d %H")), 'name': 'test_delete_subscribe_event', 'description':'test_subscribe_event', 'categorie_id':idcatego, 'prestataire_id': [idpresta1], 'room_id': [idroom], 'access': True}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        idevent = event.json()['id']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL30, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL30, 'password': 'bonjour'})
        token = x.json()['token']

        event_sub = requests.post("".join((URL,'event/subscription')), 
                                json={'event_id': idevent}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        id = event_sub.json()['id']


        event_sub = requests.delete("".join((URL,'event/subscription')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert event_sub.status_code == 201
