import logging

from pylons import request, response, session, tmpl_context as c
from string import capwords
from pylowiki.lib.utils import urlify
from pylowiki.lib.db.geoInfo import geoDeurlify, getPostalInfo, getCityInfo, getCountyInfo, getStateInfo, getGeoScope, getWorkshopScopes
from pylowiki.lib.db.workshop import getWorkshopByID

from pylowiki.lib.base import BaseController, render
import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h

import re

log = logging.getLogger(__name__)

class GeoController(BaseController):

    def showPostalInfo(self, id1, id2):
        c.country = geoDeurlify(id1)
        c.postal = id2
        
        c.heading = "Workshops in Postal Code " + c.postal
        c.geoType = 'postal'
        c.geoInfo = getPostalInfo(c.postal, c.country)
        c.city = capwords(c.geoInfo['City'])
        c.cityFlag = '/images/flags/country/united-states/city_thumb.png'
        c.cityLink = '/geo/city/' + c.country + '/' + urlify(c.geoInfo['StateFullName']) + '/' + urlify(c.geoInfo['City']) 
        c.county = capwords(c.geoInfo['County'])
        c.countyFlag = '/images/flags/country/united-states/county_thumb.png'
        c.countyLink = '/geo/county/' + c.country + '/' + urlify(c.geoInfo['StateFullName']) + '/' + urlify(c.geoInfo['County']) 
        c.state = capwords(c.geoInfo['StateFullName'])
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        c.stateLink = '/geo/state/' + c.country + '/' + urlify(c.geoInfo['StateFullName'])
        c.population = c.geoInfo['Population']
        c.medianAge = c.geoInfo['MedianAge']
        c.numberHouseholds = c.geoInfo['HouseholdsPerZipCode']
        c.personsHousehold = c.geoInfo['PersonsPerHousehold']
        scope = getGeoScope(c.postal, c.country)
        scopeLevel = '10'
        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)
           if w['deleted'] != 1 and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) < int(scopeLevel):
                             doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:
                              c.list.append(w)

        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 10, item_count = c.count
        )
        return render('/derived/list_geo.bootstrap')

    def showCityInfo(self, id1, id2, id3):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        c.city = geoDeurlify(id3)
        
        c.heading = "List Workshops: City of " + capwords(c.city)
        c.geoType = 'city'
        
        c.geoInfo = getCityInfo(c.city, c.state, c.country)
        c.city = capwords(c.city)
        c.cityFlag = '/images/flags/country/united-states/city_thumb.png'
        c.cityLink = '/geo/city/' + c.country + '/' + c.geoInfo['StateFullName'] + '/' + c.geoInfo['City'] 
        c.county = capwords(c.geoInfo['County'])
        c.countyFlag = '/images/flags/country/united-states/county_thumb.png'
        c.countyLink = '/geo/county/' + c.country + '/' + c.geoInfo['StateFullName'] + '/' + c.geoInfo['County'] 
        c.state = capwords(c.geoInfo['StateFullName'])
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        c.stateLink = '/geo/state/' + c.country + '/' + c.geoInfo['StateFullName']
        c.population = c.geoInfo['Population']
        c.medianAge = c.geoInfo['Population_Median']
        c.numberHouseholds = c.geoInfo['Total_Households']
        c.personsHousehold = c.geoInfo['Average_Household_Size']
        scope = '||' + urlify(c.country) + '||' + urlify(c.state) + '||' + urlify(c.county) + '||' + urlify(c.city) + '|' +  '00000'
        scopeLevel = "09"
        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)
           if w['deleted'] != 1 and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) < int(scopeLevel):
                             doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:
                              c.list.append(w)

        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 10, item_count = c.count
        )

        return render('/derived/list_geo.bootstrap')

    def showCountyInfo(self, id1, id2, id3):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        c.county = geoDeurlify(id3)
        
        c.heading = "List Workshops: County of " + capwords(c.county)
        c.geoType = 'county'
        
        c.geoInfo = getCountyInfo(c.county, c.state, c.country)
        c.county = capwords(c.geoInfo['County'])
        c.countyFlag = '/images/flags/country/united-states/county_thumb.png'
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        c.stateLink = '/geo/state/' + c.country + '/' + c.geoInfo['StateFullName']
        c.state = capwords(c.geoInfo['StateFullName'])
        c.population = c.geoInfo['Population']
        c.medianAge = c.geoInfo['Population_Median']
        c.numberHouseholds = c.geoInfo['Total_Households']
        c.personsHousehold = c.geoInfo['Average_Household_Size']
        scope = '||' + urlify(c.country) + '||' + urlify(c.state) + '||' + urlify(c.county) + '||' + 'LaLaLa|00000'
        scopeLevel = "07"
        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)
           if w['deleted'] != 1 and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) < int(scopeLevel):
                             doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:
                              c.list.append(w)


        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 10, item_count = c.count
        )

        return render('/derived/list_geo.bootstrap')

    def showStateInfo(self, id1, id2):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        
        c.heading = "List Workshops: State of " + capwords(c.state)
        c.geoType = 'state'

        c.geoInfo = getStateInfo(c.state, c.country)
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        c.state = capwords(c.geoInfo['StateFullName'])
        c.population = c.geoInfo['Population']
        c.medianAge = c.geoInfo['Population_Median']
        c.numberHouseholds = c.geoInfo['Total_Households']
        c.personsHousehold = c.geoInfo['Average_Household_Size']
        scope = '||' + urlify(c.country) + '||' + urlify(c.state) + '||' + 'LaLaLa||LaLaLa|00000'
        scopeLevel = "05"
        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)
           if w['deleted'] != 1 and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) < int(scopeLevel):
                             doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:
                              c.list.append(w)


        c.count = len( c.list )
        c.paginator = paginate.Page(
            c.list, page=int(request.params.get('page', 1)),
            items_per_page = 10, item_count = c.count
        )

        return render('/derived/list_geo.bootstrap')

