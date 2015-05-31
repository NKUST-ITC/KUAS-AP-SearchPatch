# -*- coding: utf-8 -*-

import os
import json
import requests
import kuas.ap as ap
import kuas.parse as parse
from lxml import etree
from flask import Flask, render_template, request, session
from flask_cors import *

ap_login_url = "http://140.127.113.231/kuas/perchk.jsp"
fnc_url = "http://140.127.113.231/kuas/fnc.jsp"
query_url = "http://140.127.113.231/kuas/%s_pro/%s.jsp"

LOGIN_TIMEOUT = 5.0
QUERY_TIMEOUT = 5.0
RANDOM_TIMEOUT = 5.0

app = Flask(__name__)
app.config.from_object("config")

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
        ap.login(s, "guest", "123")
        response = parse.course(ap.query(s, "ag302_02", {"yms_yms":yms_yms,"room_id":room_id,"unit_serch":"查 詢"}))
        return json.dumps(response[0])
    return render_template("query.html")

@app.route('/ap/query_class', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def query_department(): #This can dump the department list
    if request.method == "POST":
        yms_yms = request.form['yms_yms']
        arg = request.form['class_id']
        arg01 = yms_yms.split('#')[0]
        arg02 = yms_yms.split('#')[1]
        s = requests.session()
        ap.login(s, "guest", "123")
        response = parse.course(ap.query(s, "ag304_03", {"arg01": arg01, "arg02": arg02, "arg": arg}))
        return json.dumps(response[0])
    return render_template("query_class.html")

@app.route('/ap/query_Teacher', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def query_Teacher(): #This is the backend query Teacher
    if request.method == "POST":
        yms_yms = request.form['yms_yms'] # Sememster
        tea_num = request.form['Teacher_Number']
        tid = TeacherData[tea_num]
        tid = tid.replace('\n', '')
        s = requests.session()
        ap.login(s, "guest", "123")
        response = parse.course(ap.query(s, "ag300_02", {"yms_yms": yms_yms, "tea_str1": tid}))
        return json.dumps(response[0])
    return render_template("query_teacher.html")
    
if __name__ == '__main__':
    TeacherData = dict()
    with open('BackEndData', 'r') as fp:
        for line in fp:
            num = line.split('#')[0]
            ID = line.split('#')[1]
            TeacherData[num] = ID
    app.run(host="127.0.0.1")
