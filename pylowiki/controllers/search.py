# -*- coding: utf-8 -*-
import logging
import urllib2

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config
from pylowiki.lib.db.geoInfo import geoDeurlify, getPostalInfo, getCityInfo, getCountyInfo, getStateInfo, getCountryInfo, getGeoScope, getGeoTitles, getWorkshopScopes, getZipCodesBy
from pylowiki.lib.db.tag        import getTagCategories

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.db.activity     as activityLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.fuzzyTime       as fuzzyTime    
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.photo        as photoLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.tag          as tagLib
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.resource     as resourceLib
import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.db.activity     as activityLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.json            as jsonLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.helpers         as h
import pylowiki.lib.sort            as sort
import misaka                       as m

import simplejson as json
from hashlib import md5
log = logging.getLogger(__name__)

class SearchController(BaseController):

    """
        JSON responses:
            statusCode == 0:    Same as unix exit code (OK)
            statusCode == 1:    No query was submitted
            statusCode == 2:    Query submitted, no results found
            result:             The search result, given there was at least one
    """

    def __before__(self, action, searchType = None, **kwargs):
        # need this for facebook login in modal
        c.baseUrl = utils.getBaseUrl()
        #log.info(" action, searchType = None, **kwargs): %s %s %s"%(action, searchType, dict(**kwargs)))
        c.title = c.heading = "Civinomics Search"
        c.scope = {'level':'earth', 'name':'all'}
        c.backgroundPhoto = '/images/grey.png'
        c.user = c.authuser
        c.tagList = getTagCategories()
        userLib.setUserPrivs()
        
        self.query = ''
        self.noQuery = False
        self.searchType = 'name'
        if 'searchString' in kwargs:
            searchString = kwargs['searchString'].replace("+", " ")
        else:
            searchString = None
        if 'zip' in kwargs:
            self.zip = kwargs['zip']
            
        log.info("****SEARCH STRING**** %s"%searchString)
            
        if 'id1' in kwargs:
            id1 = kwargs['id1']
        else:
            id1 = None
            
        if action == 'searchWorkshopGeo':
            self.searchType = 'geo'
            if 'country' in kwargs:
                country = kwargs['country']
            else:
                country = '0'
            if 'state' in kwargs:
                state = kwargs['state']
            else:
                state = '0'
            if 'county' in kwargs:
                county = kwargs['county']
            else:
                county = '0'
            if 'city' in kwargs:
                city = kwargs['city']
            else:
                city = '0'
            if 'postalCode' in kwargs:
                postalCode = kwargs['postalCode']
            else:
                postalCode = '0'
            searchString = "||%s||%s||%s||%s|%s"%(country, state, county, city, postalCode)
            # kludge CCN
            if '{' in searchString or '%' in searchString:
                return
            c.geoScope = searchString
            #log.info("searchString is %s"%searchString)
            #log.info("searchString after searchWorkshopGeo: %s"%searchString)

        if 'searchQuery' in request.params and searchString == None:
            self.query = request.params['searchQuery']
            #log.info("S E A R C H + Q U E R Y 0:  %s %s"%(self.query, self.noQuery))
            self.query.replace("+", " ")
            if self.query.strip() == '':
                self.noQuery = True
        else:
            self.noQuery = True
            
        if id1 != None:
            self.query = id1
            #log.info("S E A R C H + Q U E R Y 1:  %s %s"%(self.query, self.noQuery))
            self.noQuery = False
            
        if searchType != None:
            self.searchType = searchType
            #log.info("S E A R C H + Q U E R Y 2:  %s %s"%(self.query, self.noQuery))
            self.noQuery = False
            
        if searchString != None:
            self.query = searchString
            #log.info("S E A R C H + Q U E R Y 3:  %s %s"%(self.query, self.noQuery))
            self.noQuery = False
            
        if self.query == '':
            #log.info("S E A R C H + Q U E R Y 4:  %s %s"%(self.query, self.noQuery))
            return self._noSearch()
            self.noQuery = True
        
        #log.info("S E A R C H + Q U E R Y 5:  %s %s"%(self.query, self.noQuery))
        #log.info("****SEARCH QUERY**** %s"%self.query)
        c.searchQuery = self.query


    def _noSearch(self, noRender = False):
        iPhoneApp = utils.iPhoneRequestTest(request)

        if iPhoneApp:
            statusCode = 2
            result = "No search terms were entered."
            response.headers['Content-type'] = 'application/json'
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            c.numUsers = 0
            c.numWorkshops = 0
            return render('/derived/6_search.bootstrap')
    
    def search(self):
        iPhoneApp = utils.iPhoneRequestTest(request)
        #log.info("hello")
        if self.noQuery:
            return self._noSearch()
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return self._noSearch()
        c.numUsers = userLib.searchUsers(['greetingMsg', 'name'], [self.query, self.query], count = True)
        c.numOrganizations = userLib.searchOrganizations(['name', 'url'], [self.query, self.query], count = True)
        c.numWorkshops = workshopLib.searchWorkshops(['title', 'description', 'workshop_category_tags'], [self.query, self.query, self.query], count = True)
        #log.info("Search query in search to get the count %s", self.query)
        c.numResources = resourceLib.searchResources(['title', 'text', 'link'], [self.query, self.query, self.query], count = True)
        iResources = resourceLib.searchInitiativeResources(['title', 'text', 'link'], [self.query, self.query, self.query], count = True)
        c.numResources += iResources
        c.numDiscussions = discussionLib.searchDiscussions(['title', 'text'], [self.query, self.query], count = True)
        c.numIdeas = ideaLib.searchIdeas('title', self.query, count = True)
        c.numPhotos = photoLib.searchPhotos(['title', 'description', 'tags'], [self.query, self.query, self.query], count = True)
        c.numInitiatives = initiativeLib.searchInitiatives(['title', 'description', 'tags'], [self.query, self.query, self.query], count = True)
        c.searchType = self.searchType
        c.searchQuery = self.query 
        c.scope = {'level':'earth', 'name':'all'}
        if self.query == 'civinomicon':            
            c.backgroundPhoto = '/images/civinomicon/civinomicon_bg.png'

        if iPhoneApp:
            entry = {}
            entry['numUsers'] = c.numUsers
            entry['numOrganizations'] = c.numOrganizations
            entry['numWorkshops'] = c.numWorkshops
            entry['numResources'] = c.numResources
            entry['numDiscussions'] = c.numDiscussions
            entry['numIdeas'] = c.numIdeas
            entry['numPhotos'] = c.numPhotos
            entry['searchType'] = c.searchType
            entry['searchQuery'] = c.searchQuery
            entry['scope'] = c.scope
            result = []
            result.append(entry)
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return render('/derived/6_search.bootstrap')

    def browseInitiatives(self):
        iPhoneApp = utils.iPhoneRequestTest(request)
        self.noQuery = False
        c.searchType = "browse"
        c.searchQuery = "All Initiatives" 
        c.scope = {'level':'earth', 'name':'all'}
        return render('/derived/6_browse.bootstrap')
        
    def getWorkshopCategoryTags(self):
        """ return a list of the categories available for search """
        categories = tagLib.getTagCategories()
        iPhoneApp = utils.iPhoneRequestTest(request)
        response.headers['Content-type'] = 'application/json'
        if categories:
            result = categories
            statusCode = 0
        else:
            statusCode = 2
            result = "No categories."
        
        if iPhoneApp:
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return json.dumps({'statusCode':statusCode, 'result':result})

    def searchWorkshopCategoryTags(self):
        iPhoneApp = utils.iPhoneRequestTest(request)
        if self.noQuery:
            return self._noSearch()
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return self._noSearch()
        c.numUsers = userLib.searchUsers(['greetingMsg', 'name'], [self.query, self.query], count = True)
        c.numWorkshops = workshopLib.searchWorkshops(['workshop_category_tags'], [self.query], count = True)
        c.numResources = resourceLib.searchResources(['workshop_category_tags'], [self.query], count = True)
        iResources = resourceLib.searchInitiativeResources(['initiative_tags'], [self.query], count = True)
        c.numResources += iResources
        c.numDiscussions = discussionLib.searchDiscussions(['workshop_category_tags'], [self.query], count = True)
        c.numIdeas = ideaLib.searchIdeas('workshop_category_tags', self.query, count = True)
        c.numPhotos = photoLib.searchPhotos('tags', self.query, count = True)
        c.numInitiatives = initiativeLib.searchInitiatives('tags', self.query, count = True)

        c.photos = photoLib.searchPhotos('tags', self.query)
        if c.photos and len(c.photos) != 0:
            c.photos = sort.sortBinaryByTopPop(c.photos)
            p = c.photos[0]
            c.backgroundPhoto = "/images/photos/" + p['directoryNum_photos'] + "/photo/" + p['pictureHash_photos'] + ".png"
            c.backgroundAuthor = userLib.getUserByID(p.owner)
            if iPhoneApp:
                # cant figure out how to make these json serializable yet:
                # entry['photos'] = c.photos
                # entry['p'] = p
                entry['backgroundPhoto'] = c.backgroundPhoto
                entry['backgroundAuthor'] = dict(c.backgroundAuthor)

        c.searchQuery = self.query
        c.searchTitle = self.query.replace("_", " ")
        c.searchType = "tag"
        c.scope = {'level':'earth', 'name':'all'}
        if iPhoneApp:
            entry['numUsers'] = c.numUsers
            entry['numWorkshops'] = c.numWorkshops
            entry['numResources'] = c.numResources
            entry['numDiscussions'] = c.numDiscussions
            entry['numIdeas'] = c.numIdeas
            entry['numPhotos'] = c.numPhotos
            entry['searchType'] = c.searchType
            entry['searchQuery'] = c.searchQuery
            entry['scope'] = c.scope
            result = []
            result.append(entry)
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return render('/derived/6_search.bootstrap')
        
    def searchWorkshopGeo(self):
        iPhoneApp = utils.iPhoneRequestTest(request)
        if self.noQuery:
            return self._noSearch()
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return self._noSearch()
        #log.info("searchWorkshopGeo YO CHECK THIS OUT %s %s"%(self.query, self.noQuery))
        c.geoScope = self.query
        c.numUsers = 0
        #c.numWorkshops = workshopLib.searchWorkshops(['workshop_public_scope'], [self.query], count = True)
        #c.numResources = resourceLib.searchResources(['workshop_public_scope'], [self.query], count = True)
        #iResources = resourceLib.searchInitiativeResources(['initiative_scope'], [self.query], count = True)
        #c.numResources += iResources
        #c.numDiscussions = discussionLib.searchDiscussions(['workshop_public_scope'], [self.query], count = True)
        #c.numIdeas = ideaLib.searchIdeas('workshop_public_scope', self.query, count = True)
        #c.numPhotos = photoLib.searchPhotos('scope', self.query, count = True)
        c.geoString = self.query
        c.photos = photoLib.searchPhotos('scope', self.query)
        iScope = '0' + self.query.replace('||', '|0|')
        #c.numInitiatives = initiativeLib.searchInitiatives(['scope'], [iScope], count = True)
        #log.info("search is %s"%c.searchQuery)
        entry = {}
        if c.photos:
            c.photos = sort.sortBinaryByTopPop(c.photos)
            p = c.photos[0]
            c.backgroundPhoto = "/images/photos/" + p['directoryNum_photos'] + "/photo/" + p['pictureHash_photos'] + ".png"
            c.backgroundAuthor = userLib.getUserByID(p.owner)
            if iPhoneApp:
                entry['backgroundPhoto'] = c.backgroundPhoto
                entry['backgroundAuthor'] = dict(c.backgroundAuthor)

        c.searchType = "region"
        geoScope = self.query.split('|') 
        baseUrl = config['site_base_url']
        # removes the / if there is one
        if baseUrl[-1] == "/":
            baseUrl = baseUrl[:-1]

        if geoScope[2] == '0':
            level = 'earth'
            name = 'all'
            c.searchQuery = 'Earth'
            flag = baseUrl + "/images/flags/" + level + ".gif"
            flag = flag.lower()
            try:
                f = urllib2.urlopen(urllib2.Request(flag))
                c.flag = flag
            except:
                c.flag = '/images/flags/generalFlag.gif'
            c.population = 7172450000
            c.medianAge = 28.4
            c.personsHousehold = 4
            
        elif geoScope[4] == '0':
            level = geoScope[2]
            name = level
            c.searchQuery = "" + utils.geoDeurlify(geoScope[2])
            flag = baseUrl + "/images/flags/country/" + geoScope[2] + ".gif"
            flag = flag.lower()
            try:
                f = urllib2.urlopen(urllib2.Request(flag))
                c.flag = flag
            except:
                c.flag = '/images/flags/generalFlag.gif'
            c.geoInfo = getCountryInfo(geoScope[2]) 
            if c.geoInfo:
                c.population = c.geoInfo['Country_population']
                c.medianAge = c.geoInfo['Country_median_age']
                c.personsHousehold = c.geoInfo['Country_persons_per_household']
            
        elif geoScope[6] == '0':
            level = geoScope[4]
            name = level
            c.searchQuery = "State of " + utils.geoDeurlify(geoScope[4])
            flag = baseUrl + '/images/flags/country/' + geoScope[2] + '/states/' + geoScope[4] + '.gif'
            flag = flag.lower()
            try:
                f = urllib2.urlopen(urllib2.Request(flag))
                c.flag = flag
            except:
                c.flag = '/images/flags/generalFlag.gif'
            c.geoInfo = getStateInfo(geoScope[4], geoScope[2]) 
            if c.geoInfo:
                c.population = c.geoInfo['Population']
                c.medianAge = c.geoInfo['Population_Median']
                c.personsHousehold = c.geoInfo['Average_Household_Size']
            
        elif geoScope[8] == '0':
            level = geoScope[6]
            name = level
            c.searchQuery = "County of " + utils.geoDeurlify(geoScope[6])
            flag = baseUrl + '/images/flags/country/' + geoScope[2] + '/states/' + geoScope[4] + '/counties/' + geoScope[6] + '.gif'
            flag = flag.lower()
            try:
                f = urllib2.urlopen(urllib2.Request(flag))
                c.flag = flag
            except:
                c.flag = '/images/flags/generalFlag.gif'
            county = geoDeurlify(geoScope[6])
            c.geoInfo = getCountyInfo(county, geoScope[4], geoScope[2])
            if c.geoInfo:
                c.population = c.geoInfo['Population']
                c.medianAge = c.geoInfo['Population_Median']
                c.personsHousehold = c.geoInfo['Average_Household_Size']

        elif geoScope[9] == '0':
            level = geoScope[8]
            name = level
            c.searchQuery = "City of " + utils.geoDeurlify(geoScope[8])
            flag = baseUrl + '/images/flags/country/' + geoScope[2] + '/states/' + geoScope[4] + '/counties/' + geoScope[6] + '/cities/' + geoScope[8] + '.gif'
            flag = flag.lower()
            try:
                f = urllib2.urlopen(urllib2.Request(flag))
                c.flag = flag
            except:
                c.flag = '/images/flags/generalFlag.gif'
            city = geoDeurlify(geoScope[8])
            c.geoInfo = getCityInfo(city, geoScope[4], geoScope[2]) 
            if c.geoInfo:
                c.population = c.geoInfo['Population']
                c.medianAge = c.geoInfo['Population_Median']
                c.personsHousehold = c.geoInfo['Average_Household_Size']

        else:
            level = geoScope[9]
            name = level
            c.searchQuery = "Postal Code " + utils.geoDeurlify(geoScope[9])
            c.flag = '/images/flags/generalFlag.gif'
            c.geoInfo = getPostalInfo(geoScope[9]) 
            if c.geoInfo:
                c.population = c.geoInfo['Population']
                c.medianAge = c.geoInfo['MedianAge']            
                c.personsHousehold = c.geoInfo['PersonsPerHousehold']
                c.incomePerHousehold = c.geoInfo['IncomePerHousehold']
                c.avgHouseValue = c.geoInfo['AverageHouseValue']
                c.bizAnnualPayroll = c.geoInfo['BusinessAnnualPayroll']

        c.scope = {'level':'earth', 'name':'all'}
        
        c.title = c.heading = c.searchQuery + " Activity"
        return render('/derived/6_geo_profile.bootstrap')
    
    def searchPeople(self):
        #: this function returns json data so we set the headers appropriately
        response.headers['Content-type'] = 'application/json'
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        if self.searchType == "orgURL":
            # This is a search for organizations
            people = userLib.searchOrganizations(['name', 'url'], [self.query, self.query])
        elif self.searchType == "usersAndOrgs":
            # This is a search for both people and organizations
            people = userLib.searchUsersAndOrgs(['greetingMsg', 'name'], [self.query, self.query])
        else:
            people = userLib.searchUsers(['greetingMsg', 'name'], [self.query, self.query])
        if len(people) == 0:
            return json.dumps({'statusCode': 2})
        for p in people:
            entry = {}
            entry['name'] = p['name']
            entry['email'] = p['email']
            entry['greetingMsg'] = p['greetingMsg']
            entry['photo'] = utils._userImageSource(p)
            entry['hash'] = md5(p['email']).hexdigest()
            entry['urlCode'] = p['urlCode']
            entry['url'] = p['url']
            userGeo = geoInfoLib.getGeoInfo(p.id)[0]
            entry['cityURL'] = '/workshops/geo/earth/%s/%s/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'], userGeo['countyURL'], userGeo['cityURL'])
            entry['cityTitle'] = userGeo['cityTitle']
            entry['stateURL'] = '/workshops/geo/earth/%s/%s' %(userGeo['countryURL'], userGeo['stateURL'])
            entry['stateTitle'] = userGeo['stateTitle']
            thing = userLib.getUserByCode(p['urlCode'])
            entry['date'] = thing.date.strftime('%Y-%m-%d at %H:%M:%S')
            result.append(entry)
        if len(result) == 0:
            return json.dumps({'statusCode':2})
        return json.dumps({'statusCode':0, 'result':result})
        
    def searchOrganizations( self ):
        orgURL = utils.urlify(self.query)
        if self.searchType == 'orgURL':
            orgs = userLib.searchOrganizations(['greetingMsg', 'name', 'url'], [self.query, self.query, self.query])
            if orgs and len(orgs) == 1:
                urlCode = orgs[0]['urlCode']
                profileURL = '/profile/' + urlCode + '/' + orgURL
                return redirect(profileURL)
            else:
                searchURL = '/search?searchQuery=' + orgURL
                return redirect(searchURL)
        else:
            searchURL = '/search?searchQuery=' + orgURL
            return redirect(searchURL)
    
    def searchWorkshops(self):
        #log.info("controllers/search: in searchWorkshops")
        #: this function returns json data so we set the headers appropriately
        response.headers['Content-type'] = 'application/json'
        if self.noQuery:
            #log.info("return no query")
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            #log.info("return no wildcard")
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        #log.info("searchWorkshops: self.searchType: %s"%self.searchType)
        if self.searchType == 'tag':
            #log.info("search type tag")
            keys = ['workshop_category_tags']
            values = [self.query]
        elif self.searchType == 'geo':
            #log.info("search type geo")
            keys = ['workshop_public_scope']
            values = [self.query]
            #log.info("self.query is %s"%self.query)
        else:
            #log.info("search type generic")    
            keys = ['title', 'description', 'workshop_category_tags']
            values = [self.query, self.query, self.query]
        workshops = workshopLib.searchWorkshops(keys, values)
        if not workshops:
            #log.info("return not workshops")
            return json.dumps({'statusCode':2})
        if len(workshops) == 0:
            #log.info("return len workshops 0")
            return json.dumps({'statusCode':2})
        titleToColourMapping = tagLib.getTagColouring()
        for w in workshops:
            entry = {}
            entry['title'] = w['title']
            entry['description'] = w['description']
            # is this the format it needs to be in the search template?
            entry['urlCode'] = w['urlCode']
            # for consitency, this is the entry that should hold the workshop's url code
            entry['workshopCode'] = w['urlCode']
            # is this the format it needs to be in the search template?
            entry['url'] = w['url']
            # for consitency, this is the entry that should hold the workshop's url
            entry['workshopURL'] = w['url']
            entry['activity'] = w['numPosts']
            entry['bookmarks'] = w['numBookmarks']
            #entry['activity'] = '555'
            #entry['bookmarks'] = '3000'
            mainImage = mainImageLib.getMainImage(w)
            entry['imageURL'] = utils.workshopImageURL(w, mainImage, thumbnail = True)
            entry['startTime'] = w['startTime']
            tagList = []
            for title in w['workshop_category_tags'].split('|'):
                if title and title != '':
                    tagMapping = {}
                    tagMapping['title'] = title
                    tagMapping['colour'] = titleToColourMapping[title]
                    tagList.append(tagMapping)
            entry['tags'] = tagList
            # We dont need to look up the object here            
            #thing = workshopLib.getWorkshopByCode(w['urlCode'])
            entry['bookmarked'] = '0'
            if c.authuser:
                bookmarked = followLib.isFollowing(c.authuser, w)
                if bookmarked:
                    entry['bookmarked'] = '1'
            entry['date'] = w.date.strftime('%Y-%m-%dT%H:%M:%S')
            result.append(entry)

        if len(result) == 0:
            #log.info("return len result 0")
            return json.dumps({'statusCode':2})
        return json.dumps({'statusCode':0, 'result':result})
    
    def searchResources(self):
        #: this function returns json data so we set the headers appropriately
        response.headers['Content-type'] = 'application/json'
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        if self.searchType == 'tag':
            keys = ['workshop_category_tags']
            values = [self.query]
            ikeys = ['initiative_tags']
            resources = resourceLib.searchResources(keys, values)
            resources2 = None
            iresources = resourceLib.searchInitiativeResources(ikeys, values)
        elif self.searchType == 'geo':
            keys = ['workshop_public_scope']
            values = [self.query]
            scope = "0" + self.query.replace("||", "|0|")
            ikeys = ['initiative_scope']
            ivalues = [scope]
            resources = resourceLib.searchResources(keys, values)
            resources2 = resourceLib.searchResources('scope', self.query, hasworkshop = False)
            iresources = resourceLib.searchInitiativeResources(ikeys, ivalues)
        else:
            keys = ['title', 'text', 'link']
            values = [self.query, self.query, self.query]
            resources = resourceLib.searchResources(keys, values)
            resources2 = None
            iresources = resourceLib.searchInitiativeResources(keys, values)

# Changed this to the following format because there was a huge time impact when having both lists
#         if iresources:
#             if resources:
#                 for r in resources:
#                     iresources.append(r)
#                     
#             resources = iresources
# 
#         if resources2:
#             if resources:
#                 for r in resources:
#                     resources2.append(r)
#                     
#             resources = resources2

        if iresources:
            if resources:
                for ri in iresources:
                    resources.append(ri)

        if resources2:
            if resources:
                for r2 in resources2:
                    resources.append(r2)

        if not resources:
            return json.dumps({'statusCode':2})
        if len(resources) == 0:
            return json.dumps({'statusCode':2})
        titleToColourMapping = tagLib.getTagColouring()
        c.numResources = len(resources)
        
        myRatings = {}
        if 'ratings' in session:
           myRatings = session['ratings']

        for r in resources:
            # We don't need to look up this discussion's workshop anymore.
            # w = generic.getThing(r['workshopCode'])
            # Therefore this line,
            if 'workshop_searchable' in r and r['workshop_searchable'] != u'1':
                continue
            if 'initiative_public' in r and r['initiative_public'] != u'1':
                continue
            # replaces these two:
            #if w['public_private'] != u'public':
            #    continue
            #elif w['published'] != u'1':
            #    continue
            entry = {}
            #entry['link'] = r['link']
            entry['title'] = r['title']
            entry['text'] = r['text']
            entry['urlCode'] = r['urlCode']
            entry['url'] = r['url']
            entry['link']= r['link']
            entry['type']= r['type']
            entry['addedAs'] = r['addedAs']
            #entry['domain'] = r['domain']
            #entry['tld'] = r['tld']
            entry['voteCount'] = int(r['ups']) - int(r['downs'])
            if entry['urlCode'] in myRatings:
                entry['rated'] = myRatings[entry['urlCode']]
            else:
                entry['rated'] = 0
            entry['numComments'] = discussionLib.getDiscussionForThing(r)['numComments']
            #: Note in the cases here where there are multiple tags assigned to one value,
            #: I'm adding the standard tags to the json object here as a start for us to 
            #: migrate the whole system over to using the same definitions everywhere.
            if 'workshopCode' in r:
                entry['parentCode'] = r['workshopCode']
                entry['parentURL'] = entry['parent_url'] = r['workshop_url']
                entry['parentTitle'] = entry['parent_title'] = r['workshop_title']
                entry['parentType'] = 'workshop'
                entry['parentIcon'] = 'icon-cog'
            elif 'initiativeCode' in r:
                entry['parentCode'] = r['initiativeCode']
                entry['parentURL'] = entry['initiative_url'] = r['initiative_url']
                entry['parentTitle'] = entry['initiative_title'] = r['initiative_title']
                entry['parentType'] = 'initiative'
                entry['parentIcon'] = 'icon-file'
                
            #: NOTE We won't need to look up this idea's author anymore if we can stick this gravatar hash into the object as well.
            u = userLib.getUserByID(r.owner)
            entry['authorHash'] = md5(u['email']).hexdigest()

            entry['authorCode'] = entry['userCode'] = r['userCode']
            entry['authorURL'] = entry['user_url'] = r['user_url']
            entry['authorName'] = entry['user_name'] = r['user_name']
            # We dont need to look up the object here            
            #thing = resourceLib.getResource(r['urlCode'],r['url'])
            #entry['date'] = thing.date.strftime('%Y-%m-%dT%H:%M:%S')
            entry['date'] = r.date.strftime('%Y-%m-%dT%H:%M:%S')
            tagList = []
            if 'workshopCode' in r:
                catList = r['workshop_category_tags'].split('|')
            elif 'initiativeCode' in r:
                catList = []
                catList.append(r['initiative_tags'])
            for title in catList:
                if title and title != '':
                    tagMapping = {}
                    tagMapping['title'] = title
                    #tagMapping['colour'] = titleToColourMapping[title]
                    tagList.append(tagMapping)
            entry['tags'] = tagList
            result.append(entry)
        if len(result) == 0:
            return json.dumps({'statusCode':2})
        return json.dumps({'statusCode':0, 'result':result})
    
    def searchDiscussions(self):
        #: this function returns json data so we set the headers appropriately
        response.headers['Content-type'] = 'application/json'
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        independent_discussions = None
        if self.searchType == 'tag':
            keys = ['workshop_category_tags']
            values = [self.query]
        elif self.searchType == 'geo':
            keys = ['workshop_public_scope']
            values = [self.query]
            independent_discussions = discussionLib.searchDiscussions(['scope'], values, hasworkshop = False)
        else:
            keys = ['title', 'text']
            values = [self.query, self.query]
        discussions = discussionLib.searchDiscussions(keys, values)
        if independent_discussions:
            discussions += independent_discussions
        if not discussions:
            return json.dumps({'statusCode':2})
        if len(discussions) == 0:
            return json.dumps({'statusCode':2})
        titleToColourMapping = tagLib.getTagColouring()

        myRatings = {}
        if 'ratings' in session:
           myRatings = session['ratings']

        for d in discussions:
            hasworkshop = False
            # We don't need to look up this discussion's workshop anymore.
            # w = generic.getThing(d['workshopCode'])
            # Therefore this line,
            if 'workshop_searchable' in d:
                hasworkshop = True
                if d['workshop_searchable'] != u'1':
                    continue
            # replaces these two:
            #if w['public_private'] != u'public':
            #    continue
            #elif w['published'] != u'1':
            #    continue
            entry = {}
            entry['title'] = d['title']
            entry['text'] = d['text']
            entry['urlCode'] = d['urlCode']
            entry['url'] = d['url']
            if hasworkshop:
                entry['addedAs'] = d['addedAs']
            entry['voteCount'] = int(d['ups']) - int(d['downs'])
            if entry['urlCode'] in myRatings:
                entry['rated'] = myRatings[entry['urlCode']]
            else:
                entry['rated'] = 0
            entry['numComments'] = d['numComments']
            #: Note in the cases here where there are multiple tags assigned to one value,
            #: I'm adding the standard tags to the json object here as a start for us to 
            #: migrate the whole system over to using the same definitions everywhere.
            if hasworkshop:
                entry['workshopCode'] = d['workshopCode']
                entry['workshopURL'] = entry['workshop_url'] = d['workshop_url']
                entry['workshopTitle'] = entry['workshop_title'] = d['workshop_title']
            #: NOTE We won't need to look up this idea's author anymore if we can stick this gravatar hash into the object as well.
            u = userLib.getUserByID(d.owner)
            entry['authorHash'] = md5(u['email']).hexdigest()

            entry['authorCode'] = entry['userCode'] = d['userCode']
            entry['authorURL'] = entry['user_url'] = d['user_url']
            entry['authorName'] = entry['user_name'] = d['user_name']
            # We dont need to look up the discussion here
            #thing = discussionLib.getDiscussion(d['urlCode'])
            #entry['date'] = thing.date.strftime('%Y-%m-%dT%H:%M:%S')
            entry['date'] = d.date.strftime('%Y-%m-%dT%H:%M:%S')
            tagList = []
            if hasworkshop:
                tags = d['workshop_category_tags']
            else:
                tags = d['tags']
            for title in tags.split('|'):
                if title and title != '':
                    tagMapping = {}
                    tagMapping['title'] = title
                    tagMapping['colour'] = titleToColourMapping[title]
                    tagList.append(tagMapping)
            entry['tags'] = tagList
            result.append(entry)
        if len(result) == 0:
            return json.dumps({'statusCode':2})
        return json.dumps({'statusCode':0, 'result':result})
    
    def searchIdeas(self):
        #: this function returns json data so we set the headers appropriately
        response.headers['Content-type'] = 'application/json'
        #log.info("controllers/search: searchIdeas")
        if self.noQuery:
            #log.info("searchIdeas return no query")
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            #log.info("searchIdeas return no wildcard search")
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        if self.searchType == 'tag':
            #log.info("searchIdeas type tag")
            ideas = ideaLib.searchIdeas('workshop_category_tags', self.query)
        elif self.searchType == 'geo':
            #log.info("searchIdeas type geo")
            ideas = ideaLib.searchIdeas('workshop_public_scope', self.query)
            ideas += ideaLib.searchIdeas('scope', self.query, hasworkshop = False)
        else:
            #log.info("searchIdeas type title")
            ideas = ideaLib.searchIdeas('title', self.query)
        if not ideas:
            #log.info("searchIdeas return NOT ideas")
            return json.dumps({'statusCode':2})
        if len(ideas) == 0:
            #log.info("searchIdeas return len ideas == 0")
            return json.dumps({'statusCode':2})
        titleToColourMapping = tagLib.getTagColouring()

        myRatings = {}
        if 'ratings' in session:
           myRatings = session['ratings']

        for idea in ideas:
            hasworkshop = False
            # We don't need to look up this idea's workshop anymore.
            # w = generic.getThing(idea['workshopCode'])
            # Therefore this line,
            if 'workshop_searchable' in idea:
                hasworkshop = True
                if idea['workshop_searchable'] != u'1':
                    continue
            # replaces these two:
            #if w['public_private'] != u'public':
            #    continue
            #elif w['published'] != u'1':
            #    continue
            entry = {}
            entry['title'] = idea['title']
            entry['urlCode'] = idea['urlCode']
            entry['url'] = idea['url']
            entry['voteCount'] = int(idea['ups']) + int(idea['downs'])
            entry['ups'] = int(idea['ups'])
            entry['downs'] = int(idea['downs'])
            if entry['urlCode'] in myRatings:
                entry['rated'] = myRatings[entry['urlCode']]
            else:
                entry['rated'] = 0

            entry['addedAs'] = idea['addedAs']
            entry['numComments'] = discussionLib.getDiscussionForThing(idea)['numComments']
            #: Note in the cases here where there are multiple tags assigned to one value,
            #: I'm adding the standard tags to the json object here as a start for us to 
            #: migrate the whole system over to using the same definitions everywhere.
            if hasworkshop:
                entry['workshopCode'] = idea['workshopCode']
                entry['workshopURL'] = entry['workshop_url'] = idea['workshop_url']
                entry['workshopTitle'] = entry['workshop_title'] = idea['workshop_title']
            else:
                entry['workshopCode'] = ""
                entry['workshopURL'] = entry['workshop_url'] = ""
                entry['workshopTitle'] = entry['workshop_title'] = ""
            #: NOTE We won't need to look up this idea's author anymore if we can stick this gravatar hash into the object as well.
            u = userLib.getUserByID(idea.owner)
            
            entry['authorHash'] = md5(u['email']).hexdigest()
            entry['authorCode'] = entry['userCode'] = idea['userCode']
            entry['authorURL'] = entry['user_url'] = idea['user_url']
            entry['authorName'] = entry['user_name'] = idea['user_name']
            
            # dont need to look up the idea here
            #thing = ideaLib.getIdea(idea['urlCode'])
            #entry['date'] = thing.date.strftime('%Y-%m-%dT%H:%M:%S')
            entry['date'] = idea.date.strftime('%Y-%m-%dT%H:%M:%S')
            tagList = []
            
            if hasworkshop:
                tags = idea['workshop_category_tags']
            else:
                tags = idea['tags']
            
            for title in tags.split('|'):
                if title and title != '':
                    tagMapping = {}
                    tagMapping['title'] = title
                    tagMapping['colour'] = titleToColourMapping[title]
                    tagList.append(tagMapping)
            
            entry['tags'] = tagList
            result.append(entry)
        if len(result) == 0:
            log.info("searchIdeas return len result == 0")
            return json.dumps({'statusCode':2})
        log.info("searchIdeas return result")
        return json.dumps({'statusCode':0, 'result':result})
        
    def searchPhotos(self):
        #: this function returns json data so we set the headers appropriately
        response.headers['Content-type'] = 'application/json'
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        if self.searchType == 'tag':
            photos = photoLib.searchPhotos('tags', self.query)
        elif self.searchType == 'geo':
            photos = photoLib.searchPhotos('scope', self.query)
        else:
            keys = ['title', 'description', 'tags']
            values = [self.query, self.query, self.query]
            photos = photoLib.searchPhotos(keys, values)
        if not photos:
            return json.dumps({'statusCode':2})
        if len(photos) == 0:
            return json.dumps({'statusCode':2})
            
        colors = tagLib.getTagColouring()

        myRatings = {}
        if 'ratings' in session:
           myRatings = session['ratings']

        for photo in photos:
            p = generic.getThing(photo['urlCode'])
            if p['deleted'] != u'0' or p['disabled'] != u'0':
                continue
            entry = {}
            #: NOTE We won't need to look up this idea's author anymore if we can stick this gravatar hash into the object as well.
            u = generic.getThing(photo['userCode'])
            entry['authorHash'] = md5(u['email']).hexdigest()
            entry['title'] = p['title']
            entry['urlCode'] = p['urlCode']
            entry['url'] = p['url']
            tagList = p['tags'].split('|')
            tags = []
            tagColors = []
            for tag in tagList:
                if tag and tag != '':
                    tags.append(tag)
                    color = colors[tag]
                    tagColors.append(color)
            entry['tags'] = tags
            entry['colors'] = tagColors
            entry['location'] = photoLib.getPhotoLocation(p)
            entry['voteCount'] = int(p['ups']) + int(p['downs'])
            entry['netVotes'] = int(p['ups']) - int(p['downs'])
            if entry['urlCode'] in myRatings:
                entry['rated'] = myRatings[entry['urlCode']]
            else:
                entry['rated'] = 0
            entry['thumbnail'] = "/images/photos/" + p['directoryNum_photos'] + "/thumbnail/" + p['pictureHash_photos'] + ".png"
            entry['photoLink'] = "/profile/" + u['urlCode'] + "/" + u['url'] + "/photo/show/" + p['urlCode']
            entry['numComments'] = discussionLib.getDiscussionForThing(p)['numComments']
            entry['authorCode'] = entry['userCode'] = p['userCode']
            entry['authorURL'] = entry['user_url'] = p['user_url']
            entry['authorName'] = entry['user_name'] = p['user_name']
            result.append(entry)
        if len(result) == 0:
            return json.dumps({'statusCode':2})
        return json.dumps({'statusCode':0, 'result':result})

    def searchInitiatives(self):
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        #elif self.query.count('%') == len(self.query) and self.searchType != 'geo':
            # Prevent wildcard searches
            #return json.dumps({'statusCode':2})
        result = []
        if self.searchType == 'tag':
            initiatives = initiativeLib.searchInitiatives('tags', self.query)
        elif self.searchType == 'geo':
            scope = '0' + self.query.replace('||', '|0|')
            initiatives = initiativeLib.searchInitiatives(['scope'], [scope])
        elif self.searchType == 'browse':
            initiatives = initiativeLib.getPublishedInitiatives()
        else:
            keys = ['title', 'description', 'tags']
            values = [self.query, self.query, self.query]
            initiatives = initiativeLib.searchInitiatives(keys, values)
        if not initiatives:
            return json.dumps({'statusCode':2})
        if len(initiatives) == 0:
            return json.dumps({'statusCode':2})
            
        for initiative in initiatives:
            i = initiative
            if i['deleted'] != u'0' or i['disabled'] != u'0':
                continue
            if i['public'] == '0':
                continue

            entry = jsonLib.getJsonProperties(i)

            result.append(entry)
        if len(result) == 0:
            return json.dumps({'statusCode':2})
        return json.dumps({'statusCode':0, 'result':result})
    
    def searchItemGeo(self, id1, id2):
        if 'memberButton' in request.params:
            searchItem = "users"
        elif 'workshopButton' in request.params:
            searchItem = "workshops"
        else:
            abort(404)
         
        scopeLevel = 0
        geoScopeTitle = "Planet Earth"
        geoTagString = "||"
        if 'geoTagCountry' in request.params and request.params['geoTagCountry'] != '0':
            geoTagCountry = request.params['geoTagCountry']
            geoScopeTitle = geoTagCountry
            geoTagString += utils.urlify(geoTagCountry) + "||"
            scopeLevel = 2
        else:
            geoTagCountry = "0"
            geoTagString += "||"
            
        if 'geoTagState' in request.params and request.params['geoTagState'] != '0':
            geoTagState = request.params['geoTagState']
            geoScopeTitle = "The State of " + geoTagState
            geoTagString += utils.urlify(geoTagState) + "||"
            scopeLevel = 4
        else:
            geoTagState = "0"
            geoTagString += "||"
            
        if 'geoTagCounty' in request.params and request.params['geoTagCounty'] != '0':
            geoTagCounty = request.params['geoTagCounty']
            geoScopeTitle = "The County of " + geoTagCounty
            geoTagString += utils.urlify(geoTagCounty) + "||"
            scopeLevel = 6
        else:
            geoTagCounty = "0"
            geoTagString += "||"
            
        if 'geoTagCity' in request.params and request.params['geoTagCity'] != '0':
            geoTagCity = request.params['geoTagCity']
            geoScopeTitle = "The City of " + geoTagCity
            geoTagString += utils.urlify(geoTagCity) + "|"
            scopeLevel = 8
        else:
            geoTagCity = "0"
            geoTagString += "|"
            
        if 'geoTagPostal' in request.params and request.params['geoTagPostal'] != '0':
            # no zip code granularity searches for people
            if searchItem == 'workshops':
                geoTagPostal = request.params['geoTagPostal']
                geoTagString += utils.urlify(geoTagPostal)
                scopeLevel = 9
            else:
                geoTagPostal = "0"
        else:
            geoTagPostal = "0"
            
        if searchItem == 'users':
            c.things = []
            c.thingsTitle = 'Members residing in ' + geoScopeTitle
            c.listingType = 'searchUsers'
            uScopeList = geoInfoLib.getUserScopes(geoTagString, scopeLevel)
            for uScope in uScopeList:
                user = userLib.getUserByID(uScope.owner)
                if user['activated'] == '1' and user['disabled'] == '0' and user['deleted'] == '0':
                    c.things.append(user)
                    
        elif searchItem == 'workshops':
            c.things = []
            c.thingsTitle = 'Workshops scoped under ' + geoScopeTitle
            c.listingType = 'searchWorkshops'
            c.things = []
            c.things = workshopLib.getWorkshopsByScope(geoTagString, scopeLevel)
            
        return render('/derived/6_search.bootstrap')

    def zipLookup(self):
        result = []
        j = geoInfoLib.getPostalInfo(self.zip)
        country = 'united-states'
        state = j['StateFullName']
        county = j['County']
        city = j['CityMixedCase']

        countryScope = '0||' + country + '||0||0||0|0'
        stateScope = '0||' + country + '||' + utils.urlify(state) + '||0||0|0'
        countyScope = '0||' + country + '||' + utils.urlify(state) + '||' + utils.urlify(county) + '||0|0'
        cityScope = '0||' + country + '||' + utils.urlify(state) + '||' + utils.urlify(county) + '||' + utils.urlify(city) + '|0'
        zipScope = '0||' + country + '||' + utils.urlify(state) + '||' + utils.urlify(county) + '||' + utils.urlify(city) + '|' + self.zip
        scopeMap = []
        scopeMap.extend((countryScope, stateScope, countyScope, cityScope, zipScope))

        exceptions = utils.getGeoExceptions()
        
        getGeoInfo= {
        	'Country' : getCountryInfo,
        	'State': getStateInfo,
        	'County': getCountyInfo,
        	'City': getCityInfo,
        	'Postalcode': getPostalInfo,
        }
        
        geoArguments= {
        	'Country' : [country],
        	'State': [state, country],
        	'County': [county, state, country],
        	'City': [city, state, country],
        	'Postalcode': [self.zip],
        }
        
        geoPopulation= {
        	'Country' : 'Country_population',
        	'State': 'Population',
        	'County': 'Population',
        	'City': 'Population',
        	'Postalcode': 'Population',
        }

        for scope in scopeMap:
            scopeInfo = utils.getPublicScope(scope)
            geoInfo = getGeoInfo[scopeInfo['level'].title()](*geoArguments[scopeInfo['level'].title()]) 
             
            entry = {}
            if geoInfo:
                population = geoInfo[geoPopulation[scopeInfo['level'].title()]]
                entry['population'] = population
            entry['name'] = scopeInfo['name']
            entry['flag'] = scopeInfo['flag']
            entry['href'] = scopeInfo['href']
            entry['level'] = scopeInfo['level'].title()
            entry['sep'] = ','

           #  if entry['level'] != 'Country' and entry['level'] != 'Postalcode':
#                 members = 0
#                 zipcodes = getZipCodesBy(entry['level'],entry['name'])              
#                 for zipcode in zipcodes:
#                     log.info(zipcode)
#                     members += userLib.getUsersPerZipCode(zipcode)
#                 log.info("There are %d members in %s"%(members,entry['level']))

            entry['fullName'] = entry['level'] + ' of ' + entry['name']
            entry['scope'] = scope[1:]
            
            if entry['name'] in exceptions and exceptions[entry['name']] == entry['level']:
                log.info('Found geo exception!')
                continue
            
                        # for flipboard style layout    
            defaultPhoto = "/images/grey.png"

            # current scope search for photos and initaitives is slightly different - should be reconciled
            initScope = scope.replace('||', '|0|')
            photoScope = scope[1:]

            initiatives = initiativeLib.searchInitiatives(['scope'], [initScope])
            if initiatives and len(initiatives) != 0:
                i = initiatives[-1]
                if 'directoryNum_photos' in i:
                    entry['photo'] = "/images/photos/" + i['directoryNum_photos'] + "/photo/" + i['pictureHash_photos'] + ".png"
            else:
                photos = photoLib.searchPhotos('scope', photoScope)
                if photos and len(photos) != 0:
                    photos = sort.sortBinaryByTopPop(photos)
                    p = photos[0]
                    entry['photo'] = "/images/photos/" + p['directoryNum_photos'] + "/photo/" + p['pictureHash_photos'] + ".png"
                else:
                    entry['photo'] = defaultPhoto
            
            result.append(entry)                

        if len(result) == 0:
            return json.dumps({'statusCode':2})
        return json.dumps({'statusCode':0, 'result':result})


    # kludged this function, using zipLookup with parameter would be better
    def zipLookupPhotos(self):
        result = []
        j = geoInfoLib.getPostalInfo(self.zip)
        country = 'united-states'
        state = j['StateFullName']
        county = j['County']
        city = j['CityMixedCase']

        countryScope = '0||' + country + '||0||0||0|0'
        stateScope = '0||' + country + '||' + utils.urlify(state) + '||0||0|0'
        countyScope = '0||' + country + '||' + utils.urlify(state) + '||' + utils.urlify(county) + '||0|0'
        cityScope = '0||' + country + '||' + utils.urlify(state) + '||' + utils.urlify(county) + '||' + utils.urlify(city) + '|0'
        zipScope = '0||' + country + '||' + utils.urlify(state) + '||' + utils.urlify(county) + '||' + utils.urlify(city) + '|' + self.zip
        scopeMap = []
        scopeMap.extend((countryScope, stateScope, countyScope, cityScope, zipScope))

        exceptions = utils.getGeoExceptions()

        for scope in scopeMap:
            scopeInfo = utils.getPublicScope(scope)
            entry = {}
            entry['name'] = scopeInfo['name']
            entry['flag'] = scopeInfo['flag']
            entry['href'] = scopeInfo['href']
            entry['level'] = scopeInfo['level'].title()

            if entry['name'] in exceptions and exceptions[entry['name']] == entry['level']:
                log.info('Found geo exception!')
                continue

            # for flipboard style layout    
            defaultPhoto = "/images/grey.png"

            # current scope search for photos and initaitives is slightly different - should be reconciled
            initScope = scope.replace('||', '|0|')
            photoScope = scope[1:]

            initiatives = initiativeLib.searchInitiatives(['scope'], [initScope])
            if initiatives and len(initiatives) != 0:
                i = initiatives[-1]
                entry['photo'] = "/images/photos/" + i['directoryNum_photos'] + "/photo/" + i['pictureHash_photos'] + ".png"
            else:
                photos = photoLib.searchPhotos('scope', photoScope)
                if photos and len(photos) != 0:
                    photos = sort.sortBinaryByTopPop(photos)
                    p = photos[0]
                    entry['photo'] = "/images/photos/" + p['directoryNum_photos'] + "/photo/" + p['pictureHash_photos'] + ".png"
                else:
                    entry['photo'] = defaultPhoto

            result.append(entry)                

        if len(result) == 0:
            return json.dumps({'statusCode':2})
        return json.dumps({'statusCode':0, 'result':result})
