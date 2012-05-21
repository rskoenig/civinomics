#-*- coding: utf-8 -*-
import _mysql
import sqlalchemy as sa
from sqlalchemy import orm
from pylowiki.model import Thing, Data, meta
from pylowiki.lib.utils import urlify
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl

import time, datetime
import logging
    
log = logging.getLogger(__name__)

def getDB():
    return _mysql.connect("localhost","civinomics","Sisyphus3","geo")

def geoDeurlify( something ):
    deurl = something.replace('-', ' ')
    return deurl 

def getPostalInfo( postal, country ):
    db = getDB()
    myquery = 'SELECT * from US_Postal WHERE ZipCode = ' + postal
    db.query( myquery )
    r = db.store_result()
    rlist = r.fetch_row( 1, 1 )
    return rlist[0]

def getCityInfo( city, state, country ):
    db = getDB()
    myquery = 'SELECT * from US_City WHERE City = \'' + city + '\' AND StateFullName = \'' + state + '\''
    db.query( myquery )
    r = db.store_result()
    rlist = r.fetch_row( 1, 1 )
    return rlist[0]

def getCountyInfo( county, state, country ):
    db = getDB()
    myquery = 'SELECT * from US_County WHERE County = \'' + county + '\' AND StateFullName = \'' + state + '\''
    db.query( myquery )
    r = db.store_result()
    rlist = r.fetch_row( 1, 1 )
    db.close()
    return rlist[0]

def getStateInfo( state, country ):
    db = getDB()
    myquery = 'SELECT * from US_State WHERE StateFullName = \'' + state + '\''
    db.query( myquery )
    r = db.store_result()
    rlist = r.fetch_row( 1, 1 )
    db.close()
    return rlist[0]

def getGeoScope( postalCode, country ):
        db = getDB()
        myquery = "SELECT ZipCode, CityMixedCase, County, StateFullName from US_Postal where ZipCode = " + postalCode
        db.query( myquery )
        r = db.store_result()
        rlist = r.fetch_row()
        db.close()
        city = rlist[0][1]
        county = rlist[0][2]
        state = rlist[0][3]
        geoScope = '||' + urlify(country) + '||' + urlify(state) + '||' + urlify(county) + '||' + urlify(city) + '|' +  postalCode
        return geoScope

def getUserScopes(geoInfo, scopeLevel):
    ## geoInfo: a geo object from a user
    ## scopeLevel: country = 2, state = 4, county = 6, city = 8, zip = 9
    ## format of scope attribute ||country||state||county||city|zip
    log.info('geoInfo is %s' % geoInfo)
    searchScope = geoInfo[0]['scope']
    scopeLevel = int(scopeLevel) + 1
    try:
        sList = searchScope.split('|')
        log.info('sList is %s' % len(sList))
        sList = sList[:int(scopeLevel)]
        searchScope = "|".join(sList)
        searchScope = searchScope + '%'
        log.info('searchScope is %s and scopeLevel is %s' % (searchScope,scopeLevel))
        return meta.Session.query(Thing).filter_by(objType = 'geo').filter(Thing.data.any(wc('deactivated', '0000-00-00'))).filter(Thing.data.any(wcl('scope', searchScope, 1))).all()
    except sa.orm.exc.NoResultFound:
        return False

def getGeoInfo(ownerID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'geo').filter_by(owner = ownerID).all()
    except sa.orm.exc.NoResultFound:
        return False

def getScopeTitle(postalCode, country, scope):
        db = getDB()
        myquery = "SELECT ZipCode, CityMixedCase, County, StateFullName from US_Postal where ZipCode = " + postalCode
        db.query( myquery )
        r = db.store_result()
        rlist = r.fetch_row()
        db.close()
        city = rlist[0][1]
        county = rlist[0][2]
        state = rlist[0][3]

        if scope == '10':
           return 'postal code of ' + postalCode
        elif scope == '09':
           return 'City of ' + city.title()
        elif scope == '07':
           return 'County of ' + county.title()
        elif scope == '05':
           return 'State of ' + state.title()
        elif scope == '03':
           return 'country of ' + country.title()
        elif scope == '01':
           return 'Planet Earth'
        else:
           return 'hmmm, I dunno'
        
class GeoInfo(object):
    def __init__(self, postalCode, country, ownerID ):
        g = Thing('geo', ownerID)
        
        g['postalCode'] = postalCode
        g['deactivated'] = '0000-00-00'

        db = getDB()
        myquery = "SELECT ZipCode, CityMixedCase, County, StateFullName from US_Postal where ZipCode = " + postalCode
        db.query( myquery )
        r = db.store_result()
        rlist = r.fetch_row()
        db.close()
        city = rlist[0][1]
        county = rlist[0][2]
        state = rlist[0][3]

        g['countryTitle'] = country.title()
        g['countryURL'] = '/geo/country/united-states'
        g['countryFlag'] = '/images/flags/country/united-states/united-states.gif'
        g['countryFlagThumb'] = '/images/flags/country/united-states/united-states_thumb.gif'
#
        g['stateTitle'] = state.title()
        g['stateURL'] = '/geo/state/united-states/' + urlify(state)
        g['stateFlag'] = '/images/flags/country/united-states/states/' + urlify(state) + '.gif'
        g['stateFlagThumb'] = '/images/flags/country/united-states/states/' + urlify(state) + '_thumb.gif'
        g['countyTitle'] = county.title()
        g['countyURL'] = '/geo/county/united-states/' + urlify(state) + '/' + urlify(county)
        g['countyFlag'] = '/images/flags/country/united-states/county.gif'
        g['countyFlagThumb'] = '/images/flags/country/united-states/county_thumb.png'
        g['cityTitle'] = city.title()
        g['cityURL'] = '/geo/city/united-states/' + urlify(state) + '/' + urlify(city)
        g['cityFlag'] = '/images/flags/country/united-states/city.gif'
        g['cityFlagThumb'] = '/images/flags/country/united-states/city_thumb.png'
        g['postalTitle'] = 'Zip Code ' + postalCode
        g['postalURL'] = '/geo/postal/united-states/' + postalCode
        g['postalFlag'] = '/images/flags/country/united-states/postal.gif'
        g['postalFlagThumb'] = '/images/flags/country/united-states/postal_thumb.gif'
        g['scope'] ='||' + urlify(country) + '||' + urlify(state) + '||' + urlify(county) + '||' + urlify(city) + '|' +  postalCode
        commit(g)

