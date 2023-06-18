import pprint
import logging
import datetime
import os
import pytest
import requests

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

URL = 'http://172.18.0.3:5000/'
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
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 201


    def test_get_all_room(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'company_room')), 
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress'}, 
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
                                json={'city': 'city', 'postcode':'91390', 'adress':'adress'}, 
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
                                    json={'city': 'city', 'postcode':'91390', 'adress':'adress'}, 
                                    headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id = a.json()['id']
        x = requests.patch("".join((URL,'company_room')), 
                                json={'id': id, 'city': 'city22', 'postcode':'91390', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        assert x.status_code == 204


    def test_delete_room(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        
        a = requests.post("".join((URL,'company_room')), 
                                    json={'city': 'city', 'postcode':'91390', 'adress':'adress'}, 
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
                                json={'lastname': 'lastname', 'firstname':'firstname', 'activite':'activite', 'description':'description'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 201


    def test_get_all_prestataire(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'activite':'activite', 'description':'description'}, 
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
                                json={'lastname': 'lastname', 'firstname':'firstname', 'activite':'activite', 'description':'description'}, 
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
        

    def test_update_prestataire(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'company_prestataire')), 
                                json={'lastname': 'lastname', 'firstname':'firstname', 'activite':'activite', 'description':'description'}, 
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
                                    json={'lastname': 'lastname', 'firstname':'firstname', 'activite':'activite', 'description':'description'}, 
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