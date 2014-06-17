#-*- coding: utf-8 -*-
import logging

from pylons import session, tmpl_context as c
from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl
from pylons import config
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.discussion   as discussionLib

log = logging.getLogger(__name__)

def getElection(code):
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['election', 'electionUnpublished']))\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .one()
    except:
        return False
        
def getAllElections():
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['election', 'electionUnpublished']))\
            .all()
    except:
        return False
        
def getElectionsForUser(code):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'election')\
            .filter(Thing.data.any(wc('userCode', code)))\
            .all()
    except:
        return False
        
def getBallotsForElection(code):
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['ballot', 'ballotUnpublished']))\
            .filter(Thing.data.any(wc('electionCode', code)))\
            .all()
    except:
        return False
        
def getBallot(code):
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['ballot', 'ballotUnpublished']))\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .one()
    except:
        return False
        
def getAllBallots():
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['ballot', 'ballotUnpublished']))\
            .all()
    except:
        return False
        
def getBallotMeasure(code):
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.objType.in_(['ballotmeasure', 'ballotmeasureUnpublished']))\
            .filter(Thing.data.any(wc('urlCode', code)))\
            .one()
    except:
        return False
        
def getBallotsForUser(code):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'ballot')\
            .filter(Thing.data.any(wc('userCode', code)))\
            .all()
    except:
        return False
        
def getBallotMeasures(code, count = 0, deleted = u'0'):
    try:
        q = meta.Session.query(Thing)\
            .filter_by(objType = 'ballotmeasure')\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('ballotCode', code)))\
            .order_by('sort')
        if count:
            return q.count()
        else:
            return q.all()
    except:
        return False
        
def searchBallots( keys, values, deleted = u'0', public = '1', count = False):
    try:
        if type(keys) != type([]):
            p_keys = [keys]
            p_values = [values]
        else:
            p_keys = keys
            p_values = values
        map_ballots = map(wcl, p_keys, p_values)
        q = meta.Session.query(Thing)\
                .filter_by(objType = 'ballot')\
                .filter(Thing.data.any(wc('deleted', deleted)))\
                .filter(Thing.data.any(wc('public', public)))\
                .filter(Thing.data.any(reduce(or_, map_ballots)))
        if count:
            return q.count()
        return q.all()
    except Exception as e:
        log.error(e)
        return False

# Election Object
def Election(owner, title, text, scope, electionDate, electionOfficialURL, public):
    b = Thing('election', owner.id)
    generic.linkChildToParent(b, owner)
    commit(b)
    b['urlCode'] = utils.toBase62(b)
    b['title'] = title
    b['url'] = utils.urlify(title[:20])
    b['text'] = text
    b['scope'] = scope
    b['electionDate'] = electionDate
    b['electionOfficialURL'] = electionOfficialURL
    b['deleted'] = u'0'
    b['disabled'] = u'0'
    b['election_public'] = public
    b['archived'] = u'0'
    b['views'] = '0'
    commit(b)
    return b

# Ballot Object
def Ballot(owner, election, title, number, text, instructions, ballotSlate, slateInfo):
    b = Thing('ballot', owner.id)
    generic.linkChildToParent(b, owner)
    generic.linkChildToParent(b, election)
    commit(b)
    b['urlCode'] = utils.toBase62(b)
    b['title'] = title
    b['url'] = utils.urlify(title[:20])
    b['text'] = text
    b['instructions'] = instructions
    # currently, one of 'measures' for ballot measures with a yes/no vote 
    # and 'candidates' for candidate slates running for office
    b['ballotSlate'] = ballotSlate
    # additional slate specific info. If 'measures' the term used to reference the measure in the UI.
    # If candidates, the max number of candidates in the slate which can be voted for
    b['slateInfo'] = slateInfo
    b['deleted'] = u'0'
    b['disabled'] = u'0'
    b['archived'] = u'0'
    b['views'] = '0'
    b.sort = number
    commit(b)
    return b

# Ballot Measure Object
def Ballotmeasure(owner, election, ballot, title, number, text, ballotMeasureOfficialURL):
    b = Thing('ballotmeasure', owner.id)
    generic.linkChildToParent(b, owner)
    generic.linkChildToParent(b, ballot)
    generic.linkChildToParent(b, election)
    commit(b)
    b['urlCode'] = utils.toBase62(b)
    b['title'] = title
    b['url'] = utils.urlify(title[:20])
    b['text'] = text
    b['ballotMeasureOfficialURL'] = ballotMeasureOfficialURL
    b['numComments'] = '0'
    b['deleted'] = u'0'
    b['disabled'] = u'0'
    b['public'] = u'0'
    b['archived'] = u'0'
    b['views'] = '0'
    b['ups'] = '0'
    b['downs'] = '0'
    b.sort = number
    commit(b)
    d = discussionLib.Discussion(owner = owner, discType = 'ballotmeasure', attachedThing = b, title = title)
    b['discussion_child'] = d.d['urlCode']
    commit(b)
    return b
    
# Ballot Candidate Object
def Ballotcandidate(owner, election, ballot, title, number, text, ballotCandidateParty, ballotCandidateOfficialURL):
    b = Thing('ballotcandidate', owner.id)
    generic.linkChildToParent(b, owner)
    generic.linkChildToParent(b, ballot)
    generic.linkChildToParent(b, election)
    commit(b)
    b['urlCode'] = utils.toBase62(b)
    b['title'] = title
    b['url'] = utils.urlify(title[:20])
    b['ballotCandidateParty'] = ballotCandidateParty
    b['text'] = text
    b['ballotCandidateOfficialURL'] = ballotCandidateOfficialURL
    b['numComments'] = '0'
    b['deleted'] = u'0'
    b['disabled'] = u'0'
    b['public'] = u'0'
    b['archived'] = u'0'
    b['views'] = '0'
    b['ups'] = '0'
    b['downs'] = '0'
    b.sort = number
    commit(b)
    d = discussionLib.Discussion(owner = owner, discType = 'ballotcandidate', attachedThing = b, title = title)
    b['discussion_child'] = d.d['urlCode']
    commit(b)
    return b
    
def isPublic(ballot):
    if ballot['public'] == '1':
        return True
    else:
        return False
