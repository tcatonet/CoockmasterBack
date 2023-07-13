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

EMAIL33="rehoyhi317133@carpetrah.com"
EMAIL34="rehoyhi317134@carpetrah.com"
EMAIL35="rehoyhi317135@carpetrah.com"
EMAIL36="rehoyhi317136@carpetrah.com"
EMAIL37="rehoyhi317137@carpetrah.com"
EMAIL38="rehoyhi317138@carpetrah.com"
EMAIL39="rehoyhi317139@carpetrah.com"
EMAIL40="rehoyhi317140@carpetrah.com"
EMAIL41="rehoyhi317141@carpetrah.com"
EMAIL42="rehoyhi317142@carpetrah.com"

EMAIL43="rehoyhi317143@carpetrah.com"
EMAIL44="rehoyhi317144@carpetrah.com"
EMAIL45="rehoyhi317145@carpetrah.com"

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

    def test_admin_login(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        assert x.status_code == 201

    def test_create_store(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'store')), 
                          json={'name': 'test_create_store'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        assert x.status_code == 201

    def test_create_store_with_existing_name(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'store')), 
                          json={'name': 'test_create_store'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        assert x.status_code == 422

    def test_create_product(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        x = requests.post("".join((URL,'store')), 
                          json={'name': 'test_create_product'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        y = requests.post("".join((URL,'product')), 
                        json={'store_id': x.json()['id'], 'name': 'name product test', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                        headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        assert x.status_code == 201

    def test_create_product_with_existing_name(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        x = requests.post("".join((URL,'store')), 
                        json={'name': 'test_create_product_with_existing_name'},
                        headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                        )
                
        x = requests.post("".join((URL,'product')), 
                        json={'store_id': x.json()['id'],'name': 'name product test', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                        headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                        )
        
        assert x.status_code == 422

    def test_get_existing_product(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        x = requests.post("".join((URL,'store')), 
                          json={'name': 'test_get_existing_product'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        p = requests.post("".join((URL,'product')), 
                        json={'store_id': x.json()['id'], 'name': 'name product test2221', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                        headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                        ) 
        id1 = p.json()['id']

        x = requests.get("".join((URL,'product')), json={'id': id1})
        assert x.status_code == 200




    def test_get_non_existing_product(self):
        x = requests.get("".join((URL,'product')), json={'id': -1})
        assert x.status_code == 405

    def test_delete_product(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        x = requests.post("".join((URL,'store')), 
                          json={'name': 'test_delete_product'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'product')), 
                        json={'store_id': x.json()['id'], 'name': 'test_delete_product', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                        headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                        )
        
        
        x = requests.delete("".join((URL,'product')), 
                        json={'name': 'test_delete_product'},
                        headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        
        assert x.status_code == 204

    def test_delete_non_existing_product(self):
        
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        x = requests.post("".join((URL,'store')), 
                          json={'name': 'test_delete_non_existing_product'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'product')), 
                        json={'store_id': x.json()['id'], 'name': 'test_delete_non_existing_product', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                        headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.delete("".join((URL,'product')), json={'name': 'test_delete_non_existing_product'})
        x = requests.delete("".join((URL,'product')), json={'name': 'test_delete_non_existing_product'})
        assert x.status_code == 405


    def test_update_product(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']
        
        x = requests.post("".join((URL,'store')), 
                              json={'name': 'test_update_product'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'product')), 
                        json={'store_id': x.json()['id'],'name': 'test_update_product', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                        headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                        )
        
        name = x.json()['name']
        y = requests.patch("".join((URL,'product')),
                        json={'name': name},
                        headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                           )
        
        assert y.status_code == 204


    def test_create_product_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'product_catrgorie')), 
                          json={'name': 'test_create_product_categorie'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        assert x.status_code == 201
    
    def test_get_product_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'product_catrgorie')), 
                          json={'name': 'test_get_product_categorie'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id=x.json()['id']
        y = requests.get("".join((URL,'product_catrgorie')), json={'id': id})
        assert y.status_code == 200

    
    def test_get_product_categorie_mult(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'product_catrgorie')), 
                          json={'name': 'test_get_product_categorie_mult1'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product_catrgorie')), 
                          json={'name': 'test_get_product_categorie_mult2'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        y = requests.get("".join((URL,'product_catrgorie')), json={})
        assert y.status_code == 200


    def test_add_product_to_product_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'store')), 
                          json={'name': 'test_add_product_to_product_categorie'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id_store=x.json()['id']
        x = requests.post("".join((URL,'product_catrgorie')), json={'name': 'test_add_product_to_product_categorie'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id_categorie=x.json()['id']
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': id_store, 'product_categorie_id': id_categorie,'name': 'test_add_product_to_product_categorie', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 201


    def test_get_product_store(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'store')), 
                          json={'name': 'test_get_product_store'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'name': 'name product test88', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'name': 'name product test99', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store', 'page': 1})
        assert x.status_code == 200
        

    def test_get_product_store_wrong_page(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'store')), json={'name': 'test_get_product_store_wrong_page'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'name': 'name product test288', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'name': 'name product test299', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store', 'page': -1})
        message = x.json()['message']
        assert message == 'Wrong page number' and x.status_code == 400

    def test_get_product_store_wrong_min_price(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'store')), json={'name': 'test_get_product_store_wrong_min_price'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'name': 'name product test388', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'name': 'name product test399', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store', 'page': 1, 'min_price':-1, 'max_price':100 })
        message = x.json()['message']
        
        assert message == 'Wrong price' and x.status_code == 400

    def test_get_product_store_wrong_max_price(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'store')), json={'name': 'test_get_product_store_wrong_max_price'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), json={'store_id': a.json()['id'], 'name': 'name product 4test88', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), json={'store_id': a.json()['id'], 'name': 'name product 4test99', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store', 'page': 1, 'min_price':10, 'max_price':-1 })
        message = x.json()['message']
        assert message == 'Wrong price' and x.status_code == 400

    def test_get_product_store_wrong_min_price_max_price(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'store')), 
                          json={'name': 'test_get_product_store_wrong_min_price_max_price'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'name': 'name product 5test88', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'name': 'name product 5test99', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store', 'page': 1, 'min_price':10, 'max_price':5 })
        message = x.json()['message']
        assert message == 'Wrong price' and x.status_code == 400

    def test_get_product_store_with_categorie_filter(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'store')), 
                          json={'name': 'test_get_product_store_with_categorie_filter'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        cat = requests.post("".join((URL,'product_catrgorie')), 
                            json={'name': 'test_get_product_store_with_categorie_filter1'},
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id_categorie=cat.json()['id']

        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_categorie_filter1', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_categorie_filter2', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        cat2 = requests.post("".join((URL,'product_catrgorie')), 
                              json={'name': 'test_get_product_store_with_categorie_filter2'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                             )
        id_categorie2=cat2.json()['id']
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie2, 'name': 'test_get_product_store_with_categorie_filter3', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.get("".join((URL,'store')), json={'product_categorie_id': id_categorie,'name': 'test_get_product_store_with_categorie_filter', 'page': 1, })
        assert x.status_code == 200



    def test_get_product_store_with_price_filter(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'store')), 
                          json={'name': 'test_get_product_store_with_price_filter'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        cat = requests.post("".join((URL,'product_catrgorie')), 
                            json={'name': 'test_get_product_store_with_price_filter'},
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        
        id_categorie=cat.json()['id']
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_filter1', 'description': 'description product test', 'stock': 100, 'prix': 10},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_filter2', 'description': 'description product test', 'stock': 100, 'prix': 11},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_filter3', 'description': 'description product test', 'stock': 100, 'prix': 13},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_filter4', 'description': 'description product test', 'stock': 100, 'prix': 15},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_filter5', 'description': 'description product test', 'stock': 100, 'prix': 17},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store_with_price_filter', 'page': 1, 'min_price': 11,'max_price': 15})

        assert x.text == '{"products": [{"id": 20, "product_categorie_id": 8, "note": null, "name": "test_get_product_store_with_price_filter2", "description": "description product test", "stock": 100, "prix": 11.0}, {"id": 21, "product_categorie_id": 8, "note": null, "name": "test_get_product_store_with_price_filter3", "description": "description product test", "stock": 100, "prix": 13.0}, {"id": 22, "product_categorie_id": 8, "note": null, "name": "test_get_product_store_with_price_filter4", "description": "description product test", "stock": 100, "prix": 15.0}]}'\
        and x.status_code == 200


    def test_get_product_store_with_price_min_filter(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'store')), 
                              json={'name': 'test_get_product_store_with_price_min_filter'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                        )
        
        cat = requests.post("".join((URL,'product_catrgorie')), json={'name': 'test_get_product_store_with_price_min_filter'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id_categorie=cat.json()['id']
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_min_filter1', 'description': 'description product test', 'stock': 100, 'prix': 10},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_min_filter2', 'description': 'description product test', 'stock': 100, 'prix': 11},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_min_filter3', 'description': 'description product test', 'stock': 100, 'prix': 13},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_min_filter4', 'description': 'description product test', 'stock': 100, 'prix': 15},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_min_filter5', 'description': 'description product test', 'stock': 100, 'prix': 17},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store_with_price_min_filter', 'page': 1, 'min_price': 11},)
        assert x.text == '{"products": [{"id": 25, "product_categorie_id": 9, "note": null, "name": "test_get_product_store_with_price_min_filter2", "description": "description product test", "stock": 100, "prix": 11.0}, {"id": 26, "product_categorie_id": 9, "note": null, "name": "test_get_product_store_with_price_min_filter3", "description": "description product test", "stock": 100, "prix": 13.0}, {"id": 27, "product_categorie_id": 9, "note": null, "name": "test_get_product_store_with_price_min_filter4", "description": "description product test", "stock": 100, "prix": 15.0}, {"id": 28, "product_categorie_id": 9, "note": null, "name": "test_get_product_store_with_price_min_filter5", "description": "description product test", "stock": 100, "prix": 17.0}]}'\
        and x.status_code == 200


    def test_get_product_store_with_price_max_filter(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        a = requests.post("".join((URL,'store')), 
                          json={'name': 'test_get_product_store_with_price_max_filter'},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        cat = requests.post("".join((URL,'product_catrgorie')), 
                              json={'name': 'test_get_product_store_with_price_max_filter'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id_categorie=cat.json()['id']
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_max_filter1', 'description': 'description product test', 'stock': 100, 'prix': 10},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_max_filter2', 'description': 'description product test', 'stock': 100, 'prix': 11},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_max_filter3', 'description': 'description product test', 'stock': 100, 'prix': 13},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_max_filter4', 'description': 'description product test', 'stock': 100, 'prix': 15},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'product')), 
                          json={'store_id': a.json()['id'], 'product_categorie_id': id_categorie, 'name': 'test_get_product_store_with_price_max_filter5', 'description': 'description product test', 'stock': 100, 'prix': 17},
                          headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store_with_price_max_filter', 'page': 1, 'max_price': 15})

        assert x.text == '{"products": [{"id": 29, "product_categorie_id": 10, "note": null, "name": "test_get_product_store_with_price_max_filter1", "description": "description product test", "stock": 100, "prix": 10.0}, {"id": 30, "product_categorie_id": 10, "note": null, "name": "test_get_product_store_with_price_max_filter2", "description": "description product test", "stock": 100, "prix": 11.0}, {"id": 31, "product_categorie_id": 10, "note": null, "name": "test_get_product_store_with_price_max_filter3", "description": "description product test", "stock": 100, "prix": 13.0}, {"id": 32, "product_categorie_id": 10, "note": null, "name": "test_get_product_store_with_price_max_filter4", "description": "description product test", "stock": 100, "prix": 15.0}]}'\
        and x.status_code == 200


    def test_get_product_store_with_note_filter(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL43, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL43, 'password': 'bonjour'})
        token = x.json()['token']

        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_get_product_store_with_note_filter', 'page':1},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_get_product_store_with_note_filter1', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'comentary', 'note': 5}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL44, 'password': 'bonjour', 'username': 'bono'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL44, 'password': 'bonjour'})
        token = x.json()['token']
        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_get_product_store_with_note_filter2', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']
        
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city3', 'postcode':'postcode3', 'adress':'adress3'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'c kool', 'note': 9}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_get_product_store_with_note_filter3', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )    
            
        id1 = p1.json()['id']
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL45, 'password': 'bonjour', 'username': 'bono'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL45, 'password': 'bonjour'})
        token = x.json()['token']
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city3', 'postcode':'postcode3', 'adress':'adress3'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']
        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']
        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']
      
        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'c pas kool', 'note': 3}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store_with_note_filter', 'page': 1, 'note_min': 5})

        assert x.text == '{"products": [{"id": 35, "product_categorie_id": 0, "note": 9.0, "name": "test_get_product_store_with_note_filter2", "description": "description product test", "stock": 98, "prix": 99.99}, {"id": 34, "product_categorie_id": 0, "note": 5.0, "name": "test_get_product_store_with_note_filter1", "description": "description product test", "stock": 98, "prix": 99.99}]}'\
           and x.status_code == 200
        

    def test_add_product_to_basket(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL2, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL2, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_add_product_to_basket'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_add_product_to_basket1', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )

        id1 = p1.json()['id']

        p1 = requests.get("".join((URL,'product')), json={'id': id1})

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        assert x.status_code == 201


    def test_get_all_product_from_basket(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_get_all_product_from_basket'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_get_all_product_from_basket1', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        p2 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_get_all_product_from_basket2', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )
        p3 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_get_all_product_from_basket3', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )

        id1 = p1.json()['id']
        id2 = p2.json()['id']
        id3 = p3.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id3, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.get("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )                              

        assert x.status_code == 200


    def test_delete_all_product_from_basket(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL3, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL3, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_delete_all_product_from_basket'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_delete_all_product_from_basket1', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        p2 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_delete_all_product_from_basket2', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )
        p3 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_delete_all_product_from_basket3', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )

        id1 = p1.json()['id']
        id2 = p2.json()['id']
        id3 = p3.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id3, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        x = requests.delete("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        assert x.status_code == 200



    def test_update_product_from_basket(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL4, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL4, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_update_product_from_basket'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_update_product_from_basket', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id1 = x.json()['id']

        x = requests.patch("".join((URL,'user_basket')), 
                                json={'id': id1, 'quantity':10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_calculate_price_update_product_from_basket(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL16, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL16, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_calculate_price_update_product_from_basket'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_calculate_price_update_product_from_basket', 'description': 'description product test', 'stock': 100, 'prix': 7},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id1 = x.json()['id']

        x = requests.patch("".join((URL,'user_basket')), 
                                json={'id': id1, 'quantity':7}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        prix = x.json()['prix']

        assert prix == 49.0 and x.status_code == 201


    def test_delete_product_from_basket(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL5, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL5, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_delete_product_from_basket'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_delete_product_from_basket', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id1 = x.json()['id']

        x = requests.delete("".join((URL,'user_basket')), 
                                json={'id': id1}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        x = requests.get("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_create_order(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL6, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL6, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_create_order'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}

                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_create_order', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        x = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_calculate_create_order(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL17, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL17, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_calculate_create_order'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_calculate_create_order', 'description': 'description product test', 'stock': 100, 'prix': 7},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        p2 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_calculate_create_order2', 'description': 'description product test', 'stock': 100, 'prix': 10},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id2 = p2.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':7}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':3}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        x = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        prix = x.json()['prix']
        assert x.status_code == 200 and prix == 79
        

    def test_create_order_with_empty_basket(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL15, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL15, 'password': 'bonjour'})
        token = x.json()['token']
        
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_create_order_with_empty_basket'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )
        p1 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_create_order_with_empty_basket', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']
        x = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 400


    def test_create_order_with_wrong_quantity(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_create_order_with_wrong_quantity'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )
        p1 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_create_order_with_wrong_quantity', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL13, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL13, 'password': 'bonjour'})
        token = x.json()['token']

        u2 = requests.post("".join((URL,'register')), json={'email': EMAIL14, 'password': 'bonjour', 'username': 'gérard'})
        y = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL14, 'password': 'bonjour'})
        token2 = x.json()['token']

        o = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':70}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        o = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':70}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token2}
                          )
        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        x = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        x = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token2}
                          )
        assert x.status_code == 400


    def test_get_order(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL7, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL7, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_get_order'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_get_order', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']

        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200
    

    def test_get_orders(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL8, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL8, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_get_orders'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
    
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_get_orders', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']
        p2 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_get_orders2', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id2 = p2.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']
    
        x = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']
        t = requests.post("".join((URL,'user_order')),
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': None}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_cancel_orders(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']
        
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL9, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL9, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_cancel_orders'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_cancel_orders', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']
        p2 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_cancel_orders2', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id2 = p2.json()['id']

        x = requests.post("".join((URL,'user_basket')),   
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        x = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        id = x.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        id = x.json()['id']

        x = requests.delete("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        

        assert x.status_code == 200


    def test_update_orders(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL10, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL10, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_update_orders'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_update_orders', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']
        p2 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_update_orders2', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id2 = p2.json()['id']

        x = requests.post("".join((URL,'user_basket')),   
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']
        
        x = requests.post("".join((URL,'user_order')), 
                               json={'adress_id': adress_id}, 
                               headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )

        id = x.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                               json={'id': id}, 
                               headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        
        id = x.json()['id']

        x = requests.patch("".join((URL,'user_order')), 
                               json={'id': id, 'status': 'test'}, 
                               headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        
        assert x.status_code == 200


    def test_add_product_to_basket(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL11, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL11, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_add_product_to_basket'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_add_product_to_basket', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 201


    def test_add_product_to_basket_wicth_exceed_quantity(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']


        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL12, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL12, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_add_product_to_basket_wicth_exceed_quantity'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_add_product_to_basket_wicth_exceed_quantity', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )
        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':200}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 400


    def test_create_adress(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL18, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL18, 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 201


    def test_get_all_adress(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL21, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL21, 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        x = requests.get("".join((URL,'user_adress')),
                                json={},
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_get_adress(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL22, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL22, 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.get("".join((URL,'user_adress')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200
        

    def test_update_adress(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL19, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL19, 'password': 'bonjour'})
        token = x.json()['token']

        a = requests.post("".join((URL,'user_adress')), 
                                    json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                    headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id = a.json()['id']
        x = requests.patch("".join((URL,'user_adress')), 
                                json={'id': id, 'city': 'city22', 'postcode':'postcode12', 'adress':'adress'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        assert x.status_code == 204


    def test_delete_adress(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL20, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL20, 'password': 'bonjour'})
        token = x.json()['token']
        
        a = requests.post("".join((URL,'user_adress')), 
                                    json={'city': 'city', 'postcode':'postcode', 'adress':'adress'}, 
                                    headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        id = a.json()['id']

        x = requests.delete("".join((URL,'user_adress')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 204




    def test_post_avis(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL33, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL33, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_post_avis'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}

                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_post_avis', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'comentary', 'note': 5}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        assert x.status_code == 201



    def test_post_avis(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL34, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL34, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_post_avis'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_post_avis', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )
        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']
                           
        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'comentary', 'note': 5}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 201


    def test_post_avis_that_already_exist(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL37, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL37, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_post_avis_that_already_exist'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_post_avis_that_already_exist', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'comentary', 'note': 5}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'comentary good', 'note': 8}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 400


    def test_post_avis_with_wrong_note_1(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL35, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL35, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_post_avis_with_wrong_note_1'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_post_avis_with_wrong_note_1', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'comentary', 'note': -5}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 400




    def test_post_avis_with_wrong_note_2(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL36, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL36, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_post_avis_with_wrong_note_2'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                              json={'store_id': store.json()['id'], 'name': 'test_post_avis_with_wrong_note_2', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']

        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'comentary', 'note': 200}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 400


    def test_get_avis_from_product(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL38, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL38, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_get_avis_from_product'},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_get_avis_from_product', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'comentary', 'note': 5}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL39, 'password': 'bonjour', 'username': 'bono'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL39, 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city3', 'postcode':'postcode3', 'adress':'adress3'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'c kool', 'note': 9}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.get("".join((URL,'product')), json={'id': id1})


        assert x.status_code == 200


    def test_get_note_from_product(self):
        ad = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token_admin = ad.json()['token']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL40, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL40, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), 
                              json={'name': 'test_get_note_from_product', 'page':1},
                              headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                              )

        p1 = requests.post("".join((URL,'product')), 
                           json={'store_id': store.json()['id'], 'name': 'test_get_note_from_product', 'description': 'description product test', 'stock': 100, 'prix': 99.99},
                           headers={'Content-Type': 'Application/json', 'x-access-tokens': token_admin}
                           )        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city2', 'postcode':'postcode2', 'adress':'adress2'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'comentary', 'note': 7}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL41, 'password': 'bonjour', 'username': 'bono'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL41, 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
 
        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city3', 'postcode':'postcode3', 'adress':'adress3'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']

        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']

        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'c kool', 'note': 9}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL42, 'password': 'bonjour', 'username': 'bono'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL42, 'password': 'bonjour'})
        token = x.json()['token']
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'user_adress')), 
                                json={'city': 'city3', 'postcode':'postcode3', 'adress':'adress3'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        adress_id = x.json()['id']
        a = requests.post("".join((URL,'user_order')), 
                                json={'adress_id': adress_id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']
        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['products_in_order'][0]['id']
      
        x = requests.post("".join((URL,'user_avis')), 
                                json={'product_in_order_id': id, 'product_id': id1, 'comentary': 'c pas kool', 'note': 3}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        x = requests.get("".join((URL,'product')), json={'id': id1})
        note = x.json()['note']
        assert note == round((9+3+7)/3,2)