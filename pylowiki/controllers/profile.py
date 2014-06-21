# -*- coding: utf-8 -*-
import logging
import math

from pylons import request, response, session, config, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.utils import urlify

import pylowiki.lib.helpers as h
from pylons import config

from pylowiki.lib.db.user import User
from pylowiki.lib.db.dbHelpers import commit

import pylowiki.lib.db.activity         as activityLib
import pylowiki.lib.db.geoInfo          as geoInfoLib
import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.generic          as genericLib
import pylowiki.lib.db.discussion       as discussionLib
import pylowiki.lib.db.dbHelpers        as dbHelpers
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.workshop         as workshopLib
import pylowiki.lib.db.pmember          as pMemberLib
import pylowiki.lib.db.follow           as followLib
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.flag             as flagLib
import pylowiki.lib.db.revision         as revisionLib
import pylowiki.lib.db.message          as messageLib
import pylowiki.lib.db.photo            as photoLib
import pylowiki.lib.db.mainImage        as mainImageLib
import pylowiki.lib.db.initiative       as initiativeLib
import pylowiki.lib.db.meeting          as meetingLib
import pylowiki.lib.db.ballot           as ballotLib
import pylowiki.lib.fuzzyTime           as fuzzyTime
import pylowiki.lib.mail                as mailLib

from pylowiki.lib.facebook              import FacebookShareObject
import pylowiki.lib.csvHelper           as csv
import pylowiki.lib.images              as imageLib
import pylowiki.lib.utils               as utils

import time, datetime
import simplejson as json
import copy as copy
import misaka as m


log = logging.getLogger(__name__)

class ProfileController(BaseController):
    
    def __before__(self, action, id1 = None, id2 = None):
        if action not in ['hashPicture']:
            if id1 is not None and id2 is not None:
                c.user = userLib.getUserByCode(id1)
                if not c.user:
                    abort(404)
            elif action == 'unsubscribe':
                hash, sep, email = id1.partition('__')
                c.user = userLib.getUserByEmail(email)
                if not c.user:
                    abort(404)
            else:
                abort(404)

            c.geoInfo = []
            gList = geoInfoLib.getGeoInfo(c.user.id)
            for g in gList:
                if g['disabled'] == '0':
                    c.geoInfo.append(g)
                
            c.isAdmin = False
            if 'user' in session:
                if userLib.isAdmin(c.authuser.id):
                    c.isAdmin = True
                if c.user.id == c.authuser.id or c.isAdmin:
                    c.messages = messageLib.getMessages(c.user)
                    c.unreadMessageCount = messageLib.getMessages(c.user, read = u'0', count = True)
                    
        userLib.setUserPrivs()
  
    def showUserPage(self, id1, id2, id3 = ''):
        # check to see if this is a request from the iphone app
        # entry is used for packing a json object for the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)
        if iPhoneApp:
            entry = {}
            displayWorkshops = utils.profileDisplayWorkshops(request)
        # Called when visiting /profile/urlCode/url
        rev = id3
        if id3 != '':
            c.revision = revisionLib.getRevisionByCode(id3)
        else:
            c.revision = False

        #c.revisions = revisionLib.getParentRevisions(c.user.id)
        c.title = c.user['name']
               
        c.isFollowing = False
        c.isUser = False
        c.browse = False
        if 'user' in session:
            if c.authuser.id != c.user.id:
                c.isFollowing = followLib.isFollowing(c.authuser, c.user)
            else:
                c.isUser = True
            if userLib.isAdmin(c.authuser.id):
                c.isAdmin = True
        else:
            c.browse = True

        watching = followLib.getWorkshopFollows(c.user)
        watchList = [ workshopLib.getWorkshopByCode(followObj['workshopCode']) for followObj in watching ]
        c.watching = []
        for workshop in watchList:
            if workshop['public_private'] == 'public' or (c.isUser or c.isAdmin):
                c.watching.append(workshop)

        c.bookmarkedWorkshops = []
        for workshop in c.watching:
            if workshop['public_private'] == 'public':
                c.bookmarkedWorkshops.append(workshop)
            if workshop['public_private'] == 'private' and 'user' in session and c.authuser:
                if c.isUser or c.isAdmin:
                    c.bookmarkedWorkshops.append(workshop)
        if iPhoneApp:
            if displayWorkshops:
                i = 0
                for bWorkshop in c.bookmarkedWorkshops:
                    bookmarkedWorkshopEntry = "bookmarkedWorkshop" + str(i)
                    bWorkshopCopy = copy.copy(bWorkshop)
                    bWorkshopCopy['type'] = 'Bookmarked'
                    mainImage = mainImageLib.getMainImage(bWorkshop)
                    bWorkshopCopy['imageURL'] = utils.workshopImageURL(bWorkshop, mainImage, thumbnail = True)
                    if c.isUser:
                        f = followLib.getFollow(c.user, bWorkshop)
                        if 'itemAlerts' in f and f['itemAlerts'] == '1':
                            bWorkshopCopy['newItems'] = '1'
                        else:
                            bWorkshopCopy['newItems'] = '0'
                        if 'digest' in f and f['digest'] == '1':
                            bWorkshopCopy['dailyDigest'] = '1'
                        else:
                            bWorkshopCopy['dailyDigest'] = '0'
                    entry[bookmarkedWorkshopEntry] = dict(bWorkshopCopy)
                    i = i + 1

        # NOTE this looks unused:
        interestedList = [workshop['urlCode'] for workshop in c.interestedWorkshops]
        
        c.privateWorkshops = []
        if 'user' in session and c.authuser:
            if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                privateList = pMemberLib.getPrivateMemberWorkshops(c.user, deleted = '0')
                if privateList:
                    c.privateWorkshops = [workshopLib.getWorkshopByCode(pMemberObj['workshopCode']) for pMemberObj in privateList]
        if iPhoneApp:
            if displayWorkshops:
                i = 0
                for privateWorkshop in c.privateWorkshops:
                    privateWorkshopEntry = "privateWorkshop" + str(i)
                    privateWorkshopCopy = copy.copy(privateWorkshop)
                    privateWorkshopCopy['type'] = 'Private'
                    mainImage = mainImageLib.getMainImage(privateWorkshop)
                    privateWorkshopCopy['imageURL'] = utils.workshopImageURL(privateWorkshop, mainImage, thumbnail = True)
                    if c.isUser:
                        p = pMemberLib.getPrivateMember(privateWorkshop['urlCode'], c.user['email'])
                        if 'itemAlerts' in p and p['itemAlerts'] == '1':
                            privateWorkshopCopy['newItems'] = '1'
                        else:
                            privateWorkshopCopy['newItems'] = '0'
                        if 'digest' in p and p['digest'] == '1':
                            privateWorkshopCopy['dailyDigest'] = '1'
                        else:
                            privateWorkshopCopy['dailyDigest'] = '0'
                    entry[privateWorkshopEntry] = dict(privateWorkshopCopy)
                    i = i + 1

        listenerList = listenerLib.getListenersForUser(c.user, disabled = '0')
        c.pendingListeners = []
        c.listeningWorkshops = []
        for l in listenerList:
            lw = workshopLib.getWorkshopByCode(l['workshopCode'])
            c.listeningWorkshops.append(lw)
        if iPhoneApp:
            if displayWorkshops:
                i = 0
                for lWorkshop in c.listeningWorkshops:
                    listeningWorkshopEntry = "listeningWorkshop" + str(i)
                    lWorkshopCopy = copy.copy(lWorkshop)
                    lWorkshopCopy['type'] = 'Listening'
                    mainImage = mainImageLib.getMainImage(lWorkshop)
                    lWorkshopCopy['imageURL'] = utils.workshopImageURL(lWorkshop, mainImage, thumbnail = True)
                    if c.isUser:
                        l = listenerLib.getListener(c.user['email'], lWorkshop)
                        if 'itemAlerts' in l and l['itemAlerts'] == '1':
                            lWorkshopCopy['newItems'] = '1'
                        else:
                            lWorkshopCopy['newItems'] = '0'
                        if 'digest' in l and l['digest'] == '1':
                            lWorkshopCopy['dailyDigest'] = '1'
                        else:
                            lWorkshopCopy['dailyDigest'] = '0'
                    entry[listeningWorkshopEntry] = dict(lWorkshopCopy)
                    i = i + 1
            
        facilitatorList = facilitatorLib.getFacilitatorsByUser(c.user)
        c.facilitatorWorkshops = []
        c.facilitatorInitiatives = []
        c.pendingFacilitators = []
        for f in facilitatorList:
           if 'pending' in f and f['pending'] == '1':
              c.pendingFacilitators.append(f)
           elif f['disabled'] == '0':
                try:
                    myW = workshopLib.getWorkshopByCode(f['workshopCode'])
                    if not workshopLib.isPublished(myW) or myW['public_private'] != 'public':
                     # show to the workshop owner, show to the facilitator owner, show to admin
                        if 'user' in session: 
                            if c.authuser.id == f.owner or userLib.isAdmin(c.authuser.id):
                                c.facilitatorWorkshops.append(myW)
                    else:
                        c.facilitatorWorkshops.append(myW)
                except:
                    myI = initiativeLib.getInitiative(f['initiativeCode'])
                    if myI['public'] == '0':
                     # show to the workshop owner, show to the facilitator owner, show to admin
                        if 'user' in session: 
                            if c.authuser.id == f.owner or userLib.isAdmin(c.authuser.id):
                                c.facilitatorInitiatives.append(myI)
                    else:
                        c.facilitatorInitiatives.append(myI)

                    
        # initiatives
        c.initiatives = []
        initiativeList = initiativeLib.getInitiativesForUser(c.user)
        for i in initiativeList:
            if i.objType == 'initiative':
                if i['public'] == '1':
                    if i['deleted'] != '1':
                        c.initiatives.append(i)
                else:
                    if 'user' in session and ((c.user['email'] == c.authuser['email']) or c.isAdmin):
                        c.initiatives.append(i)
                        
        c.initiativeBookmarks = []
        iwatching = followLib.getInitiativeFollows(c.user)
        initiativeList = [ initiativeLib.getInitiative(followObj['initiativeCode']) for followObj in iwatching ]
        for i in initiativeList:
            if i.objType == 'initiative':
                if i['public'] == '1':
                    if i['deleted'] != '1':
                        c.initiativeBookmarks.append(i)
                else:
                    if 'user' in session and ((c.user['email'] == c.authuser['email']) or c.isAdmin):
                        c.initiativeBookmarks.append(i)
        if iPhoneApp:
            if displayWorkshops:
                i = 0
                for facilitatorWorkshop in c.facilitatorWorkshops:
                    facilitatorWorkshopEntry = "facilitatorWorkshop" + str(i)
                    facilitatorWorkshopCopy = copy.copy(facilitatorWorkshop)
                    facilitatorWorkshopCopy['type'] = 'Facilitating'
                    mainImage = mainImageLib.getMainImage(facilitatorWorkshop)
                    facilitatorWorkshopCopy['imageURL'] = utils.workshopImageURL(facilitatorWorkshop, mainImage, thumbnail = True)
                    if c.isUser:
                        f = facilitatorLib.getFacilitatorsByUserAndWorkshop(c.user, facilitatorWorkshop)[0]
                        #log.info("f itema: %s"%f['itemAlerts'])
                        if 'itemAlerts' in f and f['itemAlerts'] == '1':
                            facilitatorWorkshopCopy['newItems'] = '1'
                        else:
                            facilitatorWorkshopCopy['newItems'] = '0'
                        if 'flagAlerts' in f and f['flagAlerts'] == '1':
                            facilitatorWorkshopCopy['newFlags'] = '1'
                        else:
                            facilitatorWorkshopCopy['newFlags'] = '0'
                        if 'digest' in f and f['digest'] == '1':
                            facilitatorWorkshopCopy['dailyDigest'] = '1'
                        else:
                            facilitatorWorkshopCopy['dailyDigest'] = '0'
                    entry[facilitatorWorkshopEntry] = dict(facilitatorWorkshopCopy)
                    i = i + 1
            #i = 0
            #for pendingFacilitator in c.pendingFacilitators:
            #    pendingFacilitatorEntry = "pendingFacilitator" + str(i)
            #    entry[pendingFacilitatorEntry] = dict(pendingFacilitator)
            #    i = i + 1
                
        #c.rawActivity = activityLib.getMemberActivity(c.user, '0')
        c.memberPosts = activityLib.getMemberPosts(c.user)
        if not c.memberPosts:
            c.memberPosts = []
        #if iPhoneApp:
        #    i = 0
        #    for mPost in c.memberPosts:
        #        mPostEntry = "memberPost" + str(i)
        #        entry[mPostEntry] = dict(mPost)
        #        i = i + 1

        c.unpublishedActivity = activityLib.getMemberPosts(c.user, '1')
        if not c.unpublishedActivity:
            c.unpublishedActivity = []
        #if iPhoneApp:
        #    i = 0
        #    for umPost in c.unpublishedActivity:
        #        umPostEntry = "unpublishedActivity" + str(i)
        #        entry[umPostEntry] = dict(umPost)
        #        i = i + 1

        if iPhoneApp:
            entry['profilePic'] = imageLib.userImageSource(c.user)
            entry['title'] = c.title
            #entry['isFollowing'] = c.isFollowing
            entry['isUser'] = c.isUser
            entry['browse'] = c.browse
            # next entries represented as __workshop/facilitator/post0..len(c.__-1)
            #entry['watching'] = c.watching
            #entry['bookmarkedWorkshops'] = c.bookmarkedWorkshops
            #entry['privateWorkshops'] = c.privateWorkshops
            #entry['listeningWorkshops'] = c.listeningWorkshops
            #entry['pendingFacilitators'] = c.pendingFacilitators
            #entry['facilitatorWorkshops'] = c.facilitatorWorkshops
            #entry['memberPosts'] = c.memberPosts
            #entry['unpublishedActivity'] = c.unpublishedActivity
            
            result = []
            result.append(entry)
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:    
            return render("/derived/6_profile.bootstrap")

        
    def showUserPhotos(self, id1, id2):
        # defaults for photo editor
        c.photo = False
        c.photoTitle = "Sample Title"
        c.description = "Sample Description"
        c.categories = []
        c.country = '0'
        c.state = '0'
        c.county = '0'
        c.city = '0'
        c.postal = '0'
        
        
        c.photos = []
        photos = photoLib.getUserPhotos(c.user)
        if photos:
            c.photos = photos
            c.photos.reverse()

        return render("/derived/6_profile_photos.bootstrap")
 
    def showUserArchives(self, id1, id2):
        return render("/derived/6_profile_archives.bootstrap")
        
            
    def getUserTrash(self, id1, id2):
        c.unpublishedActivity = activityLib.getMemberPosts(c.user, '1')
        if not c.unpublishedActivity:
            c.unpublishedActivity = []
            
        result = []
        for item in c.unpublishedActivity:
            objType = item.objType.replace("Unpublished", "")
            if objType == 'discussion' and item['discType'] != 'general':
                continue
            entry = {}
            entry['objType'] = item.objType.replace("Unpublished", "")
            if entry['objType'] != 'comment':
                entry['url']= item['url']
                entry['urlCode']=item['urlCode']
                entry['title'] = item['title']
            else:
                entry['url']= ''
                entry['urlCode']= ''
                entry['title'] = item['data']
            if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
				entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
                
            href = '/' + entry['objType'] + '/' + entry['urlCode'] + '/' + entry['url']
            if entry['objType'] == 'initiative' or entry['objType'] == 'meeting' or entry['objType'] == 'ballot' or entry['objType'] == 'election' or entry['objType'] == 'ballotcandidate':
                href += '/show'
            if entry['objType'] == 'agendaitem':
                mCode = item['meetingCode']
                mURL = item['meeting_url']
                href = '/meeting/' + mCode + '/' + mURL + '/agendaitem/' + item['urlCode']
            if entry['objType'] == 'ballotmeasure':
                mCode = item['ballotCode']
                mURL = item['ballot_url']
                href = '/ballot/' + mCode + '/' + mURL + '/ballotmeasure/' + item['urlCode']
                
            entry['href'] = href
                
            entry['unpublishedBy'] = item['unpublished_by']
            result.append(entry)
            
        if len(result) == 0:
            return json.dumps({'statusCode':1})
        return json.dumps({'statusCode':0, 'result': result})
        
    def showUserMeetings(self, id1, id2):
        return render("/derived/6_profile_meetings.bootstrap")
        
    def getUserMeetings(self, id1, id2):
        c.meetings = meetingLib.getMeetingsForUser(id1)
        if not c.meetings:
            c.meetings = []
            
        result = []
        for item in c.meetings:
            entry = {}
            entry['objType'] = 'meeting'
            entry['url']= item['url']
            entry['urlCode']=item['urlCode']
            entry['title'] = item['title']
            entry['meetingDate'] = item['meetingDate']
            entry['group'] = item['group']
            
            scopeInfo = utils.getPublicScope(item['scope'])
            entry['scopeName'] = scopeInfo['name']
            entry['scopeLevel'] = scopeInfo['level']
            entry['scopeHref'] = scopeInfo['href']
            entry['flag'] = scopeInfo['flag']
            entry['href']= '/meeting/' + entry['urlCode'] + '/' + entry['url'] + '/show'
            result.append(entry)
            
        if len(result) == 0:
            return json.dumps({'statusCode':1})
        return json.dumps({'statusCode':0, 'result': result})
        
    def showUserElections(self, id1, id2):
        return render("/derived/6_profile_elections.bootstrap")
        
    def getUserElections(self, id1, id2):
        c.elections = ballotLib.getElectionsForUser(id1)
        if not c.elections:
            c.elections = []
            
        result = []
        for item in c.elections:
            entry = {}
            entry['objType'] = 'election'
            entry['url']= item['url']
            entry['urlCode']=item['urlCode']
            entry['title'] = item['title']
            entry['text'] = item['text']
            entry['html'] = m.html(entry['text'], render_flags=m.HTML_SKIP_HTML)
            entry['electionDate'] = item['electionDate']
            
            scopeInfo = utils.getPublicScope(item['scope'])
            entry['scopeName'] = scopeInfo['name']
            entry['scopeLevel'] = scopeInfo['level']
            entry['scopeHref'] = scopeInfo['href']
            entry['flag'] = scopeInfo['flag']
            entry['href']= '/election/' + entry['urlCode'] + '/' + entry['url'] + '/show'
            result.append(entry)
            
        if len(result) == 0:
            return json.dumps({'statusCode':1})
        return json.dumps({'statusCode':0, 'result': result})
        
        
        
    def showUserBallots(self, id1, id2):
        return render("/derived/6_profile_ballots.bootstrap")
        
    def getUserBallots(self, id1, id2):
        c.ballots = ballotLib.getBallotsForUser(id1)
        if not c.ballots:
            c.ballots = []
            
        result = []
        for item in c.ballots:
            entry = {}
            entry['objType'] = 'ballot'
            entry['url']= item['url']
            entry['urlCode']=item['urlCode']
            entry['title'] = item['title']
            entry['text'] = item['text']
            entry['html'] = m.html(entry['text'], render_flags=m.HTML_SKIP_HTML)

            entry['href']= '/ballot/' + entry['urlCode'] + '/' + entry['url'] + '/show'
            result.append(entry)
            
        if len(result) == 0:
            return json.dumps({'statusCode':1})
        return json.dumps({'statusCode':0, 'result': result})
        
        
    def showUserPhoto(self, id1, id2, id3):
        if not id3 or id3 == '':
            abort(404)
        c.photo = photoLib.getPhoto(id3)
        if not c.photo:
            # see if it is a revision
            c.photo = revisionLib.getRevisionByCode(id3)
        if not c.photo:
            log.info("no photo, no revision with %s"%id3)
            abort(404)

        # the next area of fields is needed for sharing functions
        c.imgSrc = "/images/photos/" + c.photo['directoryNum_photos'] + "/orig/" + c.photo['pictureHash_photos'] + ".png"
        c.photoLink = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/photo/show/" + c.photo['urlCode']

        if 'views' not in c.photo:
            c.photo['views'] = u'0'
            
        views = int(c.photo['views']) + 1
        c.photo['views'] = str(views)
        dbHelpers.commit(c.photo)
            
        if not c.photo:
            c.photo = revisionLib.getRevisionByCode(id3)
            if not c.photo:
                abort(404)
            c.revisions = []
        else:
            c.revisions = revisionLib.getRevisionsForThing(c.photo)
        c.photoTitle = c.photo['title']
        # this value is needed for sharing
        c.name = c.photo['title']
        c.description = c.photo['description']
        # for the 6_lib item functions we leverage
        c.thing = c.photo
        c.discussion = discussionLib.getDiscussionForThing(c.photo)
        
        # defaults for photo editor
        tagString = c.photo['tags']
        tempList = tagString.split('|')
        c.categories = []
        for tag in tempList:
            if tag and tag != '':
                c.categories.append(tag)
        c.country = '0'
        c.state = '0'
        c.county = '0'
        c.city = '0'
        c.postal = '0'
        scope = c.photo['scope'].split('|')
        if scope[2] != '' and scope[2] != '0':
            c.country = geoInfoLib.geoDeurlify(scope[2].title())
            if scope[4] != '' and scope[4] != '0':
                c.state = geoInfoLib.geoDeurlify(scope[4].title())
                if scope[6] != '' and scope[6] != '0':
                    c.county = geoInfoLib.geoDeurlify(scope[6].title())
                    if scope[8] != '' and scope[8] != '0':
                        c.city = geoInfoLib.geoDeurlify(scope[8].title())
                        if scope[9] != '' and scope[9] != '0':
                            c.postal = scope[9]
                    

        #################################################
        # these values are needed for facebook sharing
        shareOk = photoLib.isPublic(c.photo)
        c.facebookShare = FacebookShareObject(
            itemType='photo',
            url=c.photoLink,
            thingCode=id3, 
            image=c.imgSrc,
            title=c.photoTitle,
            description=c.description,
            shareOk = shareOk
        )
        # add this line to tabs in the workshop in order to link to them on a share:
        # c.facebookShare.url = c.facebookShare.url + '/activity'
        #################################################

        return render("/derived/6_profile_photo.bootstrap")
    
    def showUserResources(self, id1, id2):
        # Called when visiting /profile/urlCode/url
        self._basicSetup(id1, id2, 'resources')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserDiscussions(self, id1, id2):
        # Called when visiting /profile/urlCode/url/discussions
        self._basicSetup(id1, id2, 'discussions')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserIdeas(self, id1, id2):
        # Called when visiting /profile/urlCode/url/ideas
        self._basicSetup(id1, id2, 'ideas')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserFollowers(self, id1, id2):
        # Called when visiting /profile/urlCode/url/followers
        self._basicSetup(id1, id2, 'followers')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserFollows(self, id1, id2):
        # Called when visiting /profile/urlCode/url/following
        self._basicSetup(id1, id2, 'following')
        return render("/derived/6_profile_list.bootstrap")
        
    def showUserWatching(self, id1, id2):
        # Called when visiting /profile/urlCode/url/watching
        self._basicSetup(id1, id2, 'watching')
        return render("/derived/6_profile_list.bootstrap")
    
    def showUserListening(self, id1, id2):
        # Called when visiting /profile/urlCode/url/listening
        self._basicSetup(id1, id2, 'listening')
        return render("/derived/6_profile_list.bootstrap")
        
    def showUserFacilitating(self, id1, id2):
        # Called when visiting /profile/urlCode/url/facilitating
        self._basicSetup(id1, id2, 'facilitating')
        return render("/derived/6_profile_list.bootstrap")
    
    def _basicSetup(self, code, url, page):
        # code and url are now unused here, now that __before__ is defined
        c.title = c.user['name']
        c.geoInfo = geoInfoLib.getGeoInfo(c.user.id)
        c.isFollowing = False
        c.isUser = False
        c.isAdmin = False
        if 'user' in session and c.authuser:
           c.isFollowing = followLib.isFollowing(c.authuser, c.user)
        else:
           c.isFollowing = False
        
        items = self._userItems(c.user)
        c.listingType = page
        c.things = items[page]
        c.thingsTitle = page.title()
        
        c.discussions = items['discussions']
        c.resources = items['resources']
        c.ideas = items['ideas']
        c.followers = items['followers']
        c.following = items['following']
        c.watching = items['watching']

    
    def _userItems(self, user):
        isUser = False
        isAdmin = False
        if 'user' in session and c.authuser:
            if user.id == c.authuser.id:
               isUser = True
            if userLib.isAdmin(c.authuser.id):
               isAdmin = True

        # returns a dictionary of user-created (e.g. resources, discussions, ideas)
        # or user-interested (e.g. followers, following, watching) objects
        items = {}
        
        following = followLib.getUserFollows(c.user) 
        # list of follow objects 
        items['following'] = [userLib.getUserByCode(followObj['userCode']) for followObj in following] # list of user objects

        followers = followLib.getUserFollowers(c.user)
        items['followers'] = [ userLib.getUserByID(followObj.owner) for followObj in followers ]
        
        watching = followLib.getWorkshopFollows(user)
        watchList = [ workshopLib.getWorkshopByCode(followObj['workshopCode']) for followObj in watching ]
        items['watching'] = []
        for workshop in watchList:
            if workshop['public_private'] == 'public' or (isUser or isAdmin):
                items['watching'].append(workshop)
                
        iwatching = followLib.getInitiativeFollows(c.user)
        initiativeList = [ initiativeLib.getInitiative(followObj['initiativeCode']) for followObj in iwatching ]
        for i in initiativeList:
            if i.objType == 'initiative':
                if i['public'] == '1':
                    if i['deleted'] != '1':
                        items['watching'].append(i)
                else:
                    if 'user' in session and ((c.user['email'] == c.authuser['email']) or c.isAdmin):
                        items['watching'].append(i)


        listenerList = listenerLib.getListenersForUser(c.user, disabled = '0')
        items['listening'] = []
        for l in listenerList:
            lw = workshopLib.getWorkshopByCode(l['workshopCode'])
            items['listening'].append(lw)
                
        items['facilitating'] = []
        for workshop in c.facilitatorWorkshops:
            if workshop['public_private'] == 'public' or (isUser or isAdmin):
                items['facilitating'].append(workshop)
            
        
        # Already checks for disabled/deleted by default
        # The following section feels like a good candidate for map/reduce
        createdThings = userLib.getUserPosts(user)
        items['resources'] = []
        items['discussions'] = []
        items['ideas'] = []
        items['initiatives'] = []
        items['searchWorkshops'] = []
        items['searchUsers'] = []
        for thing in createdThings:
            if 'workshopCode' in thing:
                if thing['disabled'] == '0' and thing['deleted'] == '0':
                    w = workshopLib.getWorkshopByCode(thing['workshopCode'])
                    if workshopLib.isPublished(w) or isAdmin:
                        if w['public_private'] == 'public' and thing['disabled'] != '1' and thing['deleted'] != '1' or (isUser or isAdmin):
                            if thing.objType == 'resource':
                                items['resources'].append(thing)
                            elif thing.objType == 'discussion':
                                items['discussions'].append(thing)
                            elif thing.objType == 'idea':
                                items['ideas'].append(thing)
            elif 'initiativeCode' in thing and thing.objType == 'resource' and ('initiative_public' in thing and thing['initiative_public'] == '1') and thing['deleted'] == '0':
                items['resources'].append(thing)
            elif thing.objType == 'initiative' and thing['public'] == '1' and thing['public'] == '1' and thing['deleted'] == '0':
                items['initiatives'].append(thing)
        return items

    @h.login_required
    def edit(self, id1, id2):
        c.events = eventLib.getParentEvents(c.user)
        if userLib.isAdmin(c.authuser.id) or c.user.id == c.authuser.id and not c.privs['provisional']:
            c.title = 'Edit Profile'
            if 'confTab' in session:
                c.tab = session['confTab']
                session.pop('confTab')
                session.save()
            if userLib.isAdmin(c.authuser.id):
                c.admin = True
            else:
                c.admin = False
                
            return render('/derived/6_profile_edit.bootstrap')
        else:
            abort(404)

    @h.login_required
    def csv(self, id1, id2):
        c.events = eventLib.getParentEvents(c.user)
        if userLib.isAdmin(c.authuser.id) or c.user.id == c.authuser.id and not c.privs['provisional']:
            c.title = 'Edit Profile'
            if 'confTab' in session:
                c.tab = session['confTab']
                session.pop('confTab')
                session.save()
            if userLib.isAdmin(c.authuser.id):
                c.admin = True
            else:
                c.admin = False
                
            return render('/derived/6_profile_csv.bootstrap')
        else:
            abort(404)

    @h.login_required
    def infoEditHandler(self,id1, id2):
        perror = 0
        perrorMsg = ""
        changeMsg = ""
        nameChange = False
        postalChange = False
        anyChange = False
        name = False
        email = False
        postalCode = False
        picture = False
        greetingMsg = False
        websiteLink = False
        websiteDesc = False
        
        now = datetime.datetime.now()
        SQLtoday = now.strftime("%Y-%m-%d")

        # make sure they are authorized to do this
        if c.user.id != c.authuser.id and userLib.isAdmin(c.authuser.id) != 1 and not c.privs['provisional']:
            abort(404)
            
        session['confTab'] = "tab1"
        session.save()
        
        payload = json.loads(request.body)
        if 'member_name' in payload:
            name = payload['member_name']
            if name == '':
               name = False
        if not name:
            perror = 1
            perrorMsg = perrorMsg + ' Member name required.'

        if 'email' in payload:
            email = payload['email']
            if email == '':
                email = False
            elif email != c.user['email']:
                checkUser = userLib.getUserByEmail(email)
                if checkUser:
                    perror = 1
                    perrorMsg = perrorMsg + ' Email address ' + email + ' is already in use by other member!'
                    email = c.user['email']
        if not email:
            perror = 1
            perrorMsg = perrorMsg + ' Email required.'
        
        if 'postalCode' in payload:
            postalCode = payload['postalCode']
            if postalCode == '':
                postalCode = False
            elif postalCode != c.user['postalCode']:
                # first, make sure it is valid
                checkPostal = geoInfoLib.getPostalInfo(postalCode)
                if checkPostal == None:
                    log.info("Error: Bad Postal Code in profile edit")
                    perror = 1
                    perrorMsg = perrorMsg + ' No such postal code: ' + postalCode
                    postalCode = c.user['postalCode']
        if not postalCode:
            perror = 1
            perrorMsg = perrorMsg + ' Postal code required.'

        if 'greetingMsg' in payload:
            greetingMsg = payload['greetingMsg']


        if 'websiteLink' in payload:
            websiteLink = payload['websiteLink']

        if 'websiteDesc' in payload:
            websiteDesc = payload['websiteDesc']

        if name and name != '' and name != c.user['name']:
            c.user['name'] = name
            nameChange = True
            anyChange = True
            changeMsg = changeMsg + "Member name updated. "
        if email and email != '' and email != c.user['email']:
            c.user['email'] = email
            anyChange = True
            changeMsg = changeMsg + "Member email updated. "
        if postalCode and postalCode != '' and postalCode != c.user['postalCode']:
            c.user['postalCode'] = postalCode
            anyChange = True
            changeMsg = changeMsg + "Postal code updated. "
            # get the previous geo scope info
            gList = geoInfoLib.getGeoInfo(c.user.id)
            # deactivate and disable any existing geocodes
            for g in gList:
                if g['disabled'] == u'0':
                    g['disabled'] = u'1'
                    g['deactivated'] = SQLtoday
                    dbHelpers.commit(g)
                    
            # make a new one
            g = geoInfoLib.GeoInfo(postalCode, 'United States', c.user.id)
            c.geoInfo = []
            c.geoInfo.append(g)
            postalChange = True
            
        if greetingMsg and greetingMsg != '' and greetingMsg != c.user['greetingMsg']:
            c.user['greetingMsg'] = greetingMsg
            anyChange = True
            changeMsg = changeMsg + "Greeting message updated. "
        if websiteLink and websiteLink != '' and websiteLink != c.user['websiteLink']:
            anyChange = True
            changeMsg = changeMsg + "Website link updated. "
            if not websiteLink.startswith('http://'):
                websiteLink = u'http://' + websiteLink
            c.user['websiteLink'] = websiteLink
        if websiteDesc and websiteDesc != ''and websiteDesc != c.user['websiteDesc']:
            anyChange = True
            changeMsg = changeMsg + "Website description updated. "
            c.user['websiteDesc'] = websiteDesc

        if nameChange:
            c.user['url'] = urlify(c.user['name'])
            cList = genericLib.getChildrenOfParent(c.user)
            for child in cList:
                if child.objType in ['idea', 'resource', 'discussion', 'comment', 'photo']:
                    child['user_name'] = c.user['name']
                    child['user_url'] = c.user['url']
                    dbHelpers.commit(child)
                
            if c.user.id == c.authuser.id:
                session["userURL"] = c.user['url']
                session.save()
                c.authuser = c.user
            log.info('Changed name')
            
        returnURL = "/profile/" + c.user['urlCode'] + "/" + c.user['url']
        if anyChange and perror == 0:
            dbHelpers.commit(c.user)
            eventLib.Event('Profile updated.', changeMsg, c.user, c.authuser)
            revisionLib.Revision(c.authuser, c.user)
            if postalChange:
                statusCode = 2
            else:
                statusCode = 0
            return json.dumps({'statusCode':statusCode, 'result':changeMsg, 'returnURL':returnURL})

        elif perror == 1:
            return json.dumps({'statusCode':'1', 'result':perrorMsg, 'returnURL':returnURL})
        else:
            return json.dumps({'statusCode':'1', 'result':'No changes submitted.'})

    @h.login_required
    def pictureUploadHandler(self, id1, id2):
        """
            Ideally:  
            1) User selects image, gets presented with aspect-ratio constrained selection.
            2) User adjusts centering and dimensions, hits 'start'
            3) Process image - detailed below
        
            Grab the uploaded file.  Hash and save the original first.  Then process.
            Processing means:
            1) Check to ensure it is an image (should be done in the hash + save step)
            2) Check for square dimensions.  If not square, crop.  Do not save the image here, just pass on the image object.
            3) If necessary, resize the dimensions of the image to 200px x 200px.  Save the final image here.
            
            The client expects a json-encoded string with the following format:
            
            {"files": [
              {
                "name": "picture1.jpg",
                "size": 902604,
                "url": "http:\/\/example.org\/files\/picture1.jpg",
                "thumbnail_url": "http:\/\/example.org\/files\/thumbnail\/picture1.jpg",
                "delete_url": "http:\/\/example.org\/files\/picture1.jpg",
                "delete_type": "DELETE"
              },
              {
                "name": "picture2.jpg",
                "size": 841946,
                "url": "http:\/\/example.org\/files\/picture2.jpg",
                "thumbnail_url": "http:\/\/example.org\/files\/thumbnail\/picture2.jpg",
                "delete_url": "http:\/\/example.org\/files\/picture2.jpg",
                "delete_type": "DELETE"
              }
            ]}
        """
        if (c.authuser.id != c.user.id) or c.privs['provisional']:
            abort(404)
        
        requestKeys = request.params.keys()
        if 'files[]' in requestKeys:
            file = request.params['files[]']
            filename = file.filename
            file = file.file
            image = imageLib.openImage(file)
            if not image:
                abort(404) # Maybe make this a json response instead
            imageHash = imageLib.generateHash(filename, c.authuser)
            image = imageLib.saveImage(image, imageHash, 'avatar', 'orig', thing = c.authuser)
            
            width = min(image.size)
            x = 0
            y = 0
            if 'width' in request.params:
                width = request.params['width']
                if not width or width == 'undefined':
                    width = 100
                else:
                    width = int(float(width))
            if 'x' in request.params:
                x = request.params['x']
                if not x or x == 'undefined':
                    x = 0
                else:
                    x = int(float(x))
            if 'y' in request.params:
                y = request.params['y']
                if not y or y == 'undefined':
                    y = 0
                else:
                    y = int(float(y))
            dims = {'x': x, 
                    'y': y, 
                    'width':width,
                    'height':width}
            clientWidth = -1
            clientHeight = -1
            if 'clientWidth' in request.params:
                clientWidth = request.params['clientWidth']
                if not clientWidth or clientWidth == 'null':
                    clientWidth = -1
            if 'clientHeight' in request.params:
                clientHeight = request.params['clientHeight']
                if not clientHeight or clientHeight == 'null':
                    clientHeight = -1
            image = imageLib.cropImage(image, imageHash, dims, clientWidth = clientWidth, clientHeight = clientHeight)
            image = imageLib.resizeImage(image, imageHash, 200, 200)
            image = imageLib.saveImage(image, imageHash, 'avatar', 'avatar')
            image = imageLib.resizeImage(image, imageHash, 100, 100)
            image = imageLib.saveImage(image, imageHash, 'avatar', 'thumbnail')
            
            jsonResponse =  {'files': [
                                {
                                    'name':filename,
                                    'thumbnail_url':'/images/avatar/%s/avatar/%s.png' %(c.authuser['directoryNum_avatar'], imageHash)
                                }
                            ]}
            return json.dumps(jsonResponse)
        else:
            abort(404)
            
    @h.login_required
    def photoUploadHandler(self, id1, id2):
        """
            Ideally:  
            1) User selects image, gets presented with aspect-ratio constrained selection.
            2) User adjusts centering and dimensions, hits 'start'
            3) Process image - detailed below
        
            Grab the uploaded file.  Hash and save the original first.  Then process.
            Processing means:
            1) Check to ensure it is an image (should be done in the hash + save step)
            2) Check for square dimensions.  If not square, crop.  Do not save the image here, just pass on the image object.
            3) If necessary, resize the dimensions of the image to 1200px x 1200px.  Save the final image here.
            
            The client expects a json-encoded string with the following format:
            
            {"files": [
              {
                "name": "picture1.jpg",
                "size": 902604,
                "url": "http:\/\/example.org\/files\/picture1.jpg",
                "thumbnail_url": "http:\/\/example.org\/files\/thumbnail\/picture1.jpg",
                "delete_url": "http:\/\/example.org\/files\/picture1.jpg",
                "delete_type": "DELETE"
              },
              {
                "name": "picture2.jpg",
                "size": 841946,
                "url": "http:\/\/example.org\/files\/picture2.jpg",
                "thumbnail_url": "http:\/\/example.org\/files\/thumbnail\/picture2.jpg",
                "delete_url": "http:\/\/example.org\/files\/picture2.jpg",
                "delete_type": "DELETE"
              }
            ]}
        """
        if (c.authuser.id != c.user.id) or c.privs['provisional']:
            abort(404)
        
        requestKeys = request.params.keys()
        title = "Sample Title"
        description = "Sample Description"
        tags = "|"
        scope = "||0||0||0||0|0"
        
        # first make sure the title, description, tag and location are set
        if 'files[]' in requestKeys:
            file = request.params['files[]']
            filename = file.filename
            file = file.file
            image = imageLib.openImage(file)
            if not image:
                abort(404) # Maybe make this a json response instead
            imageHash = imageLib.generateHash(filename, c.authuser)
            
            # make the photo object
            photo = photoLib.Photo(c.authuser, title, description, tags, scope)
            image = imageLib.saveImage(image, imageHash, 'photos', 'orig', thing = photo)
            
            width = min(image.size)
            x = 0
            y = 0
            if 'width' in request.params:
                width = request.params['width']
                if not width or width == 'undefined':
                    width = 100
                else:
                    width = int(float(width))
            if 'x' in request.params:
                x = request.params['x']
                if not x or x == 'undefined':
                    x = 0
                else:
                    x = int(float(x))
            if 'y' in request.params:
                y = request.params['y']
                if not y or y == 'undefined':
                    y = 0
                else:
                    y = int(float(y))
            dims = {'x': x, 
                    'y': y, 
                    'width':width,
                    'height':width}
            clientWidth = -1
            clientHeight = -1
            if 'clientWidth' in request.params:
                clientWidth = request.params['clientWidth']
                if not clientWidth or clientWidth == 'null':
                    clientWidth = -1
            if 'clientHeight' in request.params:
                clientHeight = request.params['clientHeight']
                if not clientHeight or clientHeight == 'null':
                    clientHeight = -1
            image = imageLib.cropImage(image, imageHash, dims, clientWidth = clientWidth, clientHeight = clientHeight)
            image = imageLib.resizeImage(image, imageHash, 480, 480)
            image = imageLib.saveImage(image, imageHash, 'photos', 'photo')
            image = imageLib.resizeImage(image, imageHash, 160, 160)
            image = imageLib.saveImage(image, imageHash, 'photos', 'thumbnail')
            
            jsonResponse =  {'files': [
                                {
                                    'name':filename,
                                    'thumbnail_url':'/images/photos/%s/thumbnail/%s.png' %(photo['directoryNum_photos'], imageHash),
                                    'image_hash':imageHash
                                }
                            ]}
            return json.dumps(jsonResponse)
        else:
            abort(404)
            
    @h.login_required
    def addUser(csvUser):
        csvUser['memberType'] = 100
        csvUser['password'] = "changeThis"
        csvUser['country'] = "United States"
        kwargs = {"needsPassword":"1"}
        u = User(csvUser['email'], csvUser['name'], csvUser['password'], csvUser['country'], csvUser['memberType'], csvUser['zip'], kwargs)
        user = u.u
        if 'laston' in user:
            t = time.localtime(float(user['laston']))
            user['previous'] = time.strftime("%Y-%m-%d %H:%M:%S", t)        
        user['laston'] = time.time()
        #user['activated'] = u'1'
        loginTime = time.localtime(float(user['laston']))
        loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
        commit(user)
        baseURL = c.conf['activation.url']
        url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
        mailLib.sendActivationMail(user['email'], url)
        
    @h.login_required
    def checkUser(csvUser):
        if (csvUser['email'] is None or csvUser['name'] is None or csvUser['zip'] is None):
            return false
        else:
            return true
 
        
    @h.login_required
    def csvUploadHandler(self, id1, id2):
        if (c.authuser.id != c.user.id) or c.privs['provisional']:
            abort(404)
        
        requestKeys = request.params.keys()
        
        if 'files[]' in requestKeys:
            file = request.params['files[]']
            filename = file.filename
            fileitem = file.file
            log.info(file.filename)
            csvFile = csv.saveCsv(file)
            c.csv = csv.parseCsv(csvFile.fullpath)
            for csvUser in c.csv:
                log.info(csvUser)
                if (not (csvUser['email'] == '' or csvUser['zip'] == '')):
                    if (not userLib.getUserByEmail(csvUser['email'])):
                        memberType = 100
                        kwargs = {"needsPassword":"1", "poll":csvUser['poll']}
                        password = "changeThis"
                        country = "United States"
                        u = User(csvUser['email'], csvUser['name'], password, country, memberType, csvUser['zip'], **kwargs)
            return render("/derived/6_profile_csv.bootstrap")
        else:
            abort(404)

    @h.login_required
    def photoUpdateHandler(self, id1, id2, id3):
        
        if c.privs['provisional']:
            abort(404)
            
        photo = photoLib.getPhotoByHash(id3)
        if not photo:
            abort(404)
        
        if 'title' in request.params:
            title = request.params['title']
        else:
            log.info('no title')
            abort(404)
            
        if 'description' in request.params:
            description = request.params['description']
        else:
            log.info('no description')
            abort(404)
            
        newTagStr = '|'    
        if 'categoryTags' in request.params:
            categoryTags = request.params.getall('categoryTags')
            for tag in categoryTags:
                newTagStr = newTagStr + tag + '|'

        if 'geoTagCountry' in request.params:
            country = request.params['geoTagCountry']
        else:
            country = '0'
            
        if 'geoTagState' in request.params:
            state = request.params['geoTagState']
        else:
            state = '0'
            
        if 'geoTagCounty' in request.params:
            county = request.params['geoTagCounty']
        else:
            county = '0'
            
        if 'geoTagCity' in request.params:
            city = request.params['geoTagCity']
        else:
            city = '0'

        if 'geoTagPostal' in request.params:
            postal = request.params['geoTagPostal']
        else:
            postal = '0'
            
        scope = '||' + urlify(country) + '||' + urlify(state) + '||' + urlify(county) + '||' + urlify(city) + '|' + urlify(postal)
            
        photo['title'] = title
        photo['url'] = urlify(title)
        photo['description'] = description
        photo['tags'] = newTagStr
        photo['scope'] = scope
        dbHelpers.commit(photo)
        revisionLib.Revision(c.authuser, photo)
        
        returnURL = "/profile/" + c.user['urlCode'] + "/" + c.user['url'] + "/photos/show"
                
        return redirect(returnURL)
        
        
    @h.login_required
    def setImageSource(self, id1, id2):
        try:
            payload = json.loads(request.body)
            source = payload['source']
        except:
            log.error("User %s tried to set a profile image source for user %s with an unknown source.  Body was %s." %(c.authuser.id, c.user.id, request.body))
            return json.dumps({"statusCode": 1})
        c.user['avatarSource'] = source
        dbHelpers.commit(c.user)
        
        # update in authored objects
        cList = genericLib.getChildrenOfParent(c.user)
        for child in cList:
            if child.objType in ['idea', 'resource', 'discussion', 'comment', 'photo']:
                child['user_avatar'] = utils._userImageSource(c.user)
                dbHelpers.commit(child)
        return json.dumps({"statusCode": 0})
        
    @h.login_required
    def preferencesCommentsHandler(self, id1, id2):
        # initialize to current value if any, '0' if not set in object
        cAlerts = '0'
        eAction = ''
        if 'itemAlerts' in c.user:
            cAlerts = c.user['commentAlerts']
        
        payload = json.loads(request.body)
        if 'alert' not in payload:
            return "Error"
        alert = payload['alert']
        if alert == 'comments':
            if 'commentAlerts' in c.user.keys():
                if c.user['commentAlerts'] == u'1':
                    c.user['commentAlerts'] = u'0'
                    eAction = 'Turned off'
                else:
                    c.user['commentAlerts'] = u'1'
                    eAction = 'Turned on'
            else:
                c.user['commentAlerts'] = u'1'
                eAction = 'Turned on'
        else:
            return "Error"   
        dbHelpers.commit(c.user)
        if eAction != '':
            eventLib.Event('Member comment notifications set', eAction, c.user, c.authuser)
        return eAction      
  
    @h.login_required
    def passwordUpdateHandler(self, id1, id2):
        perror = 0
        perrorMsg = ""
        changeMsg = ""
        # make sure they are authorized to do this
        if c.user.id != c.authuser.id and userLib.isAdmin(c.authuser.id) != 1 or c.privs['provisional']:
            abort(404)      
                    
        session['confTab'] = "tab4"
        session.save()
            
        
        if 'password' in request.params:
            password = request.params['password']

        else:
            password = False 
        if 'verify_password' in request.params:
            verify_password = request.params['verify_password']
        else:
            verify_password = False 

        if password and verify_password and password == verify_password:
            userLib.changePassword(c.user, password)
            changeMsg = changeMsg + "Password updated. "
        if password and verify_password and password != verify_password:
            perror = 1
            perrorMsg = 'Password and Verify Password must match'
        if password or verify_password and password != verify_password:
            perror = 1
            perrorMsg = 'Password and Verify Password must match'

        " FOR CHANGING USE PASSWORD"
        pass_error = 4
        if 'oldPassword' in request.params:
            old_password = userLib.checkPassword(c.authuser, request.params['oldPassword'])
            pass_error = 0
            
            if not old_password:
                pass_error = 2
            if request.params['oldPassword'] == '':
                pass_error = 4
                
        if 'newPassword' in request.params:
            newPassword = request.params['newPassword']
        else:
            pass_error = 1
        if 'reNewPassword' in request.params:
            reNewPassword = request.params['reNewPassword']
        else:
            pass_error = 1
            
        if newPassword == '' or reNewPassword == '' or request.params['oldPassword'] == '':
            pass_error = 1
        elif newPassword != reNewPassword:
            pass_error = 3
                        
        if 'oldPassword' not in request.params and 'newPassword' not in request.params and 'reNewPassword' not in request.params:
            pass_error = 4
        else:
            if request.params['oldPassword'] == '' and request.params['newPassword'] == '' and request.params['reNewPassword'] == '':
                pass_error = 4
            
        if pass_error == 0:
            userLib.changePassword(c.user, newPassword)
            eventLib.Event('Profile updated.', 'Password changed', c.user, c.authuser)
            log.info('changed password for  %s'%c.authuser['name'])
            alert = {'type':'success'}
            alert['title'] = 'Password Change Successful'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
        elif pass_error == 1:
            alert = {'type':'error'}
            alert['title'] = 'Password Change: All Fields Required'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
        elif pass_error == 2:
            alert = {'type':'error'}
            alert['title'] = 'Password Change: Old Password Incorrect'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
        elif pass_error == 3:
            alert = {'type':'error'}
            alert['title'] = 'Password Change: New Passwords Do Not Match'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            
        returnURL = "/profile/" + c.user['urlCode'] + "/" + c.user['url']
                
        return redirect(returnURL)

    @h.login_required
    def enableHandler(self, id1, id2):
        if not userLib.isAdmin(c.authuser.id):
            abort(404)

        session['confTab'] = "tab5"
        session.save()
        
        if 'verifyEnableUser' in request.params and 'enableUserReason' in request.params and len(request.params['enableUserReason']) > 0:
           enableUserReason = request.params['enableUserReason']

           if c.user['disabled'] == '1':
              c.user['disabled'] = '0'
              eAction = 'User Enabled'
              alert = {'type':'success'}
              alert['title'] = 'Enabled:'
              alert['content'] = 'Member Enabled'
           else:
              c.user['disabled'] = '1'
              eAction = 'User Disabled'
              alert = {'type':'warning'}
              alert['title'] = 'Disabled:'
              alert['content'] = 'Member Disabled'
              
           e = eventLib.Event(eAction, enableUserReason, c.user, c.authuser)
           dbHelpers.commit(c.user)
           session['alert'] = alert
           session.save()
        else:
           alert = {'type':'error'}
           alert['title'] = 'Error:'
           alert['content'] = 'Enter reason and verify action before submit'
           session['alert'] = alert
           session.save()

        return redirect("/profile/" + id1 + "/" + id2 + "/edit" )

    @h.login_required
    def privsHandler(self, id1, id2):
        if not userLib.isAdmin(c.authuser.id):
            abort(404)
            
        session['confTab'] = "tab5"
        session.save()
        if 'accessChangeReason' in request.params and request.params['accessChangeReason'] != '' and 'accessChangeVerify' in request.params:
            if c.user['accessLevel'] == '0':
                newAccessTitle = "Admin"
                newAccess = "200"
                oldAccessTitle = "User"
            else:
                newAccessTitle = "User"
                newAccess = "0"
                oldAccessTitle = "Admin"
                
            eAction = 'Access Level Changed from ' + oldAccessTitle + ' to ' + newAccessTitle
            c.user['accessLevel'] = '200'
            accessChangeReason = request.params['accessChangeReason']
            e = eventLib.Event(eAction, accessChangeReason, c.user, c.authuser)
            dbHelpers.commit(c.user)
            alert = {'type':'success'}
            alert['title'] = 'Success:'
            alert['content'] = 'New Access Level Set'
            session['alert'] = alert
            session.save()
        else:
            alert = {'type':'error'}
            alert['title'] = 'Error:'
            alert['content'] = 'Enter reason and specify a new access level'
            session['alert'] = alert
            session.save()

        return redirect("/profile/" + id1 + "/" + id2 + "/edit" )
        
    def unsubscribe(self, id1):
        hash, sep, email = id1.partition('__')
        if c.user['activationHash'] == hash:
            c.user['newsletter_unsubscribe'] = '1'
            dbHelpers.commit(c.user)
            alert = 'You are unsubscribed from the weekly Civinomics newsletter.'
            session['alert'] = alert
            session.save()
            
        returnURL = '/profile/%s/%s'%(c.user['urlCode'], c.user['url'])
        return redirect(returnURL)


