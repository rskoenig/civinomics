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

class TestnewsletterController(BaseController):

    def displayNewsletter(self):
        c.recentActivity = activityLib.getInitiativeActivity(3, 0, 0)
        baseUrl = utils.getBaseUrl()
        for i in c.recentActivity:
        	# scope attributes
			scopeInfo = utils.getPublicScope(i['scope'])
			i['scopeName'] = scopeInfo['name']
			i['scopeLevel'] = scopeInfo['level']
			i['scopeHref'] = scopeInfo['href']
			i['flag'] = scopeInfo['flag']

			#href
			i['href'] = baseUrl + '/initiative/' + i['urlCode'] + '/' + i['url']



        
        return render('/email/testNewsletter.html')
        
        
