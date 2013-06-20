
#-*- coding: utf-8 -*-
import logging

from pylons import tmpl_context as c, session, config, request

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
from revision import Revision
import pylowiki.lib.db.pmember      as pMemberLib
import pylowiki.lib.db.generic      as genericLib
import pylowiki.lib.mail            as mailLib

from time import time

log = logging.getLogger(__name__)

# Getters

def get_user(hash, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('urlCode', hash))).filter(Thing.data.any(wc('url', url))).one()
    except sa.orm.exc.NoResultFound:
        return False
    
def getUserByCode(code):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('urlCode', code))).one()
    except sa.orm.exc.NoResultFound:
        return False
    
def getActiveUsers(disabled = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('disabled', disabled))).all()
    except:
        return False

def getAllUsers(disabled = '0', deleted = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'user')\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .all()
    except:
        return False

def getUserByEmail(email, disabled = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('email', email.lower()))).filter(Thing.data.any(wc('disabled', disabled))).one()
    except:
        return False

def getUserByFacebookId( userid ):
    try:
        return meta.Session.query(Thing).filter_by(userid = facebookId).one()
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
    
def searchUsers( uKey, uValue, deleted = u'0', disabled = u'0', activated = u'1', count = False):
    try:
        query = meta.Session.query(Thing)\
                .filter_by(objType = 'user')\
                .filter(Thing.data.any(wcl(uKey, uValue)))\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .filter(Thing.data.any(wc('activated', activated)))
        if count:
            return query.count()
        return query.all()
    except:
        return False

def getUserPosts(user, active = 1):
    returnList = []
    if active == 1:
        postList = meta.Session.query(Thing).filter(Thing.objType.in_(['suggestion', 'resource', 'comment', 'discussion', 'idea'])).filter_by(owner = user.id).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).order_by('-date').all()
    else:
        postList = meta.Session.query(Thing).filter(Thing.objType.in_(['suggestion', 'resource', 'comment', 'discussion', 'idea'])).filter_by(owner = user.id).order_by('-date').all()

    for item in postList:
        if item.objType == 'suggestion' or item.objType == 'resource' or item.objType == 'comment' or item.objType == 'idea':
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

def generatePassword():
    """Return a system generated hash for a temporary password"""
    from string import letters, digits
    from random import choice
    pool, size = letters + digits, 20
    hash =  ''.join([choice(pool) for i in range(size)])
    return hash

# Helper functions
    
def hashPassword(password):
    return md5(password + config['app_conf']['auth.pass.salt']).hexdigest()

class User(object):
    def __init__(self, email, name, password, country, memberType, postalCode = '00000'):
        u = Thing('user')
        u['greetingMsg'] = ''
        u['websiteLink'] = ''
        u['websiteDesc'] = ''
        u['email'] = email.lower()
        u['name'] = name
        u['activated'] = '0'
        u['disabled'] = '0'
        u['deleted'] = '0'
        u['pictureHash'] = 'flash' # default picture
        u['postalCode'] =  postalCode
        u['country'] =  country
        u['memberType'] =  memberType
        u['password'] = self.hashPassword(password)
        u['totalPoints'] = 1
        u['url'] = urlify('%s' %name)
        u['numSuggestions'] = 0
        u['numReadResources'] = 0
        u['accessLevel'] = 0
        commit(u)
        u['urlCode'] = toBase62(u)
        commit(u)
        if email != config['app_conf']['admin.email'] and ('guestCode' not in session and 'workshopCode' not in session):
            self.generateActivationHash(u)
        commit(u)
 

        self.u = u
        g = GeoInfo(postalCode, country, u.id)
        
        # update any pmembers
        memberList = pMemberLib.getPrivateMemberWorkshopsByEmail(u['email'])
        for pMember in memberList:
            pMember = genericLib.linkChildToParent(pMember, u)  

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
        # this next line is needed for functional testing to be able to use the generated hash
        if 'paste.testing_variables' in request.environ:
                request.environ['paste.testing_variables']['hash_and_email'] = '%s__%s'%(hash, toEmail)
       
        u['activationHash'] = hash
        commit(u)
        Revision(u, u)
        
        # send the activation email
        mailLib.sendActivationMail(u['email'], url)
        
        log.info("Successful account creation (deactivated) for %s" %toEmail)
    
    def changePassword(self, password):
        self['password'] = self.hashPassword(password)
        return True

    def checkPassword(self, password):
        if self['password'] == self.hashPassword(password):
            return True
        return False
