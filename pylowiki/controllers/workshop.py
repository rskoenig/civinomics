import logging, re, pickle, formencode
import datetime
import re
import stripe

from formencode import validators, htmlfill
from formencode.compound import All
from formencode.foreach import ForEach
from ordereddict import OrderedDict
import webhelpers.paginate as paginate

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.revision     as revisionLib
import pylowiki.lib.db.slideshow    as slideshowLib
import pylowiki.lib.db.slide        as slideLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.idea         as ideaLib
import pylowiki.lib.db.resource     as resourceLib
import pylowiki.lib.db.comment      as commentLib
import pylowiki.lib.db.suggestion   as suggestionLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.rating       as ratingLib
import pylowiki.lib.db.tag          as tagLib
import pylowiki.lib.db.motd         as motdLib
import pylowiki.lib.db.pmember      as pMemberLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.activity     as activityLib
import pylowiki.lib.db.page         as pageLib
import pylowiki.lib.db.account      as accountLib
import pylowiki.lib.db.flag         as flagLib

import pylowiki.lib.db.dbHelpers as dbHelpers
import pylowiki.lib.utils as utils
import pylowiki.lib.sort as sort

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

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

    def __before__(self, action, workshopCode = None):
        setPrivs = ['configureBasicWorkshopHandler', 'configureTagsWorkshopHandler', 'configurePublicWorkshopHandler'\
        ,'configurePrivateWorkshopHandler', 'listPrivateMembersHandler', 'previewInvitation', 'configureScopeWorkshopHandler'\
        ,'configureStartWorkshopHandler', 'adminWorkshopHandler', 'display', 'displayAllResources', 'preferences']
        
        adminOrFacilitator = ['configureBasicWorkshopHandler', 'configureTagsWorkshopHandler', 'configurePublicWorkshopHandler'\
        ,'configurePrivateWorkshopHandler', 'listPrivateMembersHandler', 'previewInvitation', 'configureScopeWorkshopHandler'\
        ,'configureStartWorkshopHandler', 'adminWorkshopHandler', 'preferences']
        
        scoped = ['display', 'displayAllResources']
        dontGetWorkshop = ['displayCreateForm', 'displayPaymentForm', 'createWorkshopHandler']
        
        if action in dontGetWorkshop:
            return
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        if action in setPrivs:
            workshopLib.setWorkshopPrivs(c.w)
            if action in adminOrFacilitator:
                if not c.privs['admin'] and not c.privs['facilitator']:
                    return(redirect("/"))
            elif action in scoped:
                if c.w['type'] == 'personal' or c.w['public_private'] == 'private':
                    if not c.privs['guest'] and not c.privs['participant'] and not c.privs['facilitator'] and not c.privs['admin']:
                        abort(404)


    ###################################################
    # 
    # 
    # Updated functions, all are used
    # 
    # 
    ###################################################

    def guest(self, guestCode, workshopCode):
        pMember = pMemberLib.getPrivateMemberByCode(guestCode)
        session['guestCode'] = guestCode
        session['workshopCode'] = workshopCode
        session.save()
        return redirect('/workshop/%s/%s'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configureBasicWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"
        session['confTab'] = "tab1"
        session.save()

        slideshow = slideshowLib.getSlideshow(c.w['mainSlideshow_id'])
        c.slideshow = slideshowLib.getAllSlides(slideshow.id)

        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = 'Missing Info: '
        wstarted = 0
        if c.w['startTime'] != '0000-00-00':
           wstarted = 1

        if 'title' in request.params:
            wTitle = request.params['title']
            wTitle = wTitle.strip()
            if wTitle and wTitle != c.w['title']:
                c.w['title'] = wTitle
                oldTitle = c.w['url']
                c.w['url'] = utils.urlify(wTitle)
                wchanges = 1
                weventMsg += "Updated name. "
        else:
            werrMsg += 'Name '
            werror = 1

        if 'description' in request.params:
            wDescription = request.params['description']
            wDescription = wDescription.strip()
            if wDescription and wDescription != c.w['description']:
                c.w['description'] = wDescription
                wchanges = 1
                weventMsg += "Updated description. "
        else:
            werrMsg += 'Description '
            werror = 1

        if 'goals' in request.params:
           wGoals = str(request.params['goals'])
           wGoals = wGoals.strip()
           if wGoals and wGoals != c.w['goals']:
               c.w['goals'] = wGoals
               wchanges = 1
               weventMsg += "Updated goals. "
        else:
           werror = 1
           werrMsg += 'Goals '

        if 'allowIdeas' in request.params:
           allowIdeas = request.params['allowIdeas']
           if (allowIdeas == '1' or allowIdeas == '0') and allowIdeas != c.w['allowIdeas']:
              wchanges = 1
              weventMsg += "Changed allowIdeas from " + c.w['allowIdeas'] + " to " + allowIdeas + "."
              c.w['allowIdeas'] = allowIdeas
        else:
           werror = 1
           werrMsg += 'Allow Ideas '

        if 'allowResources' in request.params:
           allowResources = request.params['allowResources']
           if (allowResources == '1' or allowResources == '0') and allowResources != c.w['allowResources']:
              wchanges = 1
              weventMsg += "Changed allowResources from " + c.w['allowResources'] + " to " + allowResources + "."
              c.w['allowResources'] = allowResources
        else:
           werror = 1
           werrMsg += 'Allow Resources '
                
        # save successful changes
        if wchanges:
            dbHelpers.commit(c.w)
            eventLib.Event('Workshop Updated by %s'%c.authuser['name'], '%s'%weventMsg, c.w, c.authuser)
        else:
            werror = 1
            werrMsg = "No changes submitted."

        if werror:
            alert = {'type':'error'}
            alert['title'] = werrMsg
            session['alert'] = alert
            session.save()
        else:
            dbHelpers.commit(c.w)
            alert = {'type':'success'}
            alert['title'] = weventMsg
            session['alert'] = alert
            # to reload at the next tab
            if c.w['startTime'] == '0000-00-00':
                session['confTab'] = "tab2"
            session.save()

        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configureTagsWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"
        c.tags = tagLib.getWorkshopTags(c.w)
        currentTags = []
        if c.tags:
            for tag in c.tags:
                currentTags.append(tag['title'])
                
        session['confTab'] = "tab3"
        session.save()
            
        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = 'Missing Info: '
        wstarted = 0
        if c.w['startTime'] != '0000-00-00':
           wstarted = 1
            
        if 'categoryTags' in request.params:
            categoryTags = request.params.getall('categoryTags')
            new = 0
            orphaned = 0
            
            for tag in categoryTags:
                if tag not in currentTags:
                    tagLib.Tag(c.w, tag)
                    wchanges = 1
                    
            for tag in c.tags:
                if tag['title'] not in categoryTags:
                    tagLib.orphanTag(tag)
                    wchanges = 1
            
            
            if wchanges:
                weventMsg = weventMsg + "Updated category tags."
        else:
            werror = 1
            werrMsg += 'Category Tags '
   
        # save successful changes
        if wchanges:
            eventLib.Event('Workshop Config Updated by %s'%c.authuser['name'], '%s'%weventMsg, c.w, c.authuser)
        else:
            werror = 1
            werrMsg = "No changes submitted."

        if werror:
            alert = {'type':'error'}
            alert['title'] = werrMsg
            session['alert'] = alert
            session.save()
        else:
            dbHelpers.commit(c.w)
            alert = {'type':'success'}
            alert['title'] = weventMsg
            session['alert'] = alert
            if c.w['startTime'] == '0000-00-00':
                session['confTab'] = "tab4"
            session.save()

        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configurePublicWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"
        session['confTab'] = "tab2"
        session.save()
        
        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = ''
           
        if c.w['type'] == 'personal':
            alert = {'type':'error'}
            alert['title'] = 'Personal workshops are limited to being private invitation only with a maximum of 10 participants.'
            session['alert'] = alert
            session.save()
            return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url']))
            
        if c.w['public_private'] == 'private' and 'changeScope' in request.params:
            scopeTest = geoInfoLib.getWScopeByWorkshop(c.w)
            if not scopeTest:
                geoInfoLib.WorkshopScope(c.w, "||0|0|0|0|0|0|0|0")
            weventMsg = 'Workshop scope changed from private to public.'
            c.w['public_private'] = 'public'
            dbHelpers.commit(c.w)
            alert = {'type':'success'}
            alert['title'] = weventMsg
            session['alert'] = alert
            session.save()
            eventLib.Event('Workshop Config Updated by %s'%c.authuser['name'], '%s'%weventMsg, c.w, c.authuser)
            return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url']))
            
            

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
            
        # assemble a workshop scope string 
        # ||country||state||county||city|zip
        geoTagString = "||" + geoTagCountry + "||" + geoTagState + "||" + geoTagCounty + "||" + geoTagCity + "|" + geoTagPostal
        wscope = geoInfoLib.getWScopeByWorkshop(c.w)
        update = 0
        if not wscope:
            geoInfoLib.WorkshopScope(c.w, geoTagString)
            wchanges = 1
            
        if wscope and wscope['scope'] != geoTagString:
            geoInfoLib.editWorkshopScope(wscope, geoTagString)
            # wscope['scope'] = geoTagString
            # dbHelpers.commit(wscope)
            wchanges = 1
            
        if wchanges:
            c.w['public_private'] = 'public'
            dbHelpers.commit(c.w)
            weventMsg = weventMsg + "Updated workshop scope."
            eventLib.Event('Workshop Config Updated by %s'%c.authuser['name'], '%s'%weventMsg, c.w, c.authuser)
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
            
        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configurePrivateWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"
        session['confTab'] = "tab2"
        session.save()
            
        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = ''
        
        if 'addMember' in request.params:
            pList = pMemberLib.getPrivateMembers(workshopCode, "0")
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
                                pTest = pMemberLib.getPrivateMember(workshopCode, mEmail)
                                if pTest:
                                    if pTest['deleted'] == '1':
                                        pTest['deleted'] = '0'
                                        dbHelpers.commit(pTest)
                                    else:
                                        werror = 1
                                        werrMsg += mEmail + ' already a member.'
                                else:
                                    pMemberLib.PMember(workshopCode, mEmail, 'A', c.w)
                                    if 'sendInvite' in request.params:
                                        inviteMsg = ''
                                        if 'inviteMsg' in request.params:
                                            inviteMsg = request.params['inviteMsg']
                                        workshopLib.sendPMemberInvite(c.w, c.authuser, mEmail, inviteMsg)
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
                pTest = pMemberLib.getPrivateMember(workshopCode, removeMember)
                if pTest:
                    pTest['deleted'] = '1'
                    dbHelpers.commit(pTest)
                    weventMsg += 'Member removed: ' +  removeMember
                else:
                    werror = 1
                    werrMsg += 'No current member email: ' +  removeMember
                
            else:
                werror = 1
                werrMsg += 'No email address entered.'

        if c.w['public_private'] == 'public' and 'changeScope' in request.params:
            weventMsg = 'Workshop scope changed from public to private.'
            c.w['public_private'] = 'private'
            dbHelpers.commit(c.w)
            
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
                eventLib.Event('Workshop Config Updated by %s'%c.authuser['name'], '%s'%weventMsg, c.w, c.authuser)
                alert = {'type':'success'}
                alert['title'] = weventMsg
                session['alert'] = alert
                session.save()
            
        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url']))
        
    @h.login_required
    def listPrivateMembersHandler(self, workshopCode, workshopURL):
        c.privateMembers = pMemberLib.getPrivateMembers(c.w['urlCode'])
        return render('/derived/6_list_pmembers.bootstrap')

    @h.login_required
    def previewInvitation(self, workshopCode, workshopURL):
        c.title = "Private Workshop"

        c.facilitator = c.authuser['name']
        c.workshopName = c.w['title']
        c.inviteMsg = 'Your Invitation Message Will Appear Here'
        c.imageSrc = "/images/logo_header8.1.png"
        
        return render('/derived/6_preview_invitation.bootstrap')
        
    @h.login_required
    def configureScopeWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"

        c.title = "Configure Workshop"
        session['confTab'] = "tab2"
        session.save()
        
        if c.w['public_private'] == 'public' and 'changeScopeToPrivate' in request.params:
            c.w['public_private'] = 'private'
            eventLib.Event('Workshop Config Updated by %s'%c.authuser['name'], 'Scope changed from public to private', c.w, c.authuser)
            dbHelpers.commit(c.w)
            alert = {'type':'success'}
            alert['title'] = 'Workshop scope changed from public to private'
            session['alert'] = alert
            session.save()

        if c.w['public_private'] == 'private' and 'changeScopeToPublic' in request.params:
            c.w['public_private'] = 'public'
            eventLib.Event('Workshop Config Updated by %s'%c.authuser['name'], 'Scope changed from private to public', c.w, c.authuser)
            dbHelpers.commit(c.w)
            alert = {'type':'success'}
            alert['title'] = 'Workshop scope changed from private to public'
            session['alert'] = alert
            session.save()   
            
        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url']))

    @h.login_required
    def configureStartWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"

        werror = 0
        wstarted = 0
        if c.w['startTime'] != '0000-00-00':
           wstarted = 1

        if 'startWorkshop' in request.params:
            # Set workshop start and end time
            startTime = datetime.datetime.now(None)
            c.w['startTime'] = startTime
            endTime = datetime.datetime.now(None)
            endTime = endTime.replace(year = endTime.year + 1)
            c.w['endTime'] = endTime
            eventLib.Event('Workshop Config Updated by %s'%c.authuser['name'], 'Workshop started!', c.w, c.authuser)
            dbHelpers.commit(c.w)

            alert = {'type':'success'}
            alert['title'] = 'Workshop Started!'
            alert['content'] = ' You may return to Workshop Preferences by clicking on the cog icon on the workshop front page. Have fun!'
            session['alert'] = alert
            session.save()
            
        return redirect('/workshop/%s/%s'%(c.w['urlCode'], c.w['url']))

    @h.login_required
    def displayCreateForm(self):
        return render('/derived/6_workshop_create.bootstrap')
    
    @h.login_required
    def displayPaymentForm(self):
        c.stripeKey = config['app_conf']['stripePublicKey'].strip()
        return render('/derived/6_workshop_payment.bootstrap')
    
    @h.login_required
    def validatePaymentForm(self):
        
        pError = 0
        pErrorMsg = ''
        
        if 'name' in request.params and request.params['name'] != '':
            c.billingName = request.params['name']
        else:
            pError = 1
            pErrorMsg += 'Credit Card Name required. '
            
        if 'email' in request.params and request.params['email'] != '':
            c.billingEmail = request.params['email']
        else:
            pError = 1
            pErrorMsg += 'Billing email addresss required. '
            
        if 'stripeToken' in request.params and request.params['stripeToken'] != '':
            c.stripeToken = request.params['stripeToken']
        else:
            pError = 1
            pErrorMsg = 'Invalid credit card information.'

        c.coupon = ''
        if 'coupon' in request.params and request.params['coupon'] != '':
            if request.params['coupon'] == 'CIVCOMP1':
                c.coupon = request.params['coupon']
            
        if pError: 
            alert = {'type':'error'}
            alert['title'] = 'Error.' + pErrorMsg
            session['alert'] = alert
            session.save()
            
            return False
            
        return True

    @h.login_required
    def upgradeHandler(self, workshopCode):
        if self.validatePaymentForm():
                if 'workshopCode' in request.params:
                    workshopCode = request.params['workshopCode']
                    workshop = workshopLib.getWorkshopByCode(workshopCode)
                    workshop['type'] = 'professional'
                    dbHelpers.commit(workshop)
                    account = accountLib.Account(c.billingName, c.billingEmail, c.stripeToken, workshop, 'PRO', c.coupon)
                    alert = {'type':'success'}
                    alert['title'] = 'Your workshop has been upgraded from personal to professional. Have fun!'
                    session['alert'] = alert
                    session.save()
                    return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url']))
                else:
                    abort(404)
        else:
            c.stripeKey = config['app_conf']['stripePublicKey'].strip()
            return render('/derived/6_workshop_payment.bootstrap')
        
    @h.login_required
    def createWorkshopHandler(self):
        if 'createPersonal' in request.params:
            wType = 'personal'
        else:
            if self.validatePaymentForm():
                wType = 'professional'
            else:
                c.stripeKey = config['app_conf']['stripePublicKey'].strip()
                return render('/derived/6_workshop_payment.bootstrap')
                
        w = workshopLib.Workshop('replace with a real name!', c.authuser, 'private', wType)
        c.workshop_id = w.w.id # TEST
        c.title = 'Configure Workshop'
        c.motd = motdLib.MOTD('Welcome to the workshop!', w.w.id, w.w.id)
        if wType == 'professional':
            account = accountLib.Account(c.billingName, c.billingEmail, c.stripeToken, w.w, 'PRO', c.coupon)
        alert = {'type':'success'}
        alert['title'] = 'Your new ' + wType + ' workshop is ready to be set up. Have fun!'
        session['alert'] = alert
        session.save()

        return redirect('/workshop/%s/%s/preferences'%(w.w['urlCode'], w.w['url']))
    
    @h.login_required
    def adminWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Administrate Workshop"
        m = motdLib.getMessage(c.w.id)
        werror = 0
        werrMsg = 'Incomplete information: '

        if 'motd' in request.params:
           motd = request.params['motd']
           m['data'] = motd
           eAction = ' facilitator message updated.'
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

        if eW != veW:
           werror = 1
           if c.w['deleted'] == 1:
              eAction = 'enabled'
           else:
              eAction = 'disabled'
           werrMsg += 'Action must be verified before workshop can be ' + eAction + '.'
        elif eW == 1 and veW == 1:
           if c.w['deleted'] == '1':
              c.w['deleted'] = '0'
              eAction = 'published'
           else:
              c.w['deleted'] = '1'
              eAction = 'unpublished'

           eventLib.Event('Workshop %s'%eAction, 'Workshop %s by %s Note: %s'%(eAction, c.authuser['name'], eventReason), w, c.authuser)
           dbHelpers.commit(c.w)
           
        if werror:
            alert = {'type':'error'}
            alert['title'] = werrMsg
            session['alert'] = alert
            session.save()
        else:
            eMsg = 'Workshop ' + eAction
            alert = {'type':'success'}
            alert['title'] = eMsg
            session['alert'] = alert
            session.save()
            
        dbHelpers.commit(m)
        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url']))
    
    def display(self, workshopCode, workshopURL):
        c.title = c.w['title']

        c.isFollowing = False
        if 'user' in session:
            c.isFollowing = followLib.isFollowing(c.authuser, c.w)
        
        c.facilitators = []
        for f in (facilitatorLib.getFacilitatorsByWorkshop(c.w.id)):
           if 'pending' in f and f['pending'] == '0' and f['disabled'] == '0':
              c.facilitators.append(f)
              
        c.listeners = []
        for l in (listenerLib.getListenersForWorkshop(c.w)):
           if 'pending' in l and l['pending'] == '0' and l['disabled'] == '0':
              c.listeners.append(l)

        if c.w['startTime'] != '0000-00-00':
           c.wStarted = True
        else:
          c.wStarted = False

        c.slides = []
        c.slideshow = slideshowLib.getSlideshow(c.w['mainSlideshow_id'])
        slide_ids = [int(item) for item in c.slideshow['slideshow_order'].split(',')]
        for id in slide_ids:
            s = slideLib.getSlide(id) # Don't grab deleted slides
            if s:
                c.slides.append(s)

        c.motd = motdLib.getMessage(c.w.id)
        # kludge for now
        if c.motd == False:
           c.motd = motdLib.MOTD('Welcome to the workshop!', c.w.id, c.w.id)

        c.motd['messageSummary'] = h.literal(h.reST2HTML(c.motd['data']))
        c.information = pageLib.getInformation(c.w)
        c.activity = activityLib.getActivityForWorkshop(c.w['urlCode'])
        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)
        return render('/derived/6_workshop_home.bootstrap')
    
    @h.login_required
    def preferences(self, workshopCode, workshopURL):
        if (c.w['goals'] != '' and c.w['goals'] != 'No goals set'):
            c.basicConfig = 1
        else:
            c.basicConfig = 0
        
        c.tags = tagLib.getWorkshopTags(c.w)
        c.categories = []
        for tag in c.tags:
            c.categories.append(tag['title'])
        
        if c.categories:
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
            
        slideshow = slideshowLib.getSlideshow(c.w['mainSlideshow_id'])
        c.slideshow = slideshowLib.getAllSlides(slideshow.id)
        c.published_slides = []
        slide_ids = [int(item) for item in slideshow['slideshow_order'].split(',')]
        for id in slide_ids:
            s = slideLib.getSlide(id) # Don't grab deleted slides
            if s:
                c.published_slides.append(s)
        if len(c.slideshow) > 1 and len(c.published_slides) > 0:
            c.slideConfig = 1
        else:
            c.slideConfig = 0
            
        c.slides = c.published_slides
            
        c.facilitators = facilitatorLib.getFacilitatorsByWorkshop(c.w.id)
        c.listeners = listenerLib.getListenersForWorkshop(c.w, disabled = '0')
        c.disabledListeners = listenerLib.getListenersForWorkshop(c.w, disabled = '1')


        if c.w['public_private'] != 'public':
            c.pmembers = pMemberLib.getPrivateMembers(workshopCode)
            
        c.accounts = accountLib.getAccountsForWorkshop(c.w, deleted = '0')
        if c.accounts:
            c.accountInvoices = accountLib.getInvoicesForAccount(c.accounts[0])
        else:
            c.accountInvoices = []
            c.accounts = []
            
        c.page = pageLib.getInformation(c.w)
        if c.page and 'data' in c.page and c.page['data'] != "No workshop summary set yet":
            c.backConfig = 1
        else:
            c.backConfig = 0
        
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        c.wscope = geoInfoLib.getWScopeByWorkshop(c.w)
        if c.wscope:
            geoTags = c.wscope['scope'].split('|')
            c.country = geoTags[2]
            c.state = geoTags[4]
            c.county = geoTags[6]
            c.city = geoTags[8]
            c.postal = geoTags[9]
        else:
            c.country = "0"
            c.state = "0"
            c.county = "0"
            c.city = "0"
            c.postal = "0"
            
        c.motd = motdLib.getMessage(c.w.id)
        if c.w['startTime'] != '0000-00-00':
            c.f = facilitatorLib.getFacilitatorsByWorkshop(c.w.id)
            c.df = facilitatorLib.getFacilitatorsByWorkshop(c.w.id, 1)
            
        c.flaggedItems = {'ideas':[], 'resources':[], 'discussions':[], 'comments':[]}
        for key in c.flaggedItems.keys():
            objType = key[:-1]
            flaggedItems = flagLib.getFlaggedThings(objType, workshop = c.w)
            if flaggedItems:
                items = []
                codes = []
                for item in flaggedItems:
                    if item['urlCode'] not in codes:
                        items.append(item)
                        codes.append(item['urlCode'])
                c.flaggedItems[key] = items
        
        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)
        return render('/derived/6_workshop_preferences.bootstrap')
    