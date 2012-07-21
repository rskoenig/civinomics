import logging

from pylons import request, response, session, tmpl_context as c
from string import capwords
from pylowiki.lib.utils import urlify
from pylowiki.lib.db.geoInfo import geoDeurlify, getPostalInfo, getCityInfo, getCountyInfo, getStateInfo, getGeoScope, getWorkshopScopes

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

import re

log = logging.getLogger(__name__)

class GeoController(BaseController):

    def showPostalInfo(self, id1, id2):
        c.country = geoDeurlify(id1)
        c.postal = id2
        
        c.heading = 'Civinomics: ' + c.country + ' ' + c.postal + ' Information'
        
        c.postalInfo = getPostalInfo(c.postal, c.country)
        c.city = capwords(c.postalInfo['City'])
        c.cityFlag = '/images/flags/country/united-states/city_thumb.png'
        c.county = capwords(c.postalInfo['County'])
        c.countyFlag = '/images/flags/country/united-states/county_thumb.png'
        c.state = capwords(c.postalInfo['StateFullName'])
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        scope = getGeoScope(c.postal, c.country)
        c.wscopes = getWorkshopScopes(scope, 9)
        return render('/derived/postalInfo.bootstrap')

    def showCityInfo(self, id1, id2, id3):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        c.city = geoDeurlify(id3)
        
        c.heading = 'Civinomics: ' + c.country + ' City of ' + c.city + ' Information'
        
        c.cityInfo = getCityInfo(c.city, c.state, c.country)
        c.city = capwords(c.city)
        c.cityFlag = '/images/flags/country/united-states/city_thumb.png'
        c.county = capwords(c.cityInfo['County'])
        c.countyFlag = '/images/flags/country/united-states/county_thumb.png'
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        c.state = capwords(c.cityInfo['StateFullName'])
        scope = '||' + urlify(c.country) + '||' + urlify(c.state) + '||' + urlify(c.county) + '||' + urlify(c.city) + '|' +  '00000'
        c.wscopes = getWorkshopScopes(scope, 8)
        return render('/derived/cityInfo.bootstrap')

    def showCountyInfo(self, id1, id2, id3):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        c.county = geoDeurlify(id3)
        
        c.heading = 'Civinomics: ' + c.country + ' County of ' + c.county + '  Information'
        
        c.countyInfo = getCountyInfo(c.county, c.state, c.country)
        c.county = capwords(c.countyInfo['County'])
        c.countyFlag = '/images/flags/country/united-states/county_thumb.png'
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        c.state = capwords(c.countyInfo['StateFullName'])
        scope = '||' + urlify(c.country) + '||' + urlify(c.state) + '||' + urlify(c.county) + '||' + 'LaLaLa|00000'
        c.wscopes = getWorkshopScopes(scope, 6)
        return render('/derived/countyInfo.bootstrap')

    def showStateInfo(self, id1, id2):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        
        c.heading = 'Civinomics: ' + c.country + ' State of ' + c.state + ' Information'
        c.stateInfo = getStateInfo(c.state, c.country)
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        c.state = capwords(c.stateInfo['StateFullName'])
        scope = '||' + urlify(c.country) + '||' + urlify(c.state) + '||' + 'LaLaLa||LaLaLa|00000'
        c.wscopes = getWorkshopScopes(scope, 4)
        
        return render('/derived/stateInfo.bootstrap')

