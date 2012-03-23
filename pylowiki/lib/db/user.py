#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from hashlib import md5
from pylons import config
from pylowiki.lib.utils import urlify, toBase62

from time import time

log = logging.getLogger(__name__)

# Getters

def get_user(hash, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('urlCode', hash))).filter(Thing.data.any(wc('url', url))).one()
    except sa.orm.exc.NoResultFound:
        return False

def getUserByEmail(email):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('email', email))).one()
    except:
        return False

def getUserByID(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False
    
def checkPassword(user, password):
    if user['password'] == hashPassword(password):
        return True
    return False

# Setters

def changePassword(user, password):
    """
    changePassword(user, password)
    
    Changes a user's password.  Returns True if successful.
    
    inputs:
                user        ->    A user Thing
                password    ->    The new password, in string format
    outputs:
                True if successful
    """
    user['password'] = hashPassword(password)
    commit(user)
    return True 

def changeTagline(user, tagline):
    if len(tagline) > 140:
        return False
    user['tagline'] = tagline
    commit(user)
    return True

def changeAccessLevel(user, level):
    user['accessLevel'] = level
    commit(user)
    return True

# Helper functions
    
def hashPassword(password):
    return md5(password + config['app_conf']['auth.pass.salt']).hexdigest()


class User(object):
    def __init__(self, email, firstName, lastName, password, zipCode = '00000'):
        u = Thing('user')
        u['firstName'] = firstName
        u['lastName'] = lastName
        u['email'] = email
        u['name'] = '%s %s'%(firstName, lastName)
        u['activated'] = 0
        u['disabled'] = 0
        u['pictureHash'] = 'flash' # default picture
        u['zipCode'] =  zipCode
        u['password'] = self.hashPassword(password)
        u['totalPoints'] = 1
        u['url'] = urlify('%s %s' %(firstName, lastName))
        u['urlCode'] = toBase62('%s_%s_%s' % (firstName, lastName, int(time())))
        u['numSuggestions'] = 0
        u['numReadResources'] = 0
        commit(u)

    # TODO: Should be encrypted instead of hashed
    def hashPassword(self, password):
        return md5(password + config['app_conf']['auth.pass.salt'] ).hexdigest()

    def generateActivationHash(self):
        """Return a system generated hash for account activation"""
        from string import letters, digits
        from random import choice
        pool, size = letters + digits, 20
        return ''.join([choice(pool) for i in range(size)])

    def changePassword(self, password):
        self['password'] = self.hashPassword(password)
        return True

    def checkPassword(self, password):
        if self['password'] == self.hashPassword(password):
            return True
        return False
