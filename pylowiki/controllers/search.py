# -*- coding: utf-8 -*-
import logging
import urllib2

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config
from pylowiki.lib.db.geoInfo import geoDeurlify, getPostalInfo, getCityInfo, getCountyInfo, getStateInfo, getCountryInfo, getGeoScope, getGeoTitles, getWorkshopScopes

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.db.activity     as activityLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.photo        as photoLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.resource     as resourceLib
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.db.activity     as activityLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.utils           as utils
import pylowiki.lib.helpers as h

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
        c.title = c.heading = "Civinomics Search"
        c.scope = {'level':'earth', 'name':'all'}
        self.query = ''
        self.noQuery = False
        self.searchType = 'name'
        if 'searchString' in kwargs:
            searchString = kwargs['searchString']
        else:
            searchString = None
            
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
            
        if 'searchQuery' in request.params and searchString == None:
            self.query = request.params['searchQuery']
            if self.query.strip() == '':
                self.noQuery = True
        else:
            self.noQuery = True
            
        if id1 != None:
            self.query = id1
            self.noQuery = False
            
        if searchType != None:
            self.searchType = searchType
            self.noQuery = False
            
        if searchString != None:
            self.query = searchString
            self.noQuery = False
            
        if self.query == '':
            return self._noSearch()
            self.noQuery = True
            
        c.searchQuery = self.query

    def _noSearch(self, noRender = False):
        c.numUsers = 0
        c.numWorkshops = 0
        return render('/derived/6_search.bootstrap')
    
    def search(self):
        if self.noQuery:
            return self._noSearch()
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return self._noSearch()
        c.numUsers = userLib.searchUsers(['greetingMsg', 'name'], [self.query, self.query], count = True)
        c.numWorkshops = workshopLib.searchWorkshops(['title', 'description', 'workshop_category_tags'], [self.query, self.query, self.query], count = True)
        c.numResources = resourceLib.searchResources(['title', 'text', 'link'], [self.query, self.query, self.query], count = True)
        c.numDiscussions = discussionLib.searchDiscussions(['title', 'text'], [self.query, self.query], count = True)
        c.numIdeas = ideaLib.searchIdeas('title', self.query, count = True)
        c.numPhotos = photoLib.searchPhotos(['title', 'description', 'tags'], [self.query, self.query, self.query], count = True)
        c.searchType = "name"
        c.searchQuery = self.query 
        c.scope = {'level':'earth', 'name':'all'}
        return render('/derived/6_search.bootstrap')
        
    def searchWorkshopCategoryTags(self):
        if self.noQuery:
            return self._noSearch()
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return self._noSearch()
        c.numUsers = userLib.searchUsers(['greetingMsg', 'name'], [self.query, self.query], count = True)
        c.numWorkshops = workshopLib.searchWorkshops(['workshop_category_tags'], [self.query], count = True)
        c.numResources = resourceLib.searchResources(['workshop_category_tags'], [self.query], count = True)
        c.numDiscussions = discussionLib.searchDiscussions(['workshop_category_tags'], [self.query], count = True)
        c.numIdeas = ideaLib.searchIdeas('workshop_category_tags', self.query, count = True)
        c.numPhotos = photoLib.searchPhotos('tags', self.query, count = True)
        c.searchQuery = self.query
        c.searchType = "tag"
        c.scope = {'level':'earth', 'name':'all'}
        return render('/derived/6_search.bootstrap')
        
    def searchWorkshopGeo(self):
        if self.noQuery:
            return self._noSearch()
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return self._noSearch()
        c.numUsers = 0
        c.numWorkshops = workshopLib.searchWorkshops(['workshop_public_scope'], [self.query], count = True)
        c.numResources = resourceLib.searchResources(['workshop_public_scope'], [self.query], count = True)
        c.numDiscussions = discussionLib.searchDiscussions(['workshop_public_scope'], [self.query], count = True)
        c.numIdeas = ideaLib.searchIdeas('workshop_public_scope', self.query, count = True)
        c.numPhotos = photoLib.searchPhotos('scope', self.query, count = True)
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
        return render('/derived/6_search.bootstrap')
    
    def searchPeople(self):
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        people = userLib.searchUsers(['greetingMsg', 'name'], [self.query, self.query])
        if len(people) == 0:
            return json.dumps({'statusCode': 2})
        for p in people:
            entry = {}
            entry['name'] = p['name']
            entry['greetingMsg'] = p['greetingMsg']
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
    
    def searchWorkshops(self):
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        if self.searchType == 'tag':
            keys = ['workshop_category_tags']
            values = [self.query]
        elif self.searchType == 'geo':
            keys = ['workshop_public_scope']
            values = [self.query]
        else:    
            keys = ['title', 'description', 'workshop_category_tags']
            values = [self.query, self.query, self.query]
        workshops = workshopLib.searchWorkshops(keys, values)
        if not workshops:
            return json.dumps({'statusCode':2})
        if len(workshops) == 0:
            return json.dumps({'statusCode':2})
        titleToColourMapping = workshopLib.getWorkshopTagColouring()
        for w in workshops:
            entry = {}
            entry['title'] = w['title']
            entry['description'] = w['description']
            entry['urlCode'] = w['urlCode']
            entry['url'] = w['url']
            entry['activity'] = len(activityLib.getActivityForWorkshop(w['urlCode']))
            entry['bookmarks'] = len(followLib.getWorkshopFollowers(w))
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
            thing = workshopLib.getWorkshopByCode(w['urlCode'])
            entry['date'] = thing.date.strftime('%Y-%m-%dT%H:%M:%S')
            result.append(entry)
        if len(result) == 0:
            return json.dumps({'statusCode':2})
        return json.dumps({'statusCode':0, 'result':result})
    
    def searchResources(self):
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        if self.searchType == 'tag':
            keys = ['workshop_category_tags']
            values = [self.query]
        elif self.searchType == 'geo':
            keys = ['workshop_public_scope']
            values = [self.query]
        else:
            keys = ['title', 'text', 'link']
            values = [self.query, self.query, self.query]
        resources = resourceLib.searchResources(keys, values)
        if not resources:
            return json.dumps({'statusCode':2})
        if len(resources) == 0:
            return json.dumps({'statusCode':2})
        titleToColourMapping = workshopLib.getWorkshopTagColouring()
        for r in resources:
            w = generic.getThing(r['workshopCode'])
            if w['public_private'] != u'public':
                continue
            elif w['published'] != u'1':
                continue
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
            entry['numComments'] = discussionLib.getDiscussionForThing(r)['numComments']
            entry['workshopCode'] = w['urlCode']
            entry['workshopURL'] = w['url']
            entry['workshopTitle'] = w['title']
            u = userLib.getUserByID(r.owner)
            entry['authorCode'] = u['urlCode']
            entry['authorURL'] = u['url']
            entry['authorName'] = u['name']
            entry['authorHash'] = md5(u['email']).hexdigest()
            thing = resourceLib.getResource(r['urlCode'],r['url'])
            entry['date'] = thing.date.strftime('%Y-%m-%dT%H:%M:%S')
            tagList = []
            for title in r['workshop_category_tags'].split('|'):
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
    
    def searchDiscussions(self):
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        if self.searchType == 'tag':
            keys = ['workshop_category_tags']
            values = [self.query]
        elif self.searchType == 'geo':
            keys = ['workshop_public_scope']
            values = [self.query]
        else:
            keys = ['title', 'text']
            values = [self.query, self.query]
        discussions = discussionLib.searchDiscussions(keys, values)
        if not discussions:
            return json.dumps({'statusCode':2})
        if len(discussions) == 0:
            return json.dumps({'statusCode':2})
        titleToColourMapping = workshopLib.getWorkshopTagColouring()
        for d in discussions:
            w = generic.getThing(d['workshopCode'])
            if w['public_private'] != u'public':
                continue
            elif w['published'] != u'1':
                continue
            entry = {}
            entry['title'] = d['title']
            entry['text'] = d['text']
            entry['urlCode'] = d['urlCode']
            entry['url'] = d['url']
            entry['addedAs'] = d['addedAs']
            entry['voteCount'] = int(d['ups']) - int(d['downs'])
            entry['numComments'] = d['numComments']
            entry['workshopCode'] = w['urlCode']
            entry['workshopURL'] = w['url']
            entry['workshopTitle'] = w['title']
            u = userLib.getUserByID(d.owner)
            entry['authorCode'] = u['urlCode']
            entry['authorURL'] = u['url']
            entry['authorName'] = u['name']
            entry['authorHash'] = md5(u['email']).hexdigest()
            thing = discussionLib.getDiscussion(d['urlCode'])
            entry['date'] = thing.date.strftime('%Y-%m-%dT%H:%M:%S')
            tagList = []
            for title in d['workshop_category_tags'].split('|'):
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
        if self.noQuery:
            return json.dumps({'statusCode': 1})
        elif self.query.count('%') == len(self.query):
            # Prevent wildcard searches
            return json.dumps({'statusCode':2})
        result = []
        if self.searchType == 'tag':
            ideas = ideaLib.searchIdeas('workshop_category_tags', self.query)
        elif self.searchType == 'geo':
            ideas = ideaLib.searchIdeas('workshop_public_scope', self.query)
        else:
            ideas = ideaLib.searchIdeas('title', self.query)
        if not ideas:
            return json.dumps({'statusCode':2})
        if len(ideas) == 0:
            return json.dumps({'statusCode':2})
        titleToColourMapping = workshopLib.getWorkshopTagColouring()
        for idea in ideas:
            w = generic.getThing(idea['workshopCode'])
            if w['public_private'] != u'public':
                continue
            elif w['published'] != u'1':
                continue
            entry = {}
            entry['title'] = idea['title']
            entry['voteCount'] = int(idea['ups']) + int(idea['downs'])
            entry['urlCode'] = idea['urlCode']
            entry['url'] = idea['url']
            entry['addedAs'] = idea['addedAs']
            entry['numComments'] = discussionLib.getDiscussionForThing(idea)['numComments']
            entry['workshopCode'] = w['urlCode']
            entry['workshopURL'] = w['url']
            entry['workshopTitle'] = w['title']
            u = userLib.getUserByID(idea.owner)
            entry['authorCode'] = u['urlCode']
            entry['authorURL'] = u['url']
            entry['authorName'] = u['name']
            entry['authorHash'] = md5(u['email']).hexdigest()
            thing = ideaLib.getIdea(idea['urlCode'])
            entry['date'] = thing.date.strftime('%Y-%m-%dT%H:%M:%S')
            tagList = []
            for title in idea['workshop_category_tags'].split('|'):
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
        
    def searchPhotos(self):
        log.info("in search photos")
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
            log.info("after photo search")
        if not photos:
            log.info("no photos")
            return json.dumps({'statusCode':2})
        if len(photos) == 0:
            log.info("len photos is 0")
            return json.dumps({'statusCode':2})
            
        colors = workshopLib.getWorkshopTagColouring()
        for photo in photos:
            p = generic.getThing(photo['urlCode'])
            u = generic.getThing(photo['userCode'])
            if p['deleted'] != u'0' or p['disabled'] != u'0':
                continue
            log.info("after photo deleted disabled")
            entry = {}
            entry['title'] = p['title']
            tagList = p['tags'].split('|')
            tags = []
            tagColors = []
            for tag in tagList:
                if tag and tag != '':
                    tags.append(tag)
                    c = colors[tag]
                    tagColors.append(c)
            entry['tags'] = tags
            entry['colors'] = tagColors
            entry['location'] = photoLib.getPhotoLocation(p)
            entry['voteCount'] = int(p['ups']) - int(p['downs'])
            entry['urlCode'] = p['urlCode']
            entry['url'] = p['url']
            entry['thumbnail'] = "/images/photos/" + p['directoryNum_photos'] + "/thumbnail/" + p['pictureHash_photos'] + ".png"
            log.info(entry['thumbnail'])
            entry['photoLink'] = "/profile/" + u['urlCode'] + "/" + u['url'] + "/photo/show/" + p['urlCode']
            log.info(entry['photoLink'])
            entry['numComments'] = discussionLib.getDiscussionForThing(p)['numComments']
            entry['authorCode'] = u['urlCode']
            entry['authorURL'] = u['url']
            entry['authorName'] = u['name']
            entry['authorHash'] = md5(u['email']).hexdigest()
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
    
    