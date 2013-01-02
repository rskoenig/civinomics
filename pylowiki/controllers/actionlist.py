# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.page import get_all_pages
from pylowiki.lib.db.workshop import getActiveWorkshops, searchWorkshops, getWorkshopByID, getRecentMemberPosts
from pylowiki.lib.db.survey import getActiveSurveys, getSurveyByID
from pylowiki.lib.db.tag import searchTags
from pylowiki.lib.db.user import searchUsers, getUserByID
from pylowiki.lib.db.geoInfo import getGeoInfo, getUserScopes, getWorkshopScopes, getScopeTitle
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
            c.title = c.heading = 'All Workshops'
            c.list = getActiveWorkshops()

            c.count = len( c.list )
            c.paginator = paginate.Page(
                c.list, page=int(request.params.get('page', 1)),
                items_per_page = 15, item_count = c.count
            )

            #return render('/derived/list_workshops.bootstrap')
            #c.activity = range(12)
            c.activity = getRecentMemberPosts(10)
            return render('derived/6_main_listing.bootstrap')
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

    def help( self ):
        return render('/derived/6_help.bootstrap')

    def searchWorkshops( self, id1, id2  ):
        log.info('searchWorkshops %s %s' % (id1, id2))
        id2 = id2.replace("_", " ")
        c.title = c.heading = 'Search Workshops: ' + id1 + ' ' + id2
        c.list = searchWorkshops(id1, id2)
        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_workshops.bootstrap')

    def searchName( self, id1, id2 ):
        searchType = id1
        searchString = id2
        if searchString == '%':
           searchString = ''
        log.info('searchName')
        if searchType == 'Workshops':
              c.title = c.heading = 'Search Workshops: ' + searchString
              c.list = searchWorkshops('title', searchString)
              c.count = len( c.list )
              c.paginator = paginate.Page(
                  c.list, page=int(request.params.get('page', 1)),
                  items_per_page = 15, item_count = c.count
              )

              return render('/derived/list_workshops.bootstrap')

        else:
              c.title = c.heading = 'Search Members: ' + searchString
              c.list = searchUsers('name', searchString)
              c.count = len( c.list )
              c.paginator = paginate.Page(
                  c.list, page=int(request.params.get('page', 1)),
                  items_per_page = 15, item_count = c.count
              )

              return render('/derived/list_users.bootstrap')

    def searchGeoUsers( self, id1 ):
        log.info('searchGeoUsers')
        scopeLevel = id1
        geoInfo = getGeoInfo(c.authuser.id)
        searchScope = geoInfo[0]['scope']
        ##log.info('geoInfo is %s'%geoInfo)
        c.list = []

        scopeTitle = getScopeTitle(geoInfo[0]['postalCode'], "United States", scopeLevel)
        c.title = c.heading = 'List Members: ' + scopeTitle
        log.info('postalCode is %s scopeLevel is %s'%(geoInfo[0]['postalCode'], scopeLevel))
        scopeList = getUserScopes(searchScope, scopeLevel)
        for gInfo in scopeList:
           c.list.append(getUserByID(gInfo.owner))

        c.count = len( c.list )
        c.paginator = paginate.Page(
                  c.list, page=int(request.params.get('page', 1)),
                  items_per_page = 15, item_count = c.count
              )

        return render('/derived/list_users.bootstrap')

    def searchGeoWorkshops( self ):
        #log.info('searchGeoWorkshops')
        geoInfo = getGeoInfo(c.authuser.id)
        searchScope = geoInfo[0]['scope']
        #log.info('geoInfo is %s'%geoInfo)
        c.list = []
        if 'scopeLevel' in request.params:
           scopeLevel = request.params['scopeLevel']
           scopeTitle = getScopeTitle(geoInfo[0]['postalCode'], "United States", scopeLevel)
           c.title = c.heading = 'List Workshops: ' + scopeTitle
           scopeList = getWorkshopScopes(searchScope, scopeLevel)
           for gInfo in scopeList:
              w = getWorkshopByID(gInfo['workshopID'])
              if w['startTime'] == '0000-00-00' or w['deleted'] == '1':
                  continue
              else:
                  if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) < int(scopeLevel):
                             doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = gInfo['scope'].split('|')
                          sTest = searchScope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:
                              c.list.append(w)

           c.count = len( c.list )
           c.paginator = paginate.Page(
                     c.list, page=int(request.params.get('page', 1)),
                     items_per_page = 15, item_count = c.count
                 )

           return render('/derived/list_workshops.bootstrap')
        else:
           return redirect('/')


    def searchTags( self, id1 ):
        ##log.info('searchTags %s' % id1)
        id1 = id1.replace("_", " ")
        c.title = c.heading = 'Search Workshops by Tag: ' + id1
        tList = searchTags(id1)
        ##log.info('tList %s' % tList)
        c.list = []
        for t in tList:
           ##log.info('t %s' % t)
           w = getWorkshopByID(t['thingID'])
           if w['deleted'] == '0' and w['startTime'] != '0000-00-00':
               c.list.append(getWorkshopByID(t['thingID']))

        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_workshops.bootstrap')

    def searchUsers( self, id1, id2  ):
        log.info('searchUsers %s %s' % (id1, id2))
        id2 = id2.replace("_", " ")
        c.title = c.heading = 'Search Users: ' + id1 + ' ' + id2
        c.list = searchUsers(id1, id2)
        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_users.bootstrap')

