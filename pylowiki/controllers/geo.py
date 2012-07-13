import logging

from pylons import request, response, session, tmpl_context as c
from pylowiki.lib.utils import urlify
from pylowiki.lib.db.geoInfo import geoDeurlify, getPostalInfo, getCityInfo, getCountyInfo, getStateInfo

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
        return render('/derived/postalinfo.mako')

    def showCityInfo(self, id1, id2, id3):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        c.city = geoDeurlify(id3)
        
        c.heading = 'Civinomics: ' + c.country + ' City of ' + c.city + ' Information'
        
        c.cityInfo = getCityInfo(c.city, c.state, c.country)
        return render('/derived/cityinfo.mako')

    def showCountyInfo(self, id1, id2, id3):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        c.county = geoDeurlify(id3)
        
        c.heading = 'Civinomics: ' + c.country + ' County of ' + c.county + '  Information'
        
        c.countyInfo = getCountyInfo(c.county, c.state, c.country)
        return render('/derived/countyinfo.mako')

    def showStateInfo(self, id1, id2):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        
        c.heading = 'Civinomics: ' + c.country + ' State of ' + c.state + ' Information'
        
        c.stateInfo = getStateInfo(c.state, c.country)
        return render('/derived/stateinfo.mako')

