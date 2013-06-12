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

import pylowiki.lib.db.goal          as goalLib
import pylowiki.lib.db.mainImage     as mainImageLib
import pylowiki.lib.db.follow        as followLib
import pylowiki.lib.db.activity      as activityLib

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config
import datetime
import simplejson as json
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
        #c.list = getActiveWorkshops()
        #c.activity = getRecentActivity(10)
        c.scope = {'level':'earth', 'name':'all'}
        c.rssURL = "/activity/rss"
        return render('derived/6_main_listing.bootstrap')

    def getWorkshops(self):
        result = []
        workshops = getActiveWorkshops()
        for w in workshops:
            thisWorkshop = {}
            goals = goalLib.getGoalsForWorkshop(w) 
            mainImage = mainImageLib.getMainImage(w)
            
            thisWorkshop['title'] = w['title']
            thisWorkshop['description'] = w['description']
            thisWorkshop['urlCode'] = w['urlCode']
            thisWorkshop['url'] = w['url']
            
            # Goals
            # status:   true    ->  done
            #           false   ->  not done
            thisWorkshop['goals'] = []
            for goal in goals:
                status = False
                if goal['status'] == u'100':
                    status = True
                thisWorkshop['goals'].append({  'status': status, 
                                                'title': goal['title']})
                                                
            # mainImage
            if mainImage['pictureHash'] == 'supDawg':
                imgSrc="/images/slide/thumbnail/supDawg.thumbnail"
            elif 'format' in mainImage.keys():
                imgSrc="/images/mainImage/%s/listing/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
            else:
               imgSrc="/images/mainImage/%s/listing/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
            thisWorkshop['imgSrc'] = imgSrc
            
            # Activity/followers
            thisWorkshop['objects'] = activityLib.getActivityCountForWorkshop(w['urlCode'])
            thisWorkshop['followers'] = followLib.getWorkshopFollowers(w, count = True)
            
            result.append(thisWorkshop)
        return json.dumps(result)
        
    def getActivity(self):
        return json.dumps(getRecentActivity(10))
    
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


