from flask import Blueprint, render_template, session,abort,redirect, request, url_for
from apiModule import *
import json

app_im_del_dialog = Blueprint('app_im_del_dialog',__name__)
@app_im_del_dialog.route('/deleteDialog',methods=["GET","POST"])
def deldlg():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'),loginned=0)
    if api is None:
        error = "Authentication error"
        return render_template("index.html",loginned=0)
    m = None;
    try:
        if request.method == "POST":
            form = request.form
            m = form["id"]
    except Exception:
        return "exception"
    msg = api.messages.deleteDialog(user_id="",peer_id=m)
    return json.dumps(msg)