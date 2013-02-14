# -*- coding: utf-8 -*-
from pylowiki.tests import *
from webtest import TestResponse
from routes import url_for

from pylons import config

from pylowiki.tests.helpers.people import make_user
from pylowiki.tests.helpers.authorization import login, logout
from pylowiki.tests.helpers.registration import create_and_activate_a_user
import pylowiki.tests.helpers.authorization as auth
import pylowiki.tests.helpers.assertions as assertions
import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.link_definitions as linkDefs
import pylowiki.tests.helpers.workshops as workshop

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
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        
    def test_create_a_workshop_facilitator(self):
        """This test creates a workshop as a facilitator. While this method of creating a 
        facilitator is deprecated, it is still one unique way to see if things are working."""
        #: create a user with facilitator access privs
        facilitator = create_and_activate_a_user(self, name='FACILITATOR user', accessLevel='100')
        #: create a workshop
        workshopTitle = 'new workshop by facilitator'
        newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
        #: see if this workshop has been created
        assert workshopTitle in newWorkshop, "facilitator not able to create new workshop"

    def test_create_a_workshop_admin(self):
        """This test creates a workshop as an admin"""
        #: create a user with admin access privs
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        #: create a workshop
        workshopTitle = 'new workshop by admin'
        newWorkshop = workshop.create_new_workshop(self, admin, title=workshopTitle)
        #: see if this workshop has been created
        assert workshopTitle in newWorkshop, "admin not able to create new workshop"


    def test_create_a_workshop_guest(self):
        """This test creates a workshop as a user who is just a guest of a workshop"""
        #: create a workshop as a normal user
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: go into the settings and invite a guest
        guestLink = workshop.inviteGuest(self, newWorkshop, guestLink=True)
        #: get a new workshop form ready
        guestTitle = 'new workshop by guest'
        #: create a new workshop but pass the dontCreateWorkshop param to get the completed form, 
        #: instead of a workshop that's already been created. Note that the login=False parameter is needed,
        #: since the user is already logged in this needs to be passed or else the create_new_workshop function
        #: will try to log in as this person and this causes 
        workshopStartUrl = workshop.create_new_workshop(self, normalUser, title=guestTitle, login=False, dontCreateWorkshop=True)
        #: logout (note: comment this line out including another one below to test that this would work for normalUser)
        logout(self)
        #: visit the browse link in order to enter the site as a guest
        #: (note: comment this line out to test that this would work for normalUser)
        #inviteSent.browseUrl
        visitAsGuest = self.app.get(url=guestLink)
        #: try to submit the start workshop command for this workshop that has already been prepared
        workshopCreated = self.app.post(
            url=workshopStartUrl, 
            content_type='multipart/form-data',
            params={'name' : 'startWorkshop'}
        ).follow()
        #: if guest user is denied, we will see the home page of the site, not a workshop with guestTitle in it
        #: note: in the case the two lines above are commented out, switch the logic of these two assertions in order to get a successful test
        assert assertions.booted_to_front_page_1() in workshopCreated, "guest user not booted from workshop creation page"
        assert guestTitle not in workshopCreated, "guest user able to create workshop"
    
    def test_create_a_workshop_public(self):
        """This test tries to create a workshop as a non-logged-in visitor"""
        #: create a user
        publicUser = create_and_activate_a_user(self, name='PUBLIC user')
        publicTitle = 'new workshop by public'
        #: create a new workshop but pass the dontCreateWorkshop param to get the completed form, 
        #: instead of a workshop that's already been created
        workshopStartUrl = workshop.create_new_workshop(self, publicUser, title=publicTitle, dontCreateWorkshop=True)
        #: logout (note: comment this line out including another one below to test that this would work for normalUser)
        logout(self)
        #: now, try to submit the start workshop command for this workshop that has already been prepared
        workshopCreated = self.app.post(
            url=workshopStartUrl, 
            content_type='multipart/form-data',
            params={'name' : 'startWorkshop'}
        ).follow()
        #: if public visitor is denied, we will see the home page of the site, not a workshop with publicTitle in it
        assert assertions.booted_to_front_page_1() in workshopCreated, "public visitor not booted from workshop creation page"
        assert publicTitle not in workshopCreated, "public visitor able to create workshop"        

    def test_upgrade_workshop_user(self):
        """This test tries to upgrade a workshop as a normal user"""
        # create a private workshop as a normal user
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before test complete: normal user not able to create new workshop"
        #: go into the settings and click the upgrade button
        # this used to work, may again but for now it doesn't
        #dashboard = workshop.click(href=linkDefs.workshopDashboard(), verbose=True)
        preferences = workshop.getWorkshopPreferencesPage(self, newWorkshop)
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: fill out the payment form with info that would make for a completed form. include a spoof token value
        paymentForm = paymentPage.forms[formDefs.paymentForm()]
        paymentParams = {}
        paymentParams = formHelpers.fillPaymentForm(paymentForm, name='Tester', email='todd@civinomics.com', test=True)
        workshopUpgraded = self.app.post(
            url=str(paymentForm.action),
            params=paymentParams,
            expect_errors=True
        )
        #: unless we see an error, the workshop may have been upgraded
        assert workshopUpgraded.status_int == 404, "spoofed payment page able to be submitted"
        assert assertions.workshop_upgraded() not in workshopUpgraded

    def test_upgrade_workshop_facilitator(self):
        """This test tries to upgrade a workshop as a facilitator"""
        #: create a workshop as a facilitator
        facilitator = create_and_activate_a_user(self, name='FACILITATOR user', accessLevel='100')
        workshopTitle = 'new workshop by facilitator'
        newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: facilitator not able to create new workshop"
        #: go into the settings and click the upgrade button
        #dashboard = workshop.click(href=linkDefs.workshopDashboard(), verbose=True)
        preferences = workshop.getWorkshopPreferencesPage(self, newWorkshop)
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: fill out the payment form with info that would make for a completed form. include a spoof token value
        paymentForm = paymentPage.forms[formDefs.paymentForm()]
        paymentParams = {}
        paymentParams = formHelpers.fillPaymentForm(paymentForm, name='Tester', email='todd@civinomics.com', test=True)
        workshopUpgraded = self.app.post(
            url=str(paymentForm.action),
            params=paymentParams,
            expect_errors=True
        )
        #: unless we see an error, the workshop may have been upgraded
        assert workshopUpgraded.status_int == 404, "spoofed payment page able to be submitted"
        assert assertions.workshop_upgraded() not in workshopUpgraded

    def test_upgrade_workshop_admin(self):
        """This test tries to upgrade a workshop as an admin"""
        #: create a workshop as an admin
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        workshopTitle = 'new workshop by admin'
        newWorkshop = workshop.create_new_workshop(self, admin, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: admin not able to create new workshop"
        #: go into the settings and click the upgrade button
        #dashboard = workshop.click(href=linkDefs.workshopDashboard(), verbose=True)
        preferences = workshop.getWorkshopPreferencesPage(self, newWorkshop)
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: fill out the payment form with info that would make for a completed form. include a spoof token value
        paymentForm = paymentPage.forms[formDefs.paymentForm()]
        paymentParams = {}
        paymentParams = formHelpers.fillPaymentForm(paymentForm, name='Tester', email='todd@civinomics.com', test=True)
        workshopUpgraded = self.app.post(
            url=str(paymentForm.action),
            params=paymentParams,
            expect_errors=True
        )
        #: unless we see an error, the workshop may have been upgraded
        assert workshopUpgraded.status_int == 404, "spoofed payment page able to be submitted"
        assert assertions.workshop_upgraded() not in workshopUpgraded

    def test_upgrade_workshop_guest(self):
        """This test tries to upgrade a workshop as a guest of a workshop"""
        #: create a workshop
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: invite a guest to this workshop, recording the guest link
        guestLink = workshop.inviteGuest(self, newWorkshop, guestLink=True)
        #: go into the settings and click the upgrade button
        #dashboard = workshop.click(href=linkDefs.workshopDashboard(), verbose=True)
        preferences = workshop.getWorkshopPreferencesPage(self, newWorkshop)
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: fill out the payment form with info that would make for a completed form. include a spoof token value
        paymentForm = paymentPage.forms[formDefs.paymentForm()]
        paymentParams = {}
        paymentParams = formHelpers.fillPaymentForm(paymentForm, name='Tester', email='todd@civinomics.com', test=True)
        #: logout as a normal user and visit the site as a guest
        logout(self)
        visitAsGuest = self.app.get(url=guestLink)
        #: submit the spoofed payment form
        workshopUpgraded = self.app.post(
            url=str(paymentForm.action),
            params=paymentParams,
            expect_errors=True
        ).follow()
        #: unless we see an error, the workshop may have been upgraded
        assert assertions.booted_to_front_page_1() in workshopUpgraded, "spoofed payment page able to be submitted by public"
        assert assertions.workshop_upgraded() not in workshopUpgraded, "spoofed payment page able to upgrade workshop"

    def test_upgrade_workshop_public(self):
        """This test tries to upgrade a workshop as a non-logged-in visitor"""
        #: create a workshop
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: go into the settings and click the upgrade button
        #dashboard = workshop.click(href=linkDefs.workshopDashboard(), verbose=True)
        preferences = workshop.getWorkshopPreferencesPage(self, newWorkshop)
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: fill out the payment form with info that would make for a completed form. include a spoof token value
        paymentForm = paymentPage.forms[formDefs.paymentForm()]
        paymentParams = {}
        paymentParams = formHelpers.fillPaymentForm(paymentForm, name='Tester', email='todd@civinomics.com', test=True)
        #: logout
        logout(self)
        #: submit the spoofed payment form
        workshopUpgraded = self.app.post(
            url=str(paymentForm.action),
            params=paymentParams,
            expect_errors=True
        ).follow()
        #: unless we see an error, the workshop may have been upgraded
        assert assertions.booted_to_front_page_1() in workshopUpgraded, "spoofed payment page able to be submitted by public"
        assert assertions.workshop_upgraded() not in workshopUpgraded, "spoofed payment page able to upgrade workshop"

    def test_view_private_workshop_listing_page_nonmember_user(self):
        """This test checks to see if a member of the site who is not a member 
        of a private workshop, can see the workshop on the workshop listing page."""
        #: create a workshop
        workshopOwner = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, workshopOwner, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: now create another user and look at the listing page to see if this workshop is there
        logout(self)
        nonMember = create_and_activate_a_user(self)
        login(self, nonMember)
        workshopListingPage = workshop.getWorkshopListingPage(self)
        #: look for the title of this workshop on the page
        assert workshopTitle not in workshopListingPage, "private workshop viewable on listing page by member of site who is not member of said workshop"

    def test_view_private_workshop_listing_page_member_user(self):
        """This test checks to see if a member of the site who is a member 
        of a private workshop, can see the workshop on the workshop listing page.
        This encompasses viewing this 'as a facilitator' of the workshop, since a 
        user who creates a workshop is automatically a facilitator of that workshop."""
        #: create a workshop
        workshopOwner = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, workshopOwner, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        workshopListingPage = workshop.getWorkshopListingPage(self)
        #: look for the title of this workshop on the page
        assert workshopTitle not in workshopListingPage, "private workshop viewable on listing page by creator of said workshop"

    def test_view_private_workshop_listing_page_nonmember_facilitator(self):
        """This test checks to see if a facilitator of a workshop, who is not a member 
        of this private workshop, can see this workshop on the workshop listing page."""
        """This test checks to see if a member of the site who is a member 
        of a private workshop, can see the workshop on the workshop listing page."""
        #: create a workshop under one user
        workshopOwner = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, workshopOwner, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: user not able to create new workshop"
        logout(self)
        #: create a workshop as another user
        ownerOfOtherWorkshop = create_and_activate_a_user(self)
        otherWorkshopTitle = 'new workshop by other user'
        otherWorkshop = workshop.create_new_workshop(self, ownerOfOtherWorkshop, title=otherWorkshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: user not able to create new workshop"
        #: now this 'other' user is also a facilitator of a workshop. can this user see the other user's workshop in the listing page?
        workshopListingPage = workshop.getWorkshopListingPage(self)
        #: look for the title of this workshop on the page
        assert workshopTitle not in workshopListingPage, "private workshop viewable on listing page by creator of a different private workshop"

    def test_view_private_workshop_listing_page_nonmember_admin(self):
        """This test checks to see if an admin of the site who is not a member 
        of a private workshop, can see the workshop on the workshop listing page."""
        #: create a workshop under one user
        workshopOwner = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, workshopOwner, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: user not able to create new workshop"
        logout(self)
        #: login as an admin
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        auth.login(self, admin)
        #: can an admin see the other user's workshop in the listing page?
        workshopListingPage = workshop.getWorkshopListingPage(self)
        #: look for the title of this workshop on the page
        assert workshopTitle not in workshopListingPage, "private workshop viewable on listing page by admin"

    def test_view_private_workshop_listing_page_member_admin(self):
        """This test checks to see if an admin of the site who is a member 
        of a private workshop, can see the workshop on the workshop listing page."""
        #: create a workshop under one user
        workshopOwner = create_and_activate_a_user(self)
        #: create an admin that will be a member of this workshop
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, workshopOwner, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: user not able to create new workshop"
        #: invite the admin to be a part of it
        workshop.inviteGuest(self, newWorkshop, dontSendInvite=True, email=admin['email'])
        #: login as the admin
        auth.logout(self)
        auth.login(self, admin)
        #: can an admin, invited to be a part of this workshop, see it on the listing page?
        workshopListingPage = workshop.getWorkshopListingPage(self)
        #: look for the title of this workshop on the page
        assert workshopTitle not in workshopListingPage, "private workshop viewable on listing page by admin who is part of the workshop"

    def test_view_private_workshop_listing_page_nonmember_guest(self):
        """This test checks to see if a guest of the site who is not a member 
        of a private workshop (but is the guest of another), can see the workshop 
        on the workshop listing page."""
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: go into the settings and invite a guest. we will use this link at the end of the test
        guestLink = workshop.inviteGuest(self, newWorkshop, guestLink=True)
        #: logout, create a new user, create a workshop, see if the guest of the other workshop can see this one
        auth.logout(self)
        nextUser = create_and_activate_a_user(self)
        nextWorkshopTitle = 'next workshop by next user'
        nextWorkshop = workshop.create_new_workshop(self, nextUser, title=nextWorkshopTitle)
        assert nextWorkshopTitle in nextWorkshop, "failure before tst complete: normal user not able to create new workshop"
        auth.logout(self)
        #: visit the browse link in order to enter the site as a guest
        visitAsGuest = self.app.get(url=guestLink)
        #: can a guest, invited to be a part of a different workshop, see nextWorkshop on the listing page?
        workshopListingPage = workshop.getWorkshopListingPage(self)
        #: look for the title of this workshop on the page
        assert nextWorkshopTitle not in workshopListingPage, "private workshop viewable on listing page by guest, invited to be part of a different workshop"

    def test_view_private_workshop_listing_page_member_guest(self):
        """This test checks to see if a guest of the site who is a guest of
        the private workshop being tested, can see this workshop 
        on the workshop listing page."""
        """This test checks to see if a guest of the site who is not a member 
        of a private workshop (but is the guest of another), can see the workshop 
        on the workshop listing page."""
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: go into the settings and invite a guest. we will use this link at the end of the test
        guestLink = workshop.inviteGuest(self, newWorkshop, guestLink=True)
        #: logout, create a new user, create a workshop, see if the guest of the other workshop can see this one
        auth.logout(self)
        nextUser = create_and_activate_a_user(self)
        nextWorkshopTitle = 'next workshop by next user'
        nextWorkshop = workshop.create_new_workshop(self, nextUser, title=nextWorkshopTitle)
        assert nextWorkshopTitle in nextWorkshop, "failure before tst complete: normal user not able to create new workshop"
        auth.logout(self)
        #: visit the browse link in order to enter the site as a guest
        visitAsGuest = self.app.get(url=guestLink)
        #: can a guest, invited to be a part of a different workshop, see nextWorkshop on the listing page?
        workshopListingPage = workshop.getWorkshopListingPage(self)
        #: look for the title of this workshop on the page
        assert nextWorkshopTitle not in workshopListingPage, "private workshop viewable on listing page by guest, invited to be part of a different workshop"

    def test_view_private_workshop_listing_page_public(self):
        """This test checks to see if a non-logged-in visitor to the site can see a
        private workshop on the workshop listing page."""
        #: create a workshop
        workshopOwner = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, workshopOwner, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        auth.logout(self)
        workshopListingPage = workshop.getWorkshopListingPage(self)
        #: look for the title of this workshop on the page
        assert workshopTitle not in workshopListingPage, "private workshop viewable on listing page by the public"

    def test_view_public_workshop(self):        
        """This test creates a user, who creates a workshop, then the workshop is set as public."""
        #: create a workshop
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, normalUser)
        #: the scope needs to be set before it will show up in the 'list all' page
        scope = {}
        #: ||united-states||california||santa-cruz||santa-cruz|95060
        scope = workshop.createScope(self, state='california', county='santa-cruz', city='santa-cruz', postal='95060')

        workshop.setWorkshopScope(self, newWorkshop, normalUser, scope)

        reloadWorkshop = self.app.get(url=newWorkshop.request.url)
        
        assert reloadWorkshop == 404


