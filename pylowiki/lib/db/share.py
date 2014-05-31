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

def getShareByUserAndCode(user, code):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'share')\
                .filter_by(owner = user.id)\
                .filter(Thing.data.any(wc('urlCode', code)))\
                .all()
    except:
        return False

#def Share(user, itemCode, itemURL, email, name, message):
#       userCode, itemCode, itemURL, shareType, '', postId)
def Share(user, itemCode, itemURL, email, name, message, **kwargs):
    share = Thing('share', user.id)
    
    # this share object is used by the email share facility as well as facebook sharing.
    # there's a bit of squeezing happening with the fields: sharetype goes where email does for the facebook shares
    # - on that note, we can't record the message a user writes with their facebook share so there's no message to record here anyways
    # ParentCode has been added because it's apparent now that when an initiative or workshop is shared,
    #   there is no itemCode, just a parentCode. Before, this meant to urlCode saved at all, now parentCode is saved if present.
    if 'parentCode' in kwargs:
        share['parentCode'] = kwargs['parentCode']

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
