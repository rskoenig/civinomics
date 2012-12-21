import logging, re, pickle, formencode
import time, datetime

from formencode import validators, htmlfill
from formencode.compound import All
from formencode.foreach import ForEach
from ordereddict import OrderedDict
import webhelpers.paginate as paginate

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.workshop import Workshop, getWorkshop, isScoped
from pylowiki.lib.db.geoInfo import getScopeTitle, WorkshopScope, getGeoScope, getGeoTitles
from pylowiki.lib.db.revision import get_revision
from pylowiki.lib.db.slideshow import getSlideshow, getAllSlides
from pylowiki.lib.db.slide import getSlide
from pylowiki.lib.db.discussion import getDiscussionByID, getActiveDiscussionsForWorkshop, getDisabledDiscussionsForWorkshop, getDeletedDiscussionsForWorkshop
#from pylowiki.lib.db.resource import getResourcesByWorkshopID, getActiveResourcesByWorkshopID, getInactiveResourcesByWorkshopID, getDisabledResourcesByWorkshopID, getDeletedResourcesByWorkshopID
from pylowiki.lib.db.resource import getResourcesByWorkshopCode, getActiveResourcesByWorkshopCode, getInactiveResourcesByWorkshopCode, getDisabledResourcesByWorkshopCode, getDeletedResourcesByWorkshopCode
from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop, getAdoptedSuggestionsForWorkshop, getActiveSuggestionsForWorkshop, getInactiveSuggestionsForWorkshop, getDisabledSuggestionsForWorkshop, getDeletedSuggestionsForWorkshop
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
           f['disabled'] = '0'
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
           f['disabled'] = '1'
           commit(f)
           
        return "ok"

    @h.login_required
    def configureBasicWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"

        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""        
        else:
            return(redirect("/"))

        slideshow = getSlideshow(c.w['mainSlideshow_id'])
        c.slideshow = getAllSlides(slideshow.id)

        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = 'Missing Info: '
        wstarted = 0
        if c.w['startTime'] != '0000-00-00':
           wstarted = 1

        ##log.info('wstarted is %s' % wstarted)

        # Is there anything more painful than form validation?
        # I don't think so...

        if 'title' in request.params:
            wTitle = request.params['title']
            wTitle = wTitle.lstrip()
            wTitle = wTitle.rstrip()
            if wTitle and wTitle != c.w['title']:
                c.w['title'] = wTitle
                wchanges = 1
                weventMsg = weventMsg + "Updated name. "
        else:
            werrMsg += 'Name '
            werror = 1

        if 'goals' in request.params:
           wGoals = str(request.params['goals'])
           wGoals = wGoals.lstrip()
           wGoals = wGoals.rstrip()
           if wGoals and wGoals != c.w['goals']:
               c.w['goals'] = wGoals
               wchanges = 1
               weventMsg = weventMsg + "Updated goals. "
        else:
           werror = 1
           werrMsg += 'Goals '

        ##log.info('Got wGoals %s' % wGoals)
        if 'allowSuggestions' in request.params:
           allowSuggestions = request.params['allowSuggestions']
           if (allowSuggestions == '1' or allowSuggestions == '0') and allowSuggestions != c.w['allowSuggestions']:
              wchanges = 1
              weventMsg = weventMsg + "Changed allowSuggestions from " + c.w['allowSuggestions'] + " to " + allowSuggestions + "."
              c.w['allowSuggestions'] = allowSuggestions
        else:
           werror = 1
           werrMsg += 'Allow Suggestions '

        if 'allowResources' in request.params:
           allowResources = request.params['allowResources']
           if (allowResources == '1' or allowResources == '0') and allowResources != c.w['allowResources']:
              wchanges = 1
              weventMsg = weventMsg + "Changed allowResources from " + c.w['allowResources'] + " to " + allowResources + "."
              c.w['allowResources'] = allowResources
        else:
           werror = 1
           werrMsg += 'Allow Resources '

        if not wstarted:
            if 'publicTags' in request.params:
              publicTags = request.params.getall('publicTags')
              wpTags = ','.join(publicTags)
              if wpTags and wpTags != c.w['publicTags']:
                  wchanges = 1
                  weventMsg = weventMsg + "Updated workshop tags."
                  c.w['publicTags'] = wpTags
            else:
              werror = 1
              werrMsg += 'System Tags '
   
            if 'memberTags' in request.params:
              wMemberTags = request.params['memberTags']
              wMemberTags = wMemberTags.lstrip()
              wMemberTags = wMemberTags.rstrip()
              if wMemberTags and c.w['memberTags'] != wMemberTags:
                  wchanges = 1
                  weventMsg = weventMsg + "Updated facilitator contributed tags."
              if wMemberTags == 'none':
                  werror = 1
                  werrMsg += 'Member Tags '

              c.w['memberTags'] = wMemberTags
            else:
              werror = 1
              werrMsg += 'Member Tags '

        # save successful changes
        if wchanges and (isFacilitator(c.authuser.id, c.w.id) or isAdmin(c.authuser.id)):
            commit(c.w)
            Event('Workshop Config Updated by %s'%c.authuser['name'], '%s'%weventMsg, c.w, c.authuser)

        if werror:
            alert = {'type':'error'}
            alert['title'] = werrMsg
            session['alert'] = alert
            session.save()
        else:
            if isFacilitator(c.authuser.id, c.w.id):
                commit(c.w)
                alert = {'type':'success'}
                alert['title'] = 'Workshop basic information saved!'
                session['alert'] = alert
                session.save()

        return redirect('/workshop/%s/%s/configure'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configureSingleWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"

        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""
        else:
            return(redirect("/"))




        slideshow = getSlideshow(c.w['mainSlideshow_id'])
        c.slideshow = getAllSlides(slideshow.id)

        werror = 0
        wstarted = 0
        if c.w['startTime'] != '0000-00-00':
           wstarted = 1

        ##log.info('wstarted is %s' % wstarted)

        # Is there anything more painful than form validation?
        # I don't think so...

        if 'publicPostal' in request.params:
           pTest = request.params['publicPostal']
           sTest = getGeoScope(pTest, 'united-states')
           if sTest:
               c.w['publicPostal'] = request.params['publicPostal']
           else:
              werror = 1
              werrMsg = 'Postal Code of ' + pTest + ' does not exist.'
        else:
           werror = 1
           werrMsg = 'No Workshop Home Postal'

        if 'publicScope' in request.params:
           c.w['publicScope'] = request.params['publicScope']
           c.w['scopeMethod'] = 'publicScope'
           c.w['publicScopeTitle'] = getScopeTitle(c.w['publicPostal'], 'United States', c.w['publicScope'])
           c.w['publicPostalList'] = ''
        else:
           werror = 1
           werrMsg = 'No Workshop Public Sphere'
           alert = {'type':'error'}
           alert['title'] = werrMsg
           session['alert'] = alert
           session.save()
           return redirect('/workshop/%s/%s/configure'%(c.w['urlCode'], c.w['url']))
        if isFacilitator(c.authuser.id, c.w.id) and werror == 0:
           alert = {'type':'success'}
           alert['title'] = "Workshop Eligibility Saved!"
           session['alert'] = alert
           session.save()
           Event('Workshop Config Updated by %s'%c.authuser['name'], 'Public Sphere updated.', c.w, c.authuser)
           commit(c.w)
        else:
           alert = {'type':'error'}
           alert['title'] = werrMsg
           session['alert'] = alert
           session.save()

        return redirect('/workshop/%s/%s/configure'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configureMultipleWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"
        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""
        else:
            return(redirect("/"))

        slideshow = getSlideshow(c.w['mainSlideshow_id'])
        c.slideshow = getAllSlides(slideshow.id)

        werror = 0
        werrMsg = 'Missing Info: '
        wstarted = 0
        if c.w['startTime'] != '0000-00-00':
           wstarted = 1

        ##log.info('wstarted is %s' % wstarted)

        # Is there anything more painful than form validation?
        # I don't think so...

        if 'publicPostalList' in request.params:
           pString = request.params['publicPostalList']
           log.info('publicPostalList is %s' % pString)
           pString = pString.lstrip()
           pString = pString.rstrip()
           pString = pString.replace(' ', ',')
           pString = pString.replace(',,', ',')
           pString = pString.replace('    ', ',')
           pList = pString.split(',')
           pBad = []
           pGood = []
           for pCode in pList:
              pTest = getGeoTitles(pCode, 'united-states')
              log.info('pCode is %s pString is %s pTest is %s'%(pCode,pString, pTest))
              if pTest != '0':
                  log.info('adding pGood %s'%pCode)
                  pGood.append(pCode)
              else:
                  log.info('adding pBad %s'%pCode)
                  pBad.append(pCode)
        if pBad:
            werrMsg = ','.join(pBad)
            ##werror = 1

        if pGood:
            c.w['publicPostalList'] = ','.join(pGood)
            log.info('publicPostalList is %s'%c.w['publicPostalList'])

        if pList != '' and pGood:
            c.w['scopeMethod'] = 'publicPostalList'
            c.w['publicScope'] = '00'

        else:
          werror = 1
          werrMsg += 'Public Postal List '
           
        if c.w['scopeMethod'] == 'publicPostalList':
          c.w['publicScopeTitle'] = 'postal codes of ' + c.w['publicPostalList']
          c.w['publicScope'] = ''

        if werror == 1:
            alert = {'type':'error'}
            alert['title'] = werrMsg
            session['alert'] = alert
            session.save()
            return redirect('/workshop/%s/%s/configure'%(c.w['urlCode'], c.w['url']))  #c.form_result[''], c.form_result[''],)

        if isFacilitator(c.authuser.id, c.w.id) and werror == 0:
            Event('Workshop Config Updated by %s'%c.authuser['name'], 'Public Sphere postal code list updated.', c.w, c.authuser)
            commit(c.w)
            alert = {'type':'success'}
            alert['title'] = 'Workshop Multiple Postal Codes Saved!'
            session['alert'] = alert
            session.save()
        else:
            alert = {'type':'error'}
            alert['title'] = werrMsg
            session['alert'] = alert
            session.save()

        return redirect('/workshop/%s/%s/configure'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configureStartWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"
        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""
        else:
            return(redirect("/"))



        slideshow = getSlideshow(c.w['mainSlideshow_id'])
        c.slideshow = getAllSlides(slideshow.id)

        werror = 0
        wstarted = 0
        if c.w['startTime'] != '0000-00-00':
           wstarted = 1

        ##log.info('wstarted is %s' % wstarted)

        # Is there anything more painful than form validation?
        # I don't think so...
        if not isFacilitator(c.authuser.id, c.w.id) and not isAdmin(c.authuser.id):
            alert = {'type':'error'}
            alert['title'] = 'You are not authorized'
            session['alert'] = alert
            session.save()
            return redirect('/workshop/%s/%s'%(c.w['urlCode'], c.w['url']))

        if 'startWorkshop' in request.params:
            startButtons = request.params.getall('startWorkshop')
            if 'Start' in startButtons and 'VerifyStart' in startButtons:
                # Make sure we have all the information we need
                werror == 0
                werrMsg = ''
                goalsDefault = 'No goals set'
                if c.w['title'] == '':
                    werrMsg = werrMsg + 'No name set. '
                    werror = 1

                if c.w['goals'] == '' or c.w['goals'] == goalsDefault:
                    werrMsg = werrMsg + 'No goals set. '
                    werror = 1

                if c.w['publicTags'] == 'none':
                    werrMsg = werrMsg + 'No workshop tags set. '
                    werror = 1

                if c.w['memberTags'] == 'none' or c.w['memberTags'] == '':
                    werrMsg = werrMsg + 'No additional tags set. '
                    werror = 1

                # if we have everything...
                if werror == 1:
                    alert = {'type':'error'}
                    alert['title'] = werrMsg
                    session['alert'] = alert
                    session.save()
                    return redirect('/workshop/%s/%s/configure'%(c.w['urlCode'], c.w['url']))

                # Set workshop start and end time
                startTime = datetime.datetime.now(None)
                c.w['startTime'] = startTime
                endTime = datetime.datetime.now(None)
                endTime = endTime.replace(year = endTime.year + 1)
                c.w['endTime'] = endTime
                Event('Workshop Config Updated by %s'%c.authuser['name'], 'Workshop started!', c.w, c.authuser)
                commit(c.w)

                # Make the Tag objects
                for pTag in c.w['publicTags'].split(','):
                   pTag = pTag.lstrip()
                   pTag = pTag.rstrip()
                   Tag('system', pTag, c.w.id, c.w.owner)
                for mTag in c.w['memberTags'].split(','):
                   mTag = mTag.lstrip()
                   mTag = mTag.rstrip()
                   Tag('member', mTag, c.w.id, c.w.owner)

                # Set the geo scope objects
                if c.w['scopeMethod'] == 'publicPostalList':
                    pString = c.w['publicPostalList']
                    pList = pString.split(',')
                    for p in pList:
                       if p != '':
                          WorkshopScope(p, 'United States', c.w.id, c.w.owner)
                elif c.w['scopeMethod'] == 'publicScope':
                    p = c.w['publicPostal']
                    WorkshopScope(p, 'United States', c.w.id, c.w.owner)

                alert = {'type':'success'}
                alert['title'] = 'Workshop Started!'
                session['alert'] = alert
                session.save()
            else:
                alert = {'type':'error'}
                alert['title'] = werrMsg
                session['alert'] = alert
                session.save()

        return redirect('/workshop/%s/%s/configure'%(c.w['urlCode'], c.w['url']))

    @h.login_required
    def addWorkshopHandler(self):

        if 'user' in session and c.authuser:
            c.account = getUserAccount(c.authuser.id)
            if not c.account or c.account['numRemaining'] < 1:
                return(redirect("/"))
        else:          
            return(redirect("/"))

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
        titles = getGeoTitles(c.postal, 'united-states')
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
            
        #c.resources = getActiveResourcesByWorkshopID(c.w.id)
        c.resources = getActiveResourcesByWorkshopCode(c.w['urlCode'])
        c.resources = sortBinaryByTopPop(c.resources)
        #c.dresources = getInactiveResourcesByWorkshopID(c.w.id)
        c.dresources = getInactiveResourcesByWorkshopCode(c.w.id)
        # put disabled and deleted at the end
        if c.resources:
            if c.dresources:
                c.resources += c.dresources 
        else:
            if c.dresources:
                c.resources = c.dresources 

        c.suggestions = getActiveSuggestionsForWorkshop(code)
        c.suggestions = sortContByAvgTop(c.suggestions, 'overall')
        c.dsuggestions = getInactiveSuggestionsForWorkshop(code, urlify(url))
        # put disabled and deleted at the end
        if c.suggestions:
            if c.dsuggestions:
                c.suggestions += c.dsuggestions
        else:
            if c.dsuggestions:
                c.suggestions = c.dsuggestions

        c.asuggestions = getAdoptedSuggestionsForWorkshop(code, urlify(url))
        
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
                item['suggestionSummary'] = h.literal(h.reST2HTML(item['data']))
                ##item['suggestionSummary'] = h.literal(h.reST2HTML(item['data'][:250] + '...'))
        
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

        #return render('/derived/workshop_home.bootstrap')
        
        c.information = get_revision(int(c.w['mainRevision_id']))
        
        return render('/derived/6_workshop_home.bootstrap')

    def displayAllSuggestions(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        c.title = c.w['title']
        c.suggestions = getActiveSuggestionsForWorkshop(code, urlify(url))
        c.suggestions = sortContByAvgTop(c.suggestions, 'overall')
        c.dsuggestions = getInactiveSuggestionsForWorkshop(code, urlify(url))
        # put disabled and deleted at the end
        if c.suggestions:
            if c.dsuggestions:
                c.suggestions += c.dsuggestions
        else:
            if c.dsuggestions:
                c.suggestions = c.dsuggestions

        c.isScoped = False
        if 'user' in session:
            c.isScoped = isScoped(c.authuser, c.w)
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
                item['suggestionSummary'] = h.literal(h.reST2HTML(item['data']))
                ##item['suggestionSummary'] = h.literal(h.reST2HTML(item['data'][:250] + '...'))
        
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

        c.count = len(c.suggestions)
        c.paginator = paginate.Page(
            c.suggestions, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )


        return render('/derived/workshop_suggestions.bootstrap')

    def displayAllResources(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        c.title = c.w['title']
        c.resources = getActiveResourcesByWorkshopCode(code)
        c.resources = sortBinaryByTopPop(c.resources)
        c.dresources = getInactiveResourcesByWorkshopCode(code)
        # put disabled and deleted at the end
        if c.resources:
            if c.dresources:
                c.resources += c.dresources
        else:
            if c.dresources:
                c.resources = c.dresources

        c.count = len(c.resources)
        c.paginator = paginate.Page(
            c.resources, page=int(request.params.get('page', 1)),
            items_per_page = 15, item_count = c.count
        )
        c.listingType = 'resources'
        if 'user' in session:
           c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
           c.isScoped = isScoped(c.authuser, c.w)
           c.isAdmin = isAdmin(c.authuser.id)
        return render('/derived/6_detailed_listing.bootstrap')
        #return render('/derived/workshop_resources.bootstrap')

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
        c.resources = sortBinaryByTopPop(c.resources)
        # append the disabled and deleted resources
        resources = getInactiveResourcesByWorkshopID(c.w.id)
        if resources:
          c.resources += resources

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
            c.isScoped = isScoped(c.authuser, c.w)
            c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
            c.facilitators = getFacilitatorsByWorkshop(c.w.id)
            
            reST = r['data']
            reSTlist = self.get_reSTlist(reST)
            HTMLlist = self.get_HTMLlist(reST)
            
            c.wikilist = zip(HTMLlist, reSTlist)
            c.content = h.literal(h.reST2HTML(r['data']))
        else:
            c.content = h.literal(h.reST2HTML(r['data']))
        
        c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])
        
        c.lastmoddate = r.date
        c.lastmoduser = getUserByID(r.owner)
        
        return render('/derived/workshop_bg.bootstrap')

    @h.login_required
    def configure(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshop(code, urlify(url))
        if not isFacilitator(c.authuser.id, c.w.id) and not(isAdmin(c.authuser.id)):
            h.flash("You are not authorized", "warning")
            return render('/')

        slideshow = getSlideshow(c.w['mainSlideshow_id'])
        c.slideshow = getAllSlides(slideshow.id)
        c.published_slides = []
        slide_ids = [int(item) for item in slideshow['slideshow_order'].split(
',')]
        for id in slide_ids:
            s = getSlide(id) # Don't grab deleted slides
            if s:
                c.published_slides.append(s)

        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.facilitators = getFacilitatorsByWorkshop(c.w.id)
        r = get_revision(int(c.w['mainRevision_id']))
        reST = r['data']
        reSTlist = self.get_reSTlist(reST)
        HTMLlist = self.get_HTMLlist(reST)

        c.wikilist = zip(HTMLlist, reSTlist)
        c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])

        c.lastmoddate = r.date
        c.lastmoduser = getUserByID(r.owner)


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
        c.d = getActiveDiscussionsForWorkshop(c.w['urlCode'], urlify(c.w['url']))
        c.disabledDisc = getDisabledDiscussionsForWorkshop(c.w['urlCode'], urlify(c.w['url']))
        c.deletedDisc = getDeletedDiscussionsForWorkshop(c.w['urlCode'], urlify(c.w['url']))
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
