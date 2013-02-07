#-*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import sqlalchemy as sa
from sqlalchemy import orm
from pylowiki.model import Thing, Data, meta
from pylowiki.lib.utils import urlify
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl
import generic

import time, datetime
import logging
    
log = logging.getLogger(__name__)

def getDB():
    return MySQLdb.connect(user="civinomics",passwd="Sisyphus3",db="geo",host="civinomics.net", cursorclass=MySQLdb.cursors.DictCursor)

def geoDeurlify( something ):
    deurl = something.replace('-', ' ')
    return deurl 

def getPostalInfo( postal ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT * from US_Postal WHERE ZipCode = %s""",(postal))
    rlist = c.fetchone()
    c.close()
    db.close()
    return rlist
    
def getPostalList( country, state, county, city ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT DISTINCT ZipCode from US_Postal WHERE StateFullName = %s and County = %s and City = %s""",(state, county.upper(), city.upper()))
    rlist = c.fetchall()
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
    
def getCityList( country, state, county ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT City from US_City WHERE StateFullName = %s and County = %s""",(state, county))
    rlist = c.fetchall()
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
    
def getCountyList( county, state ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT County from US_County WHERE StateFullName = %s""",(state))
    rlist = c.fetchall()
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
    
def getStateList( country ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT StateFullName from US_State""")
    rlist = c.fetchall()
    c.close()
    db.close()
    return rlist

def getCountryInfo( country ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT * from Countries WHERE Country_name = %s""",(country))
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
    if rlist != None:
       city = rlist['CityMixedCase']
       county = rlist['County']
       state = rlist['StateFullName']
       geoScope = '||' + urlify(country) + '||' + urlify(state) + '||' + urlify(county) + '||' + urlify(city) + '|' +  postalCode
       return geoScope
    else:
       return False

def getGeoTitles( postalCode, country ):
    db = getDB()
    c = db.cursor()
    c.execute("""SELECT ZipCode, CityMixedCase, County, StateFullName from US_Postal WHERE ZipCode = %s""",(postalCode,))
    rlist = c.fetchone()
    log.info("rlist is %s",rlist)
    c.close()
    db.close()
    if rlist != None:
        #postalCode = rlist['ZipCode']
        city = rlist['CityMixedCase']
        county = rlist['County']
        state = rlist['StateFullName']
        country = geoDeurlify(country)
        if county and state:
            geoScope = '||' + country.title() + '||' + state.title() + '||' + county.title() + '||' + city.title() + '|' +  postalCode
            return geoScope
        else:
            return "0"
    else:
        return "0"

def getUserScopes(searchScope, scopeLevel):
    ## geoInfo: a geo object from a user
    ## scopeLevel: country = 2, state = 4, county = 6, city = 8, zip = 9
    ## format of scope attribute ||country||state||county||city|zip
    scopeLevel = int(scopeLevel) + 1
    try:
        sList = searchScope.split('|')
        sList = sList[:int(scopeLevel)]
        searchScope = "|".join(sList)
        searchScope = searchScope + '%'
        return meta.Session.query(Thing)\
                .filter_by(objType = 'geo')\
                .filter(Thing.data.any(wc('deactivated', '0000-00-00')))\
                .filter(Thing.data.any(wcl('scope', searchScope, 1)))\
                .all()
    except sa.orm.exc.NoResultFound:
        return False

def getWScopeByWorkshop(workshop, deleted = '0'):
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'wscope')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
                .one()
    except sa.orm.exc.NoResultFound:
        return False
        
def getWorkshopScopes(searchScope, scopeLevel):
    ## geoInfo: a geo object from a user
    ## scopeLevel: country = 3, state = 5, county = 7, city = 9, zip = 10
    ## format of scope attribute ||country||state||county||city|zip
    scopeLevel = int(scopeLevel) + 0
    try:
        sList = searchScope.split('|')
        sList = sList[:int(scopeLevel)]
        searchScope = "|".join(sList)
        searchScope = searchScope + '%'
        log.info(searchScope)
        return meta.Session.query(Thing)\
                .filter_by(objType = 'wscope')\
                .filter(Thing.data.any(wc('deleted', '0')))\
                .filter(Thing.data.any(wcl('scope', searchScope, 1)))\
                .all()
    except sa.orm.exc.NoResultFound:
        return False

def getWorkshopsInScope(country = '0', state = '0', county = '0', city = '0', postalCode = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'wscope')\
            .filter(Thing.data.any(wc('country', country)))\
            .filter(Thing.data.any(wc('state', state)))\
            .filter(Thing.data.any(wc('county', county)))\
            .filter(Thing.data.any(wc('city', city)))\
            .filter(Thing.data.any(wc('postal', postalCode)))\
            .all()
    except:
        return False

def editWorkshopScope(wscope, geoTagString):
    try:
        wscope['scope'] = geoTagString
        geoTags = geoTagString.split('|')
        wscope['country'] = geoTags[2]
        wscope['state'] = geoTags[4]
        wscope['county'] = geoTags[6]
        wscope['city'] = geoTags[8]
        wscope['postal'] = geoTags[9]
        commit(wscope)
        return wscope
    except:
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

def getPublicScope(workshop):
    scope = getWScopeByWorkshop(workshop)
    if scope:
        scope = scope['scope'].split('|')
        if scope[9] != '0':
            scopeLevel = 'postal'
        elif scope[8] != '0':
            scopeLevel = 'city'
        elif scope[6] != '0':
            scopeLevel = 'county'
        elif scope[4] != '0':
            scopeLevel = 'state'
        elif scope[2] != '0':
            scopeLevel = 'country'
        else:
            scopeLevel = 'planet'
    else:
        scopeLevel = 'planet'
        
    return scopeLevel

class WorkshopScope(object):
    def __init__(self, workshop, scope):
        wscope = Thing('wscope')
        wscope['deleted'] = '0'
        wscope['scope'] = scope
        
        geoTags = scope.split('|')
        wscope['country'] = geoTags[2]
        wscope['state'] = geoTags[4]
        wscope['county'] = geoTags[6]
        wscope['city'] = geoTags[8]
        wscope['postal'] = geoTags[9]
        
        commit(wscope)
        wscope = generic.linkChildToParent(wscope, workshop)
        commit(wscope)

class SurveyScope(object):
    def __init__(self, postalCode, country, survey, owner):
        s = Thing('sScope', owner.id)
        s['postalCode'] = postalCode
        s['country'] = country
        s['workshopID'] = survey.id
        s['deactivated'] = '0000-00-00'
        s['scope'] = getGeoScope(postalCode, country)
        commit(s)
        return s

def GeoInfo(postalCode, country, ownerID ):
    """
        Geo URL schema for workshop listings:   /workshops/geo/earth/country/state/county/city/postalCode
        location flag:                          /images/flags/country/united-states/united-states.gif
                                                /images/flags/country/united-states/united-states_thumb.gif
                                                /images/flags/country/united-states/states/{state-name}{(_thumb)?}.gif
                                                /images/flags/country/united-states/county.gif
                                                /images/flags/country/united-states/county_thumb.png
                                                /images/flags/country/united-states/city.gif
                                                /images/flags/country/united-states/city_thumb.png
                                                /images/flags/country/united-states/postal.gif
                                                /images/flags/country/united-states/postal_thumb.gif
    """
    g = Thing('geo', ownerID)
    
    g['disabled'] = '0'
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
    g['countryURL'] = 'united-states'
    g['stateTitle'] = state.title()
    g['stateURL'] = urlify(state)
    g['countyTitle'] = county.title()
    g['countyURL'] = urlify(county)
    g['cityTitle'] = city.title()
    g['cityURL'] = urlify(city)
    g['postalTitle'] = postalCode
    g['postalURL'] = postalCode
    g['scope'] ='||' + urlify(country) + '||' + urlify(state) + '||' + urlify(county) + '||' + urlify(city) + '|' +  postalCode
    commit(g)
