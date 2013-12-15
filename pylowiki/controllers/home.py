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
from pylowiki.lib.db.activity import getRecentActivity
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
			c.activity = getRecentActivity(12)
			c.rssURL = "/activity/rss"

			# Civinomicon
			c.conTitle = "Civinomicon"			
			c.conPhoto = '/images/civinomicon/final_sticker.png'
			c.conLink = '/search?searchQuery=civinomicon'

			# most recent workshops
			newWorkshops = []
			workshops = getActiveWorkshops()
			if len(workshops) == 0 :
				c.newWorkshops = 0
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


			# create mapping of the user's geoScopes
			c.scopeMap = [    
							{'level':'earth', 'name':'Earth'},
			                {'level':'country', 'name': c.authuser_geo['countryTitle']},
			                {'level':'state', 'name': c.authuser_geo['stateTitle']},
			                {'level':'county', 'name': c.authuser_geo['countyTitle']},
			                {'level':'city', 'name': c.authuser_geo['cityTitle']},
			                {'level':'postalCode', 'name': c.authuser_geo['postalCode']}
			                ]


			# add properties to mapping to help find the flags and photos
			for scope in c.scopeMap:
				scope['geoURL'] = scope['name'].replace(' ', '-')

				if scope['level'] == 'earth':
					scope['hash'] = '||0||0||0||0|0'
				if scope['level'] == 'country':
					scope['hash'] = '||' + c.scopeMap[1]['geoURL'] + '||0||0||0|0'
				if scope['level'] == 'state':
					scope['hash'] = '||' + c.scopeMap[1]['geoURL'] + '||' + c.scopeMap[2]['geoURL'] + '||0||0|0'
				if scope['level'] == 'county':
					scope['hash'] =  '||' + c.scopeMap[1]['geoURL'] + '||' + c.scopeMap[2]['geoURL'] + '||' + c.scopeMap[3]['geoURL'] + '||0|0'
				if scope['level'] == 'city':
					scope['hash'] = '||' + c.scopeMap[1]['geoURL'] + '||' + c.scopeMap[2]['geoURL'] + '||' + c.scopeMap[3]['geoURL'] + '||' + c.scopeMap[4]['geoURL'] + '|0'
				if scope['level'] == 'postalCode':
					scope['hash'] = '||' + c.scopeMap[1]['geoURL'] + '||' + c.scopeMap[2]['geoURL'] + '||' + c.scopeMap[3]['geoURL'] + '||' + c.scopeMap[4]['geoURL'] + '|' + c.scopeMap[5]['geoURL']

			county = c.authuser_geo['countyTitle']
			city = c.authuser_geo['cityTitle']
			if county == city:
			    county = county + ' County'
			    c.scopeMap[3]['name'] = county
			    city = 'City of ' + city
			    c.scopeMap[4]['name'] = city


			# set flag image urls for the geoScopes
			c.scopeMap[0]['flag'] = '/images/flags/earth.gif'
			c.scopeMap[1]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + ".gif"
			c.scopeMap[2]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + "/states/" + c.scopeMap[2]['geoURL'] + ".gif"
			c.scopeMap[3]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + "/states/" + c.scopeMap[2]['geoURL'] + "/counties/" + c.scopeMap[3]['geoURL'] + ".gif"
			c.scopeMap[4]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + "/states/" + c.scopeMap[2]['geoURL'] + "/counties/" + c.scopeMap[3]['geoURL'] + "/cities/" + c.scopeMap[4]['geoURL'] + ".gif"
			c.scopeMap[5]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + "/states/" + c.scopeMap[2]['geoURL'] + "/counties/" + c.scopeMap[3]['geoURL'] + "/cities/" + c.scopeMap[4]['geoURL'] + "/postalCodes/" + c.scopeMap[5]['geoURL'] + ".gif"
			# check to see if geoScope flag has been uploaded if not use general flag
			baseUrl = config['site_base_url']
			if baseUrl[-1] == "/":
				baseUrl = baseUrl[:-1]
			for scope in c.scopeMap:
				flag = baseUrl + scope['flag']
				flag = flag.lower()
				try:
					f = urllib2.urlopen(urllib2.Request(flag))
					scope['flag'] = flag
				except:
					scope['flag'] = '/images/flags/generalFlag.gif'


			# set the geoScopes' image 
			defaultPhoto = "/images/grey.png"

			for scope in c.scopeMap:
				initScope = '0' + scope['hash'].replace('||', '|0|')
				initiatives = initiativeLib.searchInitiatives(['scope'], [initScope])
				if initiatives and len(initiatives) != 0:
					initiatives = sort.sortBinaryByTopPop(initiatives)
					i = initiatives[0]
					scope['photo'] = "/images/photos/" + i['directoryNum_photos'] + "/photo/" + i['pictureHash_photos'] + ".png"
				else:
					photos = photoLib.searchPhotos('scope', scope['hash'])
					if photos and len(photos) != 0:
						photos = sort.sortBinaryByTopPop(photos)
						p = photos[0]
						scope['photo'] = "/images/photos/" + p['directoryNum_photos'] + "/photo/" + p['pictureHash_photos'] + ".png"
					else:
						scope['photo'] = defaultPhoto

			# don't include Earth while limited to USA
			c.scopeMap = c.scopeMap[1:]

			# get user's bookmarks, listening and facilitating
			bookmarked = followLib.getWorkshopFollows(c.authuser)
			watchList = [ workshopLib.getWorkshopByCode(followObj['workshopCode']) for followObj in bookmarked ]
			c.bookmarks = []
			for workshop in watchList:
				c.bookmarks.append(workshop)
			c.numB = len(c.bookmarks)


			privateList = pMemberLib.getPrivateMemberWorkshops(c.user, deleted = '0')
			if privateList:
				pmemberWorkshops = [workshopLib.getWorkshopByCode(pMemberObj['workshopCode']) for pMemberObj in privateList]
				c.privateWorkshops = [w for w in pmemberWorkshops if w['public_private'] != 'public']
			c.numPW = len(c.privateWorkshops)


			listenerList = listenerLib.getListenersForUser(c.user, disabled = '0')
	        c.pendingListeners = []
	        c.listeningWorkshops = []
	        for l in listenerList:
	            lw = workshopLib.getWorkshopByCode(l['workshopCode'])
	            c.listeningWorkshops.append(lw)
	        c.numLW = len(c.listeningWorkshops)

	        facilitatorList = facilitatorLib.getFacilitatorsByUser(c.user)
	        c.facilitatorWorkshops = []
	        c.pendingFacilitators = []
	        for f in facilitatorList:
	           if 'pending' in f and f['pending'] == '1':
	              c.pendingFacilitators.append(f)
	           elif f['disabled'] == '0':
	              myW = workshopLib.getWorkshopByCode(f['workshopCode'])
	              if not workshopLib.isPublished(myW) or myW['public_private'] != 'public':
	                 # show to the workshop owner, show to the facilitator owner, show to admin
	                 if 'user' in session: 
	                     if c.authuser.id == f.owner or userLib.isAdmin(c.authuser.id):
	                         c.facilitatorWorkshops.append(myW)
	              else:
	                    c.facilitatorWorkshops.append(myW)
	        c.numA = len(c.facilitatorWorkshops)

	        # initiatives
	        c.initiatives = []
	        initiativeList = initiativeLib.getInitiativesForUser(c.user)
	        for i in initiativeList:
	            if i.objType == 'initiative':
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
	                if i['public'] == '1':
	                    if i['deleted'] != '1':
	                        c.initiativeBookmarks.append(i)
	                else:
	                    if 'user' in session and ((c.user['email'] == c.authuser['email']) or c.isAdmin):
	                        c.initiativeBookmarks.append(i)
	        c.numB += len(c.initiativeBookmarks)
		

		return render('/derived/6_home.bootstrap')