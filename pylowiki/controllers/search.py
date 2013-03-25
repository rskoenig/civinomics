# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.user as userLib
import pylowiki.lib.db.workshop as workshopLib

import pylowiki.lib.helpers as h

import simplejson as json

log = logging.getLogger(__name__)

class SearchController(BaseController):

    def __before__(self):
        c.title = c.heading = "Civinomics Search"
        #h.check_if_login_required()
    
    def _noSearch(self):
        alert = {'type':'info'}
        alert['title'] = '' 
        alert['content'] = 'Searching for nothing yields nothing.  How zen.'
        session['alert'] = alert
        session.save()
        return render('/derived/6_search.bootstrap')
    
    def search(self):
        if 'searchQuery' in request.params:
            query = request.params['searchQuery']
            if query.strip() == '':
                return self._noSearch()
        else:
            return self._noSearch()
        return render('/derived/6_search.bootstrap')
    
    def searchItemName(self):
        if 'searchString' in request.params:
            searchString = request.params['searchString']
        else:
            alert = {'type':'error'}
            alert['title'] = 'Please enter a search string.' 
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            
        if 'memberButton' in request.params:
            c.things = []
            c.thingsTitle = 'Users with name like "' + searchString + '"'
            c.listingType = 'searchUsers'
            userList = userLib.searchUsers('name', searchString)
            for user in userList:
                if user['activated'] == '1' and user['disabled'] == '0' and user['deleted'] == '0':
                    c.things.append(user) 
        elif 'workshopButton' in request.params:
            c.things = []
            c.thingsTitle = 'Workshops with name like "' + searchString + '"'
            c.listingType = 'searchWorkshops'
            workshopList = workshopLib.searchWorkshops('title', searchString)
            for workshop in workshopList:
                if workshopLib.isPublished(workshop) and workshopLib.isPublic(workshop):
                    c.things.append(workshop)
        
        return render('/derived/6_search.bootstrap')
        
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