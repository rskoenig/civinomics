#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.event import Event
import sqlalchemy as sa

log = logging.getLogger(__name__)

# Getters
def getUserAccount(userID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'account').filter_by(owner = userID).one()
    except:
        return False

def getUserAccounts(user):
        uID = '|' + user['email'] + '|'
        uKey = 'admins'
        ##log.info('userID is %s, uID is %s and uKey is %s'%(userID, uID, uKey))
        accounts = meta.Session.query(Thing).filter_by(objType = 'account').filter(Thing.data.any(wcl(uKey, uID))).all()
        if accounts:
            return accounts
        else:
            return False

def isAccountAdmin(user, account):
        email = '|' + user['email'] + '|'
        account = meta.Session.query(Thing).filter_by(objType = 'account').filter(Thing.data.any(wc('urlCode', account['urlCode']))).filter(Thing.data.any(wcl('admins', email))).all()
        if account:
            return True
        else:
            return False
            
def getAccountByID(accountID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'account').filter_by(id = accountID).one()
    except:
        return False


def getAccountByCode(hash):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'account').filter(Thing.data.any(wc('urlCode', hash))).one()
    except sa.orm.exc.NoResultFound:
        return False

def getAccountByName(orgName):
    name = urlify(orgName)
    if name == 'none':
        return False
    try:
        return meta.Session.query(Thing).filter_by(objType = 'account').filter(Thing.data.any(wc('url', name))).one()
    except sa.orm.exc.NoResultFound:
        return False

# Setters
def addHostToAccount(account, numHost):
    """add ability to host numHost additional objects on site"""
    account['numHost'] += numHost
    commit(account)

def subtractHostFromAccount(account, numHost):
    """subtract ability to host numHost additional objects on site"""
    if int(account['numHost']) > 0:
       account['numHost'] -= numHost
    else:
       account['numHost'] = '0'
    commit(account)

# Object
class Account(object):
    def __init__(self, user, numHost, numParticipants, monthlyRate, type):
        a = Thing('account', user.id)
        """number of workshop or survey objects the account can host"""
        a['numHost'] = numHost
        a['numRemaining'] = numHost
        a['numParticipants'] = numParticipants
        a['monthyRate'] = monthlyRate
        a['type'] = type
        a['disabled'] = '0'
        
        if type == 'trial':
            a['orgName'] = 'Trial Account'
            a['url'] = 'trial'
        else:
            a['orgName'] = 'none'
            a['url'] = 'none'
        a['orgEmail'] = user['email']
        a['orgMessage'] = user['tagline']
        a['orgLink'] = 'none'
        a['orgLinkDesc'] = 'none'
        a['admins'] = '|' + user['email'] + '|'
        commit(a)

        a['urlCode'] = toBase62(a)
        commit(a)
        
        self.a = a

