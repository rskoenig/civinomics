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
import pylowiki.lib.db.motd         as motdLib
import pylowiki.lib.db.pmember      as pMemberLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.activity     as activityLib
import pylowiki.lib.db.page         as pageLib
import pylowiki.lib.db.account      as accountLib
import pylowiki.lib.db.flag         as flagLib
import pylowiki.lib.db.goal         as goalLib
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.mail            as mailLib
import webhelpers.feedgenerator     as feedgenerator
import pylowiki.lib.db.stats     as statsLib

import pylowiki.lib.db.dbHelpers as dbHelpers
import pylowiki.lib.utils as utils
import pylowiki.lib.sort as sort
import simplejson as json
import misaka as m
import copy as copy

from HTMLParser import HTMLParser

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

log = logging.getLogger(__name__)


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

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
        ,'configureStartWorkshopHandler', 'adminWorkshopHandler', 'display', 'info', 'activity', 'stats', 'displayAllResources', 'preferences', 'upgradeHandler']
        
        adminOrFacilitator = ['configureBasicWorkshopHandler', 'configureTagsWorkshopHandler', 'configurePublicWorkshopHandler'\
        ,'configurePrivateWorkshopHandler', 'listPrivateMembersHandler', 'previewInvitation', 'configureScopeWorkshopHandler'\
        ,'configureStartWorkshopHandler', 'adminWorkshopHandler', 'preferences']
        
        scoped = ['display', 'info', 'activity', 'stats', 'displayAllResources']
        dontGetWorkshop = ['displayCreateForm', 'displayPaymentForm', 'createWorkshopHandler']
        
        if action in dontGetWorkshop:
            return
        if workshopCode is None:
            abort(404)
        c.w = workshopLib.getWorkshopByCode(workshopCode)
        if not c.w:
            abort(404)
        c.mainImage = mainImageLib.getMainImage(c.w)
        c.published = workshopLib.isPublished(c.w)
        c.started = workshopLib.isStarted(c.w)
        if action in setPrivs:
            workshopLib.setWorkshopPrivs(c.w)
            if action in adminOrFacilitator:
                if not c.privs['admin'] and not c.privs['facilitator']:
                    return(redirect("/"))
            elif action in scoped:
                if c.w['type'] == 'personal' or c.w['public_private'] == 'private':
                    if not c.privs['guest'] and not c.privs['participant'] and not c.privs['facilitator'] and not c.privs['admin']:
                        if c.privs['visitor']:
                            return redirect('/workshop/%s/%s/login'%(c.w['urlCode'], c.w['url']))
                        else:
                            return redirect('/')


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
        session['confTab'] = "basicInfo"
        session.save()

        slideshow = slideshowLib.getSlideshow(c.w)
        c.slideshow = slideshowLib.getAllSlides(slideshow)

        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = 'Missing Info: '

        if 'title' in request.params:
            wTitle = request.params['title']
            wTitle = wTitle.strip()
            if wTitle and wTitle != c.w['title']:
                c.w['title'] = wTitle
                oldTitle = c.w['url']
                c.w['url'] = utils.urlify(wTitle)
                workshopLib.updateWorkshopChildren(c.w, 'workshop_title')
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

        testGoals = goalLib.getGoalsForWorkshop(c.w)
        if not testGoals:
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
            weventMsg += "Changes saved."
            
        if not workshopLib.isPublished(c.w):
            weventMsg += ' See your changes by clicking on the preview button above.'

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
            if not workshopLib.isPublished(c.w):
                session['confTab'] = "tags"
            session.save()

        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configureTagsWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"
        currentTags = []
        for tag in c.w['workshop_category_tags'].split('|'):
            if tag and tag != '':
                currentTags.append(tag)
                
        session['confTab'] = "tags"
        session.save()
            
        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = 'Missing Info: '
            
        if 'categoryTags' in request.params:
            categoryTags = request.params.getall('categoryTags')
            
            newTagStr = '|'
            for tag in categoryTags:
                if tag not in currentTags:
                    wchanges = 1
                newTagStr = newTagStr + tag + '|'
                    
            for tag in currentTags:
                if tag not in categoryTags:
                    wchanges = 1
            
            
            if wchanges:
                weventMsg +=  "Updated category tags."
                c.w['workshop_category_tags'] = newTagStr
                dbHelpers.commit(c.w)
                workshopLib.updateWorkshopChildren(c.w, 'workshop_category_tags')
                
            if not workshopLib.isPublished(c.w):
                weventMsg += ' See your changes by clicking on the preview button above.'
                
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
                session['confTab'] = "slideshow"
            session.save()

        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configurePublicWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"
        session['confTab'] = "participants"
        session.save()
        
        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = ''
           
        if c.w['type'] == 'personal':
            alert = {'type':'info'}
            alert['title'] = 'You must upgrade to a Professional workshop in order to change the scope to public.'
            session['alert'] = alert
            session.save()
            return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url']))
            
        if c.w['public_private'] == 'private' and 'changeScope' in request.params:
            c.w['workshop_public_scope'] =  "||0||0||0||0|0"
            workshopLib.updateWorkshopChildren(c.w, 'workshop_public_scope')
            if c.w['disabled'] == '0' and c.w['deleted'] == '0' and c.w['published'] == '1':
                c.w['workshop_searchable'] = '1'
                workshopLib.updateWorkshopChildren(c.w, 'workshop_searchable')
                
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
        geoTagString = "||" + utils.urlify(geoTagCountry) + "||" + utils.urlify(geoTagState) + "||" + utils.urlify(geoTagCounty) + "||" + utils.urlify(geoTagCity) + "|" + utils.urlify(geoTagPostal)
        if 'workshop_public_scope' not in c.w:
            c.w['workshop_public_scope'] = geoTagString
            workshopLib.updateWorkshopChildren(c.w, 'workshop_public_scope')
            wchanges = 1
        elif c.w['workshop_public_scope'] != geoTagString:
            c.w['workshop_public_scope'] = geoTagString
            workshopLib.updateWorkshopChildren(c.w, 'workshop_public_scope')
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
            session['confTab'] = "participants"
            session.save()
            
        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url'])) 

    @h.login_required
    def configurePrivateWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"
        session['confTab'] = "participants"
        session.save()
            
        werror = 0
        wchanges = 0
        weventMsg = ''
        werrMsg = ''

        
        if 'addMember' in request.params:
            pList = pMemberLib.getPrivateMembers(workshopCode, "0")
            if 'newMember' in request.params and request.params['newMember'] != '':
                if c.w['type'] == 'personal' and len(pList) >= 20:
                    werror = 1
                    werrMsg += 'You have already reached the maximum number of 20 participants for a Free workshop.'
                else:
                    newMember = request.params['newMember']
                    counter = 0
                    # clean the list to enable separation by either comma or return
                    cList = newMember.replace(',', '\n')
                    cList.strip()
                    mList = cList.split('\n')

                    if c.w['type'] == 'personal' and (len(pList) + len(mList) > 20):
                        werror = 1
                        werrMsg += 'There are already ' + str(len(pList)) + ' participants. You cannot add ' + str(len(mList)) + ' more, Free workshops are limited to a maximum of 20 participants.'
                    else:
                        for mEmail in mList:
                            mEmail = mEmail.strip()
                            # make sure a valid email address
                            if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", mEmail):
                                werror = 1
                                werrMsg = werrMsg + 'Not valid email address: ' + mEmail
                            else:
                                pMember = pMemberLib.getPrivateMember(workshopCode, mEmail)
                                user = userLib.getUserByEmail(mEmail)
                                if not user:
                                    user = None
                                myURL = config['app_conf']['site_base_url']
                                browseURL = '%s/workshop/%s/%s'%(myURL, c.w['urlCode'], c.w['url'])
                                    
                                if pMember:
                                    if pMember['deleted'] == '1':
                                        pMember['deleted'] = '0'
                                        dbHelpers.commit(pMember)
                                    else:
                                        werror = 1
                                        werrMsg += mEmail + ' already a member.'
                                else:
                                    pMember = pMemberLib.PMember(workshopCode, mEmail, 'A', c.w, user)
                                    
                                inviteMsg = ''
                                if 'inviteMsg' in request.params:
                                    inviteMsg = "\nHere's a message from your friend:\n" + request.params['inviteMsg']
                                if not user:
                                    browseURL = '%s/guest/%s/%s'%(myURL, pMember['urlCode'], c.w['urlCode'])
                                mailLib.sendPMemberInvite(c.w['title'], c.authuser['name'], mEmail, inviteMsg, browseURL)
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



        if 'deleteMembers' in request.params:
            if 'selected_members' in request.params and request.params['selected_members'] != '':
                selected_members = request.params.getall('selected_members')
                counter = 0

                for member in selected_members:    
                    pTest = pMemberLib.getPrivateMember(workshopCode, member)
                    if pTest:
                        pTest['deleted'] = '1'
                        dbHelpers.commit(pTest)
                        # see if they have the workshop bookmarked
                        user = userLib.getUserByEmail(pTest['email'])
                        follow = followLib.getFollow(user, c.w)
                        if follow:
                            follow['disabled'] = '1'
                            dbHelpers.commit(follow)
                        counter += 1
                    else:
                        werror = 1
                        werrMsg += 'No current member email: %s. ' % member
                if counter > 1:
                    weventMsg += '%s members removed. ' % counter
                else:
                    weventMsg += "1 member removed. "
                
            else:
                werror = 1
                werrMsg += 'No email address entered.'


        if 'resendInvites' in request.params:
            if 'selected_members' in request.params and request.params['selected_members'] != '':
                selected_members = request.params.getall('selected_members')
                counter = 0

                inviteMsg = ''
                if 'inviteMsg' in request.params:
                    inviteMsg = request.params['inviteMsg']
                myURL = config['app_conf']['site_base_url']
                browseURL = '%s/workshop/%s/%s'%(myURL, c.w['urlCode'], c.w['url'])

                for member in selected_members:                        
                    mailLib.sendPMemberInvite(c.w['title'], c.authuser['name'], member, inviteMsg, browseURL)
                    counter += 1

                if counter > 1:
                    weventMsg += '%s invitations have been resent. ' % counter
                else:
                    weventMsg += "1 invitation has been resent. "
                
            else:
                werror = 1
                werrMsg += 'No email address entered.'


        if c.w['public_private'] == 'public' and 'changeScope' in request.params:
            weventMsg = 'Workshop scope changed from public to private.'
            c.w['public_private'] = 'private'
            dbHelpers.commit(c.w)
            
        if 'continueToNext' in request.params:
            session['confTab'] = "participants"
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
        
        return render('/derived/6_preview_invitation.bootstrap')
        
    @h.login_required
    def configureScopeWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Configure Workshop"

        c.title = "Configure Workshop"
        session['confTab'] = "participants"
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
        if not self.checkPreferences():
            alert = {'type':'error'}
            alert['title'] = 'Workshop not started'
            alert['content'] = ' !'
            session['alert'] = alert
            session.save()
            
            return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url']))
            
        c.title = "Configure Workshop"

        werror = 0

        if 'startWorkshop' in request.params:
            # Set workshop start and end time
            c.w['published'] = '1'
            if c.w['public_private'] == 'public' and c.w['deleted'] == '0' and c.w['disabled'] == '0':
                c.w['workshop_searchable'] = '1'
                workshopLib.updateWorkshopChildren(c.w, 'workshop_searchable')
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
    def publishWorkshopHandler(self, workshopCode, workshopURL):
        c.title = "Publish Workshop"

        if workshopLib.isPublished(c.w):
            c.w['published'] = '0'
            action = "unpublished"
        else:
            c.w['published'] = '1'
            action = "republished"
        
        if c.w['public_private'] == 'public' and c.w['deleted'] == '0' and c.w['disabled'] == '0' and c.w['published'] == '1':
            c.w['workshop_searchable'] = '1'
        else:
            c.w['workshop_searchable'] = '0'
            
        workshopLib.updateWorkshopChildren(c.w, 'workshop_searchable')
            
        eventLib.Event('Workshop Config Updated by %s'%c.authuser['name'], 'Workshop %s.'%action, c.w, c.authuser)
        dbHelpers.commit(c.w)

        alert = {'type':'success'}
        alert['title'] = 'Workshop %s.'%action
        alert['content'] = ''
        session['alert'] = alert
        session.save()
        

            
        return redirect('/workshop/%s/%s/preferences'%(c.w['urlCode'], c.w['url']))

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
        
        if 'admin-submit-button' in request.params and c.privs['admin']:
            return True
        
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
            if request.params['coupon'] == 'CIVCOMP100' or request.params['coupon'] == 'CIVCOMP99':
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
                    if ('admin-submit-button' in request.params and c.privs['admin']):
                        c.stripeToken = "ADMINCOMP"
                        c.billingName = c.authuser['name']
                        c.billingEmail = "billing@civinomics.com"
                        c.coupon = ''
                        
                    account = accountLib.Account(c.billingName, c.billingEmail, c.stripeToken, workshop, 'PRO', c.coupon)
                    eventLib.Event('Workshop upgraded to Pro', 'Workshop upgraded to Pro by %s'%c.authuser['name'], workshop, c.authuser)
                        
                    alert = {'type':'success'}
                    alert['title'] = 'Your workshop has been upgraded from Free to Professional. Have fun!'
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
            scope = 'private'
        # added to make workshops free
        elif 'createPublic' in request.params:
            wType = 'professional'
            scope = 'public'
            c.stripeToken = "ADMINCOMP"
            c.billingName = c.authuser['name']
            c.billingEmail = "billing@civinomics.com"
            c.coupon = ''
        elif 'createPrivate' in request.params:
            wType = 'professional'
            scope = 'private'
            c.stripeToken = "ADMINCOMP"
            c.billingName = c.authuser['name']
            c.billingEmail = "billing@civinomics.com"
            c.coupon = ''
        # end addition
        else:
            if self.validatePaymentForm():
                wType = 'professional'
            else:
                c.stripeKey = config['app_conf']['stripePublicKey'].strip()
                return render('/derived/6_workshop_payment.bootstrap')
                
        w = workshopLib.Workshop('New Workshop', c.authuser, scope, wType)
        if 'createPublic' in request.params and 'geoString' in request.params:
            w['workshop_public_scope'] =  request.params['geoString']
        c.workshop_id = w.id # TEST
        c.title = 'Configure Workshop'
        c.motd = motdLib.MOTD('Welcome to the workshop!', w.id, w.id)
        if wType == 'professional':
            account = accountLib.Account(c.billingName, c.billingEmail, c.stripeToken, w, 'PRO', c.coupon)
        alert = {'type':'success'}
        alert['title'] = 'Your new ' + scope + ' workshop is ready to be set up. Have fun!'
        session['alert'] = alert
        session.save()

        return redirect('/workshop/%s/%s/preferences'%(w['urlCode'], w['url']))
    
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
        
    def rss(self, workshopCode, workshopURL):
        if c.w['public_private'] == 'private':
            abort(404)
            
        activity = activityLib.getActivityForWorkshop(c.w['urlCode'])
        feed = feedgenerator.Rss201rev2Feed(
            title=u"Civinomics Workshop Activity",
            link=u"http://www.civinomics.com",
            description=u'The most recent activity in "%s".'%c.w['title'],
            language=u"en"
        )
        for item in activity:
            wURL = config['site_base_url'] + "/workshop/" + c.w['urlCode'] + "/" + c.w['url'] + "/"
            
            thisUser = userLib.getUserByID(item.owner)
            activityStr = thisUser['name'] + " "
            if item.objType == 'resource':
               activityStr += 'added the resource '
            elif item.objType == 'discussion':
               activityStr += 'started the discussion '
            elif item.objType == 'idea':
                activityStr += 'posed the idea '
            elif item.objType == 'comment':
                if 'ideaCode' in item.keys():
                    newitem = ideaLib.getIdea(item['ideaCode'])
                elif 'resourceCode' in item.keys():
                    newitem = resourceLib.getResourceByCode(item['resourceCode'])
                elif 'discussionCode' in item.keys():
                    newitem = discussionLib.getDiscussion(item['discussionCode'])
                    
                activityStr += 'commented on the %s '%newitem.objType
                item = newitem
                
            activityStr += '"' + item['title'] + '"'
            wURL += item.objType + "/" + item['urlCode'] + "/" + item['url']
            feed.add_item(title=activityStr, link=wURL, guid=wURL, description='')
            
        response.content_type = 'application/xml'

        return feed.writeString('utf-8')
        
    def display(self, workshopCode, workshopURL):
        # check to see if this is a request from the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)
        # iphone app json data structure:
        entry = {}
        # these values are needed for facebook sharing
        c.facebookAppId = config['facebook.appid']
        c.channelUrl = config['facebook.channelUrl']
        c.baseUrl = utils.getBaseUrl()
        
        c.requestUrl = request.url
        c.thingCode = workshopCode
        # standard thumbnail image for facebook shares
        if c.mainImage['pictureHash'] == 'supDawg':
            c.backgroundImage = '/images/slide/slideshow/supDawg.slideshow'
        elif 'format' in c.mainImage.keys():
            c.backgroundImage = '/images/mainImage/%s/orig/%s.%s' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'], c.mainImage['format'])
        else:
            c.backgroundImage = '/images/mainImage/%s/orig/%s.jpg' %(c.mainImage['directoryNum'], c.mainImage['pictureHash'])
        # name for facebook share posts
        c.name = c.title = c.w['title']

        c.isFollowing = False
        if 'user' in session:
            c.isFollowing = followLib.isFollowing(c.authuser, c.w)
        
        c.facilitators = []
        for f in (facilitatorLib.getFacilitatorsByWorkshop(c.w)):
            if 'pending' in f and f['pending'] == '0' and f['disabled'] == '0':
                c.facilitators.append(f)
              
        c.listeners = []
        if not iPhoneApp:
            for l in (listenerLib.getListenersForWorkshop(c.w)):
                if 'pending' in l and l['pending'] == '0' and l['disabled'] == '0':
                    c.listeners.append(l)
              
        c.slides = []
        if not iPhoneApp:
            c.slideshow = slideshowLib.getSlideshow(c.w)
            slide_ids = [int(item) for item in c.slideshow['slideshow_order'].split(',')]
            for id in slide_ids:
                s = slideLib.getSlide(id) # Don't grab deleted slides
                if s:
                    c.slides.append(s)

        if not iPhoneApp:
            c.motd = motdLib.getMessage(c.w.id)
            # kludge for now
            if c.motd == False:
               c.motd = motdLib.MOTD('Welcome to the workshop!', c.w.id, c.w.id)

        if not iPhoneApp:
            c.motd['messageSummary'] = h.literal(h.reST2HTML(c.motd['data']))
        
        c.information = pageLib.getInformation(c.w)
        
        if not iPhoneApp:
            c.activity = activityLib.getActivityForWorkshop(c.w['urlCode'])
        
        if not iPhoneApp:
            if c.w['public_private'] == 'public':
                c.scope = workshopLib.getPublicScope(c.w)

        c.goals = goalLib.getGoalsForWorkshop(c.w)
        if not c.goals:
            c.goals = []
        elif iPhoneApp:
            i = 0
            for goal in c.goals:
                goalEntry = "goal" + str(i)
                entry[goalEntry] = dict(goal)
                i = i + 1
        
        if not iPhoneApp:
            # Demo workshop status
            c.demo = workshopLib.isDemo(c.w)

        # determines whether to display 'admin' or 'preview' button. Privs are checked in the template. 
        c.adminPanel = False

        if not iPhoneApp:        
            discussions = discussionLib.getDiscussionsForWorkshop(workshopCode)
            if not discussions:
                c.discussions = []
            else:
                discussions = sort.sortBinaryByTopPop(discussions)
                c.discussions = discussions[0:3]

        ideas = ideaLib.getIdeasInWorkshop(workshopCode)
        if not ideas:
            c.ideas = []
        else:
            c.ideas = sort.sortBinaryByTopPop(ideas)
            if iPhoneApp:
                i = 0
                for idea in c.ideas:
                    ideaEntry = "idea" + str(i)
                    # so that we don't modify the original, we place this idea in a temporary variable
                    formatIdea = []
                    formatIdea = copy.copy(idea)
                    ideaHtml = m.html(formatIdea['text'], render_flags=m.HTML_SKIP_HTML)
                    s = MLStripper()
                    s.feed(ideaHtml)
                    formatIdea['text'] = s.get_data()
                    # if this person has voted on the idea, we need to pack their vote data in
                    if 'user' in session:
                        rated = ratingLib.getRatingForThing(c.authuser, idea)
                        if rated:
                            if rated['amount'] == '1':
                                formatIdea['rated'] = "1"
                            elif rated['amount'] == '-1':
                                formatIdea['rated'] = "-1"
                            elif rated['amount'] == '0' :
                                formatIdea['rated'] = "0"
                            else:
                                formatIdea['rated'] = "0"
                        else:
                            formatIdea['rated'] = "0"
                    entry[ideaEntry] = dict(formatIdea)
                    i = i + 1

        if not iPhoneApp:
            disabled = ideaLib.getIdeasInWorkshop(workshopCode, disabled = '1')
            if disabled:
                c.ideas = c.ideas + disabled

        c.listingType = 'ideas'
        if iPhoneApp:
            entry['mainImage'] = dict(c.mainImage)
            entry['baseUrl'] = c.baseUrl
            entry['thingCode'] = c.thingCode
            entry['backgroundImage'] = c.backgroundImage
            entry['title'] = c.w['title']
            entry['isFollowing'] = c.isFollowing
            #entry['facilitators'] = dict(c.facilitators)
            #entry['listeners'] = c.listeners
            if c.information and 'data' in c.information:         
                entry['information'] = m.html(c.information['data'], render_flags=m.HTML_SKIP_HTML)
            #entry['information'] = dict(c.information)
            #entry['goals'] = dict(c.goals)
            #entry['ideas'] = dict(c.ideas)
            result = []
            result.append(entry)
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return render('/derived/6_workshop_home.bootstrap')
        
    def info(self, workshopCode, workshopURL):
        c.title = c.w['title']

        if c.w['public_private'] == 'public':
            c.scope = workshopLib.getPublicScope(c.w)

        c.isFollowing = False
        if 'user' in session:
            c.isFollowing = followLib.isFollowing(c.authuser, c.w)

        c.information = pageLib.getInformation(c.w)
        
        c.slides = []
        c.slideshow = slideshowLib.getSlideshow(c.w)
        slide_ids = [int(item) for item in c.slideshow['slideshow_order'].split(',')]
        for id in slide_ids:
            s = slideLib.getSlide(id) # Don't grab deleted slides
            if s:
                c.slides.append(s)

        # determines whether to display 'admin' or 'preview' button. Privs are checked in the template.
        c.adminPanel = False

        resources = resourceLib.getResourcesByWorkshopCode(workshopCode)
        if not resources:
            c.resources = []
        else:
            c.resources = sort.sortBinaryByTopPop(resources)
        disabled = resourceLib.getResourcesByWorkshopCode(workshopCode, disabled = '1')
        if disabled:
            c.resources = c.resources + disabled
        c.listingType = 'resources'

        return render('/derived/6_workshop_info.bootstrap')
        
    def activity(self, workshopCode, workshopURL):
        c.title = c.w['title']

        if c.w['public_private'] == 'public':
            c.scope = workshopLib.getPublicScope(c.w)

        c.isFollowing = False
        if 'user' in session:
            c.isFollowing = followLib.isFollowing(c.authuser, c.w)

        c.activity = activityLib.getActivityForWorkshop(c.w['urlCode'])

        # determines whether to display 'admin' or 'preview' button. Privs are checked in the template.
        c.adminPanel = False

        c.listingType = 'activity'

        return render('/derived/6_detailed_listing.bootstrap')

    def stats(self, workshopCode, workshopURL):
        c.title = c.w['title']

        if c.w['public_private'] == 'public':
            c.scope = workshopLib.getPublicScope(c.w)

        c.isFollowing = False
        if 'user' in session:
            c.isFollowing = followLib.isFollowing(c.authuser, c.w)

        c.stats = statsLib.getStatsForWorkshop(c.w['urlCode'])
        ideaList = []
        i = 0
        for idea in c.stats:
            thisIdea = {}
            thisIdea['totalVotes'] = int(idea['downs']) + int(idea['ups'])
            thisIdea['rating'] = int(idea['ups']) - int(idea['downs']) 
            thisIdea['totalYes'] = int(idea['ups'])
            thisIdea['totalNo'] = int(idea['downs'])
            thisIdea['totalVotes'] = int(idea['ups']) + int(idea['downs'])
            thisIdea['percentYes'] = thisIdea['percentNo'] = 0
            if thisIdea['totalVotes'] > 0:
                thisIdea['percentYes'] = int(float(thisIdea['totalYes'])/float(thisIdea['totalVotes']) * 100)
                thisIdea['percentNo'] = int(float(thisIdea['totalNo'])/float(thisIdea['totalVotes']) * 100)
            thisIdea['views'] = idea['views']
            log.info("i: %s"%i)
            ideaList.append(thisIdea)

        c.ideaStats = ideaList
        #getActivityCountByObjectForWorkshop(c.w['urlCode'])
        # determines whether to display 'admin' or 'preview' button. Privs are checked in the template.
        c.adminPanel = False

        c.listingType = 'stats'

        return render('/derived/6_detailed_listing.bootstrap')
   
    def checkPreferences(self):
        testGoals = goalLib.getGoalsForWorkshop(c.w)
        if testGoals and c.w['description'] and c.w['description'] != '':
            c.basicConfig = 1
        else:
            c.basicConfig = 0
        
        testTags = c.w['workshop_category_tags'].split('|')
        tagList = []
        for tag in testTags:
            if tag and tag != '':
                tagList.append(tag)
        if len(tagList):
            c.tagConfig = 1
        else:
            c.tagConfig = 0
            
        slides = slideshowLib.getSlideshow(c.w)
        slideshow = slideshowLib.getAllSlides(slides)
        published = 0
        slide_ids = [int(item) for item in slides['slideshow_order'].split(',')]
        for id in slide_ids:
            s = slideLib.getSlide(id) # Don't grab deleted slides
            if s:
                published += 1
        if len(slideshow) > 1 and published > 0:
            c.slideConfig = 1
        else:
            c.slideConfig = 0
       
        page = pageLib.getInformation(c.w)
        if page and 'data' in page:
            background = page['data']
        if background and background != utils.workshopInfo:
            c.backConfig = 1
        else:
            c.backConfig = 0
            
        pList = pMemberLib.getPrivateMembers(c.w['urlCode'], "0")
        if c.w['public_private'] == 'private' and len(pList) != 0:
            c.participantsConfig = 1
        elif c.w['public_private'] == 'public':
            c.participantsConfig = 1
        else:
            c.participantsConfig = 0


        if c.basicConfig and c.tagConfig and c.slideConfig and c.backConfig and c.participantsConfig:
            return True
        
        return False
                       
            
    @h.login_required
    def preferences(self, workshopCode, workshopURL):
        readyToStart = self.checkPreferences()
        
        c.categories = []
        for tag in c.w['workshop_category_tags'].split('|'):
            if tag and tag != '':
                c.categories.append(tag)
            
        if 'confTab' in session:
            c.tab = session['confTab']
            log.info(c.tab)
            session.pop('confTab')
            session.save()
        # hack for continue button in slideshow tab of configure
        if 'continueToNext' in request.params:
            c.tab = 'background'
            
        slideshow = slideshowLib.getSlideshow(c.w)
        c.slideshow = slideshowLib.getAllSlides(slideshow)
        c.deleted_slides = []
        c.published_slides = []
        slide_ids = [int(item) for item in slideshow['slideshow_order'].split(',')]
        for id in slide_ids:
            s = slideLib.getSlide(id) # Don't grab deleted slides
            if s:
                c.published_slides.append(s)
            
        c.slides = c.published_slides
            
        c.facilitators = facilitatorLib.getFacilitatorsByWorkshop(c.w)
        c.listeners = listenerLib.getListenersForWorkshop(c.w, disabled = '0')
        c.disabledListeners = listenerLib.getListenersForWorkshop(c.w, disabled = '1')

        c.pmembers = pMemberLib.getPrivateMembers(workshopCode)
        
        
        c.accounts = accountLib.getAccountsForWorkshop(c.w, deleted = '0')
        if c.accounts and accountLib.isComp(c.accounts[0]):
            if not c.privs['admin']:
                c.accounts = []
        
        c.page = pageLib.getInformation(c.w)
        
        c.states = geoInfoLib.getStateList('United-States')
        # ||country||state||county||city|zip
        if c.w['public_private'] == 'public' and 'workshop_public_scope' in c.w and c.w['workshop_public_scope'] != '':
            geoTags = c.w['workshop_public_scope'].split('|')
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

            
        c.motd = motdLib.getMessage(c.w.id)
        if c.w['startTime'] != '0000-00-00':
            c.f = facilitatorLib.getFacilitatorsByWorkshop(c.w)
            c.df = facilitatorLib.getFacilitatorsByWorkshop(c.w, 1)
        
        c.flaggedItems = flagLib.getFlaggedThingsInWorkshop(c.w)
        
        if c.w['public_private'] == 'public':
            c.scope = workshopLib.getPublicScope(c.w)

        myURL = config['app_conf']['site_base_url']
        c.shareURL = '%s/workshop/%s/%s'%(myURL, c.w['urlCode'], c.w['url'])

        # determines whether to display 'admin' or 'preview' button. Privs are checked in the template. 
        c.adminPanel = True

        return render('/derived/6_workshop_preferences.bootstrap')
        
    @h.login_required
    def pmemberNotificationHandler(self, workshopCode, workshopURL, userCode):
        # check to see if this is a request from the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)

        user = userLib.getUserByCode(userCode)
        pmember = pMemberLib.getPrivateMember(workshopCode, user['email'])
        # initialize to current value if any, '0' if not set in object
        iAlerts = '0'
        eAction = ''
        if 'itemAlerts' in pmember:
            iAlerts = pmember['itemAlerts']
        
        if iPhoneApp:
            try:
                alert = request.params['alert']
            except:
                statusCode = 2
                response.headers['Content-type'] = 'application/json'
                #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
                return json.dumps({'statusCode':statusCode, 'result':'error'})
        else:
            payload = json.loads(request.body)
            if 'alert' not in payload:
                return "Error"
            alert = payload['alert']
        if alert == 'items':
            if 'itemAlerts' in pmember.keys(): # Not needed after DB reset
                if pmember['itemAlerts'] == u'1':
                    listener['itemAlerts'] = u'0'
                    eAction = 'Turned off'
                else:
                    pmember['itemAlerts'] = u'1'
                    eAction = 'Turned on'
            else:
                pmember['itemAlerts'] = u'1'
                eAction = 'Turned on'
        elif alert == 'digest':
            if 'digest' in pmember.keys(): # Not needed after DB reset
                if pmember['digest'] == u'1':
                    listener['digest'] = u'0'
                    eAction = 'Turned off'
                else:
                    pmember['digest'] = u'1'
                    eAction = 'Turned on'
            else:
                pmember['digest'] = u'1'
                eAction = 'Turned on'
        else:
            if iPhoneApp:
                statusCode = 2
                response.headers['Content-type'] = 'application/json'
                #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
                return json.dumps({'statusCode':statusCode, 'result':'error'})
            else:
                return "Error"

        dbHelpers.commit(pmember)
        if eAction != '':
            eventLib.Event('Private member item notifications set', eAction, pmember, c.authuser)
        
        if iPhoneApp:
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            result = eAction
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return eAction

    