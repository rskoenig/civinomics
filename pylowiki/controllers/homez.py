# -*- coding: utf-8 -*-
import logging
import urllib2

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.page import get_all_pages
from pylowiki.lib.db.activity import getRecentActivity
from pylowiki.lib.db.tag import searchTags
from pylowiki.lib.db.user import searchUsers, getUserByID
from pylowiki.lib.db.geoInfo import getGeoInfo, getUserScopes, getWorkshopScopes, getScopeTitle
from pylowiki.lib.db.workshop import getActiveWorkshops

import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.message      as messageLib
import pylowiki.lib.db.photo        as photoLib
import pylowiki.lib.sort            as sort
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.workshop     as workshopLib

from pylons import config
import datetime
import webhelpers.feedgenerator as feedgenerator

log = logging.getLogger(__name__)


class HomezController(BaseController):

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


	def index(self):
		c.title = c.heading = c.workshopTitlebar = 'Home'
		c.activity = getRecentActivity(12)
		c.rssURL = "/activity/rss"
		defaultPhoto = "/images/grey.png"

		if 'user' in session:

			scope = c.authuser_geo['scope']

			# is there a way to get just the top photo that is less computationally intense?
			zipPhotos = photoLib.searchPhotos('scope', scope)
			if zipPhotos:
				p = zipPhotos[0]
				c.zPhoto = "/images/photos/" + p['directoryNum_photos'] + "/orig/" + p['pictureHash_photos'] + ".png"
			else:
				c.zPhoto = "/images/grey.png"

			scope = scope.split('|')
			scope[-1] = '0'
			c.testTitle = ''.join(scope)

			cityPhotos = photoLib.searchPhotos('scope', scope)
			if cityPhotos:
				p = zipPhotos[0]
				c.ctyPhoto = "/images/photos/" + p['directoryNum_photos'] + "/orig/" + p['pictureHash_photos'] + ".png"
			else:
				c.ctyPhoto = "/images/grey.png"



			countryPhotos = photoLib.searchPhotos('scope', '||united-states||0||0||0|0')
			if countryPhotos:
				countryPhotos = sort.sortBinaryByTopPop(countryPhotos)
				z = countryPhotos[0]
				c.cPhoto = "/images/photos/" + z['directoryNum_photos'] + "/orig/" + z['pictureHash_photos'] + ".png"
			else:
				c.cPhoto = "/images/grey.png"


			# hack the last part of scope of and do it again
			scope = scope
			





			# check to see if County and City have same name
			county = c.authuser_geo['countyTitle']
			city = c.authuser_geo['cityTitle']
			if county == city:
			    county = 'County of ' + county
			    city = 'City of ' + city
			# fetching geos and mapping them to local variables
			c.scopeMap = [    
							{'level':'earth', 'name':'Earth'},
			                {'level':'country', 'name': c.authuser_geo['countryTitle']},
			                {'level':'state', 'name': c.authuser_geo['stateTitle']},
			                {'level':'county', 'name': county},
			                {'level':'city', 'name': city},
			                {'level':'postalCode', 'name': c.authuser_geo['postalCode']}
			                ]

			# set flag image urls for scopes in scopeMap
			for scope in c.scopeMap:
				scope['geoURL'] = scope['name'].replace(' ', '-')

			c.scopeMap[0]['flag'] = '/images/flags/earth.gif'
			c.scopeMap[1]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + ".gif"
			c.scopeMap[2]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + "/states/" + c.scopeMap[2]['geoURL'] + ".gif"
			c.scopeMap[3]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + "/states/" + c.scopeMap[2]['geoURL'] + "/counties/" + c.scopeMap[3]['geoURL'] + ".gif"
			c.scopeMap[4]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + "/states/" + c.scopeMap[2]['geoURL'] + "/counties/" + c.scopeMap[3]['geoURL'] + "/cities/" + c.scopeMap[4]['geoURL'] + ".gif"
			c.scopeMap[5]['flag'] = '/images/flags/country/' + c.scopeMap[1]['geoURL'] + "/states/" + c.scopeMap[2]['geoURL'] + "/counties/" + c.scopeMap[3]['geoURL'] + "/cities/" + c.scopeMap[4]['geoURL'] + "/postalCodes/" + c.scopeMap[5]['geoURL'] + ".gif"

			# set the image for scopes in scopeMap
			earthPhotos = photoLib.searchPhotos('scope', '||0||0||0||0|0')
			if earthPhotos and len(earthPhotos) != 0:
				earthPhotos = sort.sortBinaryByTopPop(earthPhotos)
				p = earthPhotos[0]
				c.scopeMap[0]['photo'] = "/images/photos/" + p['directoryNum_photos'] + "/orig/" + p['pictureHash_photos'] + ".png"
			else:
				c.scopeMap[0]['photo'] = defaultPhoto

			countryPhotos = photoLib.searchPhotos('scope', '||' + c.scopeMap[1]['geoURL'] + '||0||0||0|0')
			if countryPhotos and len(countryPhotos) != 0:
				countryPhotos = sort.sortBinaryByTopPop(countryPhotos)
				p = countryPhotos[0]
				c.scopeMap[1]['photo'] = "/images/photos/" + p['directoryNum_photos'] + "/orig/" + p['pictureHash_photos'] + ".png"
			else:
				c.scopeMap[1]['photo'] = defaultPhoto

			statePhotos = photoLib.searchPhotos('scope', '||' + c.scopeMap[1]['geoURL'] + '||' + c.scopeMap[2]['geoURL'] + '||0||0|0')
			if statePhotos and len(statePhotos) != 0:
				statePhotos = sort.sortBinaryByTopPop(statePhotos)
				p = statePhotos[0]
				c.scopeMap[2]['photo'] = "/images/photos/" + p['directoryNum_photos'] + "/orig/" + p['pictureHash_photos'] + ".png"
			else:
				c.scopeMap[2]['photo'] = defaultPhoto

			countyPhotos = photoLib.searchPhotos('scope', '||' + c.scopeMap[1]['geoURL'] + '||' + c.scopeMap[2]['geoURL'] + '||' + c.scopeMap[3]['geoURL'] + '||0|0')
			if countyPhotos and len(countyPhotos) != 0:
				countyPhotos = sort.sortBinaryByTopPop(countyPhotos)
				p = countyPhotos[0]
				c.scopeMap[3]['photo'] = "/images/photos/" + p['directoryNum_photos'] + "/orig/" + p['pictureHash_photos'] + ".png"
			else:
				c.scopeMap[3]['photo'] = defaultPhoto

			cityPhotos = photoLib.searchPhotos('scope', '||' + c.scopeMap[1]['geoURL'] + '||' + c.scopeMap[2]['geoURL'] + '||' + c.scopeMap[3]['geoURL'] + '||' + c.scopeMap[4]['geoURL'] + '|0')
			if cityPhotos and len(cityPhotos) != 0:
				cityPhotos = sort.sortBinaryByTopPop(cityPhotos)
				p = cityPhotos[0]
				c.scopeMap[4]['photo'] = "/images/photos/" + p['directoryNum_photos'] + "/orig/" + p['pictureHash_photos'] + ".png"
			else:
				c.scopeMap[4]['photo'] = defaultPhoto

			zipPhotos = photoLib.searchPhotos('scope', '||' + c.scopeMap[1]['geoURL'] + '||' + c.scopeMap[2]['geoURL'] + '||' + c.scopeMap[3]['geoURL'] + '||' + c.scopeMap[4]['geoURL'] + '|' + c.scopeMap[5]['geoURL'])
			if zipPhotos and len(zipPhotos) != 0:
				zipPhotos = sort.sortBinaryByTopPop(zipPhotos)
				p = zipPhotos[0]
				c.scopeMap[5]['photo'] = "/images/photos/" + p['directoryNum_photos'] + "/orig/" + p['pictureHash_photos'] + ".png"
			else:
				c.scopeMap[5]['photo'] = defaultPhoto


			# get the base url for use in flag check below
			baseUrl = config['site_base_url']
			if baseUrl[-1] == "/":
				baseUrl = baseUrl[:-1]

			for scope in c.scopeMap:
				# check to see if flag has been uploaded if not switch it to the general flag
				flag = baseUrl + scope['flag']
				try:
					f = urllib2.urlopen(urllib2.Request(flag))
					scope['flag'] = flag
				except:
					scope['flag'] = '/images/flags/generalFlag.gif'


		# get the most recent workshops - in the future this should be a featured workshop/initiative or most viewed workshop/initiative
		newWorkshops = range(3)
		workshops = getActiveWorkshops()
		for i in range(3):
			title = workshops[i]['title']
			mainImage = mainImageLib.getMainImage(workshops[i])
			if mainImage['pictureHash'] == 'supDawg':
				imgSrc="/images/slide/thumbnail/supDawg.thumbnail"
			elif 'format' in mainImage.keys():
				imgSrc="/images/mainImage/%s/listing/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
			else:
				imgSrc="/images/mainImage/%s/listing/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
			photo = imgSrc
			newWorkshops[i] = { 'photo': photo, 'title': title}
		c.newWorkshops = newWorkshops


		# user bookmarks, listening and facilitating
		watching = followLib.getWorkshopFollows(c.authuser)
		bookmarked = followLib.getWorkshopFollows(c.authuser)
		watchList = [ workshopLib.getWorkshopByCode(followObj['workshopCode']) for followObj in watching ]
		c.watching = []
		for workshop in watchList:
			c.watching.append(workshop)

		

		c.featured = {}
		c.featured['image']= "/images/grey.png"
		c.featured['list'] = ['Hyperloop', 'Syria Arms Treaty', 'Sanctuary Camp Santa Cruz']
		c.featured['link'] = "/"

		c.votingGroups = []
		planet = {}
		planet['name'] = "Earth"
		planet['flag'] = "/images/flags/earth.gif"
		planet['image'] = "/images/grey.png"
		planet['link'] = "/workshops/geo/earth/0"
		c.votingGroups.append(planet)
		country = {}
		country['name'] = "United States"
		country['flag'] = "/images/flags/country/united-states.gif"
		country['image'] = "/images/grey.png"
		country['link'] = "/workshops/geo/earth/united-states"
		c.votingGroups.append(country)
		state = {}
		state['name'] = "California"
		state['flag'] = "/images/flags/country/united-states/states/california.gif"
		state['image'] = "/images/grey.png"
		state['link'] = "/workshops/geo/earth/united-states/california"
		c.votingGroups.append(state)
		county = {}
		county['name'] = "Santa Cruz County"
		county['flag'] = "/images/flags/country/united-states/states/california/counties/santa-cruz.gif"
		county['image'] = "/images/grey.png"
		county['link'] = "/workshops/geo/earth/united-states/california/santa-cruz"
		c.votingGroups.append(county)
		city = {}
		city['name'] = "Watsonville"
		city['flag'] = "/images/flags/country/united-states/states/california/counties/santa-cruz/cities/watsonville.gif"
		city['image'] = "/images/grey.png"
		city['link'] = "/workshops/geo/earth/united-states/california/santa-cruz/watsonville"
		c.votingGroups.append(city)
		postal = {}
		postal['name'] = "95076"
		postal['flag'] = "/images/flags/generalFlag.gif"
		postal['image'] = "/images/grey.png"
		postal['link'] = "/workshops/geo/earth/united-states/california/santa-cruz/watsonville/95076"
		c.votingGroups.append(postal)
		school = {}
		school['name'] = "Stanford Alumni"
		school['flag'] = "/images/flags/stanford.gif"
		school['image'] = "/images/grey.png"
		school['link'] = "/"
		c.votingGroups.append(school)
		work = {}
		work['name'] = "CruzioWorks"
		work['flag'] = "/images/flags/cruzio.gif"
		work['image'] = "/images/grey.png"
		work['link'] = "/"
		c.votingGroups.append(work)
		return render('/derived/6_home.bootstrap')