#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from hashlib import md5
from pylons import config

log = logging.getLogger(__name__)

# Getters

def get_user(name):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(with_characteristic('name', name))).one()
    except sa.orm.exc.NoResultFound:
        return False

def getUserByEmail(email):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(with_characteristic('email', email))).one()
    except:
        return False

def checkPassword(user, password):
    if user['password'] == hashPassword(password):
        return True
    return False

# Setters

def changePassword(user, password):
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
        u['pictureHash'] = 'flash' # default picture
        u['zipCode'] =  zipCode
        u['password'] = self.hashPassword(password)
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
