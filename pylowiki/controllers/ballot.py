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
        c.election = None
        c.items = None
        adminList = ['electionNew', 'electionNewHandler', 'electionEdit', 'electionEditHandler', 'ballotNew', 'ballotNewHandler', 'ballotEdit', 'ballotEditHandler', 'ballotmeasureEditHandler']
        if (action == 'electionNew' or action == 'electionNewHandler') and id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            c.author = c.user
            c.edit = False
            if not c.user:
                abort(404)
        elif id1 is not None and id2 is not None:
            if action == 'electionEdit' or action == 'electionEditHandler' or action == 'ballotNewHandler' or action == 'getBallots':
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
            elif action == 'ballotmeasureShow':
                c.ballotmeasure = ballotLib.getBallotMeasure(id1)
                if not c.ballotmeasure:
                    c.ballotmeasure = revisionLib.getRevisionByCode(id1)
                    
                if c.ballotmeasure:
                    c.ballot = ballotLib.getBallot(c.ballotmeasure['ballotCode'])
                else:
                    abort(404)
            elif action == 'ballotcandidateEditHandler':
                #log.info("ballotcandidateEditHandler 1")
                c.ballotcandidate = ballotLib.getBallotCandidate(id1)
                if c.ballotcandidate:
                    #log.info("ballotcandidateEditHandler 2")
                    c.ballot = ballotLib.getBallot(c.ballotcandidate['ballotCode'])
                else:
                    #log.info("ballotcandidateEditHandler abort 1")
                    abort(404)
            elif action == 'ballotcandidateShow':
                c.ballotcandidate = ballotLib.getBallotCandidate(id1)
                if not c.ballotcandidate:
                    c.ballotcandidate = revisionLib.getRevisionByCode(id1)
                    
                if c.ballotcandidate:
                    c.ballot = ballotLib.getBallot(c.ballotcandidate['ballotCode'])
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
            if not c.election:
                c.election = ballotLib.getElection(c.ballot['electionCode'])
            
        #log.info("done with before, action is %s"%action)
            
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
        #log.info('inside electionNewHandler')
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
            

    def electionEdit(self):
        c.states = geoInfoLib.getStateList('United-States')
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

        return render('/derived/6_election_edit.bootstrap')
        
    def electionEditHandler(self):
        
        # save a copy of the election before editing     
        revisionLib.Revision(c.authuser, c.election)
        
        if 'electionTitle' in request.params:
            c.election['title'] = request.params['electionTitle']

        if 'electionText' in request.params:
            c.election['text'] = request.params['electionText']

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
            c.election['scope'] = "0|0|" + utils.urlify(geoTagCountry) + "|0|" + utils.urlify(geoTagState) + "|0|" + utils.urlify(geoTagCounty) + "|0|" + utils.urlify(geoTagCity) + "|" + utils.urlify(geoTagPostal)

            
        if 'electionDate' in request.params:
            c.election['electionDate'] = request.params['electionDate']

        if 'electionOfficialURL' in request.params:
            c.election['electionOfficialURL'] = request.params['electionOfficialURL']

        if 'ballotSlate' in request.params:
            c.election['ballotSlate'] = request.params['ballotSlate']

        if 'candidateMax' in request.params:
            c.election['candidateMax'] = request.params['candidateMax']

        if 'public' in request.params:
            public = request.params['public']
            if public == 'on':
                c.election['election_public'] = '1'
            else:
                c.election['election_public'] = '0'

        dbHelpers.commit(c.election)
                
        returnURL = "/election/%s/%s/show"%(c.election['urlCode'], c.election['url'])
        
        return redirect(returnURL)

        
    
    def ballotNewHandler(self):
        if 'ballotTitle' in request.params:
            title = request.params['ballotTitle']
        else:
            title = 'New Ballot'
            
        if 'ballotNumber' in request.params:
            number = request.params['ballotNumber']
        else:
            number = '1'
            
        if 'ballotText' in request.params:
            text = request.params['ballotText']
        else:
            text = 'New ballot description'
            
        if 'ballotInstructions' in request.params:
            instructions = request.params['ballotInstructions']
        else:
            instructions = 'New ballot instructions'
            
        if 'ballotSlate' in request.params:
            ballotSlate = request.params['ballotSlate']
        else:
            ballotSlate = 'measures'
        
        if ballotSlate == 'measures':    
            if 'slateInfoMeasures' in request.params:
                slateInfo = request.params['slateInfoMeasures']
        else:
            slateInfo = 'Ballot Measures'
            
        if ballotSlate == 'candidates':    
            if 'slateInfoCandidates' in request.params:
                slateInfo = request.params['slateInfoCandidates']
        else:
            slateInfo = '1'

        #create the ballot
        c.ballot = ballotLib.Ballot(c.authuser, c.election, title, number, text, instructions, ballotSlate, slateInfo)
        if 'ballot_counter' in c.authuser:
            ballot_counter = int(c.authuser['ballot_counter'])
        else:
            ballot_counter = 0
        ballot_counter += 1
        c.authuser['ballot_counter'] = str(ballot_counter)
        dbHelpers.commit(c.authuser)

        c.edit = True
        c.author = c.authuser
       
        return render('/derived/6_election.bootstrap')
    

    def ballotEdit(self):
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
        if 'ballotInstructions' in request.params:
            c.ballot['instructions'] = request.params['ballotInstructions']
        if 'ballotSlate' in request.params:
            c.ballot['ballotSlate'] = request.params['ballotSlate']
            if c.ballot['ballotSlate'] == 'measures':
                if 'slateInfo1' in request.params:
                    c.ballot['slateInfo'] = request.params['slateInfo1']
                else:
                    c.ballot['slateInfo'] = 'ballot measure'
            else:
                if 'slateInfo2' in request.params:
                    c.ballot['slateInfo'] = request.params['slateInfo2']
                else:
                    c.ballot['slateInfo'] = 'candidate'
        if 'ballotNumber' in request.params:
            c.ballot.sort = request.params['ballotNumber']

        dbHelpers.commit(c.ballot)
        revisionLib.Revision(c.authuser, c.ballot)

        c.saveMessage = "Changes saved."

        c.edit = True
        returnURL = "/ballot/%s/%s/show"%(c.ballot['urlCode'], c.ballot['url'])
        
        return redirect(returnURL)
        
    def getBallots(self, id1, id2):
        #log.info("inside getBallots")
        c.ballots = ballotLib.getBallotsForElection(c.election['urlCode'])
        if not c.ballots:
            c.ballots = []
            
        result = []

        for item in c.ballots:
            if item.objType == 'ballotUnpublished':
                continue

            entry = {}
            if 'user' in session and (c.authuser.id == item.owner or userLib.isAdmin(c.authuser.id)):
                entry['canEdit'] = 'yes'
            else:
                entry['canEdit'] = 'no'
                
            entry['objType'] = 'ballot'
            entry['url']= item['url']
            entry['urlCode']=item['urlCode']
            entry['title'] = item['title']
            entry['text'] = item['text']
            entry['number'] = item.sort
            entry['views'] = item['views']
            entry['href'] = "/ballot/" + entry['urlCode'] + "/" + entry['url'] + "/show"
            entry['html'] = m.html(entry['text'], render_flags=m.HTML_SKIP_HTML)
            entry['date'] = item.date.strftime('%Y-%m-%d at %H:%M:%S')
            entry['fuzzyTime'] = fuzzyTime.timeSince(item.date)

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
                    html = m.html(rev['text'], render_flags=m.HTML_SKIP_HTML)
                    revision['date'] = date
                    revision['urlCode'] = code
                    revision['title'] = title
                    revision['text'] = text
                    revision['html'] = html
                    entry['revisionList'].append(revision)
                    
            result.append(entry)

        if len(result) == 0:
            return json.dumps({'statusCode':1})
        return json.dumps({'statusCode':0, 'result': result})
       
    def ballotShow(self):
        c.revisions = revisionLib.getRevisionsForThing(c.ballot)
        c.author = userLib.getUserByCode(c.ballot['userCode'])
        
        if c.ballot.objType != 'revision' and 'views' in c.ballot:
            views = int(c.ballot['views']) + 1
            c.ballot['views'] = str(views)
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

            
        ballotLib.Ballotmeasure(c.authuser, c.election, c.ballot, title, number, text, link)
        
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
            views = int(item['views'])
            views += 1
            item['views'] = str(views)
            dbHelpers.commit(item)
            entry['views'] = item['views']
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
                    url = rev['url']
                    date = str(rev.date)
                    title = rev['title']
                    text = rev['text']
                    officialURL = rev['ballotMeasureOfficialURL']
                    html = m.html(rev['text'], render_flags=m.HTML_SKIP_HTML)
                    revision['date'] = date
                    revision['urlCode'] = code
                    revision['url'] = url
                    revision['title'] = title
                    revision['text'] = text
                    revision['html'] = html
                    revision['ballotMeasureOfficialURL'] = officialURL
                    entry['revisionList'].append(revision)
                    
            result.append(entry)
            
        if len(result) == 0:
            return json.dumps({'statusCode':1})
            
        return json.dumps({'statusCode':0, 'result': result})

    # this is sort of a goofy case, it is only to show previous revisions        
    def ballotmeasureShow(self):

        #log.info("c.ballotmeasure is %s"%c.ballotmeasure)
        c.author = userLib.getUserByCode(c.ballotmeasure['userCode'])

        return render('/derived/6_ballot.bootstrap')
        
    def ballotCandidateAddHandler(self):
        if 'ballotCandidateTitle' in request.params:
            title = request.params['ballotCandidateTitle']
        else:
            title = 'New ballot candidate'
            
        if 'ballotCandidateNumber' in request.params:
            number = request.params['ballotCandidateNumber']
        else:
            number = '1'
        
        if 'ballotCandidateText' in request.params:
            text = request.params['ballotCandidateText']
        else:
            text = 'New ballot candidate description'

        if 'ballotCandidateParty' in request.params:
            party = request.params['ballotCandidateParty']
        else:
            party = 'no party specified'
            
        if 'ballotCandidateOfficialURL' in request.params:
            link = request.params['ballotCandidateOfficialURL']
        else:
            link = 'New ballot measure description'

            
        ballotLib.Ballotcandidate(c.authuser, c.election, c.ballot, title, number, text, party, link)
        
        returnURL = '/ballot/%s/%s/show'%(c.ballot['urlCode'], c.ballot['url'])
            
        return redirect(returnURL)
        
    def ballotcandidateEditHandler(self):
        # make a revision first of the previous version
        revisionLib.Revision(c.authuser, c.ballotcandidate)
        
        if 'ballotCandidateTitle' in request.params:
            title = request.params['ballotCandidateTitle']
            if title and title != '':
                c.ballotcandidate['title'] = title
                
        if 'ballotCandidateNumber' in request.params:
            number = request.params['ballotCandidateNumber']
            if number and number != '':
                c.ballotcandidate.sort = number
        
        if 'ballotCandidateText' in request.params:
            text = request.params['ballotCandidateText']
            if text and text != '':
                c.ballotcandidate['text'] = text
                
        if 'ballotCandidateParty' in request.params:
            c.ballotcandidate['ballotCandidateParty'] = request.params['ballotCandidateParty']
        else:
            c.ballotcandidate['ballotCandidateOfficialURL'] = ''
            
        if 'ballotCandidateOfficialURL' in request.params:
            c.ballotcandidate['ballotCandidateOfficialURL'] = request.params['ballotCandidateOfficialURL']
        else:
            c.ballotcandidate['ballotCandidateOfficialURL'] = ''
            
        dbHelpers.commit(c.ballotcandidate)
        
        returnURL = '/ballot/%s/%s/show'%(c.ballot['urlCode'], c.ballot['url'])
            
        return redirect(returnURL)
        
    def getBallotCandidates(self, id1, id2):
        c.ballotCandidates = ballotLib.getBallotCandidates(id1)
        if not c.ballotCandidates:
            c.ballotCandidates = []
  
        result = []
        myRatings = {}
        if 'ratings' in session:
		    myRatings = session['ratings']
		 
        mycandidateVotes = {}
        totalcandidateVotes = {}
        candidateMax = c.ballot['slateInfo']
        for item in c.ballotCandidates:
            entry = {}
            if 'user' in session and (c.authuser.id == item.owner or userLib.isAdmin(c.authuser.id)):
                entry['canEdit'] = 'yes'
            else:
                entry['canEdit'] = 'no'
            entry['objType'] = 'ballotcandidate'
            entry['url']= item['url']
            entry['urlCode']=item['urlCode']
            entry['title'] = item['title']
            entry['text'] = item['text']
            entry['number'] = item.sort
            views = int(item['views'])
            views += 1
            item['views'] = str(views)
            dbHelpers.commit(item)
            entry['views'] = item['views']
            entry['ballotCandidateParty'] = item['ballotCandidateParty']
            entry['ballotCandidateOfficialURL'] = item['ballotCandidateOfficialURL']
            entry['html'] = m.html(entry['text'], render_flags=m.HTML_SKIP_HTML)
            entry['date'] = item.date.strftime('%Y-%m-%d at %H:%M:%S')
            entry['fuzzyTime'] = fuzzyTime.timeSince(item.date)

			# user rating
            code = item['urlCode']
            if entry['urlCode'] in myRatings:
                entry['rated'] = myRatings[entry['urlCode']]
                entry['vote'] = 'voted'
                if entry['rated'] == '1':
                    mycandidateVotes[code] = 'voted'
                else:
                    mycandidateVotes[code] = 'nvote'
            else:
                entry['rated'] = 0
                entry['vote'] = 'nvote'
                mycandidateVotes[code] = 'nvote'

            entry['vote'] = 'nvote'
            entry['voteCount'] = int(item['ups']) + int(item['downs'])
            entry['ups'] = int(item['ups'])
            entry['downs'] = int(item['downs'])
            entry['netVotes'] = int(item['ups']) - int(item['downs'])
            totalcandidateVotes[code] = item['ups']
            

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
                    url = rev['url']
                    date = str(rev.date)
                    title = rev['title']
                    text = rev['text']
                    party = rev['ballotCandidateParty']
                    officialURL = rev['ballotCandidateOfficialURL']
                    html = m.html(rev['text'], render_flags=m.HTML_SKIP_HTML)
                    revision['date'] = date
                    revision['urlCode'] = code
                    revision['url'] = url
                    revision['title'] = title
                    revision['text'] = text
                    revision['html'] = html
                    revision['ballotMeasureParty'] = party
                    revision['ballotMeasureOfficialURL'] = officialURL
                    entry['revisionList'].append(revision)
                    
            result.append(entry)
            
        if len(result) == 0:
            return json.dumps({'statusCode':1})
            
        return json.dumps({'statusCode':0, 'result': result, 'mycandidateVotes': mycandidateVotes, 'totalcandidateVotes': totalcandidateVotes, 'candidateMax': candidateMax})
        

    # this is sort of a goofy case, it is only to show previous revisions        
    def ballotcandidateShow(self):
        #log.info("c.ballotcandidate is %s"%c.ballotcandidate)
        c.author = userLib.getUserByCode(c.ballotcandidate['userCode'])

        return render('/derived/6_ballot.bootstrap')

        
