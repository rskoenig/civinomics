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
from pylowiki.lib.db.user import searchUsers, getUserByID
from pylowiki.lib.db.geoInfo import getGeoInfo, getUserScopes, getWorkshopScopes, getScopeTitle
from pylowiki.lib.db.featuredSurvey import getFeaturedSurvey, setFeaturedSurvey

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

    def index( self, id ): # id is the action
        """Create a list of pages with the given action/option """
        """Valid actions: edit, revision, delete, restore, sitemap """
        c.title = c.heading = c.workshopTitlebar = 'All Workshops'
        c.list = getActiveWorkshops()
        c.activity = getRecentActivity(10)
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
    
    def rss( self ):
        c.activity = getRecentActivity(30)
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


