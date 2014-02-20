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

    def getActivity(self, comments = 0, type = 'auto', offset = 0, max = 30):
		# get recent activity and return it into json format
		result = []
		allActivity = []

		if type == 'all':
			recentActivity = activityLib.getRecentActivity(12)

		elif type == 'following' and c.authuser:
			if c.privs['participant']:
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
				followingActivity = activityLib.getActivityForObjectAndUserList(max, interestedObjects, interestedUsers, 0, 0)

			if followingActivity:
				recentActivity = followingActivity[offset:max]
			else:
				alertMsg = "You are not following any people, workshops or initiatives yet!"
				return json.dumps({'statusCode': 1 , 'alertMsg' : alertMsg , 'alertType' : 'alert-info' })

		elif type == 'geo' and c.authuser:
		    # try getting the activity of their area
		    userScope = getGeoScope( c.authuser['postalCode'], "United States" )
		    scopeList = userScope.split('|')
		    countyScope = '||united-states||' + scopeList[4] + '||' + scopeList[6]
		    #log.info("countyScope is %s"%countyScope)
		    # this is sorted by reverse date order by the SELECT in getRecentGeoActivity
		    countyActivity = activityLib.getRecentGeoActivity(max, countyScope)
		    if countyActivity:
		    	recentActivity = countyActivity[offset:max]
		    else:
		    	alertMsg = "There is no activity in your county yet. Add something!"
		    	return json.dumps({'statusCode': 1 , 'alertMsg' : alertMsg , 'alertType' : 'alert-info' })

		else:
			recentActivity = activityLib.getRecentActivity(12)
		
		myRatings = {}
		if 'ratings' in session:
			myRatings = session['ratings']

		for item in recentActivity:
			entry = {}
			# item attributes
			entry['title'] = item['title']
			entry['objType'] = item.objType
			if item.objType == 'discussion':
				if item['discType'] == 'update':
					entry['objType'] = 'update'
			entry['urlCode'] = item['urlCode']
			entry['url'] = item['url']
			entry['date'] = item.date.strftime('%Y-%m-%d at %H:%M:%S')
			entry['fuzzyTime'] = fuzzyTime.timeSince(item.date)
			if 'views' in item:
				entry['views'] = str(item['views'])
			else:
				entry['views'] = '0'

			# attributes that vary accross items
			entry['text'] = '0'
			if 'text' in item:
				entry['text'] = item['text']
			elif 'description' in item:
				entry['text'] = item['description']
			entry['html'] = m.html(entry['text'], render_flags=m.HTML_SKIP_HTML)
			if 'link' in item:
				entry['link'] = item['link']
			else:
				entry['link'] = '0'
			if 'cost' in item:
				entry['cost'] = item['cost']
			else:
				entry['cost'] = ''
			entry['article'] = 'a'
			if entry['objType'] == 'idea' or entry['objType'] == 'update' or entry['objType'] == 'initiative':
				entry['article'] = 'an'

			# href
			# note: we should standardize the way object urls are constructed
			if item.objType == 'photo':
			    entry['href'] = '/profile/' + item['userCode'] + '/' + item['user_url'] + "/photo/show/" + item['urlCode']
			else:
			    entry['href'] = '/' + item.objType + '/' + item['urlCode'] + '/' + item['url']

			if 'workshopCode' in item:
			    entry['parentHref'] = '/workshop/' + item['workshopCode'] + '/' + item['workshop_url']
			    entry['href'] = entry['parentHref'] + entry['href']
			elif 'initiativeCode' in item:
			    entry['parentHref'] = '/initiative/' + item['initiativeCode'] + '/' + item['initiative_url']
			    if entry['objType'] == 'update':
			        entry['href'] = entry['parentHref'] + '/updateShow/' + item['urlCode']
			    else:
			        entry['href'] = entry['parentHref'] + entry['href']
		    
			# modifications for children of workshops and initiatives
			entry['parentTitle'] = ''
			entry['parentObjType'] = ''
			if 'workshopCode' in item:
			    entry['parentTitle'] = item['workshop_title']
			    entry['parentObjType'] = 'workshop'
			elif 'initiativeCode' in item:
			    entry['parentTitle'] = item['initiative_title']
			    entry['parentObjType'] = 'initiative'

			# photo
			if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
				entry['mainPhoto'] = "/images/photos/%s/photo/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
				entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
			else:
				entry['mainPhoto'] = '0'
				entry['thumbnail'] = '0'

			#tags
			tags = []
			tagList = []
			if 'tags' in item:
			    tagList = item['tags'].split('|')
			elif 'initiative_tags' in item:
			    tagList = item['initiative_tags'].split('|')
			elif 'workshop_category_tags' in item:
			    tagList = item['workshop_category_tags'].split('|')
			for tag in tagList:
			    if tag and tag != '':
			        tags.append(tag)
			entry['tags'] = tags

			# scope attributes
			if 'scope' in item:
				entry['scope'] = item['scope']
			elif 'initiative_scope' in item:
				entry['scope'] = item['initiative_scope']
			elif 'workshop_public_scope' in item:
				entry['scope'] = item['workshop_public_scope']
			else:
				entry['scope'] = '0||united-states||0||0||0|0'
			scopeInfo = utils.getPublicScope(entry['scope'])
			entry['scopeName'] = scopeInfo['name']
			entry['scopeLevel'] = scopeInfo['level']
			entry['scopeHref'] = scopeInfo['href']
			entry['flag'] = scopeInfo['flag']

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

			# comments
			discussion = discussionLib.getDiscussionForThing(item)
			entry['discussion'] = discussion['urlCode']
			entry['numComments'] = 0
			if 'numComments' in item:
				entry['numComments'] = item['numComments']

			# author data
			# CCN - need to find a way to optimize this lookup
			author = userLib.getUserByID(item.owner)
			entry['authorName'] = author['name']
			entry['authorPhoto'] = utils._userImageSource(author)
			entry['authorCode'] = author['urlCode']
			entry['authorURL'] = author['url']
			entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']

			entry['parentTitle'] = ''
			entry['parentObjType'] = ''
			entry['article'] = 'a'
			if entry['objType'] == 'idea' or entry['objType'] == 'update' or entry['objType'] == 'initiative':
				entry['article'] = 'an'

			# modifications for children of workshops and initiatives
			if 'workshopCode' in item:
				entry['parentTitle'] = item['workshop_title']
				entry['parentObjType'] = 'workshop'
			elif 'initiativeCode' in item:
				entry['parentTitle'] = item['initiative_title']
				entry['parentObjType'] = 'initiative'

			result.append(entry)

		if len(result) == 0:
			return json.dumps({'statusCode':1})
		return json.dumps({'statusCode':0, 'result': result})


