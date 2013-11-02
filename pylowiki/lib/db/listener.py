#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from pylowiki.lib.utils import toBase62
import generic
import pylowiki.lib.db.user         as userLib

log = logging.getLogger(__name__)

def getListenerByCode(code):
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'listener')\
                .filter(Thing.data.any(wc('urlCode', code)))\
                .one()
    except:
        return False

def getListener(email, workshop):
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'listener')\
                .filter(Thing.data.any(wc('email', email)))\
                .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
                .one()
    except:
        return False

def getListenersForWorkshop(workshop, disabled = 0):
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'listener')\
                .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .all()
    except:
        return False

def getListenersForUser(user, disabled = 0):
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'listener')\
                .filter(Thing.data.any(wc('userCode', user['urlCode'])))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .all()
    except:
        return False

def Listener(name, title, email, workshop, pending = 1):
    # recycle existing disabled listener objects for this user and this workshop
    listener = getListener(email, workshop)
    if listener:
        listener['disabled'] = '0'
        if 'userCode' in listener:
            user = userLib.getUserByCode(listener['userCode'])
            lKey = 'listener_counter'
            if lKey in user:
                lValue = int(user[lKey])
                lValue += 1
                user[lKey] = str(lValue)
            else:
                user[lKey] = '1'
            commit(user)
        listener['pending'] = pending
        commit(listener)
    else:
        listener = Thing('listener')
        listener['name'] = name
        listener['title'] = title
        listener['email'] = email
        listener['pending'] = pending
        listener['disabled'] = u'0'
        listener['itemAlerts'] = u'0'
        listener['digest'] = u'1'
        listener['invites'] = ''
        commit(listener)
        listener['urlCode'] = toBase62(listener)
        user = userLib.getUserByEmail(email)
        if user:
            listener = generic.linkChildToParent(listener, user)
            listener['name'] = user['name']
        listener = generic.linkChildToParent(listener, workshop)
        commit(listener)  
    return listener
