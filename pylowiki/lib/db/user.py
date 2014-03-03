
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
        
def getNotActivatedUsers():
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('activated', "0"))).all()
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

def getUserByFacebookAuthId( userid ):
    log.info("getUserByFacebookAuthId: " + userid)
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('facebookAuthId', userid))).one()
    except:
        return False

def getUserByTwitterId( twitterid ):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'user').filter(Thing.data.any(wc('twitterAuthId', twitterid))).one()
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
    
def searchUsers( uKeys, uValues, deleted = u'0', disabled = u'0', activated = u'1', count = False):
    try:
        if type(uKeys) != type([]):
            u_keys = [uKeys]
            u_values = [uValues]
        else:
            u_keys = uKeys
            u_values = uValues
        map_user = map(wcl, u_keys, u_values)
        query = meta.Session.query(Thing)\
                .filter_by(objType = 'user')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .filter(Thing.data.any(wc('activated', activated)))\
                .filter(Thing.data.any(reduce(or_, map_user)))
        if count:
            return query.count()
        return query.all()
    except:
        return False
        

def getUserPosts(user, active = 1):
    returnList = []
    thingTypes = ['resource', 'comment', 'discussion', 'idea', 'initiative']
    if active == 1:
        postList = meta.Session.query(Thing).filter(Thing.objType.in_(thingTypes)).filter_by(owner = user.id).filter(Thing.data.any(wc('disabled', '0'))).filter(Thing.data.any(wc('deleted', '0'))).order_by('-date').all()
    else:
        postList = meta.Session.query(Thing).filter(Thing.objType.in_(thingTypes)).filter_by(owner = user.id).order_by('-date').all()

    for item in postList:
        if item.objType != 'discussion':
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
    
def setUserPrivs():
    c.privs = {}
    # Civinomics administrator
    c.privs['admin'] = False
    # Workshop facilitator
    c.privs['facilitator'] = False
    # Like a facilitator, but with no special privs
    c.privs['listener'] = False
    # Logged in member with privs to add objects
    c.privs['participant'] = False
    # Not logged in, privs to visit this specific workshop
    c.privs['guest'] = False
    # Logged in but not yet activated
    c.privs['provisional'] = False
    # Not logged in, visitor privs in all public workshops
    c.privs['visitor'] = True
    # is a demo workshop
    c.privs['demo'] = False
    
    if 'user' in session:
        if c.authuser['activated'] == '0':
            c.privs['provisional'] = True
            c.privs['admin'] = False
            c.privs['participant'] = False
            c.privs['guest'] = False
            c.privs['visitor'] = False
        else:
            c.privs['admin'] = isAdmin(c.authuser.id)
            c.privs['provisional'] = False
            c.privs['participant'] = True
            c.privs['guest'] = False
            c.privs['visitor'] = False

# Helper functions
    
def hashPassword(password):
    return md5(password + config['app_conf']['auth.pass.salt']).hexdigest()

class User(object):
    def __init__(self, email, name, password, country, memberType, postalCode = '00000', **kwargs):
        log.info("memberType is %s"%memberType)
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
        u['commentAlerts'] = '1'
        u['url'] = urlify('%s' %name)
        u['numSuggestions'] = '0'
        u['numReadResources'] = '0'
        u['idea_counter'] = '0'
        u['discussion_counter'] = '0'
        u['resource_counter'] = '0'
        u['follow_counter'] = '0'
        u['facilitator_counter'] = '0'
        u['listener_counter'] = '0'
        u['follower_counter'] = '0'
        u['bookmark_counter'] = '0'
        u['photo_counter'] = '0'
        u['accessLevel'] = 0
        commit(u)
        u['urlCode'] = toBase62(u)
        commit(u)
        if email != config['app_conf']['admin.email'] and ('guestCode' not in session and 'workshopCode' not in session):
            if 'externalAuthSignup' in kwargs:
                if kwargs['externalAuthSignup'] == False:
                    self.generateActivationHash(u)
            else:
                self.generateActivationHash(u)
        commit(u)
 

        self.u = u
        g = GeoInfo(postalCode, country, u.id)
        
        # update any pmembers and listeners
        updateList = genericLib.getThingsByEmail(email)
        for uItem in updateList:
            if uItem.objType == 'pmember' or uItem.objType == 'listener':
                uItem = genericLib.linkChildToParent(uItem, u)
                commit(uItem)

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
