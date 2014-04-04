#-*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.user         as userLib


class TrashController(BaseController):
    
    def __before__(self, action, code = None, url = None):
        if code != None:
            c.thing = generic.getThing(code)
            if not c.thing:
                return json.dumps({'statusCode':0, 'result': 'no thing with that code'})
        else:
            return json.dumps({'statusCode':0, 'result': 'no code entered'})
    
    
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
            
            session['facilitatorInitiatives'].remove(code)
            session.save
        else:
            abort(404)