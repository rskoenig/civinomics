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
from pylowiki.lib.db.geoInfo import getGeoInfo, getUserScopes, getWorkshopScopes, getScopeTitle
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
		log.info("in home.py")


	def index(self):
		if not 'user' in session:
			return redirect('/')
		else:
			c.title = c.heading = c.workshopTitlebar = 'Home'
			c.activity = activityLib.getRecentActivity(12)
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


			# get user's bookmarks, listening and facilitating
			bookmarked = followLib.getWorkshopFollows(c.authuser)
			watchList = [ workshopLib.getWorkshopByCode(followObj['workshopCode']) for followObj in bookmarked ]
			c.bookmarks = []
			c.followingWorkshopCodes = []
			for workshop in watchList:
				c.bookmarks.append(workshop)
				c.followingWorkshopCodes.append(workshop['urlCode'])
			c.numB = len(c.bookmarks)

			privateList = pMemberLib.getPrivateMemberWorkshops(c.user, deleted = '0')
			if privateList:
				pmemberWorkshops = [workshopLib.getWorkshopByCode(pMemberObj['workshopCode']) for pMemberObj in privateList]
				c.privateWorkshops = [w for w in pmemberWorkshops if w['public_private'] != 'public']
				
				c.followingWorkshopCodes += [w['urlCode'] for w in pmemberWorkshops if w['public_private'] != 'public' and w['urlCode'] not in c.followingWorkshopCodes]
			c.numPW = len(c.privateWorkshops)


			listenerList = listenerLib.getListenersForUser(c.user, disabled = '0')
	        c.pendingListeners = []
	        c.listeningWorkshops = []
	        for l in listenerList:
	            lw = workshopLib.getWorkshopByCode(l['workshopCode'])
	            c.listeningWorkshops.append(lw)
	            #if lw['urlCode'] not in c.followingWorkshopCodes:
	                #c.followingWorkshopCodes.append(lw['urlCode'])
	       
	        #lwactivity = len(c.followingWorkshopCodes)
	        #log.info("followingWorkshopCodes has %s items"%str(lwactivity))
	                
	        c.numLW = len(c.listeningWorkshops)

	        facilitatorList = facilitatorLib.getFacilitatorsByUser(c.user)
	        log.info('The facilitator objects: %s' % facilitatorList)
	        c.facilitatorWorkshops = []
	        #declare initiatives here for facilitated initiatives
	        c.initiatives = []
	        c.pendingFacilitators = []
	        for f in facilitatorList:
	        	if 'pending' in f and f['pending'] == '1':
	        		c.pendingFacilitators.append(f)
	        		log.info('pending invitation!')
	        	elif f['disabled'] == '0':
					if 'workshopCode' in f:
						myW = workshopLib.getWorkshopByCode(f['workshopCode'])
						c.followingWorkshopCodes.append(myW['urlCode'])
						c.facilitatorWorkshops.append(myW)
						log.info('workshop added!')
					elif 'initiativeCode' in f:
						myI = initiativeLib.getInitiative(f['initiativeCode'])
						c.initiatives.append(myI)
						log.info('initiative added!')

			log.info("Here be ze f items: %s" %c.facilitatorItems)
	        c.numA = len(c.facilitatorItems)
	        
	        log.info("c.followingWorkshopCodes is %s"%c.followingWorkshopCodes)
	        #if c.followingWorkshopCodes:
	            #c.workshopsActivity = activityLib.getActivityForWorkshopList(30, c.followingWorkshopCodes)

	        #if c.workshopsActivity:
	            #lactivity = len(c.workshopsActivity)
	            #log.info("c.workshopsActivity has %s items"%lactivity)
	            
	        #if c.usersActivity and c.workshopsActivity:
	            #log.info("combining the lists")
	            #c.interestedActivity = set(c.usersActivity + c.workshopsActivity)
	            #c.interestedActivity = list(c.interestedActivity)
	            #c.interestedActivity.sort(key=lambda x: x.date, reverse=True)
	        #elif c.usersActivity:
	            #log.info("user list")
	            #c.interestedActivity = c.usersActivity
	        #elif c.workshopsActivity:
	            #c.interestedActivity = c.workshopsActivity
	        #else:
			    #countyScope = '||' + c.scopeMap[1]['geoURL'] + '||' + c.scopeMap[2]['geoURL'] + '||' + c.scopeMap[3]['geoURL']
			    ##log.info("countyScope is %s"%countyScope)
			    #c.interestedActivity = activityLib.getRecentGeoActivity(30, countyScope)


	        # initiatives
	        initiativeList = initiativeLib.getInitiativesForUser(c.user)
	        for i in initiativeList:
	            if i.objType == 'initiative':
	                #log.info("initiaitve 1")
	                if i['public'] == '1':
	                    if i['deleted'] != '1':
	                        c.initiatives.append(i)
	                else:
	                    if 'user' in session and ((c.user['email'] == c.authuser['email']) or c.isAdmin):
	                        c.initiatives.append(i)
	        c.numA += len(c.initiatives)
	                        
	        c.initiativeBookmarks = []
	        iwatching = followLib.getInitiativeFollows(c.user)
	        initiativeList = [ initiativeLib.getInitiative(followObj['initiativeCode']) for followObj in iwatching ]
	        for i in initiativeList:
	            if i.objType == 'initiative':
	                #log.info("initiative 2")
	                if i['public'] == '1':
	                    if i['deleted'] != '1':
	                        c.initiativeBookmarks.append(i)
	                else:
	                    if 'user' in session and ((c.user['email'] == c.authuser['email']) or c.isAdmin):
	                        c.initiativeBookmarks.append(i)
	        c.numB += len(c.initiativeBookmarks)
	        
	        #c.activity = c.interestedActivity
		

		return render('/derived/6_home.bootstrap')
