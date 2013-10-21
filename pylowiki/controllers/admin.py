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
import pylowiki.lib.db.photo            as photoLib
import pylowiki.lib.db.discussion       as discussionLib
import pylowiki.lib.db.resource         as resourceLib
import pylowiki.lib.db.comment          as commentLib
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.flag             as flagLib
import pylowiki.lib.db.dbHelpers        as dbHelpers
import pylowiki.lib.db.generic          as generic
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.demo             as demoLib
import pylowiki.lib.db.message          as messageLib
import pylowiki.lib.alerts              as alertsLib
import pylowiki.lib.utils               as utils

import simplejson as json
log = logging.getLogger(__name__)

class AdminController(BaseController):

    def __before__(self, action, thingCode = None):
        if 'user' not in session:
            abort(404)
        if action in ['users', 'workshops', 'ideas', 'discussions', 'resources', 'comments', 'flaggedPhotos', 'photos']:
            if not userLib.isAdmin(c.authuser.id):
                abort(404)
                
        # Actions that require a workshop and a workshop child object
        if action in ['edit', 'enable', 'disable', 'delete', 'flag', 'immunify', 'adopt', 'publish', 'unpublish']:
            if thingCode is None:
                abort(404)
            c.thing = generic.getThing(thingCode)
            author = userLib.getUserByID(c.thing.owner)
            
            if 'workshopCode' in c.thing:
                c.w = workshopLib.getWorkshopByCode(c.thing['workshopCode'])
                workshopLib.setWorkshopPrivs(c.w)
            elif 'photoCode' in c.thing:
                # a comment of a photo
                parent = generic.getThing(c.thing['photoCode'])
                c.user = generic.getThing(parent['userCode'])
                userLib.setUserPrivs()
            elif c.thing.objType.replace("Unpublished", "") == 'photo':
                c.user = generic.getThing(c.thing['userCode'])
                userLib.setUserPrivs()
                 
            # Check if a non-admin is attempting to mess with an admin-level item
            if userLib.isAdmin(author.id):
                if not userLib.isAdmin(c.authuser.id):
                    """
                        Why are we not returning here?  Pylons will only accept an abort() here
                        to interrupt the call stack, which only returns http responses.  We want to
                        return a json response.  Trying to return from here simply ends up returning
                        two separate json responses - one for the error, and one for the success.
                        
                        Until something is written into the middleware, it's dirty, and requires code repitiion.
                    """
                    c.returnDict = json.dumps({'code':c.thing['urlCode'], 'result':'Error: cannot %s an item authored by an administrator' % action})
                    c.error = True
            
            if not c.thing:
                abort(404)
            if 'workshopCode' in c.thing:
                workshop = workshopLib.getWorkshopByCode(c.thing['workshopCode'])
                if not workshop:
                    return json.dumps({'code':thingCode, 'result':'ERROR'})
                    
        if action in ['edit', 'enable', 'disable', 'immunify', 'adopt']:
            # Check if a non-admin is attempting to mess with an item already touched by an admin
            if c.thing['disabled'] == u'1':
                event = eventLib.getEventsWithAction(c.thing, 'disabled')[0]
                if userLib.isAdmin(event.owner):
                    if not userLib.isAdmin(c.authuser.id):
                        c.returnDict = json.dumps({'code':c.thing['urlCode'], 'result':'Error: cannot %s an item touched by an administrator' % action})
                        c.error = True

        if action in ['setDemo']:
            if thingCode is None:
                abort(404)
            c.thing = generic.getThing(thingCode)
        if action in ['delete', 'setDemo']:
            if not userLib.isAdmin(c.authuser.id):
                abort(404)
        if action in ['enable', 'disable', 'immunify', 'adopt', 'publish', 'unpublish']:
            if c.thing.objType.replace("Unpublished", "") == 'photo' or 'photoCode' in c.thing:
                if not userLib.isAdmin(c.authuser.id) and c.authuser.id != c.thing.owner:
                    abort(404)
            else:
                if not userLib.isAdmin(c.authuser.id) and not facilitatorLib.isFacilitator(c.authuser, workshop):
                    abort(404)
        if action in ['enable', 'disable', 'immunify', 'delete', 'adopt']:
            # Surely there must be a more elegant way to pass along this common variable
            if 'reason' not in request.params:
                c.reason = '(No reason given.)'
            elif request.params['reason'].strip() == '':
                c.reason = '(No reason given.)'
            else:
                c.reason = request.params['reason']
        if action in ['edit']:
            if c.thing.owner == c.authuser.id:
                pass
            elif (c.thing.objType.replace("Unpublished", "") == 'photo' or 'photoCode' in c.thing) and not userLib.isAdmin(c.authuser.id):
                abort(404)
            elif not userLib.isAdmin(c.authuser.id) and not facilitatorLib.isFacilitator(c.authuser, workshop):
                abort(404)
                
    def users(self):
        c.list = userLib.getAllUsers()
        return render( "/derived/6_list_all_items.bootstrap" )
        
    def photos(self):
        c.list = photoLib.getAllPhotos()
        if not c.list:
            c.list = []
        return render( "/derived/6_list_all_items.bootstrap" )
        
    def flaggedPhotos(self):
        c.list = flagLib.getFlaggedThings('photo')
        if not c.list:
            c.list = []
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
        
    def comments(self):
        c.list = commentLib.getAllComments()
        return render( "/derived/6_list_all_items.bootstrap" )
    
    def edit(self, thingCode):
        # A bit more complicated than enable/disable/delete
        if c.error:
            return c.returnDict
        
        if c.thing['disabled'] == '1':
            # Should only happen when someone posts directly to the server instead of through the UI.
            return False
        blankText = '(blank)'
        if c.thing.objType.replace("Unpublished", "") == 'comment':
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
        elif c.thing.objType.replace("Unpublished", "") == 'idea':
            title = request.params['title']
            text = request.params['text']
            if title.strip() == '':
                title = blankText
            if ideaLib.editIdea(c.thing, title, text, c.authuser):
                alert = {'type':'success'}
                alert['title'] = 'Idea edit.'
                alert['content'] = 'Idea edit successful.'
                eventLib.Event('Idea edited by %s'%c.authuser['name'], c.thing, c.authuser)
            else:
                alert = {'type':'error'}
                alert['title'] = 'Idea edit failed.'
                alert['content'] = 'Failed to edit idea.'
        elif c.thing.objType.replace("Unpublished", "") == 'discussion':
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
        elif c.thing.objType.replace("Unpublished", "") == 'resource':
            title = request.params['title']
            link = request.params['link']
            text = request.params['text']
            if title.strip() == '':
                title = blankText
            if resourceLib.editResource(c.thing, title, text, link, c.authuser):
                alert = {'type':'success'}
                alert['title'] = 'Resource edit.'
                alert['content'] = 'Resource edit successful.'
                eventLib.Event('Resource edited by %s'%c.authuser['name'], c.thing, c.authuser)
            else:
                alert = {'type':'error'}
                alert['title'] = 'Resource edit failed.'
                alert['content'] = 'Failed to edit resource.'
        session['alert'] = alert
        session.save()
        if c.w:
            return redirect(utils.thingURL(c.w, c.thing))
        elif c.user:
            return redirect(utils.thingURL(c.user, c.thing))

    def _enableDisableDeleteEvent(self, user, thing, reason, action):
        eventTitle = '%s %s' % (action.title(), thing.objType.replace("Unpublished", ""))
        eventDescriptor = 'User with email %s %s object of type %s with code %s for this reason: %s' %(user['email'], action, thing.objType.replace("Unpublished", ""), thing['urlCode'], reason)
        eventLib.Event(eventTitle, eventDescriptor, thing, user, reason = reason, action = action) # An event for the admin/facilitator
        
        title = 'Someone %s a post you made' %(action)
        text = '(This is an automated message)'
        extraInfo = action
        parentAuthor = userLib.getUserByID(thing.owner)
        if thing.objType.replace("Unpublished", "") == 'photo':
            extraInfo = action + 'Photo'
            message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, extraInfo = extraInfo, sender = user, photoCode = thing['urlCode'])
        else:
            message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, workshop = c.w, extraInfo = extraInfo, sender = user)
        eventLib.Event(eventTitle, eventDescriptor, message, user, reason = reason, action = action) # An event for the message dispatched to the Thing's author
        message = generic.linkChildToParent(message, thing)
        dbHelpers.commit(message)
        
        if action in ['disabled', 'deleted']:
            if not flagLib.checkFlagged(thing):
                if thing.objType.replace("Unpublished", "") == 'photo':
                    flagLib.Flag(thing, user)
                else:
                    flagLib.Flag(thing, user, workshop = c.w)
                
    def _adoptEvent(self, user, thing, reason, action):
        eventTitle = '%s %s' % (action.title(), thing.objType)
        eventDescriptor = 'User with email %s %s object of type %s with code %s for this reason: %s' %(user['email'], action, thing.objType, thing['urlCode'], reason)
        eventLib.Event(eventTitle, eventDescriptor, thing, user, reason = reason, action = action) # An event for the admin/facilitator
        
        title = 'Someone %s an idea you posted' %(action)
        text = '(This is an automated message)'
        extraInfo = action
        parentAuthor = userLib.getUserByID(thing.owner)
        message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, workshop = c.w, extraInfo = extraInfo, sender = user)
        eventLib.Event(eventTitle, eventDescriptor, message, user, reason = reason, action = action) # An event for the message dispatched to the Thing's author
        message = generic.linkChildToParent(message, thing)
        dbHelpers.commit(message)

    def enable(self, thingCode):
        if c.error:
            return c.returnDict
        result = 'Successfully enabled!'
        if c.thing['disabled'] == '0':
            result = 'Already enabled!'
            # Return immediately to avoid the unnecessary set + commit
            return json.dumps({'code':thingCode, 'result':result})
        c.thing['disabled'] = '0'
        action = 'enabled'
        self._enableDisableDeleteEvent(c.authuser, c.thing, c.reason, action)
        dbHelpers.commit(c.thing)
        return json.dumps({'code':thingCode, 'result':result})
        
    def disable(self, thingCode):
        if c.error:
            return c.returnDict
        result = 'Successfully disabled!'
        if c.thing['disabled'] == '1':
            result = 'Already disabled!'
            # Return immediately to avoid the unnecessary set + commit
            return json.dumps({'code':thingCode, 'result':result})
        c.thing['disabled'] = '1'
        action = 'disabled'
        self._enableDisableDeleteEvent(c.authuser, c.thing, c.reason, action)
        dbHelpers.commit(c.thing)
        return json.dumps({'code':thingCode, 'result':result})
        
    def delete(self, thingCode):
        if c.error:
            return c.returnDict
        result = 'Successfully deleted!'
        if c.thing['deleted'] == '1':
            result = 'Object not found.'
            return json.dumps({'code':thingCode, 'result':result})
        c.thing['deleted'] = '1'
        action = 'deleted'
        self._enableDisableDeleteEvent(c.authuser, c.thing, c.reason, action)
        dbHelpers.commit(c.thing)
        return json.dumps({'code':thingCode, 'result':result})
        
    def publish(self, thingCode):
        if c.error:
            return c.returnDict
        c.thing['unpublished_by'] = ''
        c.thing.objType = c.thing.objType.replace("Unpublished", "")
        dbHelpers.commit(c.thing)
        
        # get the children and replublish them
        children = generic.getChildrenOfParent(c.thing)
        for child in children:
            child['unpublished_by'] = ''
            child.objType = child.objType.replace("Unpublished", "")
            dbHelpers.commit(child)
            
        if 'workshopCode' in c.thing:
            dparent = generic.getThing(c.thing['workshopCode'])
            returnURL = "/workshop/%s/%s/%s/%s/%s"%(dparent['urlCode'], dparent['url'], c.thing.objType.replace("Unpublished", ""), c.thing['urlCode'], c.thing['url'])
        else:
            dparent = generic.getThingByID(c.thing.owner)
            returnURL = "/profile/%s/%s/%s/show/%s"%(dparent['urlCode'], dparent['url'], c.thing.objType.replace("Unpublished", ""), c.thing['urlCode'])
        return redirect(returnURL)
        
    def unpublish(self, thingCode):
        if c.error:
            return c.returnDict
        if(c.authuser.id == c.thing.owner):
            auth = 'owner'
        elif userLib.isAdmin(c.authuser.id):
            auth = 'admin'
            
        c.thing['unpublished_by'] = auth
        c.thing.objType = c.thing.objType.replace("Unpublished", "") + "Unpublished"
        dbHelpers.commit(c.thing)
        
        # get the children and unplublish them
        children = generic.getChildrenOfParent(c.thing)
        for child in children:
            child['unpublished_by'] = 'parent'
            child.objType = child.objType.replace("Unpublished", "") + "Unpublished"
            dbHelpers.commit(child)
            
        if 'workshopCode' in c.thing:
            dparent = generic.getThing(c.thing['workshopCode'])
            returnURL = "/workshop/%s/%s/%s/%s/%s"%(dparent['urlCode'], dparent['url'], c.thing.objType.replace("Unpublished", ""), c.thing['urlCode'], c.thing['url'])
        else:
            dparent = generic.getThingByID(c.thing.owner)
            returnURL = "/profile/%s/%s/%s/show/%s"%(dparent['urlCode'], dparent['url'], c.thing.objType.replace("Unpublished", ""), c.thing['urlCode'])
        return redirect(returnURL)
        
    def flag(self, thingCode):
        if c.thing.objType != 'photo' and 'photoCode' not in c.thing:
            if not workshopLib.isScoped(c.authuser, c.w):
                return json.dumps({'code':thingCode, 'result':'Error: Unable to flag.'})
        if c.error:
            return c.returnDict
        if c.thing['disabled'] == '1':
            # Should only happen when someone posts directly to the server instead of through the UI.
            return False
        result = 'Successfully flagged!'
        if flagLib.isFlagged(c.thing, c.authuser):
            result = 'You have already flagged this item!'
            return json.dumps({'code':thingCode, 'result':result})
        if flagLib.isImmune(c.thing):
            immunifyEvent = eventLib.getEventForThingWithAction(c.thing, 'immunified')
            author = userLib.getUserByID(immunifyEvent.owner)
            if not userLib.isAdmin(c.authuser.id):
                result = 'Marked immune to flagging by %s because %s' %(author['name'], immunifyEvent['reason'])
                return json.dumps({'code':thingCode, 'result':result})
            else:
                result += ' Warning: %s has marked this as immune because %s.' % (author['email'], immunifyEvent['reason'])
        if c.thing.objType == 'photo' or 'photoCode' in c.thing:
            newFlag = flagLib.Flag(c.thing, c.authuser)
        else:
            newFlag = flagLib.Flag(c.thing, c.authuser, workshop = c.w)
        alertsLib.emailAlerts(newFlag)
        return json.dumps({'code':thingCode, 'result':result})
        
    def immunify(self, thingCode):
        if c.error:
            return c.returnDict
        if flagLib.isImmune(c.thing):
            immunifyEvent = eventLib.getEventForThingWithAction(c.thing, 'immunified')
            author = userLib.getUserByID(immunifyEvent.owner)
            result = 'Already marked immune to flagging by %s because %s' %(author['name'], immunifyEvent['reason'])
            return json.dumps({'code':thingCode, 'result':result})
        flagLib.FlagMetaData(c.thing, c.authuser, c.reason)
        result = 'Marked immune!'
        return json.dumps({'code':thingCode, 'result':result})
        
    def adopt(self, thingCode):
        if c.error:
            return c.returnDict
        if ideaLib.isAdopted(c.thing):
            adoptEvent = eventLib.getEventForThingWithAction(c.thing, 'adopted')
            author = userLib.getUserByID(adoptEvent.owner)
            result = 'Already adopted by %s because %s' %(author['name'], adoptEvent['reason'])
            return json.dumps({'code':thingCode, 'result':result})
        ideaLib.adoptIdea(c.thing)
        title = "Adopted idea"
        data = "Idea adopted by " + c.authuser['name'] + ". " + c.reason
        action = "adopted"
        self._adoptEvent(c.authuser, c.thing, c.reason, action)
        result = 'Idea Adopted!'
        return json.dumps({'code':thingCode, 'result':result})
        
    def setDemo(self, thingCode):
        response = workshopLib.setDemo(c.thing)
        return response