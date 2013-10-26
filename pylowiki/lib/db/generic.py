import logging
log = logging.getLogger(__name__)

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import with_characteristic as wc, commit
from hashlib import md5

def linkChildToParent(child, parent):
    # Defines a standard for object linking.
    # All objects that get accessed through a URL need the following two fields:
    # 
    # urlCode: obtained from toBase62() in pylowiki/lib/utils.py
    # url: obtained from urlify() in pylowiki/lib/utils.py
    # 
    # Because the urlCode field is unique, this is what we use to link objects.
    try:
        code = parent['urlCode']
    except Exception as e:
        log.error("linkChildToParent(): parent object of type %s and id %s missing 'urlCode' field." %(parent.objType, parent.id))
        return False
    
    counters = ['idea', 'resource', 'discussion', 'photo', 'listener', 'initiative']
    key = '%s%s' %(parent.objType.replace("Unpublished", ""), 'Code')
    if key in child:
        # Overwrite, give warning
        log.warning("linkChildToParent(): parent object link already exists in child objType is %s."%parent.objType)
    if parent.objType == 'initiative':
        child['public'] = parent['public']
        child['initiative_url'] = parent['url']
    if 'initiativeCode' in parent and 'initiative_url' in parent:
        child['initiativeCode'] = parent['initiativeCode']
        child['initiative_url'] = parent['initiative_url']
    if 'workshop_category_tags' in parent:
        child['workshop_category_tags'] = parent['workshop_category_tags']
    if 'workshop_public_scope' in parent:
        child['workshop_public_scope'] = parent['workshop_public_scope']
    if 'workshop_searchable' in parent:
        child['workshop_searchable'] = parent['workshop_searchable']
    if 'workshop_title' in parent:
        child['workshop_title'] = parent['workshop_title']
    if 'workshop_url' in parent:
        child['workshop_url'] = parent['workshop_url']
    if parent.objType == 'workshop':
        child['workshop_title'] = parent['title']
        child['workshop_url'] = parent['url']
    if parent.objType == 'user':
        child['user_name'] = parent['name']
        child['user_url'] = parent['url']
        if child.objType in counters:
            doit = 1
            if 'discType' in child and child['discType'] != 'general':
                doit = 0
            
            if doit:
                kName = child.objType + "_counter"
                if kName in parent:
                    value = int(parent[kName])
                    value +=1
                    parent[kName] = str(value)
                else:
                    parent[kName] = '1'
                commit(parent)
    if child.objType == 'comment':
        if 'title' in parent:
            child['parent_title'] = parent['title']
        child['parent_url'] = parent['url']
        
    child[key] = code
    return child
    
def getThing(code, keys = None, values = None):
    # Having some trouble doing this through map/reduce...for loop seems to work.  In looking at the debug
    # output, it looks like the difference between SQLAlchemy making multiple sessions and a single session.
    try:
        q = meta.Session.query(Thing)\
            .filter(Thing.data.any(wc('urlCode', code)))
        if keys is None:
            return q.one()
        if type(keys) != type([]):
            keys = [keys]
            values = [values]
        for i in range(len(keys)):
            q = q.filter(Thing.data.any(wc(keys[i], values[i])))
        return q.one()
    except Exception as e:
        return False

def getChildrenOfParent(parent):
    parentCode = parent.objType.replace("Unpublished", "")  + 'Code'
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.data.any(wc(parentCode, parent['urlCode'])))\
            .all()
    except:
        return False
        
def getThingByID(thingID):
    try:
        return meta.Session.query(Thing)\
            .filter_by(id = thingID)\
            .one()
    except:
        return False
        
# mostly for linking listeners and pmembers to users
def getThingsByEmail(email):
    try:
        q = meta.Session.query(Thing)\
            .filter(Thing.data.any(wc('email', email)))
        return q.all()
    except Exception as e:
        return False

def addedItemAs(thing, privs, role = None):
    """
        thing       ->  A Thing object
        privs       ->  The c.privs dict that sets permissions within a workshop
        role        ->  (Optional) The preferred role to use, in string format.
        
        This sets the addedAs attribute for a given Thing.  For example, if someone is
        posting a comment as a facilitator, then that comment gets the 'addedAs' attribute
        set to 'facilitator'.
        
        If the attribute already exists, it overwrites.  If the attribute does not exist, it creates.
    """
    if role is not None:
        thing['addedAs'] = role
    else:
        if privs['admin']:
            thing['addedAs'] = 'admin'
        elif privs['facilitator']:
            thing['addedAs'] = 'facilitator'
        elif privs['listener']:
            thing['addedAs'] = 'listener'
        else:
            thing['addedAs'] = 'user'
    return thing
    
def userImageSource(user, **kwargs):
        # Assumes 'user' is a Thing.
        # Defaults to a gravatar source
        # kwargs:   forceSource:   Instead of returning a source based on the user-set preference in the profile editor,
        #                          we return a source based on the value given here (civ/gravatar)
        source = 'http://www.gravatar.com/avatar/%s?r=pg&d=identicon' % md5(user['email']).hexdigest()
        large = False
        gravatar = True

        if 'className' in kwargs:
            if 'avatar-large' in kwargs['className']:
                large = True
        if 'forceSource' in kwargs:
            if kwargs['forceSource'] == 'civ':
                gravatar = False
                if 'directoryNum_avatar' in user.keys() and 'pictureHash_avatar' in user.keys():
                    source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
                else:
                    source = '/images/glyphicons_pro/glyphicons/png/glyphicons_003_user.png'
        elif 'extSource' in user.keys():
            if 'facebookSource' in user.keys():
                if user['facebookSource'] == u'1':
                    gravatar = False
                    # NOTE - when to provide large or small link?
                    if large:
                        source = user['facebookProfileBig']
                    else:
                        source = user['facebookProfileSmall']
        else:
            if 'avatarSource' in user.keys():
                if user['avatarSource'] == 'civ':
                    gravatar = False
                    source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
        if large and gravatar:
            source += '&s=200'
        return source
