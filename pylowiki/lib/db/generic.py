import logging
log = logging.getLogger(__name__)

from pylowiki.model import Thing, Data, meta
#from pylowiki.lib.images import userImageSource
#from pylowiki.lib.db.user import getUserByCode
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
    if parent.objType == 'discussion':
        child['discussion_url'] = parent['url']
        child['discussionCode'] = parent['urlCode']
        child['discussion_title'] = parent['title']
        if 'tags' in parent:
            child['discussion_tags'] = parent['tags']
        elif 'workshop_category_tags' in parent:
            child['discussion_tags'] = parent['workshop_category_tags']
        if 'scope' in parent:
            child['discussion_scope'] = parent['scope']
        elif 'workshop_public_scope' in parent:
            child['discussion_scope'] = parent['workshop_public_scope']
        elif 'workshop_private_scope' in parent:
            child['discussion_scope'] = parent['workshop_private_scope']
    if parent.objType == 'idea':
        child['idea_url'] = parent['url']
        child['ideaCode'] = parent['urlCode']
        child['idea_title'] = parent['title']
        if 'tags' in parent:
            child['idea_tags'] = parent['tags']
        elif 'workshop_category_tags' in parent:
            child['idea_tags'] = parent['workshop_category_tags']
        if 'scope' in parent:
            child['idea_scope'] = parent['scope']
        elif 'workshop_public_scope' in parent:
            child['idea_scope'] = parent['workshop_public_scope']
        elif 'workshop_private_scope' in parent:
            child['idea_scope'] = parent['workshop_private_scope']
    if parent.objType == 'resource':
        child['resource_url'] = parent['url']
        child['resourceCode'] = parent['urlCode']
        child['resource_title'] = parent['title']
        if 'tags' in parent:
            child['resource_tags'] = parent['tags']
        elif 'workshop_category_tags' in parent:
            child['resource_tags'] = parent['workshop_category_tags']
        if 'scope' in parent:
            child['resource_scope'] = parent['scope']
        elif 'workshop_public_scope' in parent:
            child['resource_scope'] = parent['workshop_public_scope']
        elif 'workshop_private_scope' in parent:
            child['resource_scope'] = parent['workshop_private_scope']
    if parent.objType == 'initiative':
        child['initiative_public'] = parent['public']
        child['initiative_url'] = parent['url']
        child['initiative_tags'] = parent['tags']
        child['initiative_scope'] = parent['scope']
        child['initiative_title'] = parent['title']
        child['initiativeCode'] = parent['urlCode']
    if 'initiativeCode' in parent and 'initiative_url' in parent and child.objType != 'rating':
        child['initiativeCode'] = parent['initiativeCode']
        child['initiative_url'] = parent['initiative_url']
        child['initiative_tags'] = parent['initiative_tags']
        child['initiative_scope'] = parent['initiative_scope']
        child['initiative_title'] = parent['initiative_title']
    if parent.objType == 'meeting':
        child['meeting_url'] = parent['url']
        child['meeting_scope'] = parent['scope']
    if 'meetingCode' in parent and 'meeting_url' in parent and child.objType != 'rating':
        child['meetingCode'] = parent['meetingCode']
        child['meeting_url'] = parent['meeting_url']
        child['meeting_scope'] = parent['meeting_scope']
    if parent.objType == 'election':
        child['election_url'] = parent['url']
        child['election_published'] = parent['election_published']
        child['election_scope'] = parent['scope']
        child['election_date'] = parent['electionDate']
    if 'electionCode' in parent and 'election_url' in parent and child.objType != 'rating':
        child['electionCode'] = parent['electionCode']
        child['election_url'] = parent['election_url']
        child['election_published'] = parent['election_published']
        child['election_scope'] = parent['election_scope']
        child['election_date'] = parent['election_date']
    if parent.objType == 'ballot':
        child['ballot_url'] = parent['url']
    if 'ballotCode' in parent and 'ballot_url' in parent and child.objType != 'rating':
        child['ballotCode'] = parent['ballotCode']
        child['ballot_url'] = parent['ballot_url']
    if 'workshop_category_tags' in parent:
        child['workshop_category_tags'] = parent['workshop_category_tags']
    if 'workshop_public_scope' in parent:
        child['workshop_public_scope'] = parent['workshop_public_scope']
    if 'workshop_searchable' in parent:
        child['workshop_searchable'] = parent['workshop_searchable']
        if 'discType' in child:
            if child['discType'] != 'general' and child['discType'] != 'update':
                child['workshop_searchable'] = '0' 
    if 'workshop_title' in parent:
        child['workshop_title'] = parent['workshop_title']
    if 'workshop_url' in parent:
        child['workshop_url'] = parent['workshop_url']
        if 'workshopCode' in parent:
            child['workshopCode'] = parent['workshopCode']
    if 'workshop_subcategory_tags' in parent:
        child['workshop_subcategory_tags'] = parent['workshop_subcategory_tags']
    if parent.objType == 'workshop':
        child['workshop_title'] = parent['title']
        child['workshop_url'] = parent['url']
    if parent.objType == 'user':
        child['user_name'] = parent['name']
        child['user_url'] = parent['url']
        child['user_avatar'] = userImageSource(parent)
        #parentUser = getUserByCode(parent['urlCode'])
        #child['user_avatar'] = userImageSource(parentUser)
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
        if 'discType' in parent:
            child['discType'] = parent['discType']
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
            .filter(Thing.objType.in_(activityTypes))\
            .all()
    except:
        return False
        
def getChildrenOfParentWithTypes(parent, thingTypes = None):
    parentCode = parent.objType.replace("Unpublished", "")  + 'Code'
    if thingTypes is None:
        thingTypes = ['initiative', 'resource', 'idea']
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.data.any(wc(parentCode, parent['urlCode'])))\
            .filter(Thing.objType.in_(thingTypes))\
            .all()
    except:
        return False
        
def updateChildrenCaracteristic(thing, caracteristic):
    value = thing[caracteristic]
    children = getChildrenOfParentWithTypes(thing)
    for child in children:
        child['readOnly'] = value
        commit(child)

def setReadOnly(thing, value = '1'):
    thing['readOnly'] = value
    commit(thing)
    children = getChildrenOfParent(thing)
    for child in children:
        child['readOnly'] = value
        commit(child)

        
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
 
def getThingsByCodeList(urlCodeList, disabled = "0", deleted = "0"):
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.data.any(wkil('urlCode', urlCodeList)))\
            .filter(Thing.data.any(wc('disabled', u'0')))\
            .filter(Thing.data.any(wc('deleted', u'0')))\
            .all()
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
