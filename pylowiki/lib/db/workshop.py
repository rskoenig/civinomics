from pylons import tmpl_context as c, config, session
from pylons import request
from pylowiki.model import Thing, meta, Data
from sqlalchemy import and_, not_

import pylowiki.lib.utils           as utils
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.pmember      as privateMemberLib
import pylowiki.lib.db.activity     as activityLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.page         as pageLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.slideshow    as slideshowLib
import pylowiki.lib.db.slide        as slideLib
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.mail            as mailLib
import pylowiki.lib.db.tag          as tagLib

from dbHelpers import commit, with_characteristic as wc, without_characteristic as wo, with_characteristic_like as wcl
import time, datetime, logging

log = logging.getLogger(__name__)

def getWorkshops( deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False
        
def getDemoWorkshops():
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('demo', '1'))).all()
    except:
        return False

def searchWorkshops( wKey, wValue):
    try:
        if wKey != 'startTime':
            return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wcl(wKey, wValue))).filter(Thing.data.any(wc('deleted', '0'))).filter(Thing.data.any(wo('startTime', '0000-00-00'))).all()
        else:
            return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wcl(wKey, wValue))).filter(Thing.data.any(wc('deleted', '0'))).all()
    except:
        return False

def getActiveWorkshops( deleted = '0'):
     try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('deleted', deleted))).filter(Thing.data.any(wc('public_private', 'public'))).filter(Thing.data.any(wc('published', '1'))).order_by('-date').all()
     except:
        return False

def getWorkshopByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter_by(id = id).one()
    except:
        return False
        
def getWorkshopByCode(urlCode):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('urlCode', urlCode))).one()
    except:
        return False

def getActiveWorkshopByCode(code):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'workshop')\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .filter(Thing.data.any(wc('deleted', '0')))\
            .filter(Thing.data.any(wc('published', u'1'))).one()
    except:
        return False

def getWorkshopsByOwner(userID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter_by(owner = userID).all()
    except:
        return False

def getWorkshopsByAccount(accountID, publicPrivate = 'public'):
    if publicPrivate == 'all':
        try:
            return meta.Session.query(Thing).filter_by(objType = 'workshop').filter_by(owner = accountID).all()
        except:
            return False
        
    else:
        try:
            return meta.Session.query(Thing).filter_by(objType = 'workshop').filter_by(owner = accountID).filter(Thing.data.any(wc('public_private', publicPrivate))).all()
        except:
            return False

def isWorkshopDeleted(id):
    try:
        w =  meta.Session.query(Thing).filter_by(objType = 'workshop').filter_by(id = id).one()
        if w['deleted'] == '1':
           return True
        else:
           return False

    except:
        return False

def getWorkshop(code, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('urlCode', code))).filter(Thing.data.any(wc('url', url))).one()
    except:
        return False

# Note that this may return multiple objects if they share the same name
def getWorkshopByTitle(title):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('title', title))).all()
    except:
       return False 

# requires a 'participants' field for the queried object
def getParticipantsByID(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()['participants']
    except:
        return False
    
def getRecentMemberPosts(number, publicPrivate = 'public'):
        counter = 0
        returnList = []
        postList = meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['idea', 'resource', 'discussion', 'event']))\
            .filter(Thing.data.any(and_(Data.key == u'workshopCode')))\
            .order_by('-date').all()
        for item in postList:
           w = False
           if item.objType == 'idea':
               w = getWorkshopByCode(item['workshopCode'])
           elif item.objType == 'resource':
               w = getWorkshopByCode(item['workshopCode'])
           elif item.objType == 'discussion':
               w = getWorkshopByCode(item['workshopCode'])
               if item['discType'] != 'general':
                  continue
           elif item.objType == 'event':
               if item['title'] == 'Suggestion Adopted':
                   returnList.append(item)
                   counter += 1

           if w and w['published'] == '1' and w['deleted'] != '1' and w['public_private'] == publicPrivate:
               if item['deleted'] != '1' and item['disabled'] != '1':
                   returnList.append(item)
                   counter += 1
 
           if counter > number:
               break

        return returnList

def getWorkshopPostsSince(code, url, memberDatetime):
        postList = meta.Session.query(Thing).filter(Thing.date > memberDatetime).filter(Thing.objType.in_(['suggestion', 'resource', 'discussion'])).filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).order_by('-date').all()
        discussionList = discussionLib.getDiscussionsForWorkshop(code)
        commentList = []
        for d in discussionList:
            cList = activityLib.getDiscussionCommentsSince(d.id, memberDatetime)
            if cList:
                commentList = commentList + cList

        returnList = postList + commentList

        return returnList
        
def getCategoryTagCount():
    categories = tagLib.getWorkshopTagCategories()
    tagDict = dict()
    for category in categories:
        tagDict[category] = 0
        tagList = tagLib.searchTags(category)
        for tag in tagList:
            workshop = getWorkshopByCode(tag['workshopCode'])
            if isPublished(workshop) and isPublic(workshop):
                tagDict[category] = tagDict[category] + 1
                
    return tagDict

def isGuest(workshop):
    if 'guestCode' in session and 'workshopCode' in session:
        pTest = privateMemberLib.getPrivateMemberByCode(session['guestCode'])
        if pTest and pTest['urlCode'] == session['guestCode'] and pTest['workshopCode'] == session['workshopCode'] and workshop['urlCode'] == session['workshopCode']:
            return True
    
    return False
    
def isPublished(workshop):
    if workshop and workshop['published'] == '1' and workshop['deleted'] == '0':
        return True
    
    return False

def isPublic(workshop):
    if workshop and workshop['public_private'] == 'public':
        return True
    
    return False
    
def isStarted(workshop):
    if workshop and workshop['startTime'] != '0000-00-00' and workshop['deleted'] == '0':
        return True
    
    return False
    
    
def isScoped(user, workshop):   
    if workshop['public_private'] != 'public':
        pTest = privateMemberLib.getPrivateMember(workshop['urlCode'], user['email'])
        if pTest:
            return True
        else:
            return False
    else:
        return True       
    
    return False

def setDemo(workshop): 
    workshop['demo'] = '1'
    workshop['deleted'] = '1'
    commit(workshop)
    return 'New demo workshop'

def isDemo(workshop):   
    if 'demo' in workshop:
        if workshop['demo'] == '1':
            return True
        else:
            return False       
 
    return False

def setWorkshopPrivs(workshop):
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
    c.privs['guest'] = isGuest(workshop)
    # Not logged in, visitor privs in all public workshops
    c.privs['visitor'] = True
    # is a demo workshop
    c.privs['demo'] = isDemo(workshop)
    
    if 'user' in session:
        c.privs['admin'] = userLib.isAdmin(c.authuser.id)
        c.privs['facilitator'] = facilitatorLib.isFacilitator(c.authuser, workshop)
        c.privs['listener'] = listenerLib.getListener(c.authuser, workshop)
        c.privs['participant'] = isScoped(c.authuser, workshop)
        c.privs['guest'] = False
        c.privs['visitor'] = False


def Workshop(title, owner, publicPrivate, type = "personal"):
    # title -> A string
    # owner -> A user object in Thing form
    #
    # Note this will generate the page and event for you.
    w = Thing('workshop', owner.id)
    w['title'] = title
    w['url'] = utils.urlify(title)
    w['startTime'] = u'0000-00-00'
    w['endTime'] = u'0000-00-00'
    w['published'] = u'0'
    w['deleted'] = u'0'
    w['disabled'] = u'0'
    w['facilitators'] = c.authuser.id
    w['description'] = u''
    w['public_private'] = publicPrivate
    w['type'] = type
    w['allowIdeas'] = u'1'
    w['allowSuggestions'] = u'1'
    w['allowResources'] = u'1'
    w['allowDiscussions']  = u'1'
    commit(w)
    w['urlCode'] = utils.toBase62(w)
    background = 'No workshop summary set yet'
    
    p = pageLib.Page(title, owner, w, background)
    e = eventLib.Event('Create workshop', 'User %s created a workshop'%(c.authuser['email']), w)
    
    slideshow = slideshowLib.Slideshow(owner, w)
    generic.linkChildToParent(slideshow, w)
    identifier = 'slide'
    title = 'Sample Title'
    caption = 'Sample Caption'
    s = slideLib.Slide(owner, slideshow, title, 'supDawg.png', 'no file here', '0')
    mainImageLib.setMainImage(owner, w, s)
    slideshow['slideshow_order'] = s.id
    commit(slideshow)
    commit(w)
    
    f = facilitatorLib.Facilitator( c.authuser, w )
    mailLib.sendWorkshopMail(c.authuser['email'])
    
    return w
        
