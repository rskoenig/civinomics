from pylons import tmpl_context as c
from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.facilitator import Facilitator, isFacilitator
from pylowiki.lib.db.user import getUserByID
from pylowiki.lib.db.pmember import getPrivateMember
from pylowiki.lib.db.geoInfo import getGeoScope
from pylowiki.lib.db.comment import getDiscussionCommentsSince
from pylowiki.lib.db.discussion import getAllActiveDiscussionsForWorkshop, getDiscussionByID
from dbHelpers import commit, with_characteristic as wc, without_characteristic as wo, with_characteristic_like as wcl
from page import Page
from event import Event
from revision import Revision
from slideshow import Slideshow, getSlideshow
from slide import Slide
from discussion import Discussion

import time, datetime
import logging

log = logging.getLogger(__name__)

# Only support for one facilitator.  Otherwise we need to make a list and add/remove from it
def changeFacilitator(workshop, facilitator):
    workshop['facilitator'] = facilitator
    commit(workshop)
    return True

def getWorkshops( deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('deleted', deleted))).all()
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
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('deleted', deleted))).filter(Thing.data.any(wc('public_private', 'public'))).filter(Thing.data.any(wo('startTime', '0000-00-00'))).order_by('-date').all()
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
        postList = meta.Session.query(Thing).filter(Thing.objType.in_(['suggestion', 'resource', 'discussion', 'event'])).order_by('-date').all()
        for item in postList:
           w = False
           if item.objType == 'suggestion':
               w = getWorkshop(item['workshopCode'], item['workshopURL'])
           elif item.objType == 'resource':
               w = getWorkshopByID(item['workshop_id'])
           elif item.objType == 'discussion':
               w = getWorkshop(item['workshopCode'], item['workshopURL'])
               if item['discType'] != 'general':
                  continue
           elif item.objType == 'event':
               if item['title'] == 'Suggestion Adopted':
                   returnList.append(item)
                   counter += 1

           if w and w['startTime'] != '0000-00-00' and w['deleted'] != '1' and w['public_private'] == publicPrivate:
               if item['deleted'] != '1' and item['disabled'] != '1':
                   returnList.append(item)
                   counter += 1
 
           if counter > number:
               break

        return returnList

def getWorkshopPostsSince(code, url, memberDatetime):
        postList = meta.Session.query(Thing).filter(Thing.date > memberDatetime).filter(Thing.objType.in_(['suggestion', 'resource', 'discussion'])).filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).order_by('-date').all()
        discussionList = getAllActiveDiscussionsForWorkshop(code)
        commentList = []
        for d in discussionList:
            cList = getDiscussionCommentsSince(d.id, memberDatetime) 
            ##log.info('d is %s and cList is %s memberDatetime is %s'%(d, cList, memberDatetime))
            if cList:
                commentList = commentList + cList

        returnList = postList + commentList

        return returnList

def isScoped(user, workshop):
   upostal = user['postalCode']
       
   if workshop['public_private'] == 'private':
        pTest = getPrivateMember(workshop['urlCode'], user['email'])
        if pTest:
           return True
           
   if isFacilitator(user.id, workshop.id):
        return True        
       
   if workshop['scopeMethod'] == 'publicPostalList':
      pstring = workshop['publicPostalList']
      pstring = pstring.replace(' ', ',')
      plist = pstring.split(',')
      if upostal in plist:
         return True
      else:
         return False
   elif workshop['scopeMethod'] == 'publicScope':
      wScope = int(workshop['publicScope'])
      ##log.info('wScope is %s'%wScope)
      offset = 10 - wScope
      offset = offset * -1
      # for indexing offset
      wScope =- 1
      wPostal = workshop['publicPostal']
      wScopeString = getGeoScope(wPostal, 'United States')
      ##log.info('wScopeString is %s'%wScopeString)
      wScopeList = wScopeString.split('|')
      uScopeString = getGeoScope(upostal, 'United States')
      ##log.info('uScopeString is %s'%uScopeString)
      uScopeList = uScopeString.split('|')
      ##log.info('offset is %s wScopeList is %s and uScopeList is %s'%(offset, wScopeList[:offset], uScopeList[:offset]))
      if offset == 0:
          if wScopeList[wScope] == uScopeList[wScope]:
              return True
          else:
              return False
      else:
          if wScopeList[:offset] == uScopeList[:offset]:
              return True
          else:
              return False
   else:
      return False

class Workshop(object):
    # title -> A string
    # owner -> A user object in Thing form
    #
    # Note this will generate the page and event for you.
    def __init__(self, title, owner, publicPrivate):
        w = Thing('workshop', owner.id)
        w['title'] = title
        w['url'] = urlify(title)
        w['startTime'] = '0000-00-00'
        w['endTime'] = '0000-00-00'

        w['deleted'] = '0'
        w['facilitators'] = c.authuser.id
        w['goals'] = 'No goals set'
        w['numResources'] = 1
        w['public_private'] = publicPrivate
       
        w['publicScope'] = 10
        w['publicScopeTitle'] = 'postal code ' + c.authuser['postalCode']
        w['publicPostal'] = c.authuser['postalCode']
        w['publicPostalList'] = ''
        # one of publicScope, publicPostalList, privateEmail, trial
        if publicPrivate == 'trial':
            w['scopeMethod'] = 'trial'
        else:
            w['scopeMethod'] = 'publicScope'
 
        w['publicTags'] = 'none'
        w['memberTags'] = 'none'

        w['allowSuggestions'] = 1
        w['allowResources'] = 1
        commit(w)
        w['urlCode'] = toBase62(w)
        self.w = w
        background = 'No wiki background set yet'
        
        p = Page(title, owner, w, background)
        #r = Revision(owner, background, p.p.id)
        
        e = Event('Create workshop', 'User %s created a workshop'%(c.authuser.id), w)
        
        slideshow = Slideshow(owner, w)
        slideshow = getSlideshow(slideshow.s.id)
        w['mainSlideshow_id'] = slideshow.id
        identifier = 'slide'
        title = 'Sample Title'
        caption = 'Sample Caption'
        s = Slide(owner, slideshow, title, caption, 'supDawg.png', 'no file here', '0')
        w['mainImage_caption'] = caption
        w['mainImage_title'] = title
        w['mainImage_hash'] = s.s['pictureHash']
        w['mainImage_postFix'] = 'orig'
        w['mainImage_identifier'] = identifier
        w['mainImage_id'] = s.s.id
        slideshow['slideshow_order'] = s.s.id
        commit(slideshow)
        
        d = Discussion(owner = owner, discType = 'background', attachedThing = w, title = 'background')
        w['backgroundDiscussion_id'] = d.d.id

        f = Discussion(owner = owner, discType = 'feedback', attachedThing = w, title = 'background')
        w['feedbackDiscussion_id'] = f.d.id

        commit(w)
        
        f = Facilitator( c.authuser.id, w.id ) 
        
        
