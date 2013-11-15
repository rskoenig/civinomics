#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
from dbHelpers import commit, with_characteristic as wc
from pylowiki.lib.utils import urlify, toBase62
import pylowiki.lib.db.generic as generic

log = logging.getLogger(__name__)

def getShareByCode(code):
    try:
        query = meta.Session.query(Thing).filter_by(objType = 'share')\
                .filter(Thing.data.any(wc('urlCode', code))).all()
    except:
        return False

def getSharesByUser(user):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'share')\
                .filter_by(owner = user.id)\
                .all()
    except:
        return False

def Share(user, itemCode, itemURL, email, name, message):
    share = Thing('share', user.id)
    share['itemCode']     = itemCode
    share['itemURL']     = itemURL
    share['email']     = email
    share['name']     = name
    share['message']     = message
    share = generic.linkChildToParent(share, user)
    commit(share)
    share['urlCode'] = toBase62(share)
    commit(share)
    return share
