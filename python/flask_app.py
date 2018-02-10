# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, redirect
import os
import base64

import json
import requests
import vk, cgi
from flask import session
import news
from apiModule import *

from flask import Flask

import sys
sys.path.append('')
from AppIm import *
from DeleteMessages import *
from DeleteDialog import *
from GetChat import *
from GetMessages import *
from ImSearch import *
from GetMessages import *
from GetHistoryAttachments import *
from ChatActions import *


app = Flask(__name__)
app.config["DEBUG"] = True

app.register_blueprint(app_im)

app.register_blueprint(app_im_del_messages)
app.register_blueprint(app_im_del_dialog)
app.register_blueprint(app_im_get_chat)
app.register_blueprint(app_im_get_messages)
app.register_blueprint(app_im_search)
app.register_blueprint(app_im_get_attachments)
app.register_blueprint(app_im_chat_actions)


MAX_FILE_SIZE = 1024 * 1024 + 1


@app.before_request
def make_session_permanent():
    session.permanent = True
    #app.permanent_session_lifetime = timedelta(minutes=5)


#@app.route('/', defaults={'path': ''})
#@app.route('/<path:path>')
@app.route('/')
def index():
    api = None
    try:
        api = getApi()
    except:
        pass
    if api is None:
        return redirect(url_for('login'))
    return render_template("index.html")




@app.route('/login')
def login():
    api = None
    try:
        api = getApi()
    except:
        pass
    if api is None:
        return render_template("login.html")
    return redirect(url_for('index'))


@app.route('/auth',methods=["GET", "POST"])
def oauth():
    #try:
        import auth
        api = None
        try:
            api = getApi()
        except:
            ''''''
        if api is not None:
            return redirect(url_for('index',logginned=1))
        import json,sys
        try:
            if request.method == "POST":
                form = request.form
                session["login"] = form["email"]
                session["password"] = form["password"]
        except Exception:
            return "err"
        except:
            error = "Authentication error. Please, check your email and password 1"
            return "login_failed_1"
        api = getApi()
        if api is None:
            error = "Authentication error. Please, check your email and password 2"
            try:
                del apiArray[session['login']]
            except:
                pass
            try:
                api = getApi()
                if api is None:
                    return "error"
                return redirect(url_for('index'),logginned=1)
            except:
                return "fatal_error"
            return "login_failed_2"
        return "login_success"\




@app.route('/execute',methods=["GET","POST"])
def execute():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    startLongPolling = 0
    ts = 0
    try:
        if request.method == "GET":
            startLongPolling = int(request.args.get('startLongPolling'))
            ts = int(request.args.get('ts'))
    except Exception:
        pass
    dlgsOffset = 0
    try:
        if request.method == "GET":
            dlgsOffset = int(request.args.get('dialogsOffset'))
    except Exception:
        pass
    if api is None:
        error = "Authentication error"
        return render_template("index.html",errors=error)
    import execute as e
    import json
    code = ""
    if startLongPolling == 1:
        code = 'var a = API.messages.getLongPollServer({"need_pts": 1}); return a;'
        r = e.execute(a=api,c=code)
        session["lpserver"] = str(r["server"])
        session["lpkey"] = str(r["key"])
        session["lpts"] = str(r["ts"])
        url = "https://" + str(r["server"]) + "?act=a_check&key=" + str(r["key"]) + "&ts=" + str(r["ts"]) +"&wait=25&mode=2&version=2";
        quotes = requests.get(url)
        contents_file = quotes.text
        return str(contents_file)
    elif startLongPolling == 2:
        ts = session["lpts"]
        try:
            if request.method == "GET":
                ts = int(request.args.get('ts'))
        except Exception:
            pass
        session["lpts"] = ts
        url = "https://" + session["lpserver"] + "?act=a_check&key=" + session["lpkey"] + "&ts=" + str(ts) +"&wait=25&mode=2&version=2";
        quotes = requests.get(url)
        contents_file = quotes.text
        return str(contents_file)
    else:
        code = ''
        if dlgsOffset == 0:
            code = 'API.stats.trackVisitor();'
        code += ' var c = API.messages.getDialogs({"offset":' + str(dlgsOffset) + '}); var b = API.users.get({"user_ids": c@.uid,"fields": "photo_50,online"}); var ids = c@.uid; var i=0; var arr=[]; while(ids.length>i){  if (ids[i]<0){ arr.push( parseInt(ids[i])/-1 ); }; i = i+1; }  ; var gr = API.groups.getById({"group_ids": arr}); var a = API.users.get({"fields": "photo_50"}); return {"msgs": c,"users":b,"me": a,"groups": gr};'
    r = e.execute(a=api,c=code)
    if startLongPolling == 1:
        pass
    return json.dumps(r)


@app.route('/logout',methods=["GET"])
def logout():
    try:
        apiArray.pop(session["login"])
    except:
        pass
    try:
        session.pop('login', None)
    except:
        pass
    return redirect(url_for('index'))