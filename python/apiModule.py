import json
import requests
import vk, cgi
from flask import session



apiArray = dict()

def getApi():
    api = None
    try:
        api = apiArray.get(session["login"])
        if api is None:
            raise Exception('api is none')
        '''api = vk.API(auth.startauth())'''
    except:
        try:
            s= vk.AuthSession('6121793', session["login"], session["password"],scope='photos, wall, messages, friends, docs, offline, audio,video')
            api = vk.API(s)
            apiArray.update([(session["login"], api)])
        except:
            return None
    return api

def getApiArray():
    return apiArray