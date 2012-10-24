#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
from dbHelpers import commit, with_characteristic as wc

log = logging.getLogger(__name__)

# Getters
def getUserAccount(userID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'account').filter_by(owner = userID).one()
    except:
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
    def __init__(self, user, numHost = 1):
        a = Thing('account', user.id)
        """number of workshop or survey objects the account can host"""
        a['numHost'] = numHost
        a['numRemaining'] = numHost
        a['disabled'] = '0'
        commit(a)

