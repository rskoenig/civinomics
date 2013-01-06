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
        return meta.Session.query(Thing).filter_by(objType = 'listener').filter(Thing.data.any(wc('userCode', user['urlCode']))).filter(Thing.data.any(wc('workshopCode', workshop['urlCode']))).one()
    except:
        return False

def getListenersForWorkshop(workshop, deleted = 0):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'listener').filter(Thing.data.any(wc('workshopCode', workshop['urlCode']))).filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

def getListenersForUser(user, deleted = 0):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'listener').filter(Thing.data.any(wc('userCode', user['urlCode']))).filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

def Listener(user, workshop, pending = 1):
    listener = Thing('listener')
    listener['userCode'] = user['urlCode']
    listener['pending'] = pending
    listener['deleted'] = '0'
    commit(listener)
    listener['urlCode'] = toBase62(listener)
    listener = generic.linkChildToParent(listener, workshop)
    commit(listener)
    return listener
