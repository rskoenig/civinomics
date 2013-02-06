# -*- coding: utf-8 -*-
from pylowiki.tests import *
from webtest import TestResponse
from routes import url_for

from pylons import config

from pylowiki.tests.helpers.people import make_user
from pylowiki.tests.helpers.authorization import login, logout
from pylowiki.tests.helpers.registration import create_and_activate_a_user
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
        #: instead of a workshop that's already been created
        workshopStartUrl = workshop.create_new_workshop(self, normalUser, title=guestTitle, dontCreateWorkshop=True)
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
        login(self, publicUser)
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
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: go into the settings and click the upgrade button
        dashboard = newWorkshop.click(href=linkDefs.workshopDashboard())
        upgradeButton = dashboard.forms[formDefs.upgradeWorkshop()]
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
        dashboard = newWorkshop.click(href=linkDefs.workshopDashboard())
        upgradeButton = dashboard.forms[formDefs.upgradeWorkshop()]
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
        dashboard = newWorkshop.click(href=linkDefs.workshopDashboard())
        upgradeButton = dashboard.forms[formDefs.upgradeWorkshop()]
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
        dashboard = newWorkshop.click(href=linkDefs.workshopDashboard())
        upgradeButton = dashboard.forms[formDefs.upgradeWorkshop()]
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
        )
        #: unless we see an error, the workshop may have been upgraded
        assert workshopUpgraded.status_int == 404, "spoofed payment page able to be submitted by guest"
        assert assertions.workshop_upgraded() not in workshopUpgraded

    def test_upgrade_workshop_public(self):
        """This test tries to upgrade a workshop as a non-logged-in visitor"""
        #: create a workshop
        normalUser = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: go into the settings and click the upgrade button
        dashboard = newWorkshop.click(href=linkDefs.workshopDashboard())
        upgradeButton = dashboard.forms[formDefs.upgradeWorkshop()]
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
        )
        #: unless we see an error, the workshop may have been upgraded
        assert workshopUpgraded.status_int == 404, "spoofed payment page able to be submitted by public"
        assert assertions.workshop_upgraded() not in workshopUpgraded

    def test_view_private_workshop_listing_page_nonmember_user(self):
        """This test checks to see if a member of the site who is not a member 
        of a private workshop, can see the workshop on the workshop listing page."""
        #: create a workshop
        workshopOwner = create_and_activate_a_user(self)
        workshopTitle = 'new workshop by user'
        newWorkshop = workshop.create_new_workshop(self, workshopOwner, title=workshopTitle)
        assert workshopTitle in newWorkshop, "failure before tst complete: normal user not able to create new workshop"
        #: visit the listing page and see that it's there

    def test_view_private_workshop_listing_page_member_user(self):
        """This test checks to see if a member of the site who is a member 
        of a private workshop, can see the workshop on the workshop listing page."""

    def test_view_private_workshop_listing_page_nonmember_facilitator(self):
        """This test checks to see if a facilitator of a workshop, who is not a member 
        of this private workshop, can see this workshop on the workshop listing page."""

    def test_view_private_workshop_listing_page_member_facilitator(self):
        """This test checks to see if a facilitator of a workshop can see this workshop
        on the workshop listing page."""

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

    def test_view_private_workshop_listing_page_public(self):
        """This test checks to see if a non-logged-in visitor to the site can see a
        private workshop on the workshop listing page."""

    