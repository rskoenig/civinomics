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
        if not 'user' in session:
            return redirect('/')
        else:
            c.title = c.heading = c.workshopTitlebar = 'Home'
            c.rssURL = "/activity/rss"

            # Civinomicon
            c.conTitle = "Civinomicon"			
            c.conPhoto = '/images/civinomicon/final_sticker.png'
            c.conLink = '/search?searchQuery=civinomicon'

            # most recent workshops
            newWorkshops = []
            workshops = getActiveWorkshops()
            if len(workshops) == 0 :
                pass#c.newWorkshops = 0
            else:
                workshops = workshops[:3]
                if workshops >= 1:
                    for w in workshops:
                        title = w['title']
                        mainImage = mainImageLib.getMainImage(w)
                        if mainImage['pictureHash'] == 'supDawg':
                            imgSrc="/images/slide/thumbnail/supDawg.thumbnail"
                        elif 'format' in mainImage.keys():
                            imgSrc="/images/mainImage/%s/listing/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
                        else:
                            imgSrc="/images/mainImage/%s/listing/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
                        photo = imgSrc
                        link = "/workshops/" + w['urlCode'] + "/" + w['url']
                        item = w
                        scope = workshopLib.getPublicScope(w)
                        level = scope['level'].title()
                        if level == 'Postalcode':
                            level = 'Zip Code'
                        fix = scope['name'].replace('-',' ')
                        name = fix.title()
                        if level == 'Earth':
                            scopeTitle = 'Planet ' + name
                        else:
                            scopeTitle = level + ' of ' + name
                        newWorkshops.append({ 'photo': photo, 'title': title, 'link': link, 'item': item, 'scopeTitle':scopeTitle})
                    c.newWorkshops = newWorkshops

        return render('/derived/6_home.bootstrap')
        
    def getActivity(self, comments = 0, type = 'auto', offset = 0, max = 0):
        # get recent activity and return it into json format
        result = []
        allActivity = []
        
        # for now, until the angular call is set up to handle slices
        max = 30

        if c.privs['participant']:
            # combine the list of interested workshops
            interestedWorkshops = list(set(session['listenerWorkshops'] + session['bookmarkedWorkshops'] + session['privateWorkshops'] + session['facilitatorWorkshops']))
            #if interestedWorkshops:
                #allActivity +=  activityLib.getActivityForWorkshopList(0, interestedWorkshops, 0, offset)
                #log.info("activity len workshop list is %s"%len(allActivity))
            
            # combine the list of interested initiatives
            interestedInitiatives = list(set(session['facilitatorInitiatives'] + session['bookmarkedInitiatives']))
            #if interestedInitiatives:
                #allActivity +=  activityLib.getActivityForInitiativeList(0, interestedInitiatives)
                #log.info("activity len initiative list is %s"%len(allActivity))
                
            interestedObjects = interestedWorkshops + interestedInitiatives
            
            # users being followed
            interestedUsers = session['followingUsers']
            #if interestedUsers:
                #allActivity +=  activityLib.getActivityForUserList(0, interestedUsers, 0, offset)
                #log.info("activity len user list is %s"%len(allActivity))
                
            allActivity = activityLib.getActivityForObjectAndUserList(max, interestedObjects, interestedUsers, comments = 0, offset = 0)
            #log.info("activity len testActivity is %s"%len(testActivity))

        if allActivity:
            # the use of set() removes duplicate entries from the list of objects
            # and the other arguments specify the object key for sorting and the sort order
            #allActivity = sorted(set(allActivity), key=lambda x: x.date, reverse=True)
            recentActivity = allActivity[offset:max]
        else:
            # try getting the activity of their area
            userScope = getGeoScope( c.authuser['postalCode'], "United States" )
            scopeList = userScope.split('|')
            countyScope = '||united-states||' + scopeList[4] + '||' + scopeList[6]
            #log.info("countyScope is %s"%countyScope)
            # this is sorted by reverse date order by the SELECT in getRecentGeoActivity
            recentActivity = activityLib.getRecentGeoActivity(max, countyScope)
            if not recentActivity:
                # # this is sorted by reverse date order by the SELECT in getRecentActivity
                recentActivity = activityLib.getRecentActivity(max)
            
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

            entry['numComments'] = 0
            entry['date'] = item.date.strftime('%Y-%m-%d at %H:%M:%S')
            entry['fuzzyTime'] = fuzzyTime.timeSince(item.date)
            if 'numComments' in item:
                entry['numComments'] = item['numComments']

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

            # author data
            author = userLib.getUserByID(item.owner)
            entry['authorName'] = author['name']
            entry['authorPhoto'] = utils._userImageSource(author)
            # can pick one or the other way to do href
            #either include two atributes in entry and construct in html or construct here in one attribute
            entry['authorCode'] = author['urlCode']
            entry['authorURL'] = author['url']
            entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']

            # photos
            if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
                entry['mainPhoto'] = "/images/photos/%s/photo/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
                entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
            else:
                entry['mainPhoto'] = '0'
                entry['thumbnail'] = '0'

            # user ratings
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

            # comments
            discussion = discussionLib.getDiscussionForThing(item)
            entry['discussion'] = discussion['urlCode']

            # attributes that vary accross objects
            entry['text'] = '0'
            if 'text' in item:
                entry['text'] = item['text'][:200] 
            elif 'description' in item:
                entry['text'] = item['description'][:200]
            if len(entry['text']) >= 200:
                entry['text'] += "..."

            if 'link' in item:
                entry['link'] = item['link']
            else:
                entry['link'] = '0'

            if 'cost' in item:
                entry['cost'] = item['cost']
            else:
                entry['cost'] = ''

            result.append(entry)

        if len(result) == 0:
            return json.dumps({'statusCode':1})
            
        return json.dumps({'statusCode':0, 'result': result})

    def jsonCommentsForItem(self, urlCode):
		result = []
		comments = commentLib.getCommentsInDiscussionByCode(urlCode)
		for comment in comments:
			entry = {}
			entry['data'] = comment['data']
			entry['commentRole'] = ''
			if 'commentRole' in comment:
				entry['commentRole'] = comment['commentRole']

			entry['date'] = fuzzyTime.timeSince(comment.date)

			# comment author
			author = userLib.getUserByID(comment.owner)
			entry['authorName'] = author['name']
			entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']
			entry['authorPhoto'] = utils._userImageSource(author)

			result.append(entry)

		if len(result) == 0:
			return json.dumps({'statusCode':1})
		return json.dumps({'statusCode':0, 'result':result})

