#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from sqlalchemy import or_
from dbHelpers import commit
from dbHelpers import with_characteristic as wc, with_characteristic_like as wcl, greaterThan_characteristic as gtc
from hashlib import md5
from pylons import config
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.geoInfo import GeoInfo
from pylowiki.lib.mail import send

from time import time

log = logging.getLogger(__name__)

# Getters

def get_user(hash, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('urlCode', hash))).filter(Thing.data.any(wc('url', url))).one()
    except sa.orm.exc.NoResultFound:
        return False
    
def getActiveUsers(disabled = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('disabled', disabled))).all()
    except:
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
    
def isAdmin(id):
    try:
        u = meta.Session.query(Thing).filter_by(id = id).one()
        if int(u['accessLevel']) >= 200:
           return True
        else:
           return False
    except:
        return False
    
def searchUsers( uKey, uValue):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wcl(uKey, uValue))).all()
    except:
        return False

def getUserPosts(user, active = 1):
    returnList = []
    if active == 1:
        postList = meta.Session.query(Thing).filter(Thing.objType.in_(['suggestion', 'resource', 'comment', 'discussion'])).filter_by(owner = user.id).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).order_by('-date').all()
    else:
        postList = meta.Session.query(Thing).filter(Thing.objType.in_(['suggestion', 'resource', 'comment', 'discussion'])).filter_by(owner = user.id).order_by('-date').all()

    for item in postList:
       if item.objType == 'suggestion' or item.objType == 'resource' or item.objType == 'comment':
           returnList.append(item)
       elif item.objType == 'discussion':
           if item['discType'] == 'general':
               returnList.append(item)

    return returnList

def checkPassword(user, password):
    if user['password'] == hashPassword(password):
        return True
    return False

def getUsersWithLevelGreater(level):
    """
        Returns a list of all users with an access level greater than the given level.
    """
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(gtc('accessLevel', level))).all()
    except:
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
    def __init__(self, email, firstName, lastName, password, country, memberType, postalCode = '00000'):
        u = Thing('user')
        u['firstName'] = firstName
        u['lastName'] = lastName
        u['tagline'] = ''
        u['email'] = email
        u['name'] = '%s %s'%(firstName, lastName)
        u['activated'] = '0'
        u['disabled'] = '0'
        u['pictureHash'] = 'flash' # default picture
        u['postalCode'] =  postalCode
        u['country'] =  country
        u['memberType'] =  memberType
        u['password'] = self.hashPassword(password)
        u['totalPoints'] = 1
        u['url'] = urlify('%s %s' %(firstName, lastName))
        u['numSuggestions'] = 0
        u['numReadResources'] = 0
        u['accessLevel'] = 0
        if email != config['app_conf']['admin.email']:
            self.generateActivationHash(u)
        commit(u)
        u['urlCode'] = toBase62(u)
        commit(u)
        self.u = u
        g = GeoInfo(postalCode, country, u.id)

    # TODO: Should be encrypted instead of hashed
    def hashPassword(self, password):
        return md5(password + config['app_conf']['auth.pass.salt'] ).hexdigest()

    def generateActivationHash(self, u):
        """Return a system generated hash for account activation"""
        from string import letters, digits
        from random import choice
        pool, size = letters + digits, 20
        hash =  ''.join([choice(pool) for i in range(size)])
        
        toEmail = u['email']
        frEmail = c.conf['activation.email']
        baseURL = c.conf['activation.url']
        url = '%s/activate/%s__%s'%(baseURL, hash, toEmail) 
        subject = "Civinomics Account Activation"
        message = 'Please click on the following link to activate your account:\n\n%s' % url
        send(toEmail, frEmail, subject, message)
        
        u['activationHash'] = hash
        commit(u)
        
        log.info("Successful account creation (deactivated) for %s" %toEmail)

    def changePassword(self, password):
        self['password'] = self.hashPassword(password)
        return True

    def checkPassword(self, password):
        if self['password'] == self.hashPassword(password):
            return True
        return False
