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

import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.message          as messageLib

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

	def index(self):
		c.title = c.heading = c.workshopTitlebar = 'Home'
		c.activity = getRecentActivity(20)
		c.rssURL = "/activity/rss"

		if 'user' in session:
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

			# check to see if flag has been uploaded if not switch it to the general flag
			baseUrl = config['site_base_url']
			if baseUrl[-1] == "/":
				baseUrl = baseUrl[:-1]
			for scope in c.scopeMap:
				flag = baseUrl + scope['flag']
				try:
					f = urllib2.urlopen(urllib2.Request(flag))
					scope['flag'] = flag
				except:
					scope['flag'] = '/images/flags/generalFlag.gif'


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