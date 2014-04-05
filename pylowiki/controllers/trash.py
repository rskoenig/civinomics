#-*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.user         as userLib

import simplejson as json


class TrashController(BaseController):
    
    def __before__(self, action, code = None, url = None):
        if code != None:
            c.thing = generic.getThing(code)
            if not c.thing:
                return json.dumps({'statusCode':1, 'errorMsg': 'no thing with that code'})
        else:
            return json.dumps({'statusCode':1, 'errorMsg': 'no code entered'})
    
    
    def trashThingHandler( self, code ):
        # to 'trash' a thing we add the string 'Unpublished' to its obj type, effectively excepting it from database searches
        if 'user' in session and (c.authuser.id == c.thing.owner or userLib.isAdmin(c.authuser.id)):
            if c.authuser.id == c.thing.owner:
                c.thing['unpublished_by'] = 'owner'
            elif userLib.isAdmin(c.authuser.id):
                c.thing['unpublished_by'] = 'admin'
            
            # get the list of children
            children = generic.getChildrenOfParent(c.thing)
            for child in children:
                child['unpublished_by'] = 'parent'
                oldType = child.objType
                child.objType = oldType + 'Unpublished'
                dbHelpers.commit(child)
            
            # now reset the object types to unpublished
            oldType = c.thing.objType
            if not 'Unpublished' in oldType: 
                c.thing.objType = oldType + 'Unpublished'
                dbHelpers.commit(c.thing)
            log.info('trashed %s' % c.thing)
            
            if c.authuser.id == c.thing.owner:
                session['facilitatorInitiatives'].remove(code)
            session.save
        else:
            return json.dumps({'statusCode':1, 'errorMsg': 'no user'})
            
    def restoreThingHandler( self, code ):
        # to 'restore' a thing we remove the string 'Unpublished'
        if 'user' in session and (c.authuser.id == c.thing.owner or userLib.isAdmin(c.authuser.id)):
            # the user is restoring something they deleted
            if c.thing['unpublished_by'] == 'owner' and c.authuser.id == c.thing.owner:
                c.thing.objType = c.thing.objType.replace('Unpublished', '')
            # the admin is restoring something
            elif userLib.isAdmin(c.authuser.id):
                c.thing.objType = c.thing.objType.replace('Unpublished', '')
            # user is trying to restore something admin deleted - this is not allowed    
            else: 
                return json.dumps({'statusCode':1, 'errorMsg': 'insufficient privs'})
            
            # restore the children
            children = generic.getChildrenOfParent(c.thing)
            for child in children:
                child.objType = child.objType.replace('Unpublished', '')
                dbHelpers.commit(child)
            
            # save the restored thing
            dbHelpers.commit(c.thing)
            log.info('restored %s' % c.thing)
            
            if c.authuser.id == c.thing.owner:
                session['facilitatorInitiatives'].append(code)
                session.save
                
        else:
            return json.dumps({'statusCode':1, 'errorMsg': 'no user'})