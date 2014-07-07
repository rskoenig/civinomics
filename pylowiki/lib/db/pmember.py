#-*- coding: utf-8 -*-
import logging
import pickle

from pylons import session, tmpl_context as c
from pylowiki.model import Thing, Data, meta
from pylowiki.lib.utils import toBase62
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from tldextract import extract
import pylowiki.lib.db.generic      as genericLib

log = logging.getLogger(__name__)

def getPrivateMembers(workshopCode, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('workshopCode', workshopCode))).filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

def getPrivateMember(workshopCode, email, deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('workshopCode', workshopCode))).filter(Thing.data.any(wc('email', email.lower()))).filter(Thing.data.any(wc('deleted', deleted))).one()
    except:
        return False
        
def getPrivateMemberByCode(code):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('urlCode', code))).one()
    except:
        return False
        
def getPrivateMemberWorkshopsByEmail(email, deleted = '0'):
    try:
            return meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('email', email.lower()))).filter(Thing.data.any(wc('type', 'A'))).filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False

def getPrivateMemberWorkshops(user, deleted = '0'):
    email = user['email']
    elist = email.split('@')
    retlist = []
    if len(elist) < 2:
        return retlist
    domain = elist[1]
    pmalist =  meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('userCode', user['urlCode']))).filter(Thing.data.any(wc('type', 'A'))).filter(Thing.data.any(wc('deleted', deleted))).all()
    if not pmalist:
        pmalist = []

    pmdlist =  meta.Session.query(Thing).filter_by(objType = 'pmember').filter(Thing.data.any(wc('email', domain))).filter(Thing.data.any(wc('type', 'D'))).filter(Thing.data.any(wc('deleted', deleted))).all()
    if not pmdlist:
        pmdlist = []

    retlist = pmalist + pmdlist
    return retlist

def setPrivateMemberWorkshopsInSession(pwdeleted = '0'):
    if 'privateWorkshops' in c.authuser:
        privateWorkshops = pickle.loads(str(c.authuser["privateWorkshops"]))   
    else:
        privateWorkshops = []
        privateList = getPrivateMemberWorkshops(c.authuser, deleted = pwdeleted)
        if privateList:
            pmemberWorkshops = [genericLib.getThing(pMemberObj['workshopCode']) for pMemberObj in privateList]
            privateList = [w for w in pmemberWorkshops if w['public_private'] != 'public']
            privateWorkshops += [w['urlCode'] for w in privateList]
        c.authuser["privateWorkshops"] = str(pickle.dumps(privateWorkshops))
        commit(c.authuser)
        
    session["privateWorkshops"] = privateWorkshops
    session.save()

def PMember(workshopCode, email, type, owner, user = None):
    p = Thing('pmember', owner.id)
    p['workshopCode'] = workshopCode
    p['email'] = email.lower()
    # type - one of A for address or D for domain
    p['type'] = type
    p['deleted'] = u'0'
    p['itemAlerts'] = u'0'
    p['digest'] = u'0'
    commit(p)
    p['urlCode'] = toBase62(p)
    commit(p)
    if user:
        privateWorkshops = []
        p = genericLib.linkChildToParent(p, user)
        if 'privateWorkshops' in user:
            privateWorkshops = pickle.loads(str(user["privateWorkshops"]))
        else:
            privateList = getPrivateMemberWorkshops(user)
            if privateList:
                pmemberWorkshops = [genericLib.getThing(pMemberObj['workshopCode']) for pMemberObj in privateList]
                privateList = [w for w in pmemberWorkshops if w['public_private'] != 'public']
                privateWorkshops += [w['urlCode'] for w in privateList]
                log.info('privateWorkshops is %s'%privateWorkshops)
                user["privateWorkshops"] = str(pickle.dumps(privateWorkshops))
                commit(user)

        if workshopCode not in privateWorkshops:
            privateWorkshops.append(workshopCode)
            user["privateWorkshops"] = str(pickle.dumps(privateWorkshops))
            commit(user)

    return p
