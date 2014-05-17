# -*- coding: utf-8 -*-
import logging
import urllib2
import datetime
import webhelpers.feedgenerator as feedgenerator

from pylons import config
from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.page import get_all_pages
from pylowiki.lib.db.tag import searchTags
from pylowiki.lib.db.user import searchUsers, getUserByID
from pylowiki.lib.db.geoInfo import getGeoInfo, getGeoScope, getUserScopes, getWorkshopScopes, getScopeTitle
from pylowiki.lib.db.workshop import getActiveWorkshops

import pylowiki.lib.db.user         	as userLib
import pylowiki.lib.db.message      	as messageLib
import pylowiki.lib.db.photo        	as photoLib
import pylowiki.lib.db.pmember      	as pMemberLib
import pylowiki.lib.sort            	as sort
import pylowiki.lib.db.mainImage    	as mainImageLib
import pylowiki.lib.db.follow       	as followLib
import pylowiki.lib.db.workshop     	as workshopLib
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.initiative   	as initiativeLib
import pylowiki.lib.db.activity   	    as activityLib
import pylowiki.lib.db.discussion 		as discussionLib
import pylowiki.lib.db.comment 			as commentLib
import pylowiki.lib.utils				as utils
import pylowiki.lib.json				as jsonLib
import pylowiki.lib.fuzzyTime			as fuzzyTime	
import misaka as m

import simplejson as json


log = logging.getLogger(__name__)

class HomeController(BaseController):

    def __before__(self):
        if c.conf['public.sitemap'] != "true": 
            h.check_if_login_required()
        if 'user' in session:
            if userLib.isAdmin(c.authuser.id):
                c.isAdmin = True
            if c.authuser:
                c.messages = messageLib.getMessages(c.authuser)
                c.unreadMessageCount = messageLib.getMessages(c.authuser, read = u'0', count = True)
        c.user = c.authuser
        #log.info("in home.py")
        userLib.setUserPrivs()

    def index(self):
    	c.postalCode = '95060'
    	if c.authuser:
    		c.postalCode = c.authuser['postalCode']
        c.title = c.heading = c.workshopTitlebar = 'Home'
        c.rssURL = "/activity/rss"
        return render('/derived/6_home.bootstrap')

    def getFollowingInitiatives(self, offset=0, limit=0):
		interestedInitiativeCodes = session['facilitatorInitiatives'] + session['bookmarkedInitiatives']
		# reverse list so most recent first
		interestedInitiativeCodes = interestedInitiativeCodes[::-1]

		offset = int(offset)
		limit = int(limit)
		interestedInitiativeCodes = interestedInitiativeCodes[offset:limit]

		interestedInitiatives = []
		for code in interestedInitiativeCodes:
			log.info('%s' % code)
			i = initiativeLib.getInitiative(code)
			interestedInitiatives.append(i)

		if len(interestedInitiatives) == 0:
			return json.dumps({'statusCode':1})
		else:
			result = []

			myRatings = {}
			if 'ratings' in session:
				myRatings = session['ratings']

			for item in interestedInitiatives:
				entry = {}
				#entry['urlCode'] = item
				entry['title'] = item['title']
				entry['urlCode'] = item['urlCode']
				entry['url'] = item['url']

				# user rating
				if entry['urlCode'] in myRatings:
					entry['rated'] = myRatings[entry['urlCode']]
					entry['vote'] = 'voted'
				else:
					entry['rated'] = 0
					entry['vote'] = 'nvote'

				# votes
				entry['voteCount'] = int(item['ups']) + int(item['downs'])
				entry['ups'] = int(item['ups'])
				entry['downs'] = int(item['downs'])
				entry['netVotes'] = int(item['ups']) - int(item['downs'])

				#goal votes
				if entry['voteCount'] < 100:
				    entry['goal'] = 100
				elif 'goal' in item:
					entry['goal'] = item['goal']
				else:
					entry['goal'] = 100

				# comments
				entry['numComments'] = 0
				if 'numComments' in item:
					entry['numComments'] = item['numComments']

				#tags
				tags = []
				tagList = []
				if 'tags' in item:
				    tagList = item['tags'].split('|')
				for tag in tagList:
				    if tag and tag != '':
				        tags.append(tag)
				entry['tags'] = tags

				# photo
				if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
					entry['mainPhoto'] = "/images/photos/%s/photo/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
					entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
				else:
					entry['thumbnail'] = "/images/icons/generalInitiative.jpg"

				entry['href'] = '/initiative/' + item['urlCode'] + '/' + item['url']

				# scope attributes
				if 'scope' in item:
					entry['scope'] = item['scope']
				else:
					entry['scope'] = '0||united-states||0||0||0|0'
				scopeInfo = utils.getPublicScope(entry['scope'])
				entry['scopeName'] = scopeInfo['name']
				entry['scopeLevel'] = scopeInfo['level']
				entry['scopeHref'] = scopeInfo['href']
				entry['flag'] = scopeInfo['flag']

				entry['authorID'] = item.owner
				
				result.append(entry)

			if len(result) == 0:
				return json.dumps({'statusCode':1})
			return json.dumps({'statusCode':0, 'result': result})



    def getActivity(self, comments = 0, type = 'auto', offset = 0, max = 7):
		# get recent activity and return it into json format
		result = []
		allActivity = []

		offset = int(offset)
		commments = int(comments)

		if type == 'all':
			recentActivity = activityLib.getRecentActivity(max, 0, offset)
				

		elif type == 'following' and c.authuser:
			if c.privs['participant'] or c.privs['provisional']:
				# combine the list of interested workshops
				interestedWorkshops = list(set(session['listenerWorkshops'] + session['bookmarkedWorkshops'] + session['privateWorkshops'] + session['facilitatorWorkshops']))

				# combine the list of interested initiatives
				interestedInitiatives = list(set(session['facilitatorInitiatives'] + session['bookmarkedInitiatives']))

				interestedObjects = interestedWorkshops + interestedInitiatives
				#log.info("activity interestedObjects is %s"%interestedObjects)

				# users being followed
				interestedUsers = session['followingUsers']
				#log.info("activity interestedUsers is %s"%interestedUsers)

				# this is sorted by reverse date order by the SELECT in getActivityForObjectAndUserList
				followingActivity = activityLib.getActivityForObjectAndUserList(max, interestedObjects, interestedUsers, 0, offset)

			if followingActivity:
				recentActivity = followingActivity
			else:
				alertMsg = "You are not following any people, workshops or initiatives yet!"
				return json.dumps({'statusCode': 1 , 'alertMsg' : alertMsg , 'alertType' : 'alert-info' })

		elif type == 'geo' and c.authuser:
		    # try getting the activity of their area
		    userScope = getGeoScope( c.authuser['postalCode'], "United States" )
		    scopeList = userScope.split('|')
		    countyScope = scopeList[6]
		    #log.info("countyScope is %s"%countyScope)
		    # this is sorted by reverse date order by the SELECT in getRecentGeoActivity
		    countyActivity = activityLib.getRecentGeoActivity(max, countyScope, 0, offset)
		    if countyActivity:
		    	recentActivity = countyActivity
		    else:
		    	alertMsg = "There is no activity in your county yet. Add something!"
		    	return json.dumps({'statusCode': 1 , 'alertMsg' : alertMsg , 'alertType' : 'alert-info' })

		elif type == 'initiatives':
			recentActivity = activityLib.getInitiativeActivity(max, 0, offset)

		else:
			recentActivity = activityLib.getRecentActivity(max, 0, offset)
		

		for item in recentActivity:
			
			entry = jsonLib.getJsonProperties(item)

			result.append(entry)

		if len(result) == 0:
			return json.dumps({'statusCode':1})
		return json.dumps({'statusCode':0, 'result': result})



