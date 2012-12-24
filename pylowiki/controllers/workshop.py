import logging, re, pickle, formencode
import time, datetime
import os
import re

from formencode import validators, htmlfill
from formencode.compound import All
from formencode.foreach import ForEach
from ordereddict import OrderedDict
import webhelpers.paginate as paginate

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.db.workshop import Workshop, getWorkshop, getWorkshopByCode, isScoped, sendPMemberInvite, isGuest
from pylowiki.lib.db.geoInfo import getScopeTitle, WorkshopScope, getGeoScope, getGeoTitles, getStateList, getCountyList, getCityList
from pylowiki.lib.db.revision import get_revision
from pylowiki.lib.db.slideshow import getSlideshow, getAllSlides
from pylowiki.lib.db.slide import getSlide
from pylowiki.lib.db.discussion import getDiscussionByID, getActiveDiscussionsForWorkshop, getDisabledDiscussionsForWorkshop, getDeletedDiscussionsForWorkshop
from pylowiki.lib.db.resource import getResourcesByWorkshopID, getActiveResourcesByWorkshopID, getInactiveResourcesByWorkshopID, getDisabledResourcesByWorkshopID, getDeletedResourcesByWorkshopID
from pylowiki.lib.db.suggestion import getSuggestionsForWorkshop, getAdoptedSuggestionsForWorkshop, getActiveSuggestionsForWorkshop, getInactiveSuggestionsForWorkshop, getDisabledSuggestionsForWorkshop, getDeletedSuggestionsForWorkshop
from pylowiki.lib.db.user import getUserByID, isAdmin
from pylowiki.lib.db.facilitator import isFacilitator, getFacilitatorsByWorkshop
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.db.tag import Tag, setWorkshopTagEnable
from pylowiki.lib.db.motd import MOTD, getMessage
from pylowiki.lib.db.pmember import PMember, getPrivateMembers, getPrivateMember, getPrivateMemberByCode
from pylowiki.lib.db.follow import Follow, getFollow, isFollowing, getWorkshopFollowers
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

class editWorkshopForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    title = validators.String(strip=True, not_empty=True, messages = {'empty' : 'Please provide a name for your workshop.'})
    goals = NoGoalsSet()
    memberTags = CommaSepList(cannot_be_empty=True)

class addWorkshopForm(formencode.Schema):
    maxTitle = 70
    allow_extra_fields = True
    filter_extra_fields = True
    workshopName = validators.String(strip=True, not_empty=True, max=maxTitle, messages = {'empty' : 'Please give your workshop a name.'})

class WorkshopController(BaseController):

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
        
    def guest(self, id1, id2):
        guestCode = id1
        workshopCode = id2
        pMember = getPrivateMemberByCode(guestCode)
        workshop = getWorkshopByCode(workshopCode)
        session['guestCode'] = guestCode
        session['workshopCode'] = workshopCode
        session.save()

        return redirect('/workshop/%s/%s'%(workshop['urlCode'], workshop['url'])) 
        

    @h.login_required
    def configureBasicWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"
        session['confTab'] = "tab1"
        session.save()

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
                oldTitle = c.w['url']
                c.w['url'] = urlify(wTitle)
                wchanges = 1
                weventMsg += "Updated name. "
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
               weventMsg += "Updated goals. "
        else:
           werror = 1
           werrMsg += 'Goals '
            
        ##log.info('Got wGoals %s' % wGoals)
        if 'allowSuggestions' in request.params:
           allowSuggestions = request.params['allowSuggestions']
           if (allowSuggestions == '1' or allowSuggestions == '0') and allowSuggestions != c.w['allowSuggestions']:
              wchanges = 1
              weventMsg += "Changed allowSuggestions from " + c.w['allowSuggestions'] + " to " + allowSuggestions + "."
              c.w['allowSuggestions'] = allowSuggestions
        else:
           werror = 1
           werrMsg += 'Allow Suggestions '

        if 'allowResources' in request.params:
           allowResources = request.params['allowResources']
           if (allowResources == '1' or allowResources == '0') and allowResources != c.w['allowResources']:
              wchanges = 1
              weventMsg += "Changed allowResources from " + c.w['allowResources'] + " to " + allowResources + "."
              c.w['allowResources'] = allowResources
        else:
           werror = 1
           werrMsg += 'Allow Resources '

        if not wstarted:
            if 'publicPrivate' in request.params:
                publicPrivate = request.params['publicPrivate']
                if (publicPrivate == 'public' or publicPrivate == 'private') and publicPrivate != c.w['public_private']:
                    wchanges = 1
                    weventMsg = weventMsg + "Changed workshop type from " + c.w['public_private'] + " to " + publicPrivate + "."
                    c.w['public_private'] = publicPrivate
                
        # save successful changes
        if wchanges and (isFacilitator(c.authuser.id, c.w.id) or isAdmin(c.authuser.id)):
            commit(c.w)
            Event('Workshop Updated by %s'%c.authuser['name'], '%s'%weventMsg, c.w, c.authuser)
        else:
            werror = 1
            werrMsg = "No changes submitted."

        if werror:
            alert = {'type':'error'}
            alert['title'] = werrMsg
            session['alert'] = alert
            session.save()
        else:
            if isFacilitator(c.authuser.id, c.w.id):
                commit(c.w)
                alert = {'type':'success'}
                alert['title'] = weventMsg
                session['alert'] = alert
                # to reload at the next tab
                if c.w['startTime'] == '0000-00-00':
                    session['confTab'] = "tab2"
                session.save()

        return redirect('/workshop/%s/%s/dashboard'%(c.w['urlCode'], c.w['url'])) 
        
    @h.login_required
    def configureTagsWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"
        session['confTab'] = "tab3"
        session.save()

        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""        
        else:
            return(redirect("/"))
            
        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = 'Missing Info: '
        wstarted = 0
        if c.w['startTime'] != '0000-00-00':
           wstarted = 1
            
        if 'categoryTags' in request.params:
            categoryTags = request.params.getall('categoryTags')
            cTags = '|'.join(categoryTags)
            if cTags and cTags != c.w['categoryTags']:
                wchanges = 1
                weventMsg = weventMsg + "Updated category tags."
                c.w['categoryTags'] = cTags
        else:
            werror = 1
            werrMsg += 'Category Tags '
   
        # save successful changes
        if wchanges and (isFacilitator(c.authuser.id, c.w.id) or isAdmin(c.authuser.id)):
            commit(c.w)
            Event('Workshop Config Updated by %s'%c.authuser['name'], '%s'%weventMsg, c.w, c.authuser)
        else:
            werror = 1
            werrMsg = "No changes submitted."

        if werror:
            alert = {'type':'error'}
            alert['title'] = werrMsg
            session['alert'] = alert
            session.save()
        else:
            if isFacilitator(c.authuser.id, c.w.id):
                commit(c.w)
            alert = {'type':'success'}
            alert['title'] = weventMsg
            session['alert'] = alert
            if c.w['startTime'] == '0000-00-00':
                session['confTab'] = "tab4"
            session.save()

        return redirect('/workshop/%s/%s/dashboard'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configurePublicWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"
        session['confTab'] = "tab2"
        session.save()
        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""
        else:
            return(redirect("/"))
        
        if c.w['type'] == 'personal':
            alert = {'type':'error'}
            alert['title'] = 'Personal workshops are limited to being private invitation only with a maximum of 10 participants.'
            session['alert'] = alert
            session.save()
            return redirect('/workshop/%s/%s/dashboard'%(c.w['urlCode'], c.w['url']))
            
        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = ''
        
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
            
        # assemble a workshop scope string 
        # ||country||state||county||city|zip
        geoTagString = "||" + geoTagCountry + "||" + geoTagState + "||" + geoTagCounty + "||" + geoTagCity + "|0"
        if geoTagString != c.w['geoTags']:
            c.w['geoTags'] = geoTagString
            c.w['public_private'] = 'public'
            commit(c.w)
            wchanges = 1
            weventMsg = weventMsg + "Updated workshop scope."
            Event('Workshop Config Updated by %s'%c.authuser['name'], '%s'%weventMsg, c.w, c.authuser)
            alert = {'type':'success'}
            alert['title'] = weventMsg
            session['alert'] = alert
            session.save()
        else:
            alert = {'type':'error'}
            alert['title'] = 'No changes submitted.'
            session['alert'] = alert
            session.save()
            
        if c.w['startTime'] == '0000-00-00':
            session['confTab'] = "tab3"
            session.save()
            
        return redirect('/workshop/%s/%s/dashboard'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configurePrivateWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"
        session['confTab'] = "tab2"
        session.save()
        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""
        else:
            return(redirect("/"))
            
        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = ''
        
        if 'addMember' in request.params:
            pList = getPrivateMembers(code, "0")
            if 'newMember' in request.params and request.params['newMember'] != '':
                if c.w['type'] == 'personal' and len(pList) >= 10:
                    werror = 1
                    werrMsg += 'You have already reached the maximum number of 10 participants for a personal workshop.'
                else:
                    newMember = request.params['newMember']
                    counter = 0
                    mList = newMember.split('\n')
                    if c.w['type'] == 'personal' and (len(pList) + len(mList) > 10):
                        werror = 1
                        werrMsg += 'There are already ' + str(len(pList)) + ' participants. You cannot add ' + str(len(mList)) + ' more, personal workshops are limited to a maximum of 10 participants.'
                    else:
                        for mEmail in mList:
                            mEmail = mEmail.strip()
                            # make sure a valid email address
                            if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", mEmail):
                                werror = 1
                                werrMsg = werrMsg + 'Not valid email address: ' + mEmail
                            else:
                                pTest = getPrivateMember(code, mEmail)
                                if pTest:
                                    if pTest['deleted'] == '1':
                                        pTest['deleted'] = '0'
                                        commit(pTest)
                                    else:
                                        werror = 1
                                        werrMsg += mEmail + ' already a member.'
                                else:
                                    PMember(code, mEmail, 'A', c.w)
                                    if 'sendInvite' in request.params:
                                        inviteMsg = ''
                                        if 'inviteMsg' in request.params:
                                            inviteMsg = request.params['inviteMsg']
                                        sendPMemberInvite(c.w, c.authuser, mEmail, inviteMsg)
                                    counter += 1
                
                    if counter:
                        if counter > 1:
                            weventMsg += str(counter) + ' new members added.'
                        else:
                            weventMsg += '1 new member added.'
                            if 'inviteMsg' in request.params:
                                weventMsg += ' An email invitation has been sent.'
                
            else:
                werror = 1
                werrMsg += 'No email address entered.'

                
        if 'deleteMember' in request.params:
            if 'removeMember' in request.params and request.params['removeMember'] != '':
                removeMember = request.params['removeMember']
                pTest = getPrivateMember(code, removeMember)
                if pTest:
                    pTest['deleted'] = '1'
                    commit(pTest)
                    weventMsg += 'Member removed: ' +  removeMember
                else:
                    werror = 1
                    werrMsg += 'No current member email: ' +  removeMember
                
            else:
                werror = 1
                werrMsg += 'No email address entered.'
    
        if 'continueToNext' in request.params:
            session['confTab'] = "tab3"
            session.save()
        else:
            if werror:
                alert = {'type':'error'}
                alert['title'] = werrMsg
                session['alert'] = alert
                session.save()
            else:
                alert = {'type':'success'}
                alert['title'] = weventMsg
                session['alert'] = alert
                session.save()
            
        return redirect('/workshop/%s/%s/dashboard'%(c.w['urlCode'], c.w['url']))
        
    @h.login_required
    def listPrivateMembersHandler(self, id1, id2):
        code = id1
        url = id2
        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""
        else:
            return(redirect("/"))
            
        c.privateMembers = getPrivateMembers(c.w['urlCode'])
        return render('/derived/list_pmembers.bootstrap')

    @h.login_required
    def previewInvitation(self, id1, id2):
        code = id1
        url = id2
        c.title = "Private Workshop"
        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""
        else:
            return(redirect("/"))
        c.facilitator = c.authuser['name']
        c.workshopName = c.w['title']
        c.inviteMsg = 'Your Invitation Message Will Appear Here'
        c.imageSrc = "/images/logo_header8.1.png"
        
        return render('/derived/preview_invitation.bootstrap')

        
    @h.login_required
    def configureScopeWorkshopHandler(self, id1, id2):
        code = id1
        url = id2
        c.title = "Configure Workshop"
        c.w = getWorkshop(code, urlify(url))
        if 'user' in session and c.authuser and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
            ""
        else:
            return(redirect("/"))

        c.title = "Configure Workshop"
        session['confTab'] = "tab2"
        session.save()
        
        if c.w['public_private'] == 'public' and 'changeScopeToPrivate' in request.params:
            c.w['public_private'] = 'private'
            Event('Workshop Config Updated by %s'%c.authuser['name'], 'Scope changed from public to private', c.w, c.authuser)
            commit(c.w)
            alert = {'type':'success'}
            alert['title'] = 'Workshop scope changed from public to private'
            session['alert'] = alert
            session.save()

        if c.w['public_private'] == 'private' and 'changeScopeToPublic' in request.params:
            c.w['public_private'] = 'public'
            Event('Workshop Config Updated by %s'%c.authuser['name'], 'Scope changed from private to public', c.w, c.authuser)
            commit(c.w)
            alert = {'type':'success'}
            alert['title'] = 'Workshop scope changed from private to public'
            session['alert'] = alert
            session.save()   
            
        return redirect('/workshop/%s/%s/dashboard'%(c.w['urlCode'], c.w['url']))

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
            # Set workshop start and end time
            startTime = datetime.datetime.now(None)
            c.w['startTime'] = startTime
            endTime = datetime.datetime.now(None)
            endTime = endTime.replace(year = endTime.year + 1)
            c.w['endTime'] = endTime
            Event('Workshop Config Updated by %s'%c.authuser['name'], 'Workshop started!', c.w, c.authuser)
            commit(c.w)

            alert = {'type':'success'}
            alert['title'] = 'Workshop Started!'
            alert['content'] = ' You may return to the Dashboard by clicking on the Dashboard link on any page in the workshop. Have fun!'
            session['alert'] = alert
            session.save()
            
        return redirect('/workshop/%s/%s'%(c.w['urlCode'], c.w['url']))

    @h.login_required
    def createWorkshopHandler(self):
        if 'user' in session and c.authuser:
            return render('/derived/workshop_create.bootstrap')
            
        return render('/derived/404.bootstrap')
        
    def paymentHandler(self):
        if 'user' in session and c.authuser:
            return render('/derived/workshop_payment.bootstrap')
            
        return render('/derived/404.bootstrap')
        
    def upgradeHandler(self, id1):
        code = id1
        c.w = getWorkshopByCode(code)
        if 'user' in session and c.authuser:
            if 'upgradeToken' in request.params:
                    if 'workshopCode' in request.params:
                        workshopCode = request.params['workshopCode']
                        workshop = getWorkshopByCode(workshopCode)
                        workshop['type'] = 'professional'
                        commit(workshop)
                        alert = {'type':'success'}
                        alert['title'] = 'Your workshop has been upgraded from personal to professional. Have fun!'
                        session['alert'] = alert
                        session.save()
                        return redirect('/workshop/%s/%s/dashboard'%(c.w['urlCode'], c.w['url']))
            else:
                return render('/derived/workshop_payment.bootstrap')
            
        return render('/derived/404.bootstrap')
        
    @h.login_required
    def newWorkshopHandler(self):
        
        if 'user' in session and c.authuser:
            if 'createPersonal' in request.params:
                wType = 'personal'
            else:

                if 'paymentToken' in request.params:
                    wType = 'professional'
                else:
                    return redirect('/workshopPayment')
                    
           
            w = Workshop('replace with a real name!', c.authuser, 'private', wType)
            c.workshop_id = w.w.id # TEST
            c.title = 'Configure Workshop'
            c.motd = MOTD('Welcome to the workshop!', w.w.id, w.w.id)
            alert = {'type':'success'}
            alert['title'] = 'Your new ' + wType + ' workshop is ready to be set up. Have fun!'
            session['alert'] = alert
            session.save()

            return redirect('/workshop/%s/%s/dashboard'%(w.w['urlCode'], w.w['url']))   
            
        else:
            alert = {'type':'error'}
            alert['title'] = 'You are not authorized'
            session['alert'] = alert
            session.save()
            return redirect('/')    

    
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
              eAction = 'published'
              ##log.info('doing undelete')
           else:
              w['deleted'] = '1'
              eAction = 'unpublished'
              ##log.info('doing delete')

           setWorkshopTagEnable(w, w['deleted'])
           eMsg = 'Workshop ' + eAction
           Event('Workshop %s'%eAction, 'Workshop %s by %s Note: %s'%(eAction, c.authuser['name'], eventReason), w, c.authuser)
           commit(w)
           
        if werror:
            alert = {'type':'error'}
            alert['title'] = werrMsg
            session['alert'] = alert
            session.save()
        else:
            alert = {'type':'success'}
            alert['title'] = eMsg
            session['alert'] = alert
            session.save()
            

            
        commit(m)
        return redirect('/workshop/%s/%s/dashboard'%(w['urlCode'], w['url']))
    
    def display(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, urlify(url))
        c.title = c.w['title']
        c.isGuest = isGuest(c.w)
        
        if 'user' in session:
            if not c.isGuest and c.authuser:
                c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
                c.isScoped = isScoped(c.authuser, c.w)
                c.isFollowing = isFollowing(c.authuser.id, c.w.id)
                c.isAdmin = isAdmin(c.authuser.id)
            
        if c.w['type'] == 'personal' or c.w['public_private'] == 'private':
            if 'user' in session or c.isGuest:
                if not c.isFacilitator and not c.isScoped and not c.isAdmin and not c.isGuest:
                    return render('/derived/404.bootstrap')            
            else:
                return render('/derived/404.bootstrap')
        
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
        c.resources = sortBinaryByTopPop(c.resources)
        c.dresources = getInactiveResourcesByWorkshopID(c.w.id)
        # put disabled and deleted at the end
        if c.resources:
            if c.dresources:
                c.resources += c.dresources 
        else:
            if c.dresources:
                c.resources = c.dresources 

        c.suggestions = getActiveSuggestionsForWorkshop(code)
        c.suggestions = sortContByAvgTop(c.suggestions, 'overall')
        c.dsuggestions = getInactiveSuggestionsForWorkshop(code)
        # put disabled and deleted at the end
        if c.suggestions:
            if c.dsuggestions:
                c.suggestions += c.dsuggestions
        else:
            if c.dsuggestions:
                c.suggestions = c.dsuggestions

        c.asuggestions = getAdoptedSuggestionsForWorkshop(code)
        
        if 'user' in session and not c.isGuest:
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
        
            if 'user' in session and not c.isGuest:    
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

    def displayAllSuggestions(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        c.title = c.w['title']
        c.suggestions = getActiveSuggestionsForWorkshop(code)
        c.suggestions = sortContByAvgTop(c.suggestions, 'overall')
        c.dsuggestions = getInactiveSuggestionsForWorkshop(code)
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
        c.resources = getActiveResourcesByWorkshopID(c.w.id)
        c.resources = sortBinaryByTopPop(c.resources)
        c.dresources = getInactiveResourcesByWorkshopID(c.w.id)
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

        return render('/derived/workshop_resources.bootstrap')

    def inactiveSuggestions(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        c.title = c.w['title']
        c.suggestions = getActiveSuggestionsForWorkshop(code)
        c.dsuggestions = getInactiveSuggestionsForWorkshop(code)

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
    def dashboard(self, id1, id2):
        code = id1
        url = id2

        c.w = getWorkshopByCode(code)
        if (c.w['goals'] != '' and c.w['goals'] != 'No goals set'):
            c.basicConfig = 1
        else:
            c.basicConfig = 0
            
        if c.w['categoryTags'] != '':
            c.tagConfig = 1
        else:
            c.tagConfig = 0
            
        if 'confTab' in session:
            c.tab = session['confTab']
            session.pop('confTab')
            session.save()
        # hack for continue button in tab4 of configure
        if 'continueToNext' in request.params:
            c.tab = 'tab5'
        
        if not isFacilitator(c.authuser.id, c.w.id) and not(isAdmin(c.authuser.id)):
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
        if len(c.slideshow) > 1 and len(c.published_slides) > 0:
            c.slideConfig = 1
        else:
            c.slideConfig = 0
            
        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
        c.facilitators = getFacilitatorsByWorkshop(c.w.id)

        if c.w['public_private'] != 'public':
            c.pmembers = getPrivateMembers(code)
            
        c.revision = get_revision(int(c.w['mainRevision_id']))
        reST = c.revision['data']
        reSTlist = self.get_reSTlist(reST)
        HTMLlist = self.get_HTMLlist(reST)
        if c.revision['data'] != "No wiki background set yet":
            c.backConfig = 1
        else:
            c.backConfig = 0

        c.wikilist = zip(HTMLlist, reSTlist)
        c.discussion = getDiscussionByID(c.w['backgroundDiscussion_id'])

        c.lastmoddate = c.revision.date
        c.lastmoduser = getUserByID(c.revision.owner)
        
        c.states = getStateList('United-States')
        # ||country||state||county||city|zip
        if c.w['geoTags'] and c.w['geoTags'] != '':
            geoTags = c.w['geoTags'].split('|')
            c.country = geoTags[2]
            c.state = geoTags[4]
            c.county = geoTags[6]
            c.city = geoTags[8]
        else:
            c.country = "0"
            c.state = "0"
            c.county = "0"
            c.city = "0"
            
        c.motd = getMessage(c.w.id)
        if c.w['startTime'] != '0000-00-00':

            c.s = getActiveSuggestionsForWorkshop(code)
            c.disabledSug = getDisabledSuggestionsForWorkshop(code)
            c.deletedSug = getDeletedSuggestionsForWorkshop(code)
            c.r = getActiveResourcesByWorkshopID(c.w.id)
            c.disabledRes = getDisabledResourcesByWorkshopID(c.w.id)
            c.deletedRes = getDeletedResourcesByWorkshopID(c.w.id)
            c.d = getActiveDiscussionsForWorkshop(c.w['urlCode'])
            c.disabledDisc = getDisabledDiscussionsForWorkshop(c.w['urlCode'])
            c.deletedDisc = getDeletedDiscussionsForWorkshop(c.w['urlCode'])
            c.f = getFacilitatorsByWorkshop(c.w.id)
            c.df = getFacilitatorsByWorkshop(c.w.id, 1)
            
        return render('/derived/6_workshop_dashboard.bootstrap')
    
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

        c.s = getActiveSuggestionsForWorkshop(code)
        c.disabledSug = getDisabledSuggestionsForWorkshop(code)
        c.deletedSug = getDeletedSuggestionsForWorkshop(code)
        c.r = getActiveResourcesByWorkshopID(c.w.id)
        c.disabledRes = getDisabledResourcesByWorkshopID(c.w.id)
        c.deletedRes = getDeletedResourcesByWorkshopID(c.w.id)
        c.d = getActiveDiscussionsForWorkshop(c.w['urlCode'])
        c.disabledDisc = getDisabledDiscussionsForWorkshop(c.w['urlCode'])
        c.deletedDisc = getDeletedDiscussionsForWorkshop(c.w['urlCode'])
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
