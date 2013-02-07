# -*- coding: utf-8 -*-
from pylowiki.tests import *
from webtest import TestResponse
from routes import url_for

from pylons import config

import pylowiki.tests.helpers.assertions as assertions
import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.link_definitions as linkDefs
from pylowiki.tests.helpers.people import make_user
from pylowiki.tests.helpers.authorization import login, logout
from pylowiki.tests.helpers.registration import create_and_activate_a_user
from pylowiki.tests.helpers.workshops import create_new_workshop, addIdeaToWorkshop, addCommentToIdeaPage

import logging
log = logging.getLogger(__name__)

class TestWorkshopController(TestController):
    """This class tests the various aspects of workshops."""
    #: Can a comment be created?
    #: Can a comment in a private workshop be seen by a user who is not a participant in this workshop?
    #: Can a user who is not a participant in this workshop create a comment in it?
    #: An admin, or a facilitor of a workshop can edit, delete, or make hidden a comment.

    def test_create_a_workshop_user(self):
        """This test creates a workshop as a normal user"""
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = create_new_workshop(self, normalUser, title=workshopTitle)
        
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        
    def test_create_a_workshop_facilitator(self):
        """This test creates a workshop as a facilitator"""
        #: create a user with facilitator access privs
        facilitator = create_and_activate_a_user(self, name='FACILITATOR user', accessLevel='100')
        #: create a workshop
        workshopTitle = 'new workshop by facilitator'
        newWorkshop = create_new_workshop(self, facilitator, title=workshopTitle)
        #: see if this workshop has been created
        assert workshopTitle in newWorkshop, "facilitator not able to create new workshop"

    def test_create_a_workshop_admin(self):
        """This test creates a workshop as an admin"""
        #: create a user with admin access privs
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        #: create a workshop
        workshopTitle = 'new workshop by admin'
        newWorkshop = create_new_workshop(self, admin, title=workshopTitle)
        #: see if this workshop has been created
        assert workshopTitle in newWorkshop, "admin not able to create new workshop"


    def test_create_a_workshop_guest(self):
        """This test creates a workshop as a user who is just a guest of a workshop"""
        #: create a workshop as a normal user
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: go into the settings and invite a guest
        dashboard = newWorkshop.click(href=linkDefs.workshopDashboard())
        privateForm = dashboard.forms[formDefs.workshopSettings_privateForm()]
        # add email of a non-member of this site or workshop, check the 'send invitation' box
        # click the invite email button
        # in the controller - look for the test situation to be on - record the value of the guest invite
        # before continuing as a guest - get a workshop creation form ready
        # prepare form as in function test_create_a_workshop_public()
        # logout, click this link to become a guest onsite for browsing this workshop
        # get on the create workshop form page, fill it in and submit
        # hopefully, this doesn't work!
        assert dashboard == 404
    
    def test_create_a_workshop_public(self):
        """This test tries to create a workshop as a non-logged-in visitor"""
        publicUser = create_and_activate_a_user(self, name='PUBLIC user')
        login(self, publicUser)
        workshopTitle = 'new workshop by public'
        rHome = self.app.get(url=url_for(controller='home', action='index'))
        rWorkshops = rHome.follow()
        # click the profile link
        rProfile = rWorkshops.click(description=linkDefs.profile(), index=0)
        # click the member dashboard link
        rDashboard = rProfile.click(description=linkDefs.profile_edit(), index=0)
        # click the create workshop button
        createWorkshopForm = rDashboard.forms[formDefs.createWorkshop_button()]
        createWorkshop = createWorkshopForm.submit()
        #: we have a choice now for creating a personal or professional workshop
        #: get the form that holds both choices
        whichWorkshopForm = createWorkshop.forms[formDefs.createWorkshop_1_form()]
        params = {}
        #: it is expected that this form has one submit value, the name of the button and its value of ''
        #: for robustness, the loadWithSubmitFields() function is used in case any other submit fields are placed in the future
        params = formHelpers.loadWithSubmitFields(whichWorkshopForm)
        params[formDefs.create_workshop_1_personal_professional()] = content.noChars()
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
                #: we've gone the professional workshop route
                #: In webtest I'm pretty sure it's not possible to use javascript files for the payment handshake that takes place here.
                #: It's possible that Selenium can handle this.
                #: For now, I'll get us to the page past the payment gateway by pressing the 'personal workshop' button
                #: then setting the workshop to be a professional one by calling the backend function.
                #: The personal option has already been selected because for now it's a forced default in 
                #: formDefs.create_workshop_1_personal_professional()
                #: 'upgrade' this workshop to professional:
                # NOTE - do this part            
        #: At this point we have a workshop creation page ready to go. we logout, fill in the form and 
        #: try to submit it to get the workshop published.
        logout(self)
        #: In the normal workshop creation process, each step represents a form submitted. 
        #: In this case we avoid this because you need to be logged in during these steps.
        # start completing workshop form - basic fields
        createWorkshopForm1 = startCreateWorkshop1.forms[formDefs.createWorkshop_2_Basics()]
        formFields1 = createWorkshopForm1.fields
        # fill out the first form for this workshop creation process
        for key in formFields1:
            if formDefs.createWorkshopForm1_title() == key:
                createWorkshopForm1[key] = 'NEW WORKSHOP TITLE'
            elif formDefs.createWorkshopForm1_description() == key:
                createWorkshopForm1[key] = 'NEW WORKSHOP DESCRIPTION'
            elif formDefs.createWorkshopForm1_goals() == key:
                createWorkshopForm1[key] = 'NEW SET OF GOALS'
            elif formDefs.createWorkshopForm1_suggestions() == key:
                # by default, allow workshop participants to add suggestions
                createWorkshopForm1.set(key, formDefs.workshopSettings_allowIdeas(True))
            elif formDefs.createWorkshopForm1_resources() == key:
                # by default, allow workshop participants to add resources
                createWorkshopForm1.set(key, formDefs.workshopSettings_allowResourceLinks(True))

        #startCreateWorkshop2 = createWorkshopForm1.submit().follow()

        #complete workshop form part 2
        createWorkshopForm2 = startCreateWorkshop1.forms[formDefs.createWorkshopForm2()]
        #: private form id="private": (optional) can invite people and include invite message
        #: NOTE for now, nothing happens in this case
        #: public form id="scope": need to set the scope
        #: NOTE creating a public workshop also requires paying for a professional workshop, need to set this up still

        # there are two fields that act as submit buttons:
        # addMember and continueToNext
        #startCreateWorkshop3 = createWorkshopForm2.submit(formDefs.createWorkshopForm2_submit()).follow()
        # add tags to the workshop
        createWorkshopForm3 = startCreateWorkshop1.forms[formDefs.createWorkshopForm3()]
        createWorkshopForm3.set('categoryTags', 'Arts', 0)
        #createWorkshopForm3.set('categoryTags', 'Civil Rights', 2)
        createWorkshopForm3.set('categoryTags', 'Economy', 4)
        #startCreateWorkshop4 = createWorkshopForm3.submit().follow()
        # add slides: add photo, press upload button .. can't get this working in test yet
        createWorkshopSlidesForm = startCreateWorkshop1.forms[formDefs.createWorkshop_FileUploadForm()]
        # <form id="fileupload" class="well" action="/workshop/4ICj/test-title/addImages/handler" method="POST" enctype="multipart/form-data">
        # <input type="file" name="files[]" multiple>
        # <button type="submit" class="btn btn-primary start"><span>Start upload</span></button>
        #createWorkshopSlidesForm['files'] = [(u'files[]', u'fireTime.jpg')]
        # should work if we have python 2.7: createWorkshopSlidesForm['files[]'] = collections.OrderedDict([('files[]', 'fireTime.jpg')])
        #uploadTest = createWorkshopSlidesForm.submit()

        # This is the button at the bottom of the slideshow creation page for proceeding to the next - 
        createWorkshopForm4 = startCreateWorkshop1.forms[formDefs.createWorkshopForm4_continueToNext()]
        #startCreateWorkshop5 = createWorkshopForm4.submit()

        # fill out wiki background: type anything in textarea then submit
        #NOTE wikibackground not updating with new content for startCreateWorkshop6
        createWorkshopForm5 = startCreateWorkshop1.forms[formDefs.createWorkshopForm5_wikiBackground()]
        # recorded post data: _method=put, textarea0=words+some+more+words, submit=, count=1, dashboard=dashboard
        # from the pdb printout of the form in the response: fields: {u'count': [<Hidden name="count" id="count">], u'data': [<Textarea name="data" id="data">], u'dashboard': [<Hidden name="dashboard" id="dashboard">], u'submit': [<Submit name="submit" id="submit">, <Submit name="submit">], u'_method': [<Hidden name="_method">]}
        createWorkshopForm5.set(formDefs.createWorkshopForm5_wikiBackground_text(), 'testing+workshop')

        params = {}
        params = formHelpers.loadWithSubmitFields(createWorkshopForm5)
        params[formDefs.parameter_submit()] = formDefs.createWorkshopForm5_wikiBackground_submit()
        #assert startCreateWorkshop5 == 404
        #: wiki background form not working, have no idea why at this point - skipping if possible
        startCreateWorkshop6 = startCreateWorkshop1
        #startCreateWorkshop6 = self.app.post(
        #    url = str(createWorkshopForm5.action),
        #    params=params
        #).follow()
        # submit_fields(): [(u'count', u'1'), (u'textarea0', u'No wiki background set yet'), (u'dashboard', u'dashboard'), (u'_method', u'put')]    
        
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

        assert assertions.not_in_new_workshop_1() not in workshopCreated, "public user able to access workshop creation page"
        assert workshopTitle not in workshopCreated, "public user able to create workshop"
        

    def test_upgrade_workshop_user(self):
        """This test tries to upgrade a workshop as a normal user"""
        # create a private workshop as a normal user
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        # click the dashboard link
        dashboard = newWorkshop.click(href=linkDefs.workshopDashboard())
        upgradeButton = dashboard.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        paymentForm = paymentPage.forms[formDefs.paymentForm()]
        paymentParams = {}
        paymentParams = formHelpers.fillPaymentForm(paymentForm, name='Tester', email='todd@civinomics.com', test=True)
        workshopUpgraded = self.app.post(
            url=str(paymentForm.action),
            params=paymentParams,
            expect_errors=True
        )
        assert workshopUpgraded.status_int == 404, "spoofed payment page able to be submitted"

    def test_upgrade_workshop_facilitator(self):
        """This test tries to upgrade a workshop as a facilitator"""
        facilitator = create_and_activate_a_user(self, name='FACILITATOR user', accessLevel='100')
        workshopTitle = 'new workshop by facilitator'
        newWorkshop = create_new_workshop(self, facilitator, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: facilitator not able to create new workshop"
        # click the dashboard link
        dashboard = newWorkshop.click(href=linkDefs.workshopDashboard())
        upgradeButton = dashboard.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        paymentForm = paymentPage.forms[formDefs.paymentForm()]
        paymentParams = {}
        paymentParams = formHelpers.fillPaymentForm(paymentForm, name='Tester', email='todd@civinomics.com', test=True)
        workshopUpgraded = self.app.post(
            url=str(paymentForm.action),
            params=paymentParams,
            expect_errors=True
        )
        assert workshopUpgraded.status_int == 404, "spoofed payment page able to be submitted"

    def test_upgrade_workshop_admin(self):
        """This test tries to upgrade a workshop as an admin"""
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        workshopTitle = 'new workshop by admin'
        newWorkshop = create_new_workshop(self, admin, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: admin not able to create new workshop"
        # click the dashboard link
        dashboard = newWorkshop.click(href=linkDefs.workshopDashboard())
        upgradeButton = dashboard.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        paymentForm = paymentPage.forms[formDefs.paymentForm()]
        paymentParams = {}
        paymentParams = formHelpers.fillPaymentForm(paymentForm, name='Tester', email='todd@civinomics.com', test=True)
        workshopUpgraded = self.app.post(
            url=str(paymentForm.action),
            params=paymentParams,
            expect_errors=True
        )
        assert workshopUpgraded.status_int == 404, "spoofed payment page able to be submitted"

    def test_upgrade_workshop_guest(self):
        """This test tries to upgrade a workshop as a guest of a workshop"""

    def test_upgrade_workshop_public(self):
        """This test tries to upgrade a workshop as a non-logged-in visitor"""

    def test_view_private_workshop_listing_page_nonmember_user(self):
        """This test checks to see if a member of the site who is not a member 
        of a private workshop, can see the workshop on the workshop listing page."""

    def test_view_private_workshop_listing_page_member_user(self):
        """This test checks to see if a member of the site who is a member 
        of a private workshop, can see the workshop on the workshop listing page."""

    def test_view_private_workshop_listing_page_nonmember_facilitator(self):
        """This test checks to see if a facilitator on the site who is not a member 
        of a private workshop, can see the workshop on the workshop listing page."""

    def test_view_private_workshop_listing_page_member_facilitator(self):
        """This test checks to see if a facilitator on the site who is a member 
        of a private workshop, can see the workshop on the workshop listing page."""

    def test_view_private_workshop_listing_page_facilitator_facilitator(self):
        """This test checks to see if a facilitator on the site who is a facilitator 
        of a private workshop, can see the workshop on the workshop listing page."""

    def test_view_private_workshop_listing_page_nonmember_admin(self):
        """This test checks to see if an admin of the site who is not a member 
        of a private workshop, can see the workshop on the workshop listing page."""

    def test_view_private_workshop_listing_page_member_admin(self):
        """This test checks to see if an admin of the site who is a member 
        of a private workshop, can see the workshop on the workshop listing page."""

    def test_view_private_workshop_listing_page_nonmember_guest(self):
        """This test checks to see if a guest of the site who is not a member 
        of a private workshop (but is the guest of another), can see the workshop 
        on the workshop listing page."""

    def test_view_private_workshop_listing_page_member_guest(self):
        """This test checks to see if a guest of the site who is a guest of
        the private workshop being tested, can see this workshop 
        on the workshop listing page."""



    