from pylons import tmpl_context as c, config, session
from pylowiki.model import Thing, meta, Data
from sqlalchemy import and_
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.facilitator import Facilitator, isFacilitator
from pylowiki.lib.db.user import getUserByID, getUserByEmail, isAdmin
from pylowiki.lib.db.pmember import getPrivateMember, getPrivateMemberByCode
from pylowiki.lib.db.geoInfo import getGeoScope
from pylowiki.lib.db.activity import getDiscussionCommentsSince
from pylowiki.lib.db.discussion import getDiscussionsForWorkshop, getDiscussionByID
from dbHelpers import commit, with_characteristic as wc, without_characteristic as wo, with_characteristic_like as wcl
from page import Page
from event import Event
from revision import Revision
from slideshow import Slideshow, getSlideshow
from slide import Slide
from discussion import Discussion

import time, datetime
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

log = logging.getLogger(__name__)

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

           if w and w['startTime'] != '0000-00-00' and w['deleted'] != '1' and w['public_private'] == publicPrivate:
               if item['deleted'] != '1' and item['disabled'] != '1':
                   returnList.append(item)
                   counter += 1
 
           if counter > number:
               break

        return returnList

def getWorkshopPostsSince(code, url, memberDatetime):
        postList = meta.Session.query(Thing).filter(Thing.date > memberDatetime).filter(Thing.objType.in_(['suggestion', 'resource', 'discussion'])).filter(Thing.data.any(wc('workshopCode', code))).filter(Thing.data.any(wc('workshopURL', url))).order_by('-date').all()
        discussionList = getDiscussionsForWorkshop(code)
        commentList = []
        for d in discussionList:
            cList = getDiscussionCommentsSince(d.id, memberDatetime) 
            ##log.info('d is %s and cList is %s memberDatetime is %s'%(d, cList, memberDatetime))
            if cList:
                commentList = commentList + cList

        returnList = postList + commentList

        return returnList
        
def getCategoryTagList():
    cTagList = []
    cTagList.append('Business')
    cTagList.append('Civil Rights')
    cTagList.append('Community')
    cTagList.append('Economy')
    cTagList.append('Education')
    cTagList.append('Entertainment')
    cTagList.append('Environment')
    cTagList.append('Family')
    cTagList.append('Government')
    cTagList.append('Health')
    cTagList.append('Housing')
    cTagList.append('Infrastructure')
    cTagList.append('Justice')
    cTagList.append('Land Use')
    cTagList.append('Municipal Services')
    cTagList.append('Policy')
    cTagList.append('Safety')
    cTagList.append('Transportation')
    cTagList.append('Other')
    return cTagList

def isGuest(workshop):
    if 'guestCode' in session and 'workshopCode' in session:
        pTest = getPrivateMemberByCode(session['guestCode'])
        if pTest and pTest['urlCode'] == session['guestCode'] and pTest['workshopCode'] == session['workshopCode'] and workshop['urlCode'] == session['workshopCode']:
            return True

    return False
    
def isScoped(user, workshop):   
    if workshop['public_private'] != 'public':
        pTest = getPrivateMember(workshop['urlCode'], user['email'])
        if pTest:
            return True
        else:
            return False
    else:
        return True       
       
    return False
    
def setWorkshopPrivs(workshop):
    c.privs = {}
    # Civinomics administrator
    c.privs['admin'] = False
    # Workshop facilitator
    c.privs['facilitator'] = False
    # Logged in member with privs to add objects
    c.privs['participant'] = False
    # Not logged in, privs to visit this specific workshop
    c.privs['guest'] = isGuest(workshop)
    # Not logged in, visitor privs in all public workshops
    c.privs['visitor'] = True
    
    if 'user' in session:
        c.privs['admin'] = isAdmin(c.authuser.id)
        c.privs['facilitator'] = isFacilitator(c.authuser.id, workshop.id)
        c.privs['participant'] = isScoped(c.authuser, workshop)
        c.privs['guest'] = False
        c.privs['visitor'] = False   
    
def sendPMemberInvite(workshop, sender, recipient, message):
    workshopName = workshop['title']
    senderName = sender['name']
    senderEmail = sender['email']
    subject = senderName + ' invites you to a workshop.'
    
    if message and message != '':
        message = '\n' + message
    
    emailDir = config['app_conf']['emailDirectory']
    imageDir = config['app_conf']['imageDirectory']
    myURL = config['app_conf']['site_base_url']
    
    # see if they are alread a user
    uTest = getUserByEmail(recipient)
    if uTest:
        browseLink = 'Login to your Civinomics account, then visit the workshop here:\n' +  myURL + '/workshop/' + workshop['urlCode'] + '/' + workshop['url']
    else:
        guest = getPrivateMember(workshop['urlCode'], recipient)
        browseLink = 'You can visit and browse the workshop here:\n' +  myURL + '/guest/' + guest['urlCode'] + '/' + workshop['urlCode']
        
    regLink = myURL + '/signup'

    htmlFile = emailDir + "/private_invite.html"
    txtFile = emailDir + "/private_invite.txt"
    headerImage = imageDir + "/email_logo.png"
    
    # open and read in HTML file
    fp = open(htmlFile, 'r')
    htmlMessage = fp.read()
    fp.close()
    
    # do the substitutions
    htmlMessage = htmlMessage.replace('${c.sender}', senderName)
    htmlMessage = htmlMessage.replace('${c.workshopName}', workshopName)
    htmlMessage = htmlMessage.replace('${c.inviteMessage}', message)
    htmlMessage = htmlMessage.replace('${c.regLink}', regLink)
    htmlMessage = htmlMessage.replace('${c.browseLink}', browseLink)
    htmlMessage = htmlMessage.replace('${c.imageSrc}', 'cid:civinomicslogo')
    
    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    # do the substitutions
    textMessage = textMessage.replace('${c.sender}', senderName)
    textMessage = textMessage.replace('${c.workshopName}', workshopName)
    textMessage = textMessage.replace('${c.inviteMessage}', message)
    textMessage = textMessage.replace('${c.regLink}', regLink)
    textMessage = textMessage.replace('${c.browseLink}', browseLink)
  
    # open and read in the image
    fp = open(headerImage, 'rb')
    logo = fp.read()
    fp.close()
    
    senderImage = ''
    if sender['pictureHash'] != 'flash':
        senderImage = "/images/avatar/" + sender['directoryNumber'] + "/profile/" + sender['pictureHash'] + ".profile"
        
    # create a MIME email object, initialize the header info
    email = MIMEMultipart(_subtype='related')
    email['Subject'] = subject
    email['From'] = senderEmail
    email['To'] = recipient
    
    # now attatch the text and html and picture parts
    part1 = MIMEText(textMessage, 'plain')
    #part2 = MIMEText(htmlMessage, 'html')
    #part3 = MIMEImage(logo, 'png')
    #part3.add_header('Content-Id', '<civinomicslogo>')
    email.attach(part1)
    #email.attach(part2)
    #email.attach(part3)
    
    # send that suckah
    s = smtplib.SMTP('localhost')
    s.sendmail(senderEmail, recipient, email.as_string())
    s.quit()

class Workshop(object):
    # title -> A string
    # owner -> A user object in Thing form
    #
    # Note this will generate the page and event for you.
    def __init__(self, title, owner, publicPrivate, type = "personal"):
        w = Thing('workshop', owner.id)
        w['title'] = title
        w['url'] = urlify(title)
        w['startTime'] = '0000-00-00'
        w['endTime'] = '0000-00-00'

        w['deleted'] = '0'
        w['facilitators'] = c.authuser.id
        w['goals'] = 'No goals set'
        w['description'] = ''
        w['pictureHash'] = 'flash' # default picture
        w['numResources'] = 1
        w['public_private'] = publicPrivate
        w['type'] = type
        w['categoryTags'] = ''
        w['geoTags'] = ''
        w['allowIdeas'] = 1
        w['allowSuggestions'] = 1
        w['allowResources'] = 1
        commit(w)
        w['urlCode'] = toBase62(w)
        self.w = w
        background = 'No wiki background set yet'
        
        p = Page(title, owner, w, background)
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
        commit(w)
        
        f = Facilitator( c.authuser, w ) 
        
        
