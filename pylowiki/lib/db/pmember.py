#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c
from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from tldextract import extract

log = logging.getLogger(__name__)

def getPrivateMembers(workshopCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('workshopCode', workshopCode))).all()
    except:
        return False

def getPrivateMemberWorkshops(email):
    elist = email.split('@')
    domain = elist[1]
    pmalist =  meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('email', email))).filter(Thing.data.any(wc('type', 'A'))).all()
    if not pmalist:
        pmalist = []

    pmdlist =  meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('email', domain))).filter(Thing.data.any(wc('type', 'D'))).all()
    if not pmdlist:
        pmdlist = []

    retlist = pmalist + pmdlist
    return retlist

class PMember(object):
    def __init__( self, workshpCode, email, type, owner):
        p = Thing('pmember', owner.id)
        p['workshopCode'] = workshopCode
        p['email'] = email
        # type - one of A for address or D for domain
        p['type'] = type
        p['deleted'] = '0'

