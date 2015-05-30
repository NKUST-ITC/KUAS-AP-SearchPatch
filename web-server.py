# -*- coding: utf-8 -*-

import os
import json
import requests

from lxml import etree
from flask import Flask, render_template, request, session
from flask_cors import *

ap_login_url = "http://140.127.113.231/kuas/perchk.jsp"
fnc_url = "http://140.127.113.231/kuas/fnc.jsp"
query_url = "http://140.127.113.231/kuas/%s_pro/%s.jsp"

RANDOM_ID = "AG009"

LOGIN_TIMEOUT = 5.0
QUERY_TIMEOUT = 5.0
RANDOM_TIMEOUT = 5.0

app = Flask(__name__)
app.config.from_object("config")

def login(session, username, password): #Login ---
    payload = {"uid": username, "pwd": password}
    r = session.post(ap_login_url, data=payload, timeout=LOGIN_TIMEOUT)
    root = etree.HTML(r.text)
    try:
        is_login = not root.xpath("//script")[-1].text.startswith("alert")
    except:
        is_login = False
    return is_login

def query(session, qid=None, args=None): #Query for all type
    payload = {} #New a payload and this will be the post data
    for key in args:
        payload[key] = args[key]
    try:
        r = session.post(query_url % (qid[:2], qid), data=payload, timeout=QUERY_TIMEOUT).content
    except requests.exceptions.ReadTimeout:
        r = ""
    return r

@app.route('/ap/logout', methods=['POST'])
@cross_origin(supports_credentials=True)

def logout():
    session.clear()
    return 'logout'

@app.route('/ap/query', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def query_classroom(): #This is a query for class room
    if request.method == "POST":
        yms_yms = request.form['yms_yms']
        room_id = request.form['room_id']
        s = requests.session()
        login(s, "guest", "123")
        return query(s, "ag302_02", {"yms_yms":yms_yms,"room_id":room_id,"unit_serch":"查 詢"})
    return render_template("query.html")

def query_department(): #This can dump the department list
    if request.method == "POST":
        

def query_class(): #This can query the class
    if request.method == "POST":
        
if __name__ == '__main__':
    app.run(host="127.0.0.1")
