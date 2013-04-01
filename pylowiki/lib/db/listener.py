#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from pylowiki.lib.utils import toBase62
import generic

log = logging.getLogger(__name__)

def getListener(user, workshop):
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'listener')\
                .filter(Thing.data.any(wc('userCode', user['urlCode'])))\
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

def Listener(user, workshop, pending = 1):
    # recycle existing disabled listener objects for this user and this workshop
    listener = getListener(user, workshop)
    if listener and listener['disabled'] == '1':
        listener['disabled'] = '0'
        listener['pending'] = pending
        commit(listener)
    else:
        listener = Thing('listener')
        listener['title'] = ''
        listener['pending'] = pending
        listener['disabled'] = u'0'
        listener['itemAlerts'] = u'0'
        listener['digest'] = u'0'
        commit(listener)
        listener['urlCode'] = toBase62(listener)
        listener = generic.linkChildToParent(listener, user)
        listener = generic.linkChildToParent(listener, workshop)
        commit(listener)  
    return listener
