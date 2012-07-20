# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.page import get_all_pages
from pylowiki.lib.db.workshop import getActiveWorkshops, searchWorkshops, getWorkshopByID
from pylowiki.lib.db.survey import getActiveSurveys, getSurveyByID
from pylowiki.lib.db.tag import searchTags
from pylowiki.lib.db.user import searchUsers, getUserByID
from pylowiki.lib.db.geoInfo import getGeoInfo, getUserScopes, getWorkshopScopes
from pylowiki.lib.db.featuredSurvey import getFeaturedSurvey, setFeaturedSurvey

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

log = logging.getLogger(__name__)

class ActionlistController(BaseController):

    def __before__(self):
        if c.conf['public.sitemap'] != "true": 
            h.check_if_login_required()

    def index( self, id ): # id is the action
        """Create a list of pages with the given action/option """
        """Valid actions: edit, revision, delete, restore, sitemap """
        c.action = id
        if c.action == "sitemap":
            c.title = c.heading = c.action
            c.action = ""
            c.list = get_all_pages()
        elif c.action == 'sitemapIssues':
            c.title = c.heading = 'Workshops'
            c.list = getActiveWorkshops()

            c.count = len( c.list )
            c.paginator = paginate.Page(
                c.list, page=int(request.params.get('page', 1)),
                items_per_page = 10, item_count = c.count
            )

            return render('/derived/list_workshops.html')
        elif c.action == 'surveys':
            c.title = c.heading = 'Surveys'
            c.list = getActiveSurveys()
        else:
            c.title = c.heading = "Which " + c.action + "?"

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
            items_per_page = 10, item_count = c.count
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

    def searchWorkshops( self, id1, id2  ):
        log.info('searchWorkshops %s %s' % (id1, id2))
        id2 = id2.replace("_", " ")
        c.title = c.heading = 'Search Workshops: ' + id1 + ' ' + id2
        c.list = searchWorkshops(id1, id2)
        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 10, item_count = c.count
        )

        return render('/derived/list_workshops.html')

    def searchName( self ):
        log.info('searchName')
        if 'searchType' in request.params and 'searchString' in request.params:
           searchType = request.params['searchType']
           searchString = request.params['searchString']

           if searchType == 'Workshops':
              c.title = c.heading = 'Search Workshops: ' + searchString
              c.list = searchWorkshops('title', searchString)
              c.count = len( c.list )
              c.paginator = paginate.Page(
                  c.list, page=int(request.params.get('page', 1)),
                  items_per_page = 10, item_count = c.count
              )

              return render('/derived/list_workshops.html')

           else:
              c.title = c.heading = 'Search Members: ' + searchString
              c.list = searchUsers('name', searchString)
              c.count = len( c.list )
              c.paginator = paginate.Page(
                  c.list, page=int(request.params.get('page', 1)),
                  items_per_page = 10, item_count = c.count
              )

              return render('/derived/list_users.html')
        else:
           return redirect('/')

    def searchGeoUsers( self ):
        log.info('searchGeoUsers')
        c.title = c.heading = 'List Nearby Members'
        geoInfo = getGeoInfo(c.authuser.id)
        searchScope = geoInfo[0]['scope']
        log.info('geoInfo is %s'%geoInfo)
        c.list = []
        if 'scopeLevel' in request.params:
           scopeLevel = request.params['scopeLevel']
           scopeList = getUserScopes(searchScope, scopeLevel)
           for gInfo in scopeList:
              c.list.append(getUserByID(gInfo.owner))

           c.count = len( c.list )
           c.paginator = paginate.Page(
                     c.list, page=int(request.params.get('page', 1)),
                     items_per_page = 10, item_count = c.count
                 )

           return render('/derived/list_users.html')
        else:
           return redirect('/')

    def searchGeoWorkshops( self ):
        log.info('searchGeoWorkshops')
        c.title = c.heading = 'List Nearby Workshops'
        geoInfo = getGeoInfo(c.authuser.id)
        searchScope = geoInfo[0]['scope']
        log.info('geoInfo is %s'%geoInfo)
        c.list = []
        if 'scopeLevel' in request.params:
           scopeLevel = request.params['scopeLevel']
           scopeList = getWorkshopScopes(searchScope, scopeLevel)
           for gInfo in scopeList:
              w = getWorkshopByID(gInfo['workshopID'])
              if w['startTime'] != '0000-00-00' and w['deleted'] != '1':
                  if w not in c.list:
                      c.list.append(w)

           c.count = len( c.list )
           c.paginator = paginate.Page(
                     c.list, page=int(request.params.get('page', 1)),
                     items_per_page = 10, item_count = c.count
                 )

           return render('/derived/list_workshops.html')
        else:
           return redirect('/')


    def searchTags( self, id1 ):
        log.info('searchTags %s' % id1)
        id1 = id1.replace("_", " ")
        c.title = c.heading = 'Search Workshops by Tag: ' + id1
        tList = searchTags(id1)
        log.info('tList %s' % tList)
        c.list = []
        for t in tList:
           log.info('t %s' % t)
           c.list.append(getWorkshopByID(t['thingID']))

        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 10, item_count = c.count
        )

        return render('/derived/list_workshops.html')

    def searchUsers( self, id1, id2  ):
        log.info('searchUsers %s %s' % (id1, id2))
        id2 = id2.replace("_", " ")
        c.title = c.heading = 'Search Users: ' + id1 + ' ' + id2
        c.list = searchUsers(id1, id2)
        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 10, item_count = c.count
        )

        return render('/derived/list_users.html')

