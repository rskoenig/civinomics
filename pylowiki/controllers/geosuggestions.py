import logging, re, pickle, formencode



from pylons import request, response, session, tmpl_context as c
from string import capwords
from pylowiki.lib.utils import urlify
from pylowiki.lib.db.geoInfo import geoDeurlify, getPostalInfo, getCityInfo, getCountyInfo, getStateInfo, getCountryInfo, getGeoScope, getGeoTitles, getWorkshopScopes
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop, getAdoptedSuggestionsForWorkshop, getActiveSuggestionsForWorkshop, getInactiveSuggestionsForWorkshop, getDisabledSuggestionsForWorkshop, getDeletedSuggestionsForWorkshop, getAllSuggestions 
from pylowiki.lib.db.workshop import Workshop, getWorkshop, isScoped, getWorkshopByID
from pylowiki.lib.base import BaseController, render
import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h

import simplejson as json

import re

log = logging.getLogger(__name__)

class GeosuggestionsController(BaseController):

    def showPostalSuggestions(self, id1, id2):
        c.country = geoDeurlify(id1)
        c.postal = id2
        
        c.heading = "Suggestions in Postal Code " + c.postal
        c.geoType = 'postal'
        c.objecttype = 'suggestion'
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
        c.countryLink = '/geo/country/' + urlify(c.country)
        c.countryFlag = '/images/flags/country/' + urlify(c.country) + '/' + urlify(c.country) + '_thumb.gif'
        c.country = capwords(c.country)
        c.population = c.geoInfo['Population']
        c.medianAge = c.geoInfo['MedianAge']
        c.numberHouseholds = c.geoInfo['HouseholdsPerZipCode']
        c.personsHousehold = c.geoInfo['PersonsPerHousehold']
        scope = getGeoScope(c.postal, c.country)
        scopeLevel = '10'

        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.suggestions = []    
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)    
           if w['deleted'] != '1' and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) == int(scopeLevel):
                             doit = 1
                      else:
                              doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:   
                            wsuggs = getSuggestionsForWorkshop(w['urlCode'], w['url'])
                            for suggestion in wsuggs:
                                c.suggestions.append(suggestion)
                                
                            
        if 'user' in session:
            ratedSuggestionIDs = []
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                ratedSuggestionIDs = sugRateDict.keys()
        
        for suggestion in c.suggestions:
            """ Grab first 250 chars as a summary """
            if len(suggestion['data']) <= 250:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
            else:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
        
            if 'user' in session:    
                """ Grab the associated rating, if it exists """
                found = False
                try:
                    index = ratedSuggestionIDs.index(suggestion.id)
                    found = True
                except:
                    pass
                if found:
                    suggestion.rating = getRatingByID(sugRateDict[suggestion.id])
                else:
                    suggestion.rating = False
                            
                            
        c.count = len( c.suggestions )
        c.paginator = paginate.Page(
            c.suggestions, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_geoSuggestions.bootstrap')



    def showCitySuggestions(self, id1, id2, id3):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        c.city = geoDeurlify(id3)
        
        c.heading = "List Suggestions: City of " + capwords(c.city)
        c.geoType = 'city'
        c.objecttype = 'suggestion'
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
        c.countryLink = '/geo/country/' + urlify(c.country)
        c.countryFlag = '/images/flags/country/' + urlify(c.country) + '/' + urlify(c.country) + '_thumb.gif'
        c.country = capwords(c.country)
        c.population = c.geoInfo['Population']
        c.medianAge = c.geoInfo['Population_Median']
        c.numberHouseholds = c.geoInfo['Total_Households']
        c.personsHousehold = c.geoInfo['Average_Household_Size']
        scope = '||' + urlify(c.country) + '||' + urlify(c.state) + '||' + urlify(c.county) + '||' + urlify(c.city) + '|' +  '00000'
        scopeLevel = "09"
        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.suggestions = [] 
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)    
           if w['deleted'] != '1' and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) == int(scopeLevel):
                             doit = 1
                      else:
                              doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:   
                            wsuggs = getSuggestionsForWorkshop(w['urlCode'], w['url'])
                            for suggestion in wsuggs:
                                c.suggestions.append(suggestion)
                                
                            
        if 'user' in session:
            ratedSuggestionIDs = []
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                ratedSuggestionIDs = sugRateDict.keys()
        
        for suggestion in c.suggestions:
            """ Grab first 250 chars as a summary """
            if len(suggestion['data']) <= 250:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
            else:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
        
            if 'user' in session:    
                """ Grab the associated rating, if it exists """
                found = False
                try:
                    index = ratedSuggestionIDs.index(suggestion.id)
                    found = True
                except:
                    pass
                if found:
                    suggestion.rating = getRatingByID(sugRateDict[suggestion.id])
                else:
                    suggestion.rating = False
                            
                            
        c.count = len( c.suggestions )
        c.paginator = paginate.Page(
            c.suggestions, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_geoSuggestions.bootstrap')
        

    def showCountySuggestions(self, id1, id2, id3):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        c.county = geoDeurlify(id3)
        
        c.heading = "List Suggestions: County of " + capwords(c.county)
        c.geoType = 'county'
        c.objecttype = 'suggestion'
        c.geoInfo = getCountyInfo(c.county, c.state, c.country)
        c.county = capwords(c.geoInfo['County'])
        c.countyFlag = '/images/flags/country/united-states/county_thumb.png'
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        c.stateLink = '/geo/state/' + c.country + '/' + c.geoInfo['StateFullName']
        c.countryLink = '/geo/country/' + urlify(c.country)
        c.countryFlag = '/images/flags/country/' + urlify(c.country) + '/' + urlify(c.country) + '_thumb.gif'
        c.country = capwords(c.country)
        c.state = capwords(c.geoInfo['StateFullName'])
        c.population = c.geoInfo['Population']
        c.medianAge = c.geoInfo['Population_Median']
        c.numberHouseholds = c.geoInfo['Total_Households']
        c.personsHousehold = c.geoInfo['Average_Household_Size']
        scope = '||' + urlify(c.country) + '||' + urlify(c.state) + '||' + urlify(c.county) + '||' + 'LaLaLa|00000'
        scopeLevel = "07"
        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.suggestions = [] 
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)    
           if w['deleted'] != '1' and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) == int(scopeLevel):
                             doit = 1
                      else:
                              doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:   
                            wsuggs = getSuggestionsForWorkshop(w['urlCode'], w['url'])
                            for suggestion in wsuggs:
                                c.suggestions.append(suggestion)
                                
                            
        if 'user' in session:
            ratedSuggestionIDs = []
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                ratedSuggestionIDs = sugRateDict.keys()
        
        for suggestion in c.suggestions:
            """ Grab first 250 chars as a summary """
            if len(suggestion['data']) <= 250:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
            else:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
        
            if 'user' in session:    
                """ Grab the associated rating, if it exists """
                found = False
                try:
                    index = ratedSuggestionIDs.index(suggestion.id)
                    found = True
                except:
                    pass
                if found:
                    suggestion.rating = getRatingByID(sugRateDict[suggestion.id])
                else:
                    suggestion.rating = False
                            
                            
        c.count = len( c.suggestions )
        c.paginator = paginate.Page(
            c.suggestions, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_geoSuggestions.bootstrap')
    
    
    def showStateSuggestions(self, id1, id2):
        c.country = geoDeurlify(id1)
        c.state = geoDeurlify(id2)
        
        c.heading = "List Suggestions: State of " + capwords(c.state)
        c.geoType = 'state'
        c.objecttype = 'suggestion'
        c.geoInfo = getStateInfo(c.state, c.country)
        c.stateFlag = '/images/flags/country/united-states/states/' + urlify(c.state) + '_thumb.gif'
        c.countryLink = '/geo/country/' + urlify(c.country)
        c.countryFlag = '/images/flags/country/' + urlify(c.country) + '/' + urlify(c.country) + '_thumb.gif'
        c.country = capwords(c.country)
        c.state = capwords(c.geoInfo['StateFullName'])
        c.population = c.geoInfo['Population']
        c.medianAge = c.geoInfo['Population_Median']
        c.numberHouseholds = c.geoInfo['Total_Households']
        c.personsHousehold = c.geoInfo['Average_Household_Size']
        scope = '||' + urlify(c.country) + '||' + urlify(c.state) + '||' + 'LaLaLa||LaLaLa|00000'
        scopeLevel = "05"
        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.suggestions = []
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)    
           if w['deleted'] != '1' and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) == int(scopeLevel):
                             doit = 1
                      else:
                              doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:   
                            wsuggs = getSuggestionsForWorkshop(w['urlCode'], w['url'])
                            for suggestion in wsuggs:
                                c.suggestions.append(suggestion)
                                
                            
        if 'user' in session:
            ratedSuggestionIDs = []
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                ratedSuggestionIDs = sugRateDict.keys()
        
        for suggestion in c.suggestions:
            """ Grab first 250 chars as a summary """
            if len(suggestion['data']) <= 250:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
            else:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
        
            if 'user' in session:    
                """ Grab the associated rating, if it exists """
                found = False
                try:
                    index = ratedSuggestionIDs.index(suggestion.id)
                    found = True
                except:
                    pass
                if found:
                    suggestion.rating = getRatingByID(sugRateDict[suggestion.id])
                else:
                    suggestion.rating = False
                            
                            
        c.count = len( c.suggestions )
        c.paginator = paginate.Page(
            c.suggestions, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_geoSuggestions.bootstrap')
    
    
        

    def showCountrySuggestions(self, id1):
        c.country = id1
        
        c.geoType = 'country'
        c.objecttype = 'suggestion'
        log.info('c.country is %s'%c.country)
        c.geoInfo = getCountryInfo(c.country)
        c.countryFlag = '/images/flags/country/' + urlify(c.country) + '/' + urlify(c.country) + '_thumb.gif'
        c.country = capwords(c.geoInfo['Country_title'])
        c.heading = "List Suggestions: Country of " + capwords(c.country)
        c.population = c.geoInfo['Country_population']
        c.medianAge = c.geoInfo['Country_median_age']
        c.numberHouseholds = c.geoInfo['Country_number_households']
        c.personsHousehold = c.geoInfo['Country_persons_per_household']
        c.countryLink = '/geo/country/' + urlify(c.country)
        c.countryFlag = '/images/flags/country/' + urlify(c.country) + '/' + urlify(c.country) + '_thumb.gif'
        c.country = capwords(c.country)
        scope = '||' + urlify(c.country) + '||LaLa||LaLaLa||LaLaLa|00000'
        scopeLevel = "03"
        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.suggestions = []
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)    
           if w['deleted'] != '1' and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) == int(scopeLevel):
                             doit = 1
                      else:
                              doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:   
                            wsuggs = getSuggestionsForWorkshop(w['urlCode'], w['url'])
                            for suggestion in wsuggs:
                                c.suggestions.append(suggestion)
                                
                            
        if 'user' in session:
            ratedSuggestionIDs = []
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                ratedSuggestionIDs = sugRateDict.keys()
        
        for suggestion in c.suggestions:
            """ Grab first 250 chars as a summary """
            if len(suggestion['data']) <= 250:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
            else:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
        
            if 'user' in session:    
                """ Grab the associated rating, if it exists """
                found = False
                try:
                    index = ratedSuggestionIDs.index(suggestion.id)
                    found = True
                except:
                    pass
                if found:
                    suggestion.rating = getRatingByID(sugRateDict[suggestion.id])
                else:
                    suggestion.rating = False
                            
                            
        c.count = len( c.suggestions )
        c.paginator = paginate.Page(
            c.suggestions, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_geoSuggestions.bootstrap')
        
        
        
    def showPlanetSuggestions(self):
        
        c.geoType = 'planet'
        c.objecttype = 'suggestion'
        c.heading = "List MF Suggestions: Planet Earth"
        scope = '||' + urlify(c.planet) + '||LaLa||LaLaLa||LaLaLa|00000'
        scopeLevel = "01"
        wscopes = getWorkshopScopes(scope, scopeLevel)
        c.suggestions = []  
        c.list = []
        for s in wscopes:
           wID = s['workshopID']
           w = getWorkshopByID(wID)    
           if w['deleted'] != '1' and w['startTime'] != '0000-00-00':
               if w not in c.list:
                      doit = 1
                      if w['scopeMethod'] == 'publicScope' and int(w['publicScope']) == int(scopeLevel):
                             doit = 1
                      else:
                              doit = 0

                      if doit:
                          offset = 10 - int(scopeLevel)
                          offset = offset * -1
                          wTest = s['scope'].split('|')
                          sTest = scope.split('|')
                          ##log.info('offset is %s'%offset)
                          if wTest[:offset] == sTest[:offset]:   
                            wsuggs = getSuggestionsForWorkshop(w['urlCode'], w['url'])
                            for suggestion in wsuggs:
                                c.suggestions.append(suggestion)
                                
                            
        if 'user' in session:
            ratedSuggestionIDs = []
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                ratedSuggestionIDs = sugRateDict.keys()
        
        for suggestion in c.suggestions:
            """ Grab first 250 chars as a summary """
            if len(suggestion['data']) <= 250:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
            else:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
        
            if 'user' in session:    
                """ Grab the associated rating, if it exists """
                found = False
                try:
                    index = ratedSuggestionIDs.index(suggestion.id)
                    found = True
                except:
                    pass
                if found:
                    suggestion.rating = getRatingByID(sugRateDict[suggestion.id])
                else:
                    suggestion.rating = False
                            
                            
        c.count = len( c.suggestions )
        c.paginator = paginate.Page(
            c.suggestions, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_geoSuggestions.bootstrap')
        
        
    def showAllSuggestions(self):
        
        c.geoType = 'none'
        c.objecttype = 'suggestion'
        c.heading = "All Suggestions"
        c.suggestions = getAllSuggestions()  
        if 'user' in session:
            ratedSuggestionIDs = []
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                ratedSuggestionIDs = sugRateDict.keys()
        
        for suggestion in c.suggestions:
            """ Grab first 250 chars as a summary """
            if len(suggestion['data']) <= 250:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
            else:
                suggestion['suggestionSummary'] = h.literal(h.reST2HTML(suggestion['data']))
        
            if 'user' in session:    
                """ Grab the associated rating, if it exists """
                found = False
                try:
                    index = ratedSuggestionIDs.index(suggestion.id)
                    found = True
                except:
                    pass
                if found:
                    suggestion.rating = getRatingByID(sugRateDict[suggestion.id])
                else:
                    suggestion.rating = False
        

        c.count = len( c.suggestions )
        c.paginator = paginate.Page(
            c.suggestions, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )

        return render('/derived/list_geoSuggestions.bootstrap')



    ##@h.login_required
    def geoHandler(self, id1, id2):
        country = id1
        postalCode = id2
        ##log.info('geoHandler %s %s' % (postalCode, country))

        titles = getGeoTitles(postalCode, country)
        ##log.info('geoHandler titles %s' % titles)
        return json.dumps({'result':titles})

