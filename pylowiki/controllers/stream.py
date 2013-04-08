# -*- coding: utf-8 -*-
import logging
import datetime

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.page import get_all_pages
from pylowiki.lib.db.workshop import getActiveWorkshops, searchWorkshops, getWorkshopByID, getWorkshopByCode, getRecentMemberPosts
from pylowiki.lib.db.survey import getActiveSurveys, getSurveyByID
from pylowiki.lib.db.tag import searchTags
from pylowiki.lib.db.user import searchUsers, getUserByID
from pylowiki.lib.db.geoInfo import getGeoInfo, getUserScopes, getWorkshopScopes, getScopeTitle
from pylowiki.lib.db.featuredSurvey import getFeaturedSurvey, setFeaturedSurvey
from pylons import config

import pylowiki.lib.db.follow           as followLib
import pylowiki.lib.db.facilitator      as facilitatorLib
import webhelpers.paginate              as paginate
import pylowiki.lib.helpers             as h
import webhelpers.feedgenerator         as feedgenerator
import pylowiki.lib.db.workshop         as workshopLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.message          as messageLib
import pylowiki.lib.db.pmember          as pMemberLib

log = logging.getLogger(__name__)

class StreamController(BaseController):

    def __before__(self, action, id1 = None, id2 = None):
        if action not in ['hashPicture']:
            if id1 is not None and id2 is not None:
                c.user = userLib.get_user(id1, id2)
                if not c.user:
                    abort(404)
            else:
                abort(404)
            c.isAdmin = False
            if 'user' in session:
                if userLib.isAdmin(c.authuser.id):
                    c.isAdmin = True
                if c.user.id == c.authuser.id or c.isAdmin:
                    c.messages = messageLib.getMessages(c.user)
                    c.unreadMessageCount = messageLib.getMessages(c.user, read = u'0', count = True)


    def index( self, id ): # id is the action
        """Create a list of pages with the given action/option """
        """Valid actions: edit, revision, delete, restore, sitemap """
        c.title = c.heading = c.workshopTitlebar = 'All Workshops'
        c.list = getActiveWorkshops()
        c.activity = getRecentMemberPosts(10)
        c.scope = {'level':'earth', 'name':'all'}
        c.rssURL = "/activity/rss"
        return render('derived/6_main_listing.bootstrap')

        if c.action == "restore":
            c.list = get_all_pages(1)

        if 'user' in session:
            if not c.authuser:
                session.delete()
                return redirect('/')
            items = []
            userZip = int(c.authuser['postalCode'])
            for item in c.list:
                itemZip = map(int, item['publicPostalList'].split(','))
                if userZip in itemZip:
                    items.append(item)
            c.list = items
            
        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )
        if len(c.list) >= 1:
            featuredSurvey = getFeaturedSurvey()
            if not featuredSurvey:
                setFeaturedSurvey(c.list[0])
                c.mainSurvey = c.list[0]
                c.surveys = c.list[1:]
            else:
                featuredSurveyID = int(featuredSurvey['survey'])
                featuredSurvey = getSurveyByID(featuredSurveyID)
                log.info(featuredSurvey['active'])
                if int(featuredSurvey['active']) == 0:
                    c.mainSurvey = None
                else:
                    c.mainSurvey = featuredSurvey
                for i in range(len(c.list)):
                    if c.list[i].id == featuredSurveyID:
                        c.list.pop(i)
                        break
                c.surveys = c.list
        else:
            c.mainSurvey = []
        return render('/derived/list_surveys.bootstrap')
    

    def stream( self ):  
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

        facilitatorList = facilitatorLib.getFacilitatorsByUser(c.user)
        c.facilitatorWorkshops = []
        c.pendingFacilitators = []
        for f in facilitatorList:
           if 'pending' in f and f['pending'] == '1':
              c.pendingFacilitators.append(f)
           elif f['disabled'] == '0':
              myW = workshopLib.getWorkshopByCode(f['workshopCode'])
              if not workshopLib.isPublished(myW) or myW['public_private'] != 'public':
                 # show to the workshop owner, show to the facilitator owner, show to admin
                 if 'user' in session: 
                     if c.authuser.id == f.owner or userLib.isAdmin(c.authuser.id):
                         c.facilitatorWorkshops.append(myW)
              else:
                    c.facilitatorWorkshops.append(myW)

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
 
        interestedList = [workshop['urlCode'] for workshop in c.interestedWorkshops]
        
        listenerList = listenerLib.getListenersForUser(c.user, disabled = '0')
        c.pendingListeners = []
        c.listeningWorkshops = []
        for l in listenerList:
            if 'pending' in l and l['pending'] == '1':
                c.pendingListeners.append(l)
            else:
                lw = workshopLib.getWorkshopByCode(l['workshopCode'])
                c.listeningWorkshops.append(lw)
        
        c.privateWorkshops = []
        if 'user' in session and c.authuser:
            if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                privateList = pMemberLib.getPrivateMemberWorkshops(c.user, deleted = '0')
                if privateList:
                    c.privateWorkshops = [workshopLib.getWorkshopByCode(pMemberObj['workshopCode']) for pMemberObj in privateList]

        following = followLib.getUserFollows(c.user) # list of follow objects
        c.following = [userLib.getUserByCode(followObj['userCode']) for followObj in following] # list of user objects


        return render("/derived/6_stream.bootstrap")


    def rss( self ):
        c.activity = getRecentMemberPosts(30)
        feed = feedgenerator.Rss201rev2Feed(
            title=u"Civinomics Workshop Activity Feed",
            link=u"http://www.civinomics.com",
            description=u"The most recent activity in Civinomics public workshops.",
            language=u"en"
        )
        for item in c.activity:
            w = getWorkshopByCode(item['workshopCode'])
            wURL = config['site_base_url'] + "/workshop/" + w['urlCode'] + "/" + w['url'] + "/"
            
            thisUser = getUserByID(item.owner)
            activityStr = thisUser['name'] + " "
            if item.objType == 'resource':
               activityStr += 'added the resource '
            elif item.objType == 'discussion':
               activityStr += 'started the discussion '
            elif item.objType == 'idea':
                activityStr += 'posed the idea '

            activityStr += '"' + item['title'] + '"'
            wURL += item.objType + "/" + item['urlCode'] + "/" + item['url']
            feed.add_item(title=activityStr, link=wURL, guid=wURL, description='')
            
        response.content_type = 'application/xml'

        return feed.writeString('utf-8')


