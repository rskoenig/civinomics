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
import pylowiki.lib.db.comment          as commentLib
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.flag             as flagLib
import pylowiki.lib.db.dbHelpers        as dbHelpers
import pylowiki.lib.db.generic          as generic

import simplejson as json
log = logging.getLogger(__name__)

class AdminController(BaseController):

    def __before__(self, action, thingCode = None):
        if 'user' not in session:
            abort(404)
        if action in ['users', 'workshops', 'ideas', 'discussions', 'resources']:
            if not userLib.isAdmin(c.authuser.id):
                abort(404)
        if action in ['edit', 'enable', 'disable', 'delete', 'flag']:
            if thingCode is None:
                abort(404)
            c.thing = generic.getThing(thingCode)
            if not c.thing:
                return json.dumps({'code':thingCode, 'result':'ERROR'})
            workshop = workshopLib.getWorkshopByCode(c.thing['workshopCode'])
            if not workshop:
                return json.dumps({'code':thingCode, 'result':'ERROR'})
            if c.thing.owner != c.authuser.id or not userLib.isAdmin(c.authuser.id) or not facilitatorLib.isFacilitator(c.authuser.id, workshop.id):
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
        
    
    def edit(self, thingCode):
        # A bit more complicated than enable/disable/delete
        blankText = '(blank)'
        if c.thing.objType == 'comment':
            data = request.params['textarea' + thingCode]
            data = data.strip()
            
            c.thing = commentLib.editComment(c.thing, data)
            if not c.thing:
                alert = {'type':'error'}
                alert['title'] = 'Comment edit failed.'
                alert['content'] = 'Failed to edit comment.'
            else:
                alert = {'type':'success'}
                alert['title'] = 'Comment edit.'
                alert['content'] = 'Comment edit successful.'
                eventLib.Event('Comment edited by %s'%c.authuser['name'], c.thing, c.authuser)
        elif c.thing.objType == 'idea':
            title = request.params['title']
            if title.strip() == '':
                title = blankText
            if ideaLib.editIdea(c.thing, title, c.authuser):
                alert = {'type':'success'}
                alert['title'] = 'Idea edit.'
                alert['content'] = 'Idea edit successful.'
                eventLib.Event('Idea edited by %s'%c.authuser['name'], c.thing, c.authuser)
            else:
                alert = {'type':'error'}
                alert['title'] = 'Idea edit failed.'
                alert['content'] = 'Failed to edit idea.'
        elif c.thing.objType == 'discussion':
            title = request.params['title']
            text = request.params['text']
            if title.strip() == '':
                title = blankText
            if discussionLib.editDiscussion(c.thing, title, text, c.authuser):
                alert = {'type':'success'}
                alert['title'] = 'Discussion edit.'
                alert['content'] = 'Discussion edit successful.'
                eventLib.Event('Discussion edited by %s'%c.authuser['name'], c.thing, c.authuser)
            else:
                alert = {'type':'error'}
                alert['title'] = 'Discussion edit failed.'
                alert['content'] = 'Failed to edit discussion.'
        
        session['alert'] = alert
        session.save()
        return redirect(session['return_to'])
        
    def enable(self, thingCode):
        result = 'Successfully enabled!'
        if c.thing['disabled'] == '0':
            result = 'Already enabled!'
            # Return immediately to avoid the unnecessary set + commit
            return json.dumps({'code':thingCode, 'result':result})
        c.thing['disabled'] = '0'
        dbHelpers.commit(c.thing)
        return json.dumps({'code':thingCode, 'result':result})
        
    def disable(self, thingCode):
        result = 'Successfully disabled!'
        if c.thing['disabled'] == '1':
            result = 'Already disabled!'
            # Return immediately to avoid the unnecessary set + commit
            return json.dumps({'code':thingCode, 'result':result})
        c.thing['disabled'] = '1'
        dbHelpers.commit(c.thing)
        return json.dumps({'code':thingCode, 'result':result})
        
    def delete(self, thingCode):
        result = 'Successfully deleted!'
        if c.thing['deleted'] == '1':
            result = 'Object not found.'
            return json.dumps({'code':thingCode, 'result':result})
        c.thing['deleted'] = '1'
        dbHelpers.commit(c.thing)
        return json.dumps({'code':thingCode, 'result':result})
        
    def flag(self, thingCode):
        result = 'Successfully flagged!'
        if flagLib.isFlagged(c.thing, c.authuser):
            result = 'Already flagged!'
            return json.dumps({'id':thingCode, 'result':result})
        flagLib.Flag(c.thing, c.authuser)
        return json.dumps({'id':thingCode, 'result':result})
        