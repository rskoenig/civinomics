import urllib2

from pylons import tmpl_context as c, config, session
from pylons import request
from pylowiki.model import Thing, meta, Data
from sqlalchemy import and_, not_, or_

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

from dbHelpers import commit, with_characteristic as wc, without_characteristic as wo, with_characteristic_like as wcl
import time, datetime, logging

log = logging.getLogger(__name__)

def getWorkshops( deleted = '0'):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False
        
def getPublicWorkshopCodes( deleted = '0'):
    publicList = {}
    try:
        pWorkshops = meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('public_private', 'public'))).filter(Thing.data.any(wc('deleted', deleted))).all()
        for p in pWorkshops:
            pCode = p['urlCode']
            publicList[pCode] = 1
        return publicList
    except:
        return False
        
def getDemoWorkshops():
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('demo', '1'))).all()
    except:
        return False

def searchWorkshops( keys, values, deleted = u'0', published = u'1', public_private = u'public', count = False):
    try:
        if type(keys) != type([]):
            w_keys = [keys]
            w_values = [values]
        else:
            w_keys = keys
            w_values = values
        map_workshop = map(wcl, w_keys, w_values)
        q = meta.Session.query(Thing)\
                .filter_by(objType = 'workshop')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('published', published)))\
                .filter(Thing.data.any(wc('public_private', public_private)))\
                .filter(Thing.data.any(reduce(or_, map_workshop)))
        if count:
            return q.count()
        return q.all()
    except Exception as e:
        log.error(e)
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
        
def updateWorkshopChildren(workshop, workshopKey):
    code = workshop['urlCode']        
    key = '%s%s' %(workshop.objType, 'Code')
    log.info("key is %s, code is %s"%(key, code))
    try:
        itemList = meta.Session.query(Thing)\
                .filter(Thing.objType.in_(['idea', 'resource', 'discussion']))\
                .filter(Thing.data.any(wc(key, code)))\
                .all()
                
        for item in itemList:
            if workshopKey == "workshop_title":
                item[workshopKey] = workshop["title"]
                item['workshop_url'] = workshop['url']
            else:
                item[workshopKey] = workshop[workshopKey]
            commit(item)
            if item.objType == 'discussion':
                discussionCode = item['urlCode']
                commentList = meta.Session.query(Thing)\
                    .filter_by(objType = 'comment')\
                    .filter(Thing.data.any(wc('discussionCode', discussionCode)))\
                    .all()
                for comment in commentList:
                    if workshopKey == "workshop_title":
                        comment[workshopKey] = workshop["title"]
                        comment['workshop_url'] = workshop['url']
                    else:
                        comment[workshopKey] = workshop[workshopKey]
                    commit(comment)                            
    except Exception as e:
        return False
        

def getWorkshopTagCategories():
    workshopTags = []
    workshopTags.append('Animals')
    workshopTags.append('Arts')
    workshopTags.append('Business')
    workshopTags.append('Civil Rights')
    workshopTags.append('Community')
    workshopTags.append('Economy')
    workshopTags.append('Education')
    workshopTags.append('Employment')
    workshopTags.append('Entertainment')
    workshopTags.append('Environment')
    workshopTags.append('Family')
    workshopTags.append('Government')
    workshopTags.append('Health')
    workshopTags.append('Housing')
    workshopTags.append('Infrastructure')
    workshopTags.append('Justice')
    workshopTags.append('Land Use')
    workshopTags.append('Municipal Services')
    workshopTags.append('NonProfit')
    workshopTags.append('Outdoors')
    workshopTags.append('Policy')
    workshopTags.append('Safety')
    workshopTags.append('Sports')
    workshopTags.append('Transportation')
    workshopTags.append('Other')
    return workshopTags

    
def getWorkshopTagColouring():
    mapping = { 'Civil Rights':         'red-tag',
                'Health' :              'red-tag',
                'Safety' :              'red-tag',
                'Justice':              'red-tag',
                'Animals':              'green-tag',
                'Land Use':             'green-tag',
                'Environment':          'green-tag',
                'Outdoors':             'green-tag',
                'Arts':                 'orange-tag',
                'Entertainment':        'orange-tag',
                'Sports':               'orange-tag',
                'Family':               'orange-tag',
                'Community':            'orange-tag',
                'Other':                'orange-tag',
                'Business':             'black-tag',
                'Economy':              'black-tag',
                'Employment':           'black-tag',
                'Education':            'black-tag',
                'Housing':              'black-tag',
                'Transportation':       'blue-tag',
                'Infrastructure':       'blue-tag',
                'Municipal Services':   'blue-tag',
                'Government':           'grey-tag',
                'NonProfit':            'grey-tag',
                'Policy':               'grey-tag'}
    
    #mapping = { 'red-tag': ['Civil Rights', 'Health', 'Safety', 'Justice'],
    #            'green-tag': ['Land Use', 'Environment'],
    #            'orange-tag':['Arts', 'Entertainment', 'Sports', 'Family', 'Community', 'Other'],
    #            'black-tag': ['Business', 'Economy', 'Employment', 'Education', 'Housing'],
    #            'blue-tag': ['Transportation', 'Infrastructure', 'Municipal Services'],
    #            'grey-tag': ['Government', 'NonProfit', 'Policy']
    #            }
    return mapping


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
        if userLib.isAdmin(user.id):
            return True
        pTest = privateMemberLib.getPrivateMember(workshop['urlCode'], user['email'])
        if pTest:
            return True
        else:
            return False
    else:
        return True       
    
    return False
    
def getWorkshopsByScope(searchScope, scopeLevel):
    ## searchScope: a geo scope string
    ## scopeLevel: country = 2, state = 4, county = 6, city = 8, zip = 9
    ## format of scope attribute ||country||state||county||city|zip
    scopeLevel = int(scopeLevel) + 1
    try:
        sList = searchScope.split('|')
        sList = sList[:int(scopeLevel)]
        searchScope = "|".join(sList)
        searchScope = searchScope + '%'
        return meta.Session.query(Thing)\
                .filter_by(objType = 'workshop')\
                .filter(Thing.data.any(wc('deleted', '0')))\
                .filter(Thing.data.any(wc('public_private', 'public')))\
                .filter(Thing.data.any(wc('published', '1')))\
                .filter(Thing.data.any(wcl('workshop_public_scope', searchScope, 1)))\
                .all()
    except sa.orm.exc.NoResultFound:
        return False
    
def getPublicScope(workshop):
    if 'workshop_public_scope' in workshop and workshop['workshop_public_scope'] != '':
        scope = workshop['workshop_public_scope'].split('|')
        flag = '/images/flags/'
        href = '/workshops/geo/earth'
        if scope[9] != '0':
            scopeLevel = 'postalCode'
            scopeName  = scope[9]
            flag += 'generalFlag.gif'
            href += '/' + scope[2] + '/' + scope[4] + '/' + scope[6] + '/' + scope[8] + '/' + scope[9]
        elif scope[8] != '0':
            scopeLevel = 'city'
            scopeName  = scope[8]
            flag += 'country/' + scope[2] + '/states/' + scope[4] + '/counties/' + scope[6] + '/cities/' + scope[8] + '.gif'
            href += '/' + scope[2] + '/' + scope[4] + '/' + scope[6] + '/' + scope[8]
        elif scope[6] != '0':
            scopeLevel = 'county'
            scopeName  = scope[6]
            flag += 'country/' + scope[2] + '/states/' + scope[4] + '/counties/' + scope[6] + '.gif'
            href += '/' + scope[2] + '/' + scope[4] + '/' + scope[6]
        elif scope[4] != '0':
            scopeLevel = 'state'
            scopeName  = scope[4]
            flag += 'country/' + scope[2] + '/states/' + scope[4] + '.gif'
            href += '/' + scope[2] + '/' + scope[4]
        elif scope[2] != '0':
            scopeLevel = 'country'
            scopeName  = scope[2]
            flag += 'country/' + scope[2] + '.gif'
            href += '/' + scope[2]
        else:
            scopeLevel = 'earth'
            scopeName  = 'earth'
            flag += 'earth.gif'

        # make sure the flag exists
        baseUrl = config['site_base_url']
        if baseUrl[-1] == "/":
            baseUrl = baseUrl[:-1]
        flag = baseUrl + flag
        try:
            f = urllib2.urlopen(urllib2.Request(flag))
            flag = flag
        except:
            flag = '/images/flags/generalFlag.gif'
    else:
        scopeLevel = 'earth'
        scopeName  = 'earth'
        flag += 'earth.gif'
    return {'level':scopeLevel, 'name':scopeName, 'flag':flag, 'href':href}

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
        testL = listenerLib.getListener(c.authuser, workshop)
        if testL and testL['pending'] != '1':
            c.privs['listener'] = True
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
    w['workshop_category_tags'] = ''
    w['workshop_searchable'] = u'0'
    commit(w)
    w['urlCode'] = utils.toBase62(w)
    background = utils.workshopInfo
    
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
        
