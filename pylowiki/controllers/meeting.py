# -*- coding: utf-8 -*-
import logging
import datetime

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.meeting      as meetingLib
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
import pylowiki.lib.fuzzyTime		as fuzzyTime
import misaka as m

import simplejson as json

log = logging.getLogger(__name__)

class MeetingController(BaseController):
    
    def __before__(self, action, id1 = None, id2 = None, id3 = None):
        c.user = None
        c.meeting = None
        c.items = None
        adminList = ['meetingNew', 'meetingNewHandler', 'meetingEdit', 'meetingEditHandler', 'itemEditHandler']
        if (action == 'meetingNew' or action == 'meetingNewHandler') and id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            c.author = c.user
            c.meetingEdit = False
            if not c.user:
                abort(404)
        elif id1 is not None and id2 is not None:
            c.meeting = meetingLib.getMeeting(id1)
            if not c.meeting:
                c.meeting = revisionLib.getRevisionByCode(id1)
                if not c.meeting:
                    abort(404)
        else:
            abort(404)

        if 'user' in session and c.authuser:
            userLib.setUserPrivs()
        else:
            if action in adminList:
                abort(404)
        if c.meeting:
            c.author = userLib.getUserByCode(c.meeting['userCode'])
    
    def meetingNew(self):
        
        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        c.country = "0"
        c.state = "0"
        c.county = "0"
        c.city = "0"
        c.postal = "0"
        
        c.editMeeting = False
       
        return render('/derived/6_meeting_edit.bootstrap')
        
    def meetingNewHandler(self):
        if 'meetingTitle' in request.params:
            title = request.params['meetingTitle']
        else:
            title = 'New Meeting'
            
        if 'meetingText' in request.params:
            text = request.params['meetingText']
        else:
            text = ''
            
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
            scope = "0|0|" + utils.urlify(geoTagCountry) + "|0|" + utils.urlify(geoTagState) + "|0|" + utils.urlify(geoTagCounty) + "|0|" + utils.urlify(geoTagCity) + "|" + utils.urlify(geoTagPostal)
        else:
            scope = '0|0|united-states|0|0|0|0|0|0|0'
            
        if 'tag' in request.params:
            tag = request.params['tag']
        else:
            tag = ''
            
        if 'meetingGroup' in request.params:
            group = request.params['meetingGroup']
        else:
            group = ''
            
        if 'meetingLocation' in request.params:
            location = request.params['meetingLocation']
        else:
            location = ''
            
        if 'meetingDate' in request.params:
            meetingDate = request.params['meetingDate']
        else:
            meetingDate = ''
            
        if 'meetingTime' in request.params:
            meetingTime = request.params['meetingTime']
        else:
            meetingTime = ''

        if 'agendaPostDate' in request.params:
            agendaPostDate = request.params['agendaPostDate']
        else:
            agendaPostDate = '' 
            
        #create the meeting
        c.meeting = meetingLib.Meeting(c.authuser, title, text, scope, group, location, meetingDate, meetingTime, tag, agendaPostDate)
        if 'meeting_counter' in c.authuser:
            meeting_counter = int(c.authuser['meeting_counter'])
        else:
            meeting_counter = 0
        meeting_counter += 1
        c.authuser['meeting_counter'] = str(meeting_counter)

        c.level = scope

        # now that the edits have been commited, update the scopeProps for the template to use:
        scopeProps = utils.getPublicScope(c.meeting)
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
        if c.meeting['scope'] != '':
            geoTags = c.meeting['scope'].split('|')
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

        c.editMeeting = True
       
        return render('/derived/6_meeting.bootstrap')
    

    def meetingEdit(self):
        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        if c.meeting['scope'] != '':
            geoTags = c.meeting['scope'].split('|')
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
            if c.complete and c.meeting['public'] == '0':
                c.meeting['public'] = '1'
                startTime = datetime.datetime.now(None)
                c.meeting['publishDate'] = startTime
                c.meeting['unpublishDate'] = u'0000-00-00'
                dbHelpers.commit(c.meeting)
                c.saveMessage = "Your meeting is now live! It is publicly viewable."
        elif 'public' in request.params and request.params['public'] == 'unpublish':
            if c.meeting['public'] == '1':
                c.meeting['public'] = '0'
                endTime = datetime.datetime.now(None)
                c.meeting['unpublishDate'] = endTime
                dbHelpers.commit(c.meeting)
                c.saveMessage = "Your meeting has been unpublished. It is no longer publicy viewable."

        c.editMeeting = True

        return render('/derived/6_meeting_edit.bootstrap')
        
    def meetingEditHandler(self):
        if 'meetingTitle' in request.params:
            c.meeting['title'] = request.params['meetingTitle']
            c.meeting['url'] = utils.urlify(c.meeting['title'])
        if 'meetingText' in request.params:
            c.meeting['text'] = request.params['meetingText']
        if 'meetingDate' in request.params:
            c.meeting['meetingDate'] = request.params['meetingDate']
        if 'meetingTime' in request.params:
            c.meeting['meetingTime'] = request.params['meetingTime']
        if 'agendaPostDate' in request.params:
            c.meeting['agendaPostDate'] = request.params['agendaPostDate']
        if 'tag' in request.params:
            c.meeting['tag'] = request.params['tag']
        if 'meetingGroup' in request.params:
            c.meeting['group'] = request.params['meetingGroup']
        if 'meetingLocation' in request.params:
            c.meeting['location'] = request.params['meetingLocation']


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
            if c.meeting['scope'] != geoTagString:
                c.meeting['scope'] = geoTagString

                wchanges = 1

        dbHelpers.commit(c.meeting)
        revisionLib.Revision(c.authuser, c.meeting)

        # now that the agenda edits have been commited, update the scopeProps for the template to use:
        scopeProps = utils.getPublicScope(c.meeting)
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
        if c.meeting['scope'] != '':
            geoTags = c.meeting['scope'].split('|')
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

        c.editMeeting = True
        returnURL = "/meeting/%s/%s/show"%(c.meeting['urlCode'], c.meeting['url'])
        
        return redirect(returnURL)
        
    def meetingShow(self):

        c.revisions = revisionLib.getRevisionsForThing(c.meeting)
        c.author = userLib.getUserByCode(c.meeting['userCode'])
        c.agendaItems = meetingLib.getAgendaItems(c.meeting['urlCode'])
        
        if c.meeting.objType != 'revision' and 'views' in c.meeting:
            views = int(c.meeting['views']) + 1
            c.meeting['views'] = str(views)
            dbHelpers.commit(c.meeting)

        return render('/derived/6_meeting.bootstrap')
        
    def meetingAgendaItemAddHandler(self):
        if 'agendaItemTitle' in request.params:
            title = request.params['agendaItemTitle']
        else:
            title = ''
        
        if 'agendaItemText' in request.params:
            text = request.params['agendaItemText']
        else:
            text = ''

        if 'agendaItemVote' in request.params:
            canVote = request.params['agendaItemVote']
        else:
            canVote = ''

        if 'agendaItemComment' in request.params:
            canComment = request.params['agendaItemComment']
        else:
            canComment = ''
            
        meetingLib.Agendaitem(c.authuser, c.meeting, title, text, canVote, canComment)
        
        returnURL = '/meeting/%s/%s/show'%(c.meeting['urlCode'], c.meeting['url'])
            
        return redirect(returnURL)
        
    def getMeetingAgendaItems(self, id1, id2):
        c.agendaItems = meetingLib.getAgendaItems(id1)
        if not c.agendaItems:
            c.agendaItems = []
            
        result = []
        myRatings = {}
        if 'ratings' in session:
		    myRatings = session['ratings']
        for item in c.agendaItems:
            entry = {}
            entry['objType'] = 'agendaitem'
            entry['url']= item['url']
            entry['urlCode']=item['urlCode']
            entry['title'] = item['title']
            entry['text'] = item['text']
            entry['html'] = m.html(entry['text'], render_flags=m.HTML_SKIP_HTML)
            entry['date'] = item.date.strftime('%Y-%m-%d at %H:%M:%S')
            entry['fuzzyTime'] = fuzzyTime.timeSince(item.date)

			# user rating
            if entry['urlCode'] in myRatings:
                entry['rated'] = myRatings[entry['urlCode']]
                entry['vote'] = 'voted'
            else:
                entry['rated'] = 0
                entry['vote'] = 'nvote'

            entry['vote'] = 'nvote'
            entry['voteCount'] = int(item['ups']) + int(item['downs'])
            entry['ups'] = int(item['ups'])
            entry['downs'] = int(item['downs'])
            entry['netVotes'] = int(item['ups']) - int(item['downs'])

            # comments
            discussion = discussionLib.getDiscussionForThing(item)
            entry['discussion'] = discussion['urlCode']

            entry['numComments'] = '0'
            if 'numComments' in item:
                entry['numComments'] = discussion['numComments']
			
            result.append(entry)
            
        if len(result) == 0:
            return json.dumps({'statusCode':1})
            
        return json.dumps({'statusCode':0, 'result': result})
        

        
