import logging, re, pickle, formencode
import time, datetime

from formencode import validators, htmlfill
from formencode.compound import All
from formencode.foreach import ForEach

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.workshop import Workshop, getWorkshop, isScoped
from pylowiki.lib.db.geoInfo import getScopeTitle, WorkshopScope, getGeoTitles
from pylowiki.lib.db.revision import get_revision
from pylowiki.lib.db.slideshow import getSlideshow
from pylowiki.lib.db.slide import getSlide
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.resource import getResourcesByWorkshopID, getActiveResourcesByWorkshopID, getInactiveResourcesByWorkshopID, getDisabledResourcesByWorkshopID, getDeletedResourcesByWorkshopID
from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop, getActiveSuggestionsForWorkshop, getInactiveSuggestionsForWorkshop, getDisabledSuggestionsForWorkshop, getDeletedSuggestionsForWorkshop
from pylowiki.lib.db.user import getUserByID, isAdmin
from pylowiki.lib.db.facilitator import isFacilitator, getFacilitatorsByWorkshop
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.tag import Tag, setWorkshopTagEnable
from pylowiki.lib.db.motd import MOTD, getMessage
from pylowiki.lib.db.follow import Follow, getFollow, isFollowing, getWorkshopFollowers
from pylowiki.lib.db.account import Account, getUserAccount
from pylowiki.lib.db.event import Event

from pylowiki.lib.utils import urlify
from pylowiki.lib.sort import sortBinaryByTopPop, sortContByAvgTop

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h
from pylowiki.lib.db.dbHelpers import commit

import re

log = logging.getLogger(__name__)

class CommaSepList(validators.FancyValidator):
    cannot_be_empty=True
    reassemble_value = ''

    def _to_python(self, value, state):
        return value.split(",")

    def validate_python(self, value, state):
        for elem in value:
            elem.strip()
            if (elem == '' or elem == 'none') and len(value) == 1 and self.cannot_be_empty == True:
                h.flash("Additional workshop tags error.", 'error')
                raise formencode.Invalid('Enter at least one tag. For multiple tags, separate each with a comma.', value, state)
            elif elem == '' and len(value) > 1:
                h.flash("Additional workshop tags error.", 'error')
                raise formencode.Invalid('For multiple tags, separate each with one comma.', value, state)

class NoGoalsSet(validators.FancyValidator):
    max = 300
    messages = {
        'too_many': 'Sorry, the description of goals should not exceed 300 characters. Your entry has %(max)i characters.',
    }

    def _to_python(self, value, state):
        # _to_python gets run before validate_python.  Here we
        # strip whitespace off the password, because leading and
        # trailing whitespace in a password is too elite.
        value = value.strip()
        if value == 'No goals set':
            value = ''
        return value

    def validate_python(self, value, state):
        if value == '':
            raise formencode.Invalid('Please provide a description of this workshop\'s goals.', value, state)
        if len(value) > self.max:
            raise validators.Invalid(self.message("too_many", state, max=self.max), value, state)

class NotBothPublicInputs(validators.FancyValidator):

    def validate_python(self, field_dict, state):

        pubScope = field_dict['publicScope']
        pubPostList = field_dict['publicPostalList']

        if pubScope and pubPostList:
            h.flash("Public scope error.", 'error')
            raise formencode.Invalid("Please select a public scope, or enter a list of zipcodes.", field_dict, state, error_dict={'publicScope':'Please select a public scope,', 'publicPostalList':'OR enter a list of zipcodes.'})

class editWorkshopForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    title = validators.String(strip=True, not_empty=True, messages = {'empty' : 'Please provide a name for your workshop.'})
    goals = NoGoalsSet()
    publicScope = formencode.validators.String(if_missing=None)
    publicPostalList = formencode.validators.String(if_missing=None)
    chained_validators = [validators.RequireIfPresent('publicScope', missing="publicPostalList", messages = {'empty' : 'Please select one of these options OR provide a list of zipcodes in the next field.'})]
    chained_validators = [validators.RequireIfPresent('publicPostalList', missing="publicScope", messages = {'empty' : 'Please select one of these options OR provide a list of zipcodes in the next field.'})]
    chained_validators = [NotBothPublicInputs()]
    publicPostalList = CommaSepList(cannot_be_empty=False)
    memberTags = CommaSepList(cannot_be_empty=True)

class addWorkshopForm(formencode.Schema):
    maxTitle = 70
    allow_extra_fields = True
    filter_extra_fields = True
    workshopName = validators.String(strip=True, not_empty=True, max=maxTitle, messages = {'empty' : 'Please give your workshop a name.'})

class WorkshopController(BaseController):

    @h.login_required
    def addWorkshop(self):
        c.account = getUserAccount(c.authuser.id)
        if c.account and c.account['numRemaining'] > 0:
            c.title = "Create New Workshop"
            c.heading = "Basic information"

            # tracks remaining number of workshops which can
            # be created by this user
            numRemaining = c.account['numRemaining'] 
            numRemaining = int(numRemaining) - 1
            c.account['numRemaining'] = numRemaining
            commit(c.account)

            return render('/derived/workshop_create.bootstrap')
        else:
            h.flash("You are not authorized to view that page", "warning")
            return redirect('/')

    @h.login_required
    def followHandler(self, id1, id2):
        code = id1
        url = id2
        ##log.info('followHandler %s %s' % (code, url))
        w = getWorkshop(code, urlify(url))
        f = getFollow(c.authuser.id, w.id)
        if f:
           ##log.info('f is %s' % f)
           f['disabled'] = False
           commit(f)
        elif not isFollowing(c.authuser.id, w.id): 
           ##log.info('not isFollowing')
           f = Follow(c.authuser.id, w.id, 'workshop') 
        else:
           ##log.info('else')
           f = Follow(c.authuser.id, w.id, 'workshop') 
           
        return "ok"

    @h.login_required
    def unfollowHandler(self, id1, id2):
        code = id1
        url = id2
        ##log.info('unfollowHandler %s %s' % (code, url))
        w = getWorkshop(code, urlify(url))
        f = getFollow(c.authuser.id, w.id)
        if f:
           ##log.info('f is %s' % f)
           f['disabled'] = True
           commit(f)
           
        return "ok"

    @h.login_required
    def configureWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"

        c.w = getWorkshop(code, urlify(url))
        werror = 0
        werrMsg = 'Missing Info: '
        wstarted = 0
        if c.w['startTime'] != '0000-00-00':
           wstarted = 1

        ##log.info('wstarted is %s' % wstarted)

        # Is there anything more painful than form validation?
        # I don't think so...

        if 'title' in request.params:
            wTitle = request.params['title']
            c.w['title'] = wTitle
        else:
            werrMsg += 'Name '
            werror = 1

        if 'goals' in request.params:
           wGoals = str(request.params['goals'])
           wGoals = wGoals.lstrip()
           wGoals = wGoals.rstrip()
           ##c.w['goals'] = request.params['goals']
           c.w['goals'] = wGoals
        else:
           werror = 1
           werrMsg += 'Goals '

        log.info('Got wGoals %s' % wGoals)
        if 'allowSuggestions' in request.params:
           allowSuggestions = request.params['allowSuggestions']
           if allowSuggestions == '1' or allowSuggestions == '0':
              c.w['allowSuggestions'] = allowSuggestions
        else:
           werror = 1
           werrMsg += 'Allow Suggestions '

        if 'allowResources' in request.params:
           allowResources = request.params['allowResources']
           if allowResources == '1' or allowResources == '0':
              c.w['allowResources'] = allowResources
        else:
           werror = 1
           werrMsg += 'Allow Resources '


        # Hmm... Take this out so they can't change it?
        #if 'publicPostal' in request.params:
        #   c.w['publicPostal'] = request.params['publicPostal']
        #else:
        #   werror = 1
        #   werrMsg = 'No Workshop Postal'

        if not wstarted:
            werrCheckParticipants = False
            if 'publicScope' in request.params:
              c.w['publicScope'] = request.params['publicScope']
              c.w['scopeMethod'] = 'publicScope'
            else:
              # NOTE setting publicScope to '' instead of 00, since 00 is a valid state to have if publicPostalList has a value (line 237)
              c.w['publicScope'] = ''
              # NOTE set these only if the other input field does not have content, use werrCheckParticipants to watch for this 
              # werror = 1
              # werrMsg += 'Participants'
              werrCheckParticipants = True

            if 'publicPostalList' in request.params:
              plist = request.params['publicPostalList']
              plist = plist.lstrip()
              plist = plist.rstrip()
              plist = plist.replace(' ', ',')
              plist = plist.replace(',,', ',')
              plist = plist.replace('    ', ',')
              c.w['publicPostalList'] = plist
              if plist != '':
                 c.w['scopeMethod'] = 'publicPostalList'
                 c.w['publicScope'] = '00'
            else:
              werror = 1
              werrMsg += 'Public Postal List '
           
            if c.w['scopeMethod'] == 'publicScope':
              c.w['publicScopeTitle'] = getScopeTitle(c.w['publicPostal'], 'United States', c.w['publicScope'])
            elif c.w['scopeMethod'] == 'publicPostalList':
              c.w['publicScopeTitle'] = 'postal codes of ' + c.w['publicPostalList']

            if 'publicTags' in request.params:
              publicTags = request.params.getall('publicTags')
              c.w['publicTags'] = ','.join(publicTags)
            else:
              werror = 1
              werrMsg += 'System Tags '
   
            if 'memberTags' in request.params:
              wMemberTags = request.params['memberTags']
              wMemberTags = wMemberTags.lstrip()
              wMemberTags = wMemberTags.rstrip()
              c.w['memberTags'] = wMemberTags
            else:
              werror = 1
              werrMsg += 'Member Tags '

            if 'startWorkshop' in request.params:
              startButtons = request.params.getall('startWorkshop')
              ##log.info('Got startWorkshop %s' % ','.join(startButtons))
              if 'Start' in startButtons and 'VerifyStart' in startButtons and werror == 0:
                 startTime = datetime.datetime.now()
                 #c.w['startTime'] = startTime.ctime()
                 c.w['startTime'] = startTime
                 endTime = datetime.datetime.now()
                 endTime = endTime.replace(year = endTime.year + 1)
                 #c.w['endTime'] = endTime.ctime()
                 c.w['endTime'] = endTime
                 for wTag in request.params.getall('publicTags'):
                    wTag = wTag.lstrip()
                    wTag = wTag.rstrip()
                    Tag('system', wTag, c.w.id, c.w.owner)
                 for mTag in wMemberTags.split(','):
                    mTag = mTag.lstrip()
                    mTag = mTag.rstrip()
                    Tag('member', mTag, c.w.id, c.w.owner)
                 if c.w['scopeMethod'] == 'publicPostalList':
                    pString = c.w['publicPostalList']
                    pList = pString.split(',')
                    for p in pList:
                       if p != '':
                          WorkshopScope(p, 'United States', c.w.id, c.w.owner)
                 elif c.w['scopeMethod'] == 'publicScope':
                    p = c.w['publicPostal']
                    WorkshopScope(p, 'United States', c.w.id, c.w.owner)

            formSchema = editWorkshopForm()
            try:
                c.form_result = formSchema.to_python(request.params)
            except formencode.Invalid, error:
                alert = {'type':'error'}
                alert['title'] = 'All * Fields Required'
                alert['content'] = ''
                "alert['content'] = 'Please check all Required Fields'"
                session['alert'] = alert
                session.save()
                c.form_result = error.value
                c.form_errors = error.error_dict or {}
                log.info("form_result "+ str(c.form_result))
                log.info("form_errors "+ str(c.form_errors))
                c.form_result['memberTags'] = wMemberTags
                c.form_result['publicPostalList'] = plist
                html = render('/derived/workshop_configure.bootstrap')
                return htmlfill.render(
                    html,
                    defaults=c.form_result,
                    errors=c.form_errors
                )
            else:
                if werror == 1:
                    alert = {'type':'error'}
                    alert['title'] = 'Missing Info: Workshop Tags'
                    alert['content'] = ''
                    "alert['content'] = 'Please check all Required Fields'"
                    session['alert'] = alert
                    session.save()
                    "h.flash( werrMsg, 'error')"
                    return redirect('/workshop/%s/%s/configure'%(c.w['urlCode'], c.w['url']))  #c.form_result[''], c.form_result[''],)
                else:
                    if isFacilitator(c.authuser.id, c.w.id):
                        commit(c.w)
                    h.flash('Workshop configuration complete!', 'success')
            return redirect('/workshop/%s/%s'%(c.w['urlCode'], c.w['url']))  #c.form_result[''], c.form_result[''],)
        else:
           if werror == 1:
                alert = {'type':'error'}
                alert['title'] = 'Missing Info: Workshop Tags'
                alert['content'] = ''
                "alert['content'] = 'Please check all Required Fields'"
                session['alert'] = alert
                session.save()
                "h.flash( werrMsg, 'error')"
                return redirect('/workshop/%s/%s/configure'%(c.w['urlCode'], c.w['url']))  #c.form_result[''], c.form_result[''],)
           else:
              if isFacilitator(c.authuser.id, c.w.id):
                 commit(c.w)
                 h.flash('Workshop configuration complete!', 'success')
        return redirect('/workshop/%s/%s'%(c.w['urlCode'], c.w['url']))  #c.form_result[''], c.form_result[''],)


    @h.login_required
    def addWorkshopHandler(self):
        workshopName = request.params['workshopName']
        try:
            publicPrivate = request.params['publicPrivate']
        except:
            publicPrivate = ''

        formSchema = addWorkshopForm()
        try:
            form_result = formSchema.to_python(request.params)
        except validators.Invalid, error:
            h.flash("Errors found, please fix the highlighted areas", "warning")
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            html = render('/derived/workshop_configure.bootstrap')
            return htmlfill.render(
                html,
                defaults=c.form_result,
                errors=c.form_errors
            )

        w = Workshop(workshopName, c.authuser, publicPrivate)
        c.workshop_id = w.w.id # TEST
        c.title = 'Add slideshow'
        c.motd = MOTD('Welcome to the workshop!', w.w.id, w.w.id)
        c.postal = w.w['publicPostal']
        titles = getGeoTitles('united-states', c.postal)
        sList = titles.split('|')
        c.country = sList[2].title()
        c.state = sList[4].title()
        c.county = sList[6].title()
        c.city = sList[8].title()
        return redirect('/workshop/%s/%s/configure'%(w.w['urlCode'], w.w['url']))
    
    @h.login_required
    def adminWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Administrate Workshop"

        w = getWorkshop(code, urlify(url))
        if not isFacilitator(c.authuser.id, w.id) and not isAdmin(c.authuser.id):
           h.flash("You are not authorized", "warning")
           return redirect('/')

        m = getMessage(w.id)
         
        werror = 0
        werrMsg = 'Incomplete information: '

        if 'motd' in request.params:
           motd = request.params['motd']
           m['data'] = motd
        else:
           werror = 1
           werrMsg += 'Message text '
            
        if 'enableMOTD' in request.params:
           enable = request.params['enableMOTD']
           if enable == '1' or enable == '0':
              m['enabled'] = enable
           else:
              werror = 1
              werrMsg += 'Publish message or not '
        else:
           werror = 1
           werrMsg += 'Publish message or not '

        eventReason = ''
        if 'eventReason' in request.params:
            eventReason = request.params['eventReason']

        eW = 0
        veW = 0
        if 'enableWorkshop' in request.params:
           eW = 1

        if 'verifyEnableWorkshop' in request.params:
           veW = 1

        #log.info('Enable is %s and Verify is %s' % (eW, veW))
        if eW != veW:
           ##log.info('not equal')
           werror = 1
           if w['deleted'] == 1:
              eAction = 'enabled'
           else:
              eAction = 'disabled'
           werrMsg += 'Action must be verified before workshop can be ' + eAction + '.'
        elif eW == 1 and veW == 1:
           ##log.info('equal and deleted is %s' % w['deleted'])
           if w['deleted'] == '1':
              w['deleted'] = '0'
              eAction = 'enabled'
              ##log.info('doing undelete')
           else:
              w['deleted'] = '1'
              eAction = 'disabled'
              ##log.info('doing delete')

           setWorkshopTagEnable(w, w['deleted'])
           Event('Workshop %s'%eAction, 'Workshop %s by %s Note: %s'%(eAction, c.authuser['name'], eventReason), w, c.authuser)
           commit(w)

            
        commit(m)
        return redirect('/workshop/%s/%s/admin'%(w['urlCode'], w['url']))
    
    def display(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, urlify(url))
        c.title = c.w['title']
        
        if 'user' in session:
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            c.isScoped = isScoped(c.authuser, c.w)
            c.isFollowing = isFollowing(c.authuser.id, c.w.id)
            c.isAdmin = isAdmin(c.authuser.id)
        
        fList = []
        for f in (getFacilitatorsByWorkshop(c.w.id)):
           if 'pending' in f and f['pending'] == '0' and f['disabled'] == '0':
              fList.append(f)
        
        c.facilitators = fList
        c.followers = getWorkshopFollowers(c.w.id)

        ##log.info('c.isFollowing is %s' % c.isFollowing)
        if c.w['startTime'] != '0000-00-00':
           c.wStarted = True
        else:
          c.wStarted = False

        c.slides = []
        c.slideshow = getSlideshow(c.w['mainSlideshow_id'])
        slide_ids = [int(item) for item in c.slideshow['slideshow_order'].split(',')]
        for id in slide_ids:
            s = getSlide(id) # Don't grab deleted slides
            if s:
                c.slides.append(s)
            
        c.resources = getActiveResourcesByWorkshopID(c.w.id)
        c.dresources = getInactiveResourcesByWorkshopID(c.w.id)
        c.resources = sortBinaryByTopPop(c.resources)
        c.suggestions = getActiveSuggestionsForWorkshop(code, urlify(url))
        c.suggestions = sortContByAvgTop(c.suggestions, 'overall')
        c.dsuggestions = getInactiveSuggestionsForWorkshop(code, urlify(url))
        
        if 'user' in session:
            ratedSuggestionIDs = []
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                """
                    Here we get a Dictionary with the commentID as the key and the ratingID as the value
                    Check to see if the commentID as a string is in the Dictionary keys
                    meaning it was already rated by this user
                """
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall']))
                ratedSuggestionIDs = sugRateDict.keys()
        
        for item in c.suggestions:
            """ Grab first 250 chars as a summary """
            if len(item['data']) <= 250:
                item['suggestionSummary'] = h.literal(h.reST2HTML(item['data']))
            else:
                item['suggestionSummary'] = h.literal(h.reST2HTML(item['data'][:250] + '...'))
        
            if 'user' in session:    
                """ Grab the associated rating, if it exists """
                found = False
                try:
                    index = ratedSuggestionIDs.index(item.id)
                    found = True
                except:
                    pass
                if found:
                    item.rating = getRatingByID(sugRateDict[item.id])
                else:
                    item.rating = False

        c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])

        if 'feedbackDiscussion_id' in c.w:
           c.discussion = getDiscussionByID(c.w['feedbackDiscussion_id'])
        else:
           c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])

        c.motd = getMessage(c.w.id)
        # kludge for now
        if c.motd == False:
           c.motd = MOTD('Welcome to the workshop!', c.w.id, c.w.id)

        """ Grab first 250 chars as a summary """
        if len(c.motd['data']) <= 140:
            c.motd['messageSummary'] = h.literal(h.reST2HTML(c.motd['data']))
        else:
            c.motd['messageSummary'] = h.literal(h.reST2HTML(c.motd['data'][:140] + '...'))


        return render('/derived/workshop_home.bootstrap')

    def inactiveSuggestions(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        c.title = c.w['title']
        c.suggestions = getActiveSuggestionsForWorkshop(code, urlify(url))
        c.dsuggestions = getInactiveSuggestionsForWorkshop(code, urlify(url))

        return render('/derived/suggestion_list.html')

    def inactiveResources(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        c.title = c.w['title']
        c.resources = getActiveResourcesByWorkshopID(c.w.id)
        c.dresources = getInactiveResourcesByWorkshopID(c.w.id)

        return render('/derived/resource_list.html')

    def background(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        c.title = c.w['title']
        c.resources = getActiveResourcesByWorkshopID(c.w.id)
        c.commentsDisabled = 0
        
        c.slides = []
        c.slideshow = getSlideshow(c.w['mainSlideshow_id'])
        slide_ids = [int(item) for item in c.slideshow['slideshow_order'].split(',')]
        for id in slide_ids:
            s = getSlide(id) # Don't grab deleted slides
            if s:
                c.slides.append(s)
        
        r = get_revision(int(c.w['mainRevision_id']))
        if 'user' in session:
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            c.facilitators = getFacilitatorsByWorkshop(c.w.id)
            
            reST = r['data']
            reSTlist = self.get_reSTlist(reST)
            HTMLlist = self.get_HTMLlist(reST)
            
            c.wikilist = zip(HTMLlist, reSTlist)
        else:
            c.content = h.literal(h.reST2HTML(r['data']))
        
        c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])
        
        c.lastmoddate = r.date
        c.lastmoduser = getUserByID(r.owner)
        
        return render('/derived/workshop_bg.bootstrap')

    def feedback(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        r = get_revision(int(c.w['mainRevision_id']))
        c.lastmoddate = r.date
        c.lastmoduser = getUserByID(r.owner)
        c.commentsDisabled = 0

        c.title = c.w['title']
        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.facilitators = getFacilitatorsByWorkshop(c.w.id)
        c.isScoped = isScoped(c.authuser, c.w)

        if 'feedbackDiscussion_id' in c.w:
           c.discussion = getDiscussionByID(c.w['feedbackDiscussion_id'])
        else:
           c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])

        c.rating = False
        if 'ratedThings_workshop_overall' in c.authuser.keys():
            """
                Here we get a Dictionary with the commentID as the key and the ratingID as the value
                Check to see if the commentID as a string is in the Dictionary keys
                meaning it was already rated by this user
            """
            workRateDict = pickle.loads(str(c.authuser['ratedThings_workshop_overall']))
            if c.w.id in workRateDict.keys():
                c.rating = getRatingByID(workRateDict[c.w.id])

        c.motd = getMessage(c.w.id)
        c.motd['messageSummary'] = h.literal(h.reST2HTML(c.motd['data']))

        return render("/derived/workshop_feedback.bootstrap")
    
    @h.login_required
    def configure(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        if not isFacilitator(c.authuser.id, c.w.id) and not(isAdmin(c.authuser.id)):
            h.flash("You are not authorized", "warning")
            return render('/')

        return render('/derived/workshop_configure.bootstrap')
    
    @h.login_required
    def admin(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        if not isFacilitator(c.authuser.id, c.w.id) and not(isAdmin(c.authuser.id)):
           h.flash("You are not authorized", "warning")
           return redirect('/')

        c.title = c.w['title']
        c.motd = getMessage(c.w.id)

        c.s = getActiveSuggestionsForWorkshop(code, urlify(url))
        c.disabledSug = getDisabledSuggestionsForWorkshop(code, urlify(url))
        c.deletedSug = getDeletedSuggestionsForWorkshop(code, urlify(url))
        c.r = getActiveResourcesByWorkshopID(c.w.id)
        c.disabledRes = getDisabledResourcesByWorkshopID(c.w.id)
        c.deletedRes = getDeletedResourcesByWorkshopID(c.w.id)
        c.f = getFacilitatorsByWorkshop(c.w.id)
        c.df = getFacilitatorsByWorkshop(c.w.id, 1)
        
        return render('/derived/workshop_admin.bootstrap')
    
    # ------------------------------------------
    #    Helper functions for wiki controller
    #-------------------------------------------

    @h.login_required
    def CleanList( self, l ):
        """ Remove all empty rows from list """
        counter = 0
        length = len( l )
        while counter < length:
            if l[counter].isspace() or l[counter] == None or l[counter] == "":
                del l[counter]
                length = len( l )   
            counter += 1
        return l


    @h.login_required
    def isodd( self, integer ):
        """ if interger is odd return True, else return False"""
        if integer % 2 == 0:
            return False
        else:
            return True
    
    @h.login_required
    def get_reSTlist( self, reST ):
        """Accept a reST string and return a list of sections
        This code is a bit ugly but it works... 
        SORRY IF YOU HAVE TO WORK ON THIS..."""

        splitter = re.compile('(.*\r\n[=\-`:~^_*+#]{3,}.+\r\n+)') # Create regex object that splits reST string by headings
        reSTlist = self.CleanList(splitter.split( reST )) # Split the reST into a list, and remove any empty rows
        
        """reSTlist has heading and section data in seperate rows.
        The logic below merges the heading and section data rows."""
        
        lenght = len( reSTlist )
        
        if self.isodd( lenght ): # if the length is odd, the first row doesn't have a heading and will be in its own section
            offset = counter = 1
        else:
            offset = counter = 0

        """ join the heading list row with the data list row """
        while counter < lenght: # loop through list until end
            if self.isodd( counter + offset ): # do nothing if even
                reSTlist[counter-1] = reSTlist[counter-1] + reSTlist[counter]
                reSTlist[counter] = "" # set current row to empty
            counter = counter + 1

        return self.CleanList( reSTlist ) # remove empty rows and return list

    @h.login_required
    def get_HTMLlist( self, reST):
        """Accept reST list, convert to html, remove newlines so regex works, split HTML into a list by heading."""

        splitter = re.compile('(<div class\="section".*?)(?=<div class\="section")', re.DOTALL) # Create regex object to split HTML by header section.
        HTMLlist = self.CleanList(splitter.split(h.literal(h.reST2HTML( reST ))))
        
        if len(HTMLlist) == 1: # This only happens if there are two sections but only one heading
            splitter = re.compile('(<div class\="section".*</div>)', re.DOTALL) # Create regex object to split HTML by header section.
            HTMLlist = self.CleanList(splitter.split(h.literal(h.reST2HTML( reST ))))      
    
        return HTMLlist
