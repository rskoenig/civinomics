#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c
from pylowiki.model import Thing, Data, meta
from pylowiki.lib.utils import toBase62
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from tldextract import extract

log = logging.getLogger(__name__)

def getPrivateMembers(workshopCode, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('workshopCode', workshopCode))).filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

def getPrivateMember(workshopCode, email, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('workshopCode', workshopCode))).filter(Thing.data.any(wc('email', email))).filter(Thing.data.any(wc('deleted', deleted))).one()
    except:
        return False
        
def getPrivateMemberByCode(code):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('urlCode', code))).one()
    except:
        return False

def getPrivateMemberWorkshops(email, deleted = '0'):
    elist = email.split('@')
    domain = elist[1]
    pmalist =  meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('email', email))).filter(Thing.data.any(wc('type', 'A'))).filter(Thing.data.any(wc('deleted', deleted))).all()
    if not pmalist:
        pmalist = []

    pmdlist =  meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('email', domain))).filter(Thing.data.any(wc('type', 'D'))).filter(Thing.data.any(wc('deleted', deleted))).all()
    if not pmdlist:
        pmdlist = []

    retlist = pmalist + pmdlist
    return retlist

class PMember(object):
    def __init__( self, workshopCode, email, type, owner):
        p = Thing('pmember', owner.id)
        p['workshopCode'] = workshopCode
        p['email'] = email
        # type - one of A for address or D for domain
        p['type'] = type
        p['deleted'] = '0'
        commit(p)
        p['urlCode'] = toBase62(p)
        commit(p)