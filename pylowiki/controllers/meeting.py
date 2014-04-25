# -*- coding: utf-8 -*-
import logging
import datetime

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.agenda       as agendaLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.revision     as revisionLib

from pylowiki.lib.facebook          import FacebookShareObject
import pylowiki.lib.helpers         as h
import pylowiki.lib.utils           as utils

import simplejson as json

log = logging.getLogger(__name__)

class AgendaController(BaseController):
    
    def __before__(self, action, id1 = None, id2 = None, id3 = None):
        c.user = None
        c.agenda = None
        c.items = None
        adminList = ['agendaNew', 'agendaNewHandler', 'agendaEdit', 'agendaEditHandler', 'itemEditHandler']
        if id1 is not None and id2 is not None:
            c.agenda = agendaLib.getAgenda(id1)
        else:
            abort(404)
            
        if action in adminList:
            if 'user' in session and c.authuser:
                userLib.setUserPrivs()
            else:
                abort(404)
    

    def agendaNewHandler(self):
        if 'agendaTitle' in request.params:
            title = request.params['agendaTitle']
        else:
            title = 'New Meeting Agenda'
            
        if 'agendaText' in request.params:
            text = request.params['agendaText']
        else:
            text = ''

        # the scope if initiative is created from a geoSearch page
        if 'agendaRegionScope' in request.params:
            scope = request.params['agendaRegionScope']
            
        else:
            scope = '0|0|united-states|0|0|0|0|0|0|0'
            
        if 'agendaTag' in request.params:
            tag = request.params['agendaTag']
        else:
            tag = ''
            
        if 'agendaGroup' in request.params:
            group = request.params['agendaGroup']
        else:
            group = ''
            
        if 'agendaMeetingDate' in request.params:
            meetingDate = request.params['agendaMeetingDate']
        else:
            meetingDate = ''

        if 'agendaPostDate' in request.params:
            agendaPostDate = request.params['agendaPostDate']
        else:
            agendaPostDate = '' 
            
        #create the agenda
        c.agenda = agendaLib.Agenda(c.user, title, text, scope, group, meetingDate, agendaPostDate, tag)

        c.level = scope

        # now that the initiative edits have been commited, update the scopeProps for the template to use:
        scopeProps = utils.getPublicScope(c.initiative)
        scopeName = scopeProps['name'].title()
        scopeLevel = scopeProps['level'].title()
        if scopeLevel == 'Earth':
            c.scopeTitle = scopeName
        else:
            c.scopeTitle = scopeLevel + ' of ' + scopeName
        c.scopeFlag = scopeProps['flag']
        c.scopeHref = scopeProps['href']

        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        if c.initiative['scope'] != '':
            geoTags = c.initiative['scope'].split('|')
            c.country = utils.geoDeurlify(geoTags[2])
            c.state = utils.geoDeurlify(geoTags[4])
            c.county = utils.geoDeurlify(geoTags[6])
            c.city = utils.geoDeurlify(geoTags[8])
            c.postal = utils.geoDeurlify(geoTags[9])
        else:
            c.country = "0"
            c.state = "0"
            c.county = "0"
            c.city = "0"
            c.postal = "0"

        c.editAgenda = True
       
        return render('/derived/6_agenda.bootstrap')
    

    def agendaEdit(self):
        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        if c.initiative['scope'] != '':
            geoTags = c.agenda['scope'].split('|')
            c.country = utils.geoDeurlify(geoTags[2])
            c.state = utils.geoDeurlify(geoTags[4])
            c.county = utils.geoDeurlify(geoTags[6])
            c.city = utils.geoDeurlify(geoTags[8])
            c.postal = utils.geoDeurlify(geoTags[9])
        else:
            c.country = "0"
            c.state = "0"
            c.county = "0"
            c.city = "0"
            c.postal = "0"

        if 'public' in request.params:
            log.info("got %s"%request.params['public'])
        if 'public' in request.params and request.params['public'] == 'publish':
            if c.complete and c.agenda['public'] == '0':
                c.agenda['public'] = '1'
                startTime = datetime.datetime.now(None)
                c.agenda['publishDate'] = startTime
                c.agenda['unpublishDate'] = u'0000-00-00'
                dbHelpers.commit(c.agenda)
                c.saveMessage = "Your meeting agenda is now live! It is publicly viewable."
        elif 'public' in request.params and request.params['public'] == 'unpublish':
            if c.agenda['public'] == '1':
                c.agenda['public'] = '0'
                endTime = datetime.datetime.now(None)
                c.agenda['unpublishDate'] = endTime
                dbHelpers.commit(c.agenda)
                c.saveMessage = "Your meeting agenda has been unpublished. It is no longer publicy viewable."

        c.editAgenda = True

        return render('/derived/6_agenda_edit.bootstrap')
        
    def agendaEditHandler(self):
        if 'title' in request.params:
            c.agenda['title'] = request.params['title']
            c.agenda['url'] = utils.urlify(c.agenda['title'])
        if 'text' in request.params:
            c.initiative['text'] = request.params['text']
        if 'tag' in request.params:
            c.initiative['tags'] = request.params['tag']


        # update the scope based on info in the scope dropdown selector, if they're in the submitted form
        if 'geoTagCountry' in request.params:
            if 'geoTagCountry' in request.params and request.params['geoTagCountry'] != '0':
                geoTagCountry = request.params['geoTagCountry']
            else:
                geoTagCountry = "0"
                
            if 'geoTagState' in request.params and request.params['geoTagState'] != '0':
                geoTagState = request.params['geoTagState']
            else:
                geoTagState = "0"
                
            if 'geoTagCounty' in request.params and request.params['geoTagCounty'] != '0':
                geoTagCounty = request.params['geoTagCounty']
            else:
                geoTagCounty = "0"
                
            if 'geoTagCity' in request.params and request.params['geoTagCity'] != '0':
                geoTagCity = request.params['geoTagCity']
            else:
                geoTagCity = "0"
                
            if 'geoTagPostal' in request.params and request.params['geoTagPostal'] != '0':
                geoTagPostal = request.params['geoTagPostal']
            else:
                geoTagPostal = "0"

            # assemble the scope string 
            # ||country||state||county||city|zip
            geoTagString = "0|0|" + utils.urlify(geoTagCountry) + "|0|" + utils.urlify(geoTagState) + "|0|" + utils.urlify(geoTagCounty) + "|0|" + utils.urlify(geoTagCity) + "|" + utils.urlify(geoTagPostal)
            if c.agenda['scope'] != geoTagString:
                c.agenda['scope'] = geoTagString

                wchanges = 1

        dbHelpers.commit(c.agenda)
        revisionLib.Revision(c.authuser, c.agenda)

        # now that the agenda edits have been commited, update the scopeProps for the template to use:
        scopeProps = utils.getPublicScope(c.agenda)
        scopeName = scopeProps['name'].title()
        scopeLevel = scopeProps['level'].title()
        if scopeLevel == 'Earth':
            c.scopeTitle = scopeName
        else:
            c.scopeTitle = scopeLevel + ' of ' + scopeName
        c.scopeFlag = scopeProps['flag']
        c.scopeHref = scopeProps['href']

        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        if c.agenda['scope'] != '':
            geoTags = c.initiative['scope'].split('|')
            c.country = utils.geoDeurlify(geoTags[2])
            c.state = utils.geoDeurlify(geoTags[4])
            c.county = utils.geoDeurlify(geoTags[6])
            c.city = utils.geoDeurlify(geoTags[8])
            c.postal = utils.geoDeurlify(geoTags[9])
        else:
            c.country = "0"
            c.state = "0"
            c.county = "0"
            c.city = "0"
            c.postal = "0"

        if c.error:
            c.saveMessageClass = 'alert-error'
            c.saveMessage = errorMessage
        else:
            c.saveMessage = "Changes saved."

        c.editAgenda = True
        
        return render('/derived/6_agenda_edit.bootstrap')
        
    def agendaShowHandler(self):

        c.revisions = revisionLib.getRevisionsForThing(c.agenda)
        
        if c.agenda.objType != 'revision' and 'views' in c.agenda:
            views = int(c.agenda['views']) + 1
            c.agenda['views'] = str(views)
            dbHelpers.commit(c.agenda)

        return render('/derived/6_agenda_home.bootstrap')

        
