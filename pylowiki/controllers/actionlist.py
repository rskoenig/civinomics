# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.page import get_all_pages
from pylowiki.lib.db.workshop import getActiveWorkshops, searchWorkshops, getWorkshopByID, getWorkshopByCode
from pylowiki.lib.db.activity import getRecentActivity
from pylowiki.lib.db.survey import getActiveSurveys, getSurveyByID
from pylowiki.lib.db.tag import searchTags
from pylowiki.lib.db.user import searchUsers, getUserByID, getUserByCode, searchOrganizations
from pylowiki.lib.db.geoInfo import getGeoInfo, getUserScopes, getWorkshopScopes, getScopeTitle
from pylowiki.lib.db.featuredSurvey import getFeaturedSurvey, setFeaturedSurvey
import pylowiki.lib.db.initiative as initiativeLib
import pylowiki.lib.utils as utils

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config
import datetime
import webhelpers.feedgenerator as feedgenerator

log = logging.getLogger(__name__)

class ActionlistController(BaseController):

    def __before__(self):
        if c.conf['public.sitemap'] != "true": 
            h.check_if_login_required()

    # function is depricated
    '''
    def index( self, id ): # id is the action
    
        """Create a list of pages with the given action/option """
        """Valid actions: edit, revision, delete, restore, sitemap """
        c.title = c.heading = c.workshopTitlebar = 'All Workshops'
        c.list = getActiveWorkshops()
        c.activity = getRecentActivity(20)
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
    '''

    def rss( self ):
        c.activity = getRecentActivity(30)
        feed = feedgenerator.Rss201rev2Feed(
            title=u"Civinomics Workshop Activity Feed",
            link=u"http://www.civinomics.com",
            description=u"The most recent activity in Civinomics public workshops and initiatives.",
            language=u"en"
        )
        for item in c.activity:
            thisUser = getUserByID(item.owner)
            if item.objType == 'comment':
                continue
            if 'workshopCode' in item:
                parent = getWorkshopByCode(item['workshopCode'])
                baseURL = config['site_base_url'] + "/workshop/" + parent['urlCode'] + "/" + parent['url']
                baseTitle = 'the workshop named <a href="' + baseURL + '">' + parent['title'] + '</a>'
            elif 'initiativeCode' in item or item.objType == 'initiative':
                if 'initiativeCode' in item:
                    parent = initiativeLib.getInitiative(item['initiativeCode'])
                else:
                    parent = item
                baseURL = config['site_base_url'] + "/initiative/" + parent['urlCode'] + "/" + parent['url']
                baseTitle = 'the initiative named "<a href="' + baseURL + '">' + parent['title'] + '</a>"'
            elif item.objType == 'photo':
                parent = thisUser
                baseURL = config['site_base_url'] + "/profile/" + parent['urlCode'] + "/" + parent['url']
            elif 'scope' in item:
                baseURL = config['site_base_url'] + item.objType + "/" + item['urlCode'] + "/" + item['url']
                scope = utils.getPublicScope(item)
                baseTitle = scope['scopeString']
                itemURL = baseURL
            
            
            activityStr = ""
            userName = thisUser['name']
            if item.objType == 'resource':
               activityStr += 'A new resource added to ' + baseTitle + ' by ' + userName
            elif item.objType == 'discussion':
                if 'initiativeCode' in item:
                    activityStr += 'A new progress report added to ' + baseTitle + ' by ' + userName
                else:
                    activityStr += 'A new discussion started in ' + baseTitle + ' by ' + userName
            elif item.objType == 'idea':
                activityStr += 'A new idea posed in ' + baseTitle + ' by ' + userName
            elif item.objType == 'initiative':
                activityStr += 'A new initiative launched by ' + userName
                itemURL = baseURL
            elif item.objType == 'photo':
                activityStr += 'A new photo added by ' + userName
                itemURL = baseURL + "/" + item.objType + "/show/" + item['urlCode']

            #activityStr += '"' + item['title'] + '"'
            if 'workshopCode' in item:
                itemURL = baseURL + "/" + item.objType + "/" + item['urlCode'] + "/" + item['url']
            elif 'initiativeCode' in item:
                if item.objType == 'discussion':
                    itemURL = baseURL + '/updateShow/' + item['urlCode']
                else:
                    itemURL = baseURL + "/" + item.objType + "/" + item['urlCode'] + "/" + item['url']
            
            itemTitle = '<a href="' + itemURL + '">' + item['title'] + '</a>'
                
            feed.add_item(title=item['title'], link=itemURL, guid=itemURL, description=activityStr)
            
        response.content_type = 'application/xml'

        return feed.writeString('utf-8')

    # function is depricated
    '''
    def searchTags( self, id1 ):
        id1 = id1.replace("_", " ")
        c.title = c.heading = 'Search Workshops by Tag: ' + id1
        tList = searchTags(id1)
        c.list = []
        """return all the thingIDs that are tags with title id1 """
        for t in tList:
            w = getWorkshopByCode(t['workshopCode'])
            if w['deleted'] == '0' and w['published'] == '1' and w['public_private'] == 'public':
                c.list.append(getWorkshopByCode(t['workshopCode']))

        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        c.activity = getRecentActivity(20)
        c.scope = {'level':'earth', 'name':'all'}
        c.rssURL = "/activity/rss"

        return render('/derived/6_main_listing.bootstrap')
    '''




