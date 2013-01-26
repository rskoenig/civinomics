import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

import pylowiki.lib.utils           as utils
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.workshop     as workshopLib

from string import capwords
import simplejson as json
import re

log = logging.getLogger(__name__)

class GeoController(BaseController):

    def __before__(self, action, country = '0', state = '0', county = '0', city = '0', postalCode = '0'):
        if action != 'workshopSearch':
            # We aren't rendering a page, and instead are drilling down geo scope for workshop config
            return
        c.title = c.heading = 'Public workshops in '
        
        if country == '0':
            c.scope = 'planet'
            scopeLevel = '01'
            location = 'earth'
        elif state == '0':
            c.scope = 'country'
            scopeLevel = '03'
            location = country
        elif county == '0':
            c.scope = 'state'
            scopeLevel = '05'
            location = state
        elif city == '0':
            c.scope = 'county'
            scopeLevel = '07'
            location = county
        elif postalCode == '0':
            c.scope = 'city'
            scopeLevel = '09'
            location = city
        else:
            c.scope = 'postalCode'
            scopeLevel = '10'
            location = postalCode
        c.title += capwords(geoInfoLib.geoDeurlify(location))
        c.heading += capwords(geoInfoLib.geoDeurlify(location))
        c.workshopTitlebar = capwords(geoInfoLib.geoDeurlify(location)) + ' workshops'
        
        # Find all workshops within the filtered area
        country = capwords(geoInfoLib.geoDeurlify(country))
        state = capwords(geoInfoLib.geoDeurlify(state))
        county = capwords(geoInfoLib.geoDeurlify(county))
        city = capwords(geoInfoLib.geoDeurlify(city))
        postalCode = capwords(geoInfoLib.geoDeurlify(postalCode))
        scopeList = geoInfoLib.getWorkshopsInScope(country = country, state = state, county = county, city = city, postalCode = postalCode)
        c.list = []
        for scopeObj in scopeList:
            workshop = workshopLib.getActiveWorkshopByCode(scopeObj['workshopCode'])
            if workshop:
                c.list.append(workshop)
        c.activity = []

    def workshopSearch(self, planet = None, country = None, state = None, county = None, city = None, postalCode = None):
        return render('derived/6_main_listing.bootstrap')

    ######################################################################
    # 
    # Used for drilling down geographic scope when selecting scope in workshop config
    # 
    ######################################################################

    def geoHandler(self, id1, id2):
        country = id1
        postalCode = id2

        titles = geoInfoLib.getGeoTitles(postalCode, country)
        return json.dumps({'result':titles})
        
    def geoStateHandler(self, id1):
        country = id1

        states = geoInfoLib.getStateList(country)
        sList = ""
        for state in states:
            if state['StateFullName'] != 'District of Columbia':
                sList = sList + state['StateFullName'] + '|'
        return json.dumps({'result':sList})

    def geoCountyHandler(self, id1, id2):
        country = id1
        state = geoInfoLib.geoDeurlify(id2)
        state = state.title()

        counties = geoInfoLib.getCountyList(country, state)
        cList = ""
        for county in counties:
            cList = cList + county['County'].title() + '|'
        return json.dumps({'result':cList})


    def geoCityHandler(self, id1, id2, id3):
        country = id1
        state = geoInfoLib.geoDeurlify(id2)
        state = state.title()
        county = geoInfoLib.geoDeurlify(id3)
        county = county.upper()

        cities = geoInfoLib.getCityList(country, state, county)
        cList = ""
        for city in cities:
            cList = cList + city['City'].title() + '|'
        return json.dumps({'result':cList})

    def geoPostalHandler(self, id1, id2, id3, id4):
        country = id1
        state = geoInfoLib.geoDeurlify(id2)
        state = state.title()
        county = geoInfoLib.geoDeurlify(id3)
        county = county.upper()
        city = geoInfoLib.geoDeurlify(id4)
        city = city.upper()

        postalCodes = geoInfoLib.getPostalList(country, state, county, city)
        pList = ""
        for postal in postalCodes:
            pList = pList + str(postal['ZipCode']) + '|'
        return json.dumps({'result':pList})

