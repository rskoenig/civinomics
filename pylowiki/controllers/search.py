# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.db.activity     as activityLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.helpers as h

import simplejson as json
from hashlib import md5
log = logging.getLogger(__name__)

class SearchController(BaseController):

    """
        JSON responses:
            statusCode == 0:    Same as unix exit code (OK)
            statusCode == 1:    No query was submitted
            statusCode == 2:    Query submitted, no results found
            result:             The search result, given there was at least one
    """

    def __before__(self, action):
        c.title = c.heading = "Civinomics Search"
        self.query = ''
        self.noQuery = False
        if 'searchQuery' in request.params:
            self.query = request.params['searchQuery']
            if self.query.strip() == '':
                self.noQuery = True
        else:
            self.noQuery = True
    
    def _noSearch(self, noRender = False):
        c.numUsers = 0
        c.numWorkshops = 0
        return render('/derived/6_search.bootstrap')
    
    def search(self):
        if self.noQuery:
            return self._noSearch()
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return self._noSearch()
        c.numUsers = userLib.searchUsers('name', self.query, count = True)
        c.numWorkshops = workshopLib.searchWorkshops(['title', 'description'], [self.query, self.query], count = True)
        return render('/derived/6_search.bootstrap')
    
    def searchPeople(self):
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        people = userLib.searchUsers('name', self.query)
        if len(people) == 0:
            return json.dumps({'statusCode': 2})
        for p in people:
            entry = {}
            entry['name'] = p['name']
            entry['hash'] = md5(p['email']).hexdigest()
            entry['urlCode'] = p['urlCode']
            entry['url'] = p['url']
            userGeo = geoInfoLib.getGeoInfo(p.id)[0]
            entry['cityURL'] = '/workshops/geo/earth/%s/%s/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'], userGeo['countyURL'], userGeo['cityURL'])
            entry['cityTitle'] = userGeo['cityTitle']
            entry['stateURL'] = '/workshops/geo/earth/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'])
            entry['stateTitle'] = userGeo['stateTitle']
            result.append(entry)
        return json.dumps({'statusCode':0, 'result':result})
    
    def searchWorkshops(self):
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        keys = ['title', 'description']
        values = [self.query, self.query]
        workshops = workshopLib.searchWorkshops(keys, values)
        if len(workshops) == 0:
            return json.dumps({'statusCode':2})
        for w in workshops:
            entry = {}
            entry['title'] = w['title']
            entry['description'] = w['description']
            entry['urlCode'] = w['urlCode']
            entry['url'] = w['url']
            entry['activity'] = len(activityLib.getActivityForWorkshop(w['urlCode']))
            entry['bookmarks'] = len(followLib.getWorkshopFollowers(w))
            mainImage = mainImageLib.getMainImage(w)
            entry['imageURL'] = utils.workshopImageURL(w, mainImage, thumbnail = True)
            result.append(entry)
        return json.dumps({'statusCode':0, 'result':result})
        
    def searchItemGeo(self, id1, id2):
        if 'memberButton' in request.params:
            searchItem = "users"
        elif 'workshopButton' in request.params:
            searchItem = "workshops"
        else:
            abort(404)
         
        scopeLevel = 0
        geoScopeTitle = "Planet Earth"
        geoTagString = "||"
        if 'geoTagCountry' in request.params and request.params['geoTagCountry'] != '0':
            geoTagCountry = request.params['geoTagCountry']
            geoScopeTitle = geoTagCountry
            geoTagString += utils.urlify(geoTagCountry) + "||"
            scopeLevel = 2
        else:
            geoTagCountry = "0"
            geoTagString += "||"
            
        if 'geoTagState' in request.params and request.params['geoTagState'] != '0':
            geoTagState = request.params['geoTagState']
            geoScopeTitle = "The State of " + geoTagState
            geoTagString += utils.urlify(geoTagState) + "||"
            scopeLevel = 4
        else:
            geoTagState = "0"
            geoTagString += "||"
            
        if 'geoTagCounty' in request.params and request.params['geoTagCounty'] != '0':
            geoTagCounty = request.params['geoTagCounty']
            geoScopeTitle = "The County of " + geoTagCounty
            geoTagString += utils.urlify(geoTagCounty) + "||"
            scopeLevel = 6
        else:
            geoTagCounty = "0"
            geoTagString += "||"
            
        if 'geoTagCity' in request.params and request.params['geoTagCity'] != '0':
            geoTagCity = request.params['geoTagCity']
            geoScopeTitle = "The City of " + geoTagCity
            geoTagString += utils.urlify(geoTagCity) + "|"
            scopeLevel = 8
        else:
            geoTagCity = "0"
            geoTagString += "|"
            
        if 'geoTagPostal' in request.params and request.params['geoTagPostal'] != '0':
            # no zip code granularity searches for people
            if searchItem == 'workshops':
                geoTagPostal = request.params['geoTagPostal']
                geoTagString += utils.urlify(geoTagPostal)
                scopeLevel = 9
            else:
                geoTagPostal = "0"
        else:
            geoTagPostal = "0"
            
        if searchItem == 'users':
            c.things = []
            c.thingsTitle = 'Members residing in ' + geoScopeTitle
            c.listingType = 'searchUsers'
            uScopeList = geoInfoLib.getUserScopes(geoTagString, scopeLevel)
            for uScope in uScopeList:
                user = userLib.getUserByID(uScope.owner)
                if user['activated'] == '1' and user['disabled'] == '0' and user['deleted'] == '0':
                    c.things.append(user)
                    
        elif searchItem == 'workshops':
            c.things = []
            c.thingsTitle = 'Workshops scoped under ' + geoScopeTitle
            c.listingType = 'searchWorkshops'
            c.things = []
            wScopeList = geoInfoLib.getWorkshopScopes(geoTagString, scopeLevel)
            for wscope in wScopeList:
                workshop = workshopLib.getWorkshopByCode(wscope['workshopCode'])
                if workshopLib.isPublic(workshop) and workshopLib.isPublished(workshop):
                    c.things.append(workshop)
        
        return render('/derived/6_search.bootstrap')
    
    