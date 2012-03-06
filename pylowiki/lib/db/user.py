#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
from dbHelpers import commit
from hashlib import md5
from pylons import config

log = logging.getLogger(__name__)

def get_user(name):
    try:
        return meta.Session.query(Data).filter(with_characteristic('name', name))
    except sa.orm.exc.noResultFound:
        return False

class User(object):
    def __init__(self, firstName, lastName, email, password, zipCode = '00000'):
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
