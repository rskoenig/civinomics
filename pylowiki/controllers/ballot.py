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
        adminList = ['electionNew', 'electionNewHandler', 'electionEdit', 'electionEditHandler', 'ballotNew', 'ballotNewHandler', 'ballotEdit', 'ballotEditHandler', 'ballotmeasureEditHandler']
        if (action == 'electionNew' or action == 'electionNewHandler') and id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            c.author = c.user
            c.edit = False
            if not c.user:
                abort(404)
        elif id1 is not None and id2 is not None:
            if action == 'electionEditHandler' or action == 'ballotNewHandler':
                c.election = ballotLib.getElection(id1)
                if not c.election:
                    abort(404)
            elif action == 'electionShow':
                c.election = ballotLib.getElection(id1)
                if not c.election:
                    c.election = revisionLib.getRevisionByCode(id1)
                    if not c.election:
                        abort(404)
            elif action == 'ballotmeasureEditHandler':
                c.ballotmeasure = ballotLib.getBallotMeasure(id1)
                if c.ballotmeasure:
                    c.ballot = ballotLib.getBallot(c.ballotmeasure['ballotCode'])
                else:
                    abort(404)
            else:
                c.ballot = ballotLib.getBallot(id1)
                if not c.ballot:
                    c.ballot = revisionLib.getRevisionByCode(id1)
                    if not c.ballot:
                        abort(404)
            if id3 is not None:
                c.ballotmeasure = ballotLib.getBallotMeasure(id3)
                if not c.ballotmeasure:
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
            
        log.info("done with before, action is %s"%action)
            
    def electionNew(self):
        
        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        c.country = "0"
        c.state = "0"
        c.county = "0"
        c.city = "0"
        c.postal = "0"
        
        c.edit = False
       
        return render('/derived/6_election_edit.bootstrap')
        
    def electionNewHandler(self):
        log.info('inside electionNewHandler')
        if 'electionTitle' in request.params:
            title = request.params['electionTitle']
        else:
            title = 'New Election'
            
        if 'electionText' in request.params:
            text = request.params['electionText']
        else:
            text = 'New election description'
            
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
            
        if 'ballotSlate' in request.params:
            ballotSlate = request.params['ballotSlate']
        else:
            ballotSlate = 'measures'
            
        if 'candidateMax' in request.params:
            candidateMax = request.params['candidateMax']
        else:
            candidateMax = '0'

        if 'public' in request.params:
            public = request.params['public']
        else:
            public = ''
            
        #create the election
        c.election = ballotLib.Election(c.authuser, title, text, scope, electionDate, electionOfficialURL, public)
        if 'election_counter' in c.authuser:
            election_counter = int(c.authuser['election_counter'])
        else:
            election_counter = 0
        election_counter += 1
        c.authuser['election_counter'] = str(election_counter)
        dbHelpers.commit(c.authuser)

        c.level = scope

        # now that the edits have been commited, update the scopeProps for the template to use:
        scopeProps = utils.getPublicScope(c.election)
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
        if c.election['scope'] != '':
            geoTags = c.election['scope'].split('|')
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

        c.edit = True
       
        return render('/derived/6_election.bootstrap')
        
    def electionShow(self):

        c.revisions = revisionLib.getRevisionsForThing(c.election)
        c.author = userLib.getUserByCode(c.election['userCode'])
        
        if c.election.objType != 'revision' and 'views' in c.election:
            views = int(c.election['views']) + 1
            c.election['views'] = str(views)
            dbHelpers.commit(c.election)

        return render('/derived/6_election.bootstrap')
    
    def ballotNewHandler(self):
        if 'ballotTitle' in request.params:
            title = request.params['ballotTitle']
        else:
            title = 'New Ballot'
            
        if 'ballotText' in request.params:
            text = request.params['ballotText']
        else:
            text = 'New ballot description'
            
        if 'ballotSlate' in request.params:
            ballotSlate = request.params['ballotSlate']
        else:
            ballotSlate = 'measures'
            
        if 'candidateMax' in request.params:
            candidateMax = request.params['candidateMax']
        else:
            candidateMax = '0'

        #create the ballot
        c.ballot = ballotLib.Ballot(c.authuser, c.election, title, text, scope, electionDate, electionOfficialURL, ballotSlate, candidateMax, public)
        if 'ballot_counter' in c.authuser:
            ballot_counter = int(c.authuser['ballot_counter'])
        else:
            ballot_counter = 0
        ballot_counter += 1
        c.authuser['ballot_counter'] = str(ballot_counter)
        dbHelpers.commit(c.authuser)

        c.edit = True
       
        return render('/derived/6_election.bootstrap')
    

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
        if 'ballotSlate' in request.params:
            c.ballot['ballotSlate'] = request.params['ballotSlate']
        if 'candidateMax' in request.params:
            c.ballot['candidateMax'] = request.params['candidateMax']
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
        
    def ballotMeasureAddHandler(self):
        if 'ballotMeasureTitle' in request.params:
            title = request.params['ballotMeasureTitle']
        else:
            title = 'New ballot measure (single yes/no vote)'
            
        if 'ballotMeasureNumber' in request.params:
            number = request.params['ballotMeasureNumber']
        else:
            number = '1'
        
        if 'ballotMeasureText' in request.params:
            text = request.params['ballotMeasureText']
        else:
            text = 'New ballot measure description'

        
        if 'ballotMeasureOfficialURL' in request.params:
            link = request.params['ballotMeasureOfficialURL']
        else:
            link = 'New ballot measure description'

            
        ballotLib.Ballotmeasure(c.authuser, c.ballot, title, number, text, link)
        
        returnURL = '/ballot/%s/%s/show'%(c.ballot['urlCode'], c.ballot['url'])
            
        return redirect(returnURL)
        
    def ballotmeasureEditHandler(self):
        # make a revision first of the previous version
        revisionLib.Revision(c.authuser, c.ballotmeasure)
        
        if 'ballotMeasureTitle' in request.params:
            title = request.params['ballotMeasureTitle']
            if title and title != '':
                c.ballotmeasure['title'] = title
                
        if 'ballotMeasureNumber' in request.params:
            number = request.params['ballotMeasureNumber']
            if number and number != '':
                c.ballotmeasure.sort = number
        
        if 'ballotMeasureText' in request.params:
            text = request.params['ballotMeasureText']
            if text and text != '':
                c.ballotmeasure['text'] = text

        if 'ballotMeasureOfficialURL' in request.params:
            c.ballotmeasure['ballotMeasureOfficialURL'] = request.params['ballotMeasureOfficialURL']
        else:
            c.ballotmeasure['ballotMeasureOfficialURL'] = ''
            
        dbHelpers.commit(c.ballotmeasure)
        
        returnURL = '/ballot/%s/%s/show'%(c.ballot['urlCode'], c.ballot['url'])
            
        return redirect(returnURL)
        
    def getBallotMeasures(self, id1, id2):
        c.ballotMeasures = ballotLib.getBallotMeasures(id1)
        if not c.ballotMeasures:
            c.ballotMeasures = []
            
        result = []
        myRatings = {}
        if 'ratings' in session:
		    myRatings = session['ratings']
        for item in c.ballotMeasures:
            entry = {}
            if 'user' in session and (c.authuser.id == item.owner or userLib.isAdmin(c.authuser.id)):
                entry['canEdit'] = 'yes'
            else:
                entry['canEdit'] = 'no'
            entry['objType'] = 'ballotmeasure'
            entry['url']= item['url']
            entry['urlCode']=item['urlCode']
            entry['title'] = item['title']
            entry['text'] = item['text']
            entry['number'] = item.sort
            entry['ballotMeasureOfficialURL'] = item['ballotMeasureOfficialURL']
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
                    officialURL = rev['ballotMeasureOfficialURL']
                    html = m.html(rev['text'], render_flags=m.HTML_SKIP_HTML)
                    revision['date'] = date
                    revision['urlCode'] = code
                    revision['title'] = title
                    revision['text'] = text
                    revision['html'] = html
                    revision['ballotMeasureOfficialURL'] = officialURL
                    entry['revisionList'].append(revision)
                    
            result.append(entry)
            
        if len(result) == 0:
            return json.dumps({'statusCode':1})
            
        return json.dumps({'statusCode':0, 'result': result})
        

        
