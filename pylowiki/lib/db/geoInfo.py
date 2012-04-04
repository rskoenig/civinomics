#-*- coding: utf-8 -*-
import _mysql
from pylowiki.model import Thing, Data, meta
from pylowiki.lib.utils import urlify
from dbHelpers import commit, with_characteristic


def getDB():
    return _mysql.connect("localhost","civinomics","Sisyphus3","geo")

    return url

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

def getGeoInfo(userID):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'geo').filter_by(owner = userID).all()
    except sa.orm.exc.NoResultFound:
        return False

class GeoInfo(object):
    def __init__(self, postalCode, country, userID ):
        g = Thing('geo', userID)
        
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
        g['countyFlagThumb'] = '/images/flags/country/united-states/county_thumb.gif'
        g['cityTitle'] = city.title()
        g['cityURL'] = '/geo/city/united-states/' + urlify(state) + '/' + urlify(city)
        g['cityFlag'] = '/images/flags/country/united-states/city.gif'
        g['cityFlagThumb'] = '/images/flags/country/united-states/city_thumb.gif'
        g['postalTitle'] = 'Zip Code ' + postalCode
        g['postalURL'] = '/geo/postal/united-states/' + postalCode
        g['postalFlag'] = '/images/flags/country/united-states/postal.gif'
        g['postalFlagThumb'] = '/images/flags/country/united-states/postal_thumb.gif'
        g['scope'] ='|' + urlify(country) + '||' + urlify(state) + '||' + urlify(county) + '||' + urlify(city) + '|' +  postalCode
        commit(g)

