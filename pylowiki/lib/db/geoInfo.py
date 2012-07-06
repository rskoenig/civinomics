#-*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import sqlalchemy as sa
from sqlalchemy import orm
from pylowiki.model import Thing, Data, meta
from pylowiki.lib.utils import urlify
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl

import time, datetime
import logging
    
log = logging.getLogger(__name__)

def getDB():
    return MySQLdb.connect(user="civinomics",passwd="Sisyphus3",db="geo", cursorclass=MySQLdb.cursors.DictCursor)

def geoDeurlify( something ):
    deurl = something.replace('-', ' ')
    return deurl 

def getPostalInfo( postal, country ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT * from US_Postal WHERE ZipCode = %s""",(postal,))
    rlist = c.fetchone()
    c.close()
    db.close()
    return rlist

def getCityInfo( city, state, country ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT * from US_City WHERE City = %s AND StateFullName = %s""",(city,state))
    rlist = c.fetchone()
    c.close()
    db.close()
    return rlist

def getCountyInfo( county, state, country ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT * from US_County WHERE County = %s AND StateFullName = %s""",(county,state))
    rlist = c.fetchone()
    c.close()
    db.close()
    return rlist

def getStateInfo( state, country ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT * from US_State WHERE StateFullName = %s""",(state,))
    rlist = c.fetchone()
    c.close()
    db.close()
    return rlist

def getGeoScope( postalCode, country ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT ZipCode, CityMixedCase, County, StateFullName from US_Postal WHERE ZipCode = %s""",(postalCode,))
    rlist = c.fetchone()
    c.close()
    db.close()
    city = rlist['CityMixedCase']
    county = rlist['County']
    state = rlist['StateFullName']
    geoScope = '||' + urlify(country) + '||' + urlify(state) + '||' + urlify(county) + '||' + urlify(city) + '|' +  postalCode
    return geoScope

def getUserScopes(geoInfo, scopeLevel):
    ## geoInfo: a geo object from a user
    ## scopeLevel: country = 2, state = 4, county = 6, city = 8, zip = 9
    ## format of scope attribute ||country||state||county||city|zip
    ##log.info('geoInfo is %s' % geoInfo)
    searchScope = geoInfo[0]['scope']
    scopeLevel = int(scopeLevel) + 1
    try:
        sList = searchScope.split('|')
        ##log.info('sList is %s' % len(sList))
        sList = sList[:int(scopeLevel)]
        searchScope = "|".join(sList)
        searchScope = searchScope + '%'
        ##log.info('searchScope is %s and scopeLevel is %s' % (searchScope,scopeLevel))
        return meta.Session.query(Thing).filter_by(objType = 'geo').filter(Thing.data.any(wc('deactivated', '0000-00-00'))).filter(Thing.data.any(wcl('scope', searchScope, 1))).all()
    except sa.orm.exc.NoResultFound:
        return False

def getWorkshopScopes(geoInfo, scopeLevel):
    ## geoInfo: a geo object from a user
    ## scopeLevel: country = 2, state = 4, county = 6, city = 8, zip = 9
    ## format of scope attribute ||country||state||county||city|zip
    ##log.info('geoInfo is %s' % geoInfo)
    searchScope = geoInfo[0]['scope']
    scopeLevel = int(scopeLevel) + 1
    try:
        sList = searchScope.split('|')
        ##log.info('sList is %s' % len(sList))
        sList = sList[:int(scopeLevel)]
        searchScope = "|".join(sList)
        searchScope = searchScope + '%'
        ##log.info('searchScope is %s and scopeLevel is %s' % (searchScope,scopeLevel))
        return meta.Session.query(Thing).filter_by(objType = 'wscope').filter(Thing.data.any(wc('deactivated', '0000-00-00'))).filter(Thing.data.any(wcl('scope', searchScope, 1))).all()
    except sa.orm.exc.NoResultFound:
        return False

def getGeoInfo(ownerID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'geo').filter_by(owner = ownerID).all()
    except sa.orm.exc.NoResultFound:
        return False

def getScopeTitle(postalCode, country, scope):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT ZipCode, CityMixedCase, County, StateFullName from US_Postal WHERE ZipCode = %s""",(postalCode,))
    rlist = c.fetchone()
    c.close()
    db.close()
    city = rlist['CityMixedCase']
    county = rlist['County']
    state = rlist['StateFullName']

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
        
class WorkshopScope(object):
    def __init__(self, postalCode, country, workshopID, ownerID):
        w = Thing('wscope', ownerID)
        w['postalCode'] = postalCode
        w['country'] = country
        w['workshopID'] = workshopID
        w['deactivated'] = '0000-00-00'
        w['scope'] = getGeoScope(postalCode, country)
        commit(w)

class GeoInfo(object):
    def __init__(self, postalCode, country, ownerID ):
        g = Thing('geo', ownerID)
        
        g['postalCode'] = postalCode
        g['deactivated'] = '0000-00-00'

        db = getDB()
        c = db.cursor()
        c.execute("""SELECT ZipCode, CityMixedCase, County, StateFullName from US_Postal WHERE ZipCode = %s""",(postalCode,))
        rlist = c.fetchone()
        c.close()
        db.close()
        city = rlist['CityMixedCase']
        county = rlist['County']
        state = rlist['StateFullName']

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

