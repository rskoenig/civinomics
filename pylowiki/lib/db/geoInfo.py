#-*- coding: utf-8 -*-
import _mysql

def getDB():
    return _mysql.connect("localhost","civinomics","Sisyphus3","geo")

def geoUrlify(url):
    url = url.strip()
    url = url.replace(' ', '_')
    url = url.encode('utf8')
    url = quote(url)
    return url

def geoDeurlify( something ):
    deurl = something.replace('-', ' ')
    return deurl 

def getScope( postalCode, country ):
    db = getDB()
    myquery = "SELECT ZipCode, CityMixedCase, County, StateFullName from US_Postal where ZipCode = " + postalCode
    db.query( myquery )
    r = db.store_result()
    rlist = r.fetch_row()
    db.close()

    postal = rlist[0][0]
    city = rlist[0][1]
    county = rlist[0][2]
    state = rlist[0][3]
    results = '|US||' + state.title() + '||' + county.title() + '||' + city.title() + '|' +  postal
    return results

def getPostalInfo( postalCode, country ):
    db = getDB()
    myquery = "SELECT * from US_Postal where ZipCode = " + postalCode
    db.query( myquery )
    r = db.store_result()
    rlist = r.fetch_row( 1, 1 )
    db.close()
    return rlist[0]

def getCityInfo( city, state, country ):
    db = getDB()
    myquery = 'SELECT * from US_City WHERE City = \'' + city + '\' AND State = \'' + state + '\''
    db.query( myquery )
    r = db.store_result()
    rlist = r.fetch_row( 1, 1 )

    # Get the county and state full name from the postal code table
    myquery = "SELECT County, StateFullName from US_Postal where City = \'" + rlist[0]['City'] + "\' AND State = \'" + rlist[0]['State'] + "\'"
    db.query( myquery )
    r = db.store_result()
    rlist2 = r.fetch_row( 1, 1 )

    rlist[0]['County'] = rlist2[0]['County']
    rlist[0]['StateFullName'] = rlist2[0]['StateFullName']
    db.close()
    return rlist[0]


def getCountyInfo( county, state, country ):
    db = getDB()
    myquery = 'SELECT * from US_County WHERE County = \'' + county + '\' AND State = \'' + state + '\''
    db.query( myquery )
    r = db.store_result()
    rlist = r.fetch_row( 1, 1 )
    db.close()
    return rlist[0]

def getStateInfo( state, country ):
    db = getDB()
    myquery = 'SELECT * from US_State WHERE State = \'' + state + '\''
    db.query( myquery )
    r = db.store_result()
    rlist = r.fetch_row( 1, 1 )
    db.close()
    return rlist[0]


