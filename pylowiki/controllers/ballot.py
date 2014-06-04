# -*- coding: utf-8 -*-
import logging
import datetime

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.ballot       as ballotLib
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

class BallotController(BaseController):
    
    def __before__(self, action, id1 = None, id2 = None, id3 = None):
        c.user = None
        c.ballot = None
        c.items = None
        adminList = ['ballotNew', 'ballotNewHandler', 'ballotEdit', 'ballotEditHandler', 'ballotitemEditHandler']
        if (action == 'ballotNew' or action == 'ballotNewHandler') and id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            c.author = c.user
            c.ballotEdit = False
            if not c.user:
                abort(404)
        elif id1 is not None and id2 is not None:
            if action == 'ballotitemEditHandler':
                c.ballotitem = ballotLib.getBallotItem(id1)
                if c.ballotitem:
                    c.ballot = ballotLib.getBallot(c.ballotitem['ballotCode'])
                else:
                    abort(404)
            else:
                c.ballot = ballotLib.getBallot(id1)
                
            if not c.ballot:
                c.ballot = revisionLib.getRevisionByCode(id1)
                if not c.ballot:
                    abort(404)
            if id3 is not None:
                c.ballotitem = ballotLib.getBallotItem(id3)
                if not c.ballotitem:
                    abort(404)
        else:
            abort(404)

        if 'user' in session and c.authuser:
            userLib.setUserPrivs()
        else:
            if action in adminList:
                abort(404)
        if c.ballot:
            c.author = userLib.getUserByCode(c.ballot['userCode'])
    
    def ballotNew(self):
        
        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        c.country = "0"
        c.state = "0"
        c.county = "0"
        c.city = "0"
        c.postal = "0"
        
        c.editBallot = False
       
        return render('/derived/6_ballot_edit.bootstrap')
        
    def ballotNewHandler(self):
        if 'ballotTitle' in request.params:
            title = request.params['ballotTitle']
        else:
            title = 'New Ballot'
            
        if 'ballotText' in request.params:
            text = request.params['ballotText']
        else:
            text = 'New ballot description'
            
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
            
        if 'electionDate' in request.params:
            electionDate = request.params['electionDate']
        else:
            electionDate = ''
            
        if 'electionOfficialURL' in request.params:
            electionOfficialURL = request.params['electionOfficialURL']
        else:
            electionOfficialURL = ''

        if 'public' in request.params:
            public = request.params['public']
        else:
            public = ''
            
        #create the ballot
        c.ballot = ballotLib.Ballot(c.authuser, title, text, scope, electionDate, electionOfficialURL, public)
        if 'ballot_counter' in c.authuser:
            ballot_counter = int(c.authuser['ballot_counter'])
        else:
            ballot_counter = 0
        ballot_counter += 1
        c.authuser['ballot_counter'] = str(ballot_counter)
        dbHelpers.commit(c.authuser)

        c.level = scope

        # now that the edits have been commited, update the scopeProps for the template to use:
        scopeProps = utils.getPublicScope(c.ballot)
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
        if c.ballot['scope'] != '':
            geoTags = c.ballot['scope'].split('|')
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

        c.editBallot = True
       
        return render('/derived/6_ballot.bootstrap')
    

    def ballotEdit(self):
        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        if c.ballot['scope'] != '':
            geoTags = c.ballot['scope'].split('|')
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

        if 'public' in request.params and request.params['public'] == 'publish':
            if c.complete and c.ballot['public'] == '0':
                c.ballot['public'] = '1'
                startTime = datetime.datetime.now(None)
                c.ballot['publishDate'] = startTime
                c.ballot['unpublishDate'] = u'0000-00-00'
                dbHelpers.commit(c.ballot)
                c.saveMessage = "Your ballot is now live! It is publicly viewable."
        elif 'public' in request.params and request.params['public'] == 'unpublish':
            if c.ballot['public'] == '1':
                c.ballot['public'] = '0'
                endTime = datetime.datetime.now(None)
                c.ballot['unpublishDate'] = endTime
                dbHelpers.commit(c.ballot)
                c.saveMessage = "Your ballot has been unpublished. It is no longer publicy viewable."

        c.editBallot = True

        return render('/derived/6_ballot_edit.bootstrap')
        
    def ballotEditHandler(self):
        if 'ballotTitle' in request.params:
            title = request.params['ballotTitle']
            if title and title != '':
                c.ballot['title'] = request.params['ballotTitle']
                c.ballot['url'] = utils.urlify(c.ballot['title'])
        if 'ballotText' in request.params:
            c.ballot['text'] = request.params['ballotText']
        if 'electionDate' in request.params:
            c.ballot['electionDate'] = request.params['electionDate']
            c.ballot.sort = c.ballot['electionDate']
        if 'electionOfficialURL' in request.params:
            c.ballot['electionOfficialURL'] = request.params['electionOfficialURL']
        if 'public' in request.params:
            c.ballot['public'] = request.params['public']
        else:
            c.ballot['public'] = ''


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
            if c.ballot['scope'] != geoTagString:
                c.ballot['scope'] = geoTagString

                wchanges = 1

        dbHelpers.commit(c.ballot)
        revisionLib.Revision(c.authuser, c.ballot)

        # now that the ballot edits have been commited, update the scopeProps for the template to use:
        scopeProps = utils.getPublicScope(c.ballot)
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
        if c.ballot['scope'] != '':
            geoTags = c.ballot['scope'].split('|')
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

        c.editBallot = True
        returnURL = "/ballot/%s/%s/show"%(c.ballot['urlCode'], c.ballot['url'])
        
        return redirect(returnURL)
        
    def ballotShow(self):

        c.revisions = revisionLib.getRevisionsForThing(c.ballot)
        c.author = userLib.getUserByCode(c.ballot['userCode'])
        
        if c.ballot.objType != 'revision' and 'views' in c.ballot:
            views = int(c.ballot['views']) + 1
            c.ballot['views'] = str(views)
            dbHelpers.commit(c.ballot)

        return render('/derived/6_ballot.bootstrap')
        
    def ballotItemAddHandler(self):
        if 'ballotItemTitle' in request.params:
            title = request.params['ballotItemTitle']
        else:
            title = 'New ballot item'
            
        if 'ballotItemNumber' in request.params:
            number = request.params['ballotItemNumber']
        else:
            number = '1'
        
        if 'ballotItemText' in request.params:
            text = request.params['ballotItemText']
        else:
            text = 'New ballot item description'

        
        if 'ballotItemOfficialURL' in request.params:
            link = request.params['ballotItemOfficialURL']
        else:
            link = 'New ballot item description'

            
        ballotLib.Ballotitem(c.authuser, c.ballot, title, number, text, link)
        
        returnURL = '/ballot/%s/%s/show'%(c.ballot['urlCode'], c.ballot['url'])
            
        return redirect(returnURL)
        
    def ballotitemEditHandler(self):
        # make a revision first of the previous version
        revisionLib.Revision(c.authuser, c.ballotitem)
        
        if 'ballotItemTitle' in request.params:
            title = request.params['ballotItemTitle']
            if title and title != '':
                c.ballotitem['title'] = title
                
        if 'ballotItemNumber' in request.params:
            number = request.params['ballotItemNumber']
            if number and number != '':
                c.ballotitem.sort = number
        
        if 'ballotItemText' in request.params:
            text = request.params['ballotItemText']
            if text and text != '':
                c.ballotitem['text'] = text

        if 'ballotItemOfficialURL' in request.params:
            c.ballotitem['ballotItemOfficialURL'] = request.params['ballotItemOfficialURL']
        else:
            c.ballotitem['ballotItemOfficialURL'] = ''
            
        dbHelpers.commit(c.ballotitem)
        
        returnURL = '/ballot/%s/%s/show'%(c.ballot['urlCode'], c.ballot['url'])
            
        return redirect(returnURL)
        
    def getBallotItems(self, id1, id2):
        c.ballotItems = ballotLib.getBallotItems(id1)
        if not c.ballotItems:
            c.ballotItems = []
            
        result = []
        myRatings = {}
        if 'ratings' in session:
		    myRatings = session['ratings']
        for item in c.ballotItems:
            entry = {}
            if 'user' in session and (c.authuser.id == item.owner or userLib.isAdmin(c.authuser.id)):
                entry['canEdit'] = 'yes'
            else:
                entry['canEdit'] = 'no'
            entry['objType'] = 'ballotitem'
            entry['url']= item['url']
            entry['urlCode']=item['urlCode']
            entry['title'] = item['title']
            entry['text'] = item['text']
            entry['ballotItemOfficialURL'] = item['ballotItemOfficialURL']
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
                
            # get revisions
            revisions = revisionLib.getRevisionsForThing(item)
            if revisions:
                entry['revisions'] = 'yes'
            else:
                entry['revisions'] = 'no'
            entry['revisionList'] = []
            if revisions:
                for rev in revisions:
                    revision = {}
                    code = rev['urlCode'] 
                    date = str(rev.date)
                    title = rev['title']
                    text = rev['text']
                    officialURL = rev['ballotItemOfficialURL']
                    html = m.html(rev['text'], render_flags=m.HTML_SKIP_HTML)
                    revision['date'] = date
                    revision['urlCode'] = code
                    revision['title'] = title
                    revision['text'] = text
                    revision['html'] = html
                    revision['ballotItemOfficialURL'] = officialURL
                    entry['revisionList'].append(revision)
                    
            result.append(entry)
            
        if len(result) == 0:
            return json.dumps({'statusCode':1})
            
        return json.dumps({'statusCode':0, 'result': result})
        

        
