# -*- coding: utf-8 -*-
import logging

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers         as h
import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic

log = logging.getLogger(__name__)

class InitiativeController(BaseController):
    
    @h.login_required
    def __before__(self, action, id1 = None, id2 = None):
        c.user = None
        c.initiative = None
        existingList = ['initiativeEditHandler', 'initiativeShowHandler', 'initiativeEdit']
        if action == 'initiativeNewHandler' and id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            if not c.user:
                abort(404)
        elif action in existingList and id1 is not None and id2 is not None:
                c.initiative = initiativeLib.getInitiative(id1)
                if c.initiative:
                    c.user = userLib.getUserByCode(c.initiative['userCode'])
                else:
                  abort(404)  
        else:
            abort(404)
            
        c.resources = []
        # for compatibility with comments
        c.thing = c.initiative
        c.discussion = discussionLib.getDiscussionForThing(c.initiative)
        userLib.setUserPrivs()


    def initiativeNewHandler(self):
        title = ""
        description = ""
        scope = ""
        
        if 'initiativeTitle' in request.params:
            title = request.params['initiativeTitle']
        else:
            log.init("no initiative title")
            
        if 'initiativeDescription' in request.params:
            description = request.params['initiativeDescription']
        else:
            log.init("no initiative description")
        
        if 'initiativeScope' in request.params:
            level = request.params['initiativeScope']
            userScope = geoInfoLib.getGeoScope(c.user['postalCode'], c.user['country'])
            scopeList = userScope.split('|')
            index = 0
            for scope in scopeList:
                if scope == '':
                    scopeList[index] = '0'
                index += 1
                
            if level == 'city':
                scopeList[9] = '0'
            elif level == 'county':
                scopeList[9] = '0'
                scopeList[8] = '0'
                
            scope = '|'.join(scopeList)
            log.info('userScope is %s'%userScope)
                
        else:
            log.init("no initiative scope")
            
        if title != '' and description != '' and scope != '':
            c.initiative = initiativeLib.Initiative(c.user, title, description, scope)
            c.level = level
        else:
            log.info("missing initiaitve info: title is %s description is %s and scope is %s"%(title, description, scope))
            abort(404)
            
        return render('/derived/6_initiative_edit.bootstrap')
        
    def initiativeEdit(self):
        
        return render('/derived/6_initiative_edit.bootstrap')
 
    def initiativeShowHandler(self):
            
        return render('/derived/6_initiative_home.bootstrap')
 
