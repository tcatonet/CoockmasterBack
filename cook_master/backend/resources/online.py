# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

from flask import Blueprint


app_online = Blueprint('online', __name__)


@app_online.route("/online")
def check():
    return "True", 200
 