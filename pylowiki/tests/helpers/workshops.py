# -*- coding: utf-8 -*-
from pylowiki.tests import *
from routes import url_for
import re

import pylowiki.tests.helpers.assertions as assertions
import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.link_definitions as linkDefs
from pylowiki.tests.helpers.authorization import login

import logging
log = logging.getLogger(__name__)

def addCommentToIdeaPage(self, ideaPage, commentText):
    # comment on this idea
    addCommentForm = ideaPage.forms[formDefs.addComment()]
    addCommentForm.set(formDefs.addComment_text(), commentText)
    # the form for submitting an idea has an extra parameter added to it as well.
    # this is an easy way to add the extra parameter
    params = {}
    params = formHelpers.loadWithSubmitFields(addCommentForm)
    params[formDefs.parameter_submit()] = formDefs.addComment_submit()
    commentAdded = self.app.get(
        url = str(addCommentForm.action),
        params=params
    ).follow()
    return commentAdded

def addIdeaToWorkshop(self, workshop, ideaText):
    """Add an idea to a workshop"""
    # go to the ideas page
    ideasPage = workshop.click(description=linkDefs.ideas_page(), index=0)
    # click the 'add idea' link
    addIdea = ideasPage.click(description=linkDefs.addIdea(), index=0)
    # obtain the form for this
    addForm = addIdea.forms[formDefs.addIdea()]
    addForm.set(formDefs.addIdea_text(), ideaText)
    # this form does not include submit as a parameter, but it must be included in the postdata
    params = {}
    params = formHelpers.loadWithSubmitFields(addForm)
    #for key, value in addForm.submit_fields():
    #    params[key] = value
    params[formDefs.parameter_submit()] = content.noChars()
    ideaAdded = self.app.post(
        url=str(addForm.action), 
        content_type=addForm.enctype,
        params=params
    ).follow()
    ideaPage = ideaAdded.click(description=ideaText, index=0)
    return ideaPage

def create_new_workshop(self, thisUser, **kwargs):
    """Unless otherwise indicated, logs in as the specified user and creates a new workshop.
    Returns this workshop's main page. """
    #: sometimes the user will already be logged in, in which case we don't need to do this here
    if 'login' in kwargs:
        if kwargs['login'] == True:
            login(self, thisUser)
    else:
        #: if there's no mention of this parameter, the default action is to log the user in
        login(self, thisUser)
    # load the home page, which redirects to the list all workshops page
    rHome = self.app.get(url=url_for(controller='home', action='index'))
    rWorkshops = rHome.follow()
    # click the profile link
    rProfile = rWorkshops.click(description=linkDefs.profile(), index=0)
    # click the edit link
    rDashboard = rProfile.click(description=linkDefs.profile_edit(), index=0)
    # click the create workshop button
    createWorkshopForm = rDashboard.forms[formDefs.createWorkshop_button()]
    createWorkshop = createWorkshopForm.submit()
    #: we have a choice now for creating a personal or professional workshop
    #: get the form that holds both choices
    whichWorkshopForm = createWorkshop.forms[formDefs.createWorkshop_1_form()]
    params = {}
    #: it is expected that this form has one submit value, the name of the button and its value of ''
    #: for robustness, the loadWithSubmitFields() function is used in case any other submit fields are 
    #: needed here, although currently there are not
    params = formHelpers.loadWithSubmitFields(whichWorkshopForm)
    params[formDefs.create_workshop_1_personal_professional(kwargs)] = content.noChars()
    startCreateWorkshop1 = self.app.post(
        url=str(whichWorkshopForm.action), 
        content_type=whichWorkshopForm.enctype,
        params=params
    ).follow()
    #: now we are either creating a personal or a professional workshop
    #if 'personal' in kwargs:
        #if kwargs['personal'] == True:
            #: we've gone the personal workshop route, do nothing here
        #else:
            #: NOTE: COMING SOON
            #: upgradeToProfessional
            #: createScope
            #: setWorkshopScope
            #: DONE!

    #: start completing workshop form - basic fields
    #: this line selects the form we want for this part by its id parameter from all the forms 
    #: in the page, startCreateWorkshop1
    createWorkshopForm1 = startCreateWorkshop1.forms[formDefs.createWorkshop_2_Basics()]
    #: load all the fields in this form
    formFields1 = createWorkshopForm1.fields
    # fill out the form's fields appropriately
    for key in formFields1:
        #: if this is the title field, set the form's title field
        if formDefs.createWorkshopForm1_title() == key:
            if 'title' in kwargs:
                createWorkshopForm1[key] = kwargs['title']
                workshopTitle = kwargs['title']
            else:
                createWorkshopForm1[key] = 'NEW WORKSHOP TITLE'
                workshopTitle = 'NEW WORKSHOP TITLE'
        #: if this is the description field, set the form's description field
        elif formDefs.createWorkshopForm1_description() == key:
            if 'description' in kwargs:
                createWorkshopForm1[key] = kwargs['description']
            else:
                createWorkshopForm1[key] = 'NEW WORKSHOP DESCRIPTION'
        #: and so on..
        elif formDefs.createWorkshopForm1_goals() == key:
            if 'goals' in kwargs:
                createWorkshopForm1[key] = kwargs['goals']
            else:
                createWorkshopForm1[key] = 'NEW SET OF GOALS'
        #: check this box if needed
        elif formDefs.createWorkshopForm1_suggestions() == key:
            if 'allowIdeas' in kwargs:
                createWorkshopForm1.set(key, kwargs['allowIdeas'])
            else:
                #: by default, we check this box in order to allow workshop participants
                #: to add suggestions
                createWorkshopForm1.set(key, formDefs.workshopSettings_allowIdeas(True))
        elif formDefs.createWorkshopForm1_resources() == key:
            if 'allowResourceLinks' in kwargs:
                createWorkshopForm1.set(key, kwargs['allowResourceLinks'])
            else:
                # by default, allow workshop participants to add resources
                createWorkshopForm1.set(key, formDefs.workshopSettings_allowResourceLinks(True))

    #: save these settings by 'pressing' the submit button. the page is reloaded and we resume
    #: with completing the create workshop process
    startCreateWorkshop2 = createWorkshopForm1.submit().follow()

    #: complete workshop form, private or public?
    #: for now, private is the default. these lines determine if the private or public scope form
    #: is loaded.
    if 'private' in kwargs:
        createWorkshopForm2 = startCreateWorkshop2.forms[formDefs.createWorkshopForm2(kwargs['private'])]
    else:
        createWorkshopForm2 = startCreateWorkshop2.forms[formDefs.createWorkshopForm2()]
    
    #: There are two fields that act as submit buttons:
    #: addMember and continueToNext. createWorkshopForm2_submit presses the continue button
    startCreateWorkshop3 = createWorkshopForm2.submit(formDefs.createWorkshopForm2_submit()).follow()
    
    #: step3 add tags to the workshop
    #: load this form
    createWorkshopForm3 = startCreateWorkshop3.forms[formDefs.createWorkshopForm3()]
    #: for now, set some arbitrary tags
    #: NOTE tag selection coming soon
    createWorkshopForm3.set('categoryTags', 'Arts', 0)
    #createWorkshopForm3.set('categoryTags', 'Civil Rights', 2)
    createWorkshopForm3.set('categoryTags', 'Economy', 4)
    startCreateWorkshop4 = createWorkshopForm3.submit().follow()

    #: step4 - the slideshow
    #: add slides: add photo, press upload button .. can't get this working in test yet,
    #: looks lik the solution will involve loading the upload field with a tuple, the photo being
    #: represented with a string
    createWorkshopSlidesForm = startCreateWorkshop4.forms[formDefs.createWorkshop_FileUploadForm()]
    # <form id="fileupload" class="well" action="/workshop/4ICj/test-title/addImages/handler" method="POST" enctype="multipart/form-data">
    # <input type="file" name="files[]" multiple>
    # <button type="submit" class="btn btn-primary start"><span>Start upload</span></button>
    # createWorkshopSlidesForm['files'] = [(u'files[]', u'fireTime.jpg')]
    # should work if we have python 2.7: createWorkshopSlidesForm['files[]'] = collections.OrderedDict([('files[]', 'fireTime.jpg')])
    # uploadTest = createWorkshopSlidesForm.submit()

    #: press the continue button (which is a form itself) at the bottom of the slideshow creation page
    createWorkshopForm4 = startCreateWorkshop4.forms[formDefs.createWorkshopForm4_continueToNext()]
    startCreateWorkshop5 = createWorkshopForm4.submit()

    #: fill out wiki background
    # NOTE strangely enough wikibackground is not updating with new content for startCreateWorkshop6
    createWorkshopForm5 = startCreateWorkshop5.forms[formDefs.createWorkshopForm5_wikiBackground()]
    # recorded post data: _method=put, textarea0=words+some+more+words, submit=, count=1, dashboard=dashboard
    # from the pdb printout of the form in the response: fields: {u'count': [<Hidden name="count" id="count">], u'data': [<Textarea name="data" id="data">], u'dashboard': [<Hidden name="dashboard" id="dashboard">], u'submit': [<Submit name="submit" id="submit">, <Submit name="submit">], u'_method': [<Hidden name="_method">]}
    createWorkshopForm5.set(formDefs.createWorkshopForm5_wikiBackground_text(), 'testing+workshop')

    #: form preparation for wiki background
    params = {}
    params = formHelpers.loadWithSubmitFields(createWorkshopForm5)
    params[formDefs.parameter_submit()] = formDefs.createWorkshopForm5_wikiBackground_submit()

    #: wiki background form not working, have no idea why at this point - skipping for now
    #: NOTE yes, startCreateWorkshop6 is the same as startCreateWorkshop5. when startCreateWorkshop5
    #: starts working, it's likely no code will then have to change past this point
    startCreateWorkshop6 = startCreateWorkshop5
    # this is what would happen instead:
    #startCreateWorkshop6 = self.app.post(
    #    url = str(createWorkshopForm5.action),
    #    params=params
    #).follow()

    # notes about the form's fields
    # submit_fields(): [(u'count', u'1'), (u'textarea0', u'No wiki background set yet'), (u'dashboard', u'dashboard'), (u'_method', u'put')]    
    
    #: because we haven't created a slide for the slideshow, the publish form will not display.
    # <form name="edit_issue" id="edit_issue" class="left form-inline" 
    # action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureStartWorkshopHandler" 
    # enctype="multipart/form-data" method="post" >
    #: So, instead we will post to this address on our own
    # startCreateWorkshop6.request.url == http://localhost/workshop/4ICj/test-title/configureContinueHandler
    #: grab this workshop's url and parse out the url and workshop code
    workshopUrl = startCreateWorkshop6.request.url
    urlParts = workshopUrl.split('/')
    url_index = len(urlParts)-2
    this_url = urlParts[url_index]
    urlCode_index = len(urlParts)-3
    this_urlCode = urlParts[urlCode_index]
    
    #: create the publish workshop action url
    startUrl = '/workshop/%s/%s/configureStartWorkshopHandler'%(this_urlCode,this_url)

    #: hit the publish button unless this is not the desired action
    if 'dontCreateWorkshop' in kwargs:
        if kwargs['dontCreateWorkshop'] == True:
            return startUrl
        else:
            # start the workshop
            workshopCreated = self.app.post(
                url=startUrl, 
                content_type='multipart/form-data',
                params={'name' : 'startWorkshop'}
            ).follow()
            # assert that this action was successful
            assert assertions.not_in_new_workshop_1() not in workshopCreated
            assert workshopTitle in workshopCreated
            return workshopCreated
    else:
        # start the workshop
        workshopCreated = self.app.post(
            url=startUrl, 
            content_type='multipart/form-data',
            params={'name' : 'startWorkshop'}
        ).follow()
        # assert that this action was successful
        assert assertions.not_in_new_workshop_1() not in workshopCreated
        assert workshopTitle in workshopCreated
        return workshopCreated

def createScope(self, **kwargs):
    """Returns a dictionary of settings for determining scope in the ui. If a scope is requested,
    all of the larger area scopes must be designated as well."""
    import pylowiki.lib.db.geoInfo as geoInfoLib
    #: example scope string format: lowercase with '-' for ' ' and a single '|' in front of postal code 
    #: ||united-states||california||santa-cruz||santa-cruz|95060
    geoTagCountry = 'united-states'
    if 'state' in kwargs:
        geoTagState = kwargs['state']
    else:
        geoTagState = ''
    if 'county' in kwargs:
        geoTagCounty = kwargs['county']
    else:
        geoTagCounty = ''
    if 'city' in kwargs:
        geoTagCity = kwargs['city']
    else:
        geoTagCity = ''
    if 'postal' in kwargs:
        geoTagPostal = kwargs['postal']
    else:
        geoTagPostal = ''

    geoTagString = "||" + geoTagCountry + "||" + geoTagState + "||" + geoTagCounty + "||" + geoTagCity + "|" + geoTagPostal
    return geoTagString

def getWorkshopCode(self, workshop):
    """returns the code associated with a workshop"""
    # structure: http://localhost/workshop/4ICj/new-workshop-by-user
    parts = workshop.request.url.split('/')
    codeIndex = len(parts)-2
    thisCode = parts[codeIndex]
    return thisCode

def getWorkshopListingPage(self):
    """return the workshops listing page"""
    return self.app.get(url='/%s'%(linkDefs.workshopListingPage()))

def getWorkshopPreferencesPage(self, workshop):
    """return the preferences page for a workshop"""
    return workshop.click(href=linkDefs.workshopSettings(), index=0)
    

def inviteGuest(self, workshop, **kwargs):
    """Invite a guest to the workshop and return whatever is needed"""
    #: go into the settings and invite a guest
    # this used to work, may again but for now it doesn't
    #dashboard = workshop.click(href=linkDefs.workshopDashboard(), verbose=True)
    preferences = self.app.get(url='%s/%s'%(workshop.request.url,linkDefs.workshopSettings()))
    privateForm = preferences.forms[formDefs.workshopSettings_privateForm()]
    #: add email of a non-member of this site or workshop, check the 'send invitation' box
    if 'email' in kwargs:
        guestEmail = kwargs['email']
    else:
        guestEmail = content.email_to_todd_1()
    privateForm.set(formDefs.workshopSettings_privateForm_invite(), guestEmail)
    # check the invite email box unless dontSendInvite is set
    # this interface looks to be no longer used
    #if 'dontSendInvite' in kwargs:
    #    if kwargs['dontSendInvite'] == False:
    #        privateForm.set(formDefs.workshopSettings_privateForm_sendInviteMsg(), content.checkbox(True))
    #else:
    #    privateForm.set(formDefs.workshopSettings_privateForm_sendInviteMsg(), content.checkbox(True))

    #: the guest invite link is recorded in /lib/db/workshop.py
    params = {}
    params = formHelpers.loadWithSubmitFields(privateForm)
    #: add a field that the controller checks for when this invite is submitted
    params[formDefs.workshopSettings_privateForm_addMemberField()] = formDefs.workshopSettings_privateForm_addMemberField()
    #: submit the invite request
    inviteSent = self.app.post(
        url = str(privateForm.action),
        params=params
    )
    inviteFollowed = inviteSent.follow()
    if 'guestLink' in kwargs:
        if kwargs['guestLink'] == True:
            return inviteSent.browseUrl
        else:
            return guestEmail
    else:
        return guestEmail

def setWorkshopScope(self, workshop, user, newScope):
    workshopCode = getWorkshopCode(self, workshop)
    import pylowiki.lib.db.workshop as workshopLib
    import pylowiki.lib.db.geoInfo as geoInfoLib
    workshopObj = workshopLib.getWorkshopByCode(workshopCode)
    wscope = geoInfoLib.getWScopeByWorkshop(workshopObj)
    update = 0
    # if no scope set, set it
    if not wscope:
        geoInfoLib.WorkshopScope(workshopObj, newScope)
        wchanges = 1
    # if there's already a scope, and it's different from the current one, change it
    if wscope and wscope['scope'] != newScope:
        geoInfoLib.editWorkshopScope(wscope, newScope)
        # wscope['scope'] = geoTagString
        # dbHelpers.commit(wscope)
        wchanges = 1
    # if there are chagnes, we make sure the workshop is public
    #from pylons import session
    if wchanges:
        workshopObj['public_private'] = 'public'
        import pylowiki.lib.db.dbHelpers as dbHelpers
        dbHelpers.commit(workshopObj)
        weventMsg = "Updated workshop scope."
        from pylowiki.lib.db.user import getUserByEmail
        userObj = getUserByEmail(user['email'])
        import pylowiki.lib.db.event as eventLib
        eventLib.Event('Workshop Config Updated by %s'%user['name'], '%s'%weventMsg, workshopObj, userObj)
        #alert = {'type':'success'}
        #alert['title'] = weventMsg
        #session['alert'] = alert
        #session.save()
    # if not, do nothing
    #else:
        #alert = {'type':'error'}
        #alert['title'] = 'No changes submitted.'
        #session['alert'] = alert
        #session.save()
    # if the shop's being created, save the session
    #if c.w['startTime'] == '0000-00-00':
        #session['confTab'] = "tab3"
        #session.save()

def upgradeToProfessional(self, workshop, user):
    workshopCode = getWorkshopCode(self, workshop)
    import pylowiki.lib.db.workshop as workshopLib
    workshopObj = workshopLib.getWorkshopByCode(workshopCode)
    workshopObj['type'] = 'professional'
    import pylowiki.lib.db.dbHelpers as dbHelpers
    dbHelpers.commit(workshopObj)
    #: now create the account object this workshop needs to be associated with
    import pylowiki.lib.db.account as accountLib
    #: using a mock account function because we're currently not able to use paste to test the stripe payment service
    account = accountLib.AccountTest(user['name'], user['email'], 'stripeToken', workshopObj, 'PRO', 'coupon')