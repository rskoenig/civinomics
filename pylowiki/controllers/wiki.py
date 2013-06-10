# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.page         as pageLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.facilitator  as facilitatorLib

import pylowiki.lib.helpers as h
import re

log = logging.getLogger(__name__)

class WikiController(BaseController):

    @h.login_required 
    def __before__(self, action, workshopCode = None):
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        if not userLib.isAdmin(c.authuser.id) and not facilitatorLib.isFacilitator(c.authuser, c.w):
            abort(404)
   
    def updateBackgroundHandler(self, workshopCode, workshopURL):
        session['confTab'] = "background"
        
        try:
            request.params['submit'] #Try submit, if false redirect back.
            data = request.params['data']
            page = pageLib.getInformation(c.w)
            pageLib.editInformation(page, data, c.authuser)
            aTitle = 'Information Updated.'
            if not workshopLib.isPublished(c.w):
                aTitle += ' Preview your changes by clicking on the workshop name above.'
            alert = {'type':'success'}
            alert['title'] = aTitle
        except Exception as e:
            log.info(e)
            alert = {'type':'error'}
            alert['title'] = 'Error updating information.'
            
        session['alert'] = alert
        if c.w['startTime'] == '0000-00-00':
            session['confTab'] = "participants"
        session.save()
        return redirect(session['return_to'])
