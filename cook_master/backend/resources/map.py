# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

from pprint import pformat

from flask import Blueprint
from flask import jsonify
from flask import current_app as app

app_mapping = Blueprint('map', __name__)
adv_mapping = Blueprint('amap', __name__)


@app_mapping.route("/map")
def site_map():
    routes = []
    
    for rule in app.url_map.iter_rules():
        routes.append('%s' % pformat(rule))
        
    routes.sort()
    return jsonify(routes), 200


@adv_mapping.route("/amap")
def site_map():
    routes = []
    
    for rule in app.url_map.iter_rules():
        routes.append('%s' % vars(rule))
    return jsonify(routes), 200
