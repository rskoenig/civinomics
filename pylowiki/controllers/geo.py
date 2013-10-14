import logging

from pylons import request, response, session, tmpl_context as c, config
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.activity     as activityLib
import webhelpers.feedgenerator     as feedgenerator
import pylowiki.lib.db.user         as userLib

from string import capwords
import simplejson as json
import re
from pylowiki.lib.utils import urlify

log = logging.getLogger(__name__)

class GeoController(BaseController):

    def __before__(self, action, country = '0', state = '0', county = '0', city = '0', postalCode = '0'):
        if action != 'workshopSearch' and action != 'rss':
            # We aren't rendering a page, and instead are drilling down geo scope for workshop config
            return
        c.title = c.heading = 'Public workshops in '
            
        c.rssURL = "/workshops/rss/earth"
        searchScope = '||' + urlify(country) + '||' + urlify(state) + '||' + urlify(county) + '||' + urlify(city) + '|' +  postalCode
        #country = 3, state = 5, county = 7, city = 9, zip = 10
        if country == '0':
            c.scope = {'level':'earth', 'name':'earth'}
            location = 'earth'
            scopeLevel = 0
        elif state == '0':
            c.scope = {'level':'country', 'name':country}
            location = country
            scopeLevel = 2
            c.rssURL += '/%s'%country
        elif county == '0':
            c.scope = {'level':'state', 'name':state}
            location = state
            scopeLevel = 4
            c.rssURL += '/%s/%s'%(country, state)
        elif city == '0':
            c.scope = {'level':'county', 'name':county}
            location = county
            scopeLevel = 6
            c.rssURL += '/%s/%s/%s'%(country, state, county)
        elif postalCode == '0':
            c.scope = {'level':'city', 'name':city}
            location = city
            scopeLevel = 8
            c.rssURL += '/%s/%s/%s/%s'%(country, state, county, city)
        else:
            c.scope = {'level':'postalCode', 'name':postalCode}
            location = postalCode
            scopeLevel = 9
            c.rssURL += '/%s/%s/%s/%s/%s'%(country, state, county, city, postalCode)
            
        c.scopeTitle = capwords(geoInfoLib.geoDeurlify(location))
        c.title += capwords(geoInfoLib.geoDeurlify(location))
        c.heading += capwords(geoInfoLib.geoDeurlify(location))
        c.workshopTitlebar = capwords(geoInfoLib.geoDeurlify(location)) + ' workshops'
        
        # Find all workshops within the filtered area
        c.list = workshopLib.getWorkshopsByScope(searchScope, scopeLevel)
        workshopCodes = []
        for workshop in c.list:
            workshopCodes.append(workshop['urlCode'])
        c.activity = activityLib.getActivityForWorkshops(workshopCodes)

    def workshopSearch(self, planet = '0', country = '0', state = '0', county = '0', city = '0', postalCode = '0'):
        return render('derived/6_main_listing.bootstrap')

    def rss(self, planet = '0', country = '0', state = '0', county = '0', city = '0', postalCode = '0'):
        feed = feedgenerator.Rss201rev2Feed(
            title=u"Civinomics Public Workshop Activity",
            link=u"http://www.civinomics.com",
            description=u'The most recent activity in Civinomics public workshops scoped to %s.'%c.scopeTitle,
            language=u"en"
        )
        for item in c.activity:
            w = workshopLib.getWorkshopByCode(item['workshopCode'])
            wURL = config['site_base_url'] + "/workshop/" + w['urlCode'] + "/" + w['url'] + "/"
            
            thisUser = userLib.getUserByID(item.owner)
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

        try:
            useJson = request.params['json']
            if useJson == '1':
                iPhoneApp = True
            else:
                iPhoneApp = False
        except KeyError:
            iPhoneApp = False
        try:
            states = geoInfoLib.getStateList(country)
            sList = ""
            if states:
                result = states
                statusCode = 0
            else:
                statusCode = 2
                result = "No states"
            if iPhoneApp:
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':statusCode, 'result':result})
            else:
                for state in states:
                    if state['StateFullName'] != 'District of Columbia':
                        sList = sList + state['StateFullName'] + '|'
                return json.dumps({'result':sList})
        except:
            if iPhoneApp:
                statusCode = 2
                result = "No states."
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':statusCode, 'result':result})
            else:
                return json.dumps({'result':"No states."})

    def geoCountyHandler(self, id1, id2):
        country = id1
        state = geoInfoLib.geoDeurlify(id2)
        state = state.title()

        try:
            useJson = request.params['json']
            if useJson == '1':
                iPhoneApp = True
            else:
                iPhoneApp = False
        except KeyError:
            iPhoneApp = False

        try:
            counties = geoInfoLib.getCountyList(country, state)
            cList = ""
            if counties:
                result = counties
                statusCode = 0
            else:
                statusCode = 2
                result = "No counties"
            if iPhoneApp:
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':statusCode, 'result':result})
            else:
                for county in counties:
                    cList = cList + county['County'].title() + '|'
                return json.dumps({'result':cList})
        except:
            if iPhoneApp:
                statusCode = 2
                result = "No counties"
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':statusCode, 'result':result})
            else:
                return json.dumps({'result':"No counties"})

    def geoCityHandler(self, id1, id2, id3):
        country = id1
        state = geoInfoLib.geoDeurlify(id2)
        state = state.title()
        county = geoInfoLib.geoDeurlify(id3)
        county = county.upper()

        try:
            useJson = request.params['json']
            if useJson == '1':
                iPhoneApp = True
            else:
                iPhoneApp = False
        except KeyError:
            iPhoneApp = False

        try:
            cities = geoInfoLib.getCityList(country, state, county)
            cList = ""
            if cities:
                result = cities
                statusCode = 0
            else:
                statusCode = 2
                result = "No cities"
            if iPhoneApp:
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':statusCode, 'result':result})
            else:
                for city in cities:
                    cList = cList + city['City'].title() + '|'
                return json.dumps({'result':cList})
        except:
            if iPhoneApp:
                statusCode = 2
                result = "No cities"
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':statusCode, 'result':result})
            else:
                return json.dumps({'result':"No cities"})

    def geoPostalHandler(self, id1, id2, id3, id4):
        country = id1
        state = geoInfoLib.geoDeurlify(id2)
        state = state.title()
        county = geoInfoLib.geoDeurlify(id3)
        county = county.upper()
        city = geoInfoLib.geoDeurlify(id4)
        city = city.upper()

        try:
            useJson = request.params['json']
            if useJson == '1':
                iPhoneApp = True
            else:
                iPhoneApp = False
        except KeyError:
            iPhoneApp = False

        try:
            postalCodes = geoInfoLib.getPostalList(country, state, county, city)
            pList = ""
            if postalCodes:
                result = postalCodes
                statusCode = 0
            else:
                statusCode = 2
                result = "No zipcodes"
            if iPhoneApp:
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':statusCode, 'result':result})
            else:
                for postal in postalCodes:
                    pList = pList + str(postal['ZipCode']) + '|'
                return json.dumps({'result':pList})
        except:
            if iPhoneApp:
                statusCode = 2
                result = "No zipcodes"
                response.headers['Content-type'] = 'application/json'
                return json.dumps({'statusCode':statusCode, 'result':result})
            else:
                return json.dumps({'result':"No zipcodes"})

    def geoCityStateCountryHandler(self, id1):
        try:
            useJson = request.params['json']
            if useJson == '1':
                iPhoneApp = True
            else:
                iPhoneApp = False
        except KeyError:
            iPhoneApp = False

        postalInfo = geoInfoLib.getPostalInfo(id1)
        if postalInfo:
            city = postalInfo['City'].title()
            state = postalInfo['StateFullName']
            result = city + ", " + state + ', United States'
            statusCode = 0
        else:
            statusCode = 2
            result = "No such zipcode."
        if iPhoneApp:
            response.headers['Content-type'] = 'application/json'
            result = {
                'CityMixedCase': postalInfo['CityMixedCase'], 
                'County': postalInfo['County'], 
                'State': postalInfo['State'],
                'StateFullName': postalInfo['StateFullName']
            }
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return json.dumps({'statusCode':statusCode, 'result':result})
        
    def geoCityStateCountryLinkHandler(self, id1):
        postalInfo = geoInfoLib.getPostalInfo(id1)
        if postalInfo:
            countryTitle = "United States"
            countryURL = "/workshops/geo/earth/united-states"
            stateTitle = postalInfo['StateFullName'].title()
            stateURL = countryURL + "/" + urlify(stateTitle)
            countyURL = stateURL + "/" + urlify(postalInfo['County'])
            cityTitle = postalInfo['City'].title()
            cityURL = countyURL + "/" + urlify(cityTitle)
            statusCode = 0
        else:
            statusCode = 2
            result = "No such zipcode."
        return json.dumps({'statusCode':statusCode, 'cityTitle':cityTitle, 'cityURL':cityURL, 'stateTitle':stateTitle, 'stateURL':stateURL, 'countryTitle':countryTitle, 'countryURL':countryURL})


