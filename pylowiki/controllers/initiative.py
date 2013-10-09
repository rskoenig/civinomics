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
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic

log = logging.getLogger(__name__)

class InitiativeController(BaseController):
    
    @h.login_required
    def __before__(self, action, id1 = None, id2 = None):
        c.user = None
        c.initiative = None
        if action == 'initiativeNewHandler' and id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            if not c.user:
                abort(404)
        elif (action == 'initiativeEditHandler' or action == 'initiativeShowHandler') and id1 is not None and id2 is not None:
                c.initiative = initiativeLib.getInitiative(id1)
                if c.initiative:
                    c.user = userLib.getUserByCode(initiative['userCode'])
                else:
                  abort(404)  
        else:
            abort(404)
            
        userLib.setUserPrivs()


    def initiativeNewHandler(self):

        return render('/derived/6_initiative_new.bootstrap')
 
