# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers as h

import pylowiki.lib.db.activity         as activityLib
import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.workshop         as workshopLib
import pylowiki.lib.db.idea             as ideaLib
import pylowiki.lib.db.discussion       as discussionLib
import pylowiki.lib.db.resource         as resourceLib
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.flag             as flagLib

log = logging.getLogger(__name__)

class AdminController(BaseController):

    def __before__(self, action):
        if 'user' not in session:
            abort(404)
        if not userLib.isAdmin(c.authuser.id):
            abort(404)
    
    def users(self):
        c.list = userLib.getAllUsers()
        return render( "/derived/6_list_all_items.bootstrap" )
    
    def workshops(self):
        c.list = workshopLib.getWorkshops()
        return render( "/derived/6_list_all_items.bootstrap" )
    
    def ideas(self):
        c.list = ideaLib.getAllIdeas()
        return render( "/derived/6_list_all_items.bootstrap" )
    
    def discussions(self):
        c.list = discussionLib.getDiscussions()
        return render( "/derived/6_list_all_items.bootstrap" )
    
    def resources(self):
        c.list = resourceLib.getAllResources()
        return render( "/derived/6_list_all_items.bootstrap" )