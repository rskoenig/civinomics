# -*- coding: utf-8 -*-
from pylowiki.tests import *
from routes import url_for
import re

import pylowiki.tests.helpers.assertions as assertions
from pylowiki.tests.helpers.authorization import login
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.link_definitions as linkDefs


import logging
log = logging.getLogger(__name__)

def addWorkshopForm():
    return 'create_issue'

def addWorkshopFormName():
    return 'workshopName'


#: create_new_workshop is a helper function for creating a new workshop
def create_new_workshop(self, thisUser, **kwargs):
    """ Logs in as the specified user and creates a new workshop.
    Returns this workshop's main page. """
    #: kwarg options:
    #: allowIdeas = helpers/form_Definitions.workshopSettings_allowIdeas(True/False)
    #:  - setting for allowing participants to add ideas 
    #: allowResourceLinks = helpers/form_Definitions.workshopSettings_allowResourceLinks(True/False)
    #:  - setting for allowing participants to add resource links

    login(self, thisUser)
    # start at the home page, which redirects to the workshops page
    rHome = self.app.get(url=url_for(controller='home', action='index'))
    rWorkshops = rHome.follow()
    # click the profile link
    rProfile = rWorkshops.click(description=linkDefs.profile(), index=0)
    # click the member dashboard link
    rDashboard = rProfile.click(description=linkDefs.member_dashboard(), index=0)
    # click the create workshop button
    createWorkshopForm = rDashboard.forms[formDefs.createWorkshop_button()]
    createWorkshop = createWorkshopForm.submit()
    
    #NOTE we have a choice now for creating a personal or professional workshop
    whichWorkshopForm = createWorkshop.forms[formDefs.createWorkshop()]
    formFields = whichWorkshopForm.fields
    # this form has two submit buttons. the javascript works to set a post field named after the buton
    # that is pressed. this funcion mimics that action.
    for key in formFields:
        thisButton = re.search(formDefs.personal_workshop_button_search(), key)
        #log.info("in form fields finder "+key)
        if thisButton != None:
            log.info("found button "+key)
            # we have the value for the personal button, set it in the form as a post value
            submittedWhichForm = whichWorkshopForm.submit(key)
            startCreateWorkshop1 = submittedWhichForm.follow()
            # we have entered either a personal or professional workshop creation now
            break
        #log.info("I am inside the for loop")
    #log.info("I am outside the for loop")

    # start completing workshop form - basic fields
    createWorkshopForm1 = startCreateWorkshop1.forms[formDefs.createWorkshopForm1()]
    formFields1 = createWorkshopForm1.fields
    # fill out the first form for this workshop creation process
    for key in formFields1:
        log.info("createWorkshopForm1 key: %s"%key)
        if formDefs.createWorkshopForm1_title() == key:
            createWorkshopForm1[key] = 'test title'
        elif formDefs.createWorkshopForm1_description() == key:
            createWorkshopForm1[key] = 'test description'
        elif formDefs.createWorkshopForm1_goals() == key:
            createWorkshopForm1[key] = 'goals'
        elif formDefs.createWorkshopForm1_suggestions() == key:
            if 'allowIdeas' in kwargs:
                createWorkshopForm1.set(key, kwargs['allowIdeas'])
            else:
                # by default, allow workshop participants to add suggestions
                createWorkshopForm1.set(key, formDefs.workshopSettings_allowIdeas(True))
        elif formDefs.createWorkshopForm1_resources() == key:
            if 'allowResourceLinks' in kwargs:
                createWorkshopForm1.set(key, kwargs['allowResourceLinks'])
            else:
                # by default, allow workshop participants to add resources
                createWorkshopForm1.set(key, formDefs.workshopSettings_allowResourceLinks(True))

    startCreateWorkshop2 = createWorkshopForm1.submit().follow()

    #complete workshop form part 2
    if 'private' in kwargs:
        createWorkshopForm2 = startCreateWorkshop2.forms[formDefs.createWorkshopForm2(kwargs['private'])]
    else:
        createWorkshopForm2_submit = startCreateWorkshop2.forms[formDefs.createWorkshopForm2()]
    #: private form id="private": (optional) can invite people and include invite message
    #: NOTE for now, nothing happens in this case
    #: public form id="scope": need to set the scope
    #: NOTE creating a public workshop also requires paying for a professional workshop, need to set this up still

    # there are two fields that act as submit buttons:
    # addMember and continueToNext
    startCreateWorkshop3 = createWorkshopForm2.submit(formDefs.createWorkshopForm2_submit()).follow()
    # add tags to the workshop
    createWorkshopForm3 = startCreateWorkshop3.forms[formDefs.createWorkshopForm3()]
    createWorkshopForm3.set('categoryTags', 'Arts', 0)
    createWorkshopForm3.set('categoryTags', 'Civil Rights', 2)
    createWorkshopForm3.set('categoryTags', 'Economy', 4)
    startCreateWorkshop4 = createWorkshopForm3.submit().follow()
    # add slides: add photo, press upload button .. can't get this working in test yet
    createWorkshopSlidesForm = startCreateWorkshop4.forms[formDefs.createWorkshop_FileUploadForm()]
    # <form id="fileupload" class="well" action="/workshop/4ICj/test-title/addImages/handler" method="POST" enctype="multipart/form-data">
    # <input type="file" name="files[]" multiple>
    # <button type="submit" class="btn btn-primary start"><span>Start upload</span></button>
    #createWorkshopSlidesForm['files'] = [(u'files[]', u'fireTime.jpg')]
    # should work if we have python 2.7: createWorkshopSlidesForm['files[]'] = collections.OrderedDict([('files[]', 'fireTime.jpg')])
    #uploadTest = createWorkshopSlidesForm.submit()

    # This is the button at the bottom of the slideshow creation page for proceeding to the next - 
    createWorkshopForm4 = startCreateWorkshop4.forms[formDefs.createWorkshopForm4_continueToNext()]
    startCreateWorkshop5 = createWorkshopForm4.submit()
    # fill out wiki background: type anything in textarea then submit
    #NOTE wikibackground not updating with new content for startCreateWorkshop6
    createWorkshopForm5 = startCreateWorkshop5.forms[formDefs.createWorkshopForm5_wikiBackground()]
    # recorded post data: _method=put, textarea0=words+some+more+words, submit=, count=1, dashboard=dashboard
    # from the pdb printout of the form in the response: fields: {u'count': [<Hidden name="count" id="count">], u'textarea0': [<Textarea name="textarea0" id="textarea0">], u'dashboard': [<Hidden name="dashboard" id="dashboard">], u'submit': [<Submit name="submit" id="submit">, <Submit name="submit">], u'_method': [<Hidden name="_method">]}
    createWorkshopForm5.set(formDefs.createWorkshopForm5_wikiBackground_text(), 'testing+workshop')
    # submit_fields(): [(u'count', u'1'), (u'textarea0', u'No wiki background set yet'), (u'dashboard', u'dashboard'), (u'_method', u'put')]
    startCreateWorkshop6 = createWorkshopForm5.submit().follow()
    # because we haven't created a slide for the slideshow, the publish form will not display. this is the form:
    # <form name="edit_issue" id="edit_issue" class="left form-inline" 
    # action = "/workshop/${c.w['urlCode']}/${c.w['url']}/configureStartWorkshopHandler" 
    # enctype="multipart/form-data" method="post" >
    # So, instead we will post to this address on our own
    #startCreateWorkshop6.request.url == http://localhost/workshop/4ICj/test-title/configureContinueHandler
    workshopUrl = startCreateWorkshop6.request.url
    urlParts = workshopUrl.split('/')
    
    url_index = len(urlParts)-2
    this_url = urlParts[url_index]
    
    urlCode_index = len(urlParts)-3
    this_urlCode = urlParts[urlCode_index]
    
    workshopCreated = self.app.post(
        url='/workshop/%s/%s/configureStartWorkshopHandler'%(this_urlCode,this_url), 
        content_type='multipart/form-data',
        params={'name' : 'startWorkshop'}
    ).follow()

    #assert startCreateWorkshop6 == 404
    assert assertions.not_in_new_workshop_1() not in workshopCreated
    assert assertions.in_new_workshop_1() in workshopCreated
    assert assertions.in_new_workshop_2() in workshopCreated

    #return workshopCreated.response.url
    return workshopCreated






