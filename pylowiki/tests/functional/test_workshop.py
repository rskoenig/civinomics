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
import pylowiki.tests.helpers.page_definitions as pageDefs
import pylowiki.tests.helpers.workshops as workshop

import logging
log = logging.getLogger(__name__)

class TestWorkshopController(TestController):
    """This class tests the various aspects of workshops."""

    """ Finish the postal scope test """

    def test_workshop_complimentary_upgrade_admin(self):
        """ Test that a 'complimentary upgrade' by an admin will work for the user. """
        #: create a user
        #: create a private workshop as this user
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'private workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: logout
        logout(self)
        #: create an admin
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        #: login as this admin
        login(self, admin)
        #: go to this user's private workshop
        adminSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        #: go to the preferences
        preferences = workshop.getWorkshopPreferencesPage(self, adminSeeWorkshop)
        #: click the upgrade button
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: click the 'complimentary upgrade' button
        compUpgradeForm = paymentPage.forms[formDefs.paymentFormAdminUpgrade()]
        upgradeParams = {}
        upgradeParams = formHelpers.loadWithSubmitFields(compUpgradeForm)
        upgradeParams[formDefs.paymentFormAdminUpgradeSubmitName()] = ''
        workshopUpgraded = self.app.post(
            url=str(compUpgradeForm.action),
            params=upgradeParams
        ).follow()
        #: the workshop is now upgraded. how do we tell? log in as the owner of the workshop
        #: and do something you can only do with a professional workshop
        logout(self)
        #: login as user
        login(self, normalUser)
        #: visit this workshop and confirm it is now upgraded
        normalUserSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        #: how to tell on workshop's page? Not sure.
        #: how to tell on preferences page?
        #:  - there is no upgrade to professional button
        preferencePage = workshop.getWorkshopPreferencesPage(self, normalUserSeeWorkshop)
        assert formDefs.upgradeWorkshop() not in preferencePage, "workshop was not upgraded with comp upgrade action by admin"
        
    def test_workshop_complimentary_upgrade_facilitator(self):
        """ Test that a 'complimentary upgrade' by a faciltator will not work. 
        Prepare the spoof by getting the form ready as an admin, then logging in as a facilitator."""
        #: create a user
        #: create a private workshop as this user
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'private workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: logout
        logout(self)
        #: create an admin
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        #: login as this admin
        login(self, admin)
        #: go to this user's private workshop
        adminSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        #: go to the preferences
        preferences = workshop.getWorkshopPreferencesPage(self, adminSeeWorkshop)
        #: click the upgrade button
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: now we have the 'complimentary upgrade' form we need for trying this. before
        #: pressing it, we will log back in as the owner of this workshop
        logout(self)
        login(self, normalUser)
        #: click the 'complimentary upgrade' button
        compUpgradeForm = paymentPage.forms[formDefs.paymentFormAdminUpgrade()]
        upgradeParams = {}
        upgradeParams = formHelpers.loadWithSubmitFields(compUpgradeForm)
        upgradeParams[formDefs.paymentFormAdminUpgradeSubmitName()] = ''
        #: we hope this will not work
        workshopUpgraded = self.app.post(
            url=str(compUpgradeForm.action),
            params=upgradeParams
        )
        #: currently, the appropriate response will be to reload the payment page, without the
        #: 'complimentary payment' button present.
        assert formDefs.paymentFormAdminUpgrade() not in workshopUpgraded, "complimentary upgrade button present on facilitator's payment page"
        #: if the workshop is actually upgraded. how do we tell?
        #:  - there is no 'upgrade to professional' button on the preferences page
        normalUserSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        preferencePage = workshop.getWorkshopPreferencesPage(self, normalUserSeeWorkshop)
        assert formDefs.upgradeWorkshop() in preferencePage, "workshop was upgraded with comp upgrade action by facilitator"

    def test_workshop_complimentary_upgrade_user(self):
        """ Test that a 'complimentary upgrade' by a user will not work. 
        Prepare the spoof by getting the form ready as an admin, then logging in as a user."""
        #: create a user
        #: create a private workshop as this user
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'private workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: logout
        logout(self)
        #: create an admin
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        #: login as this admin
        login(self, admin)
        #: go to this user's private workshop
        adminSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        #: go to the preferences
        preferences = workshop.getWorkshopPreferencesPage(self, adminSeeWorkshop)
        #: click the upgrade button
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: now we have the 'complimentary upgrade' form we need for trying this. before
        #: pressing it, we will log back in as the owner of this workshop
        logout(self)
        notWorkshopOwner = create_and_activate_a_user(self)
        login(self, notWorkshopOwner)
        #: click the 'complimentary upgrade' button
        compUpgradeForm = paymentPage.forms[formDefs.paymentFormAdminUpgrade()]
        upgradeParams = {}
        upgradeParams = formHelpers.loadWithSubmitFields(compUpgradeForm)
        upgradeParams[formDefs.paymentFormAdminUpgradeSubmitName()] = ''
        #: we hope this will not work
        workshopUpgraded = self.app.post(
            url=str(compUpgradeForm.action),
            params=upgradeParams
        )
        #: currently, the appropriate response will be to reload the payment page, without the
        #: 'complimentary payment' button present.
        assert formDefs.paymentFormAdminUpgrade() not in workshopUpgraded, "complimentary upgrade button present on user's payment page"
        #: if the workshop is actually upgraded. how do we tell?
        #:  - there is no 'upgrade to professional' button on the preferences page
        #: we must log back in as the owner of this workshop in order to test this
        logout(self)
        login(self, normalUser)
        normalUserSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        preferencePage = workshop.getWorkshopPreferencesPage(self, normalUserSeeWorkshop)
        assert formDefs.upgradeWorkshop() in preferencePage, "workshop was upgraded with comp upgrade action by user"

    def test_workshop_complimentary_upgrade_guest(self):
        """ Test that a 'complimentary upgrade' by a guest will not work. 
        Prepare the spoof by getting the form ready as an admin, then logging in as a guest."""
        #: create a user
        #: create a private workshop as this user
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'private workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: go into the settings and invite a guest
        guestLink = workshop.inviteGuest(self, newWorkshop, guestLink=True)
        #: logout
        logout(self)
        #: create an admin
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        #: login as this admin
        login(self, admin)
        #: go to this user's private workshop
        adminSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        #: go to the preferences
        preferences = workshop.getWorkshopPreferencesPage(self, adminSeeWorkshop)
        #: click the upgrade button
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: now we have the 'complimentary upgrade' form we need for trying this. before
        #: pressing it, we will log back in as a guest of this workshop
        logout(self)
        visitAsGuest = self.app.get(url=guestLink)
        #: click the 'complimentary upgrade' button
        compUpgradeForm = paymentPage.forms[formDefs.paymentFormAdminUpgrade()]
        upgradeParams = {}
        upgradeParams = formHelpers.loadWithSubmitFields(compUpgradeForm)
        upgradeParams[formDefs.paymentFormAdminUpgradeSubmitName()] = ''
        #: we hope this will not work
        workshopUpgraded = self.app.post(
            url=str(compUpgradeForm.action),
            params=upgradeParams
        )
        #: currently, the appropriate response will be to reload the payment page, without the
        #: 'complimentary payment' button present.
        assert formDefs.paymentFormAdminUpgrade() not in workshopUpgraded, "complimentary upgrade button present on workshop's payment page, guest viewing it"
        #: if the workshop is actually upgraded. how do we tell?
        #:  - there is no 'upgrade to professional' button on the preferences page
        #: we must log back in as the owner of this workshop in order to test this
        logout(self)
        login(self, normalUser)
        normalUserSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        preferencePage = workshop.getWorkshopPreferencesPage(self, normalUserSeeWorkshop)
        assert formDefs.upgradeWorkshop() in preferencePage, "workshop was upgraded with comp upgrade action by guest"

    def test_workshop_complimentary_upgrade_public(self):
        """ Test that a 'complimentary upgrade' by a public visitor will not work. 
        Prepare the spoof by getting the form ready as an admin, then logging in as a user."""
        #: create a user
        #: create a private workshop as this user
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'private workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: logout
        logout(self)
        #: create an admin
        admin = create_and_activate_a_user(self, name='ADMIN user', accessLevel='200')
        #: login as this admin
        login(self, admin)
        #: go to this user's private workshop
        adminSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        #: go to the preferences
        preferences = workshop.getWorkshopPreferencesPage(self, adminSeeWorkshop)
        #: click the upgrade button
        upgradeButton = preferences.forms[formDefs.upgradeWorkshop()]
        paymentPage = upgradeButton.submit()
        #: now we have the 'complimentary upgrade' form we need for trying this. before
        #: pressing it, we will log out in order to test this action as a public visitor
        logout(self)
        #: click the 'complimentary upgrade' button
        compUpgradeForm = paymentPage.forms[formDefs.paymentFormAdminUpgrade()]
        upgradeParams = {}
        upgradeParams = formHelpers.loadWithSubmitFields(compUpgradeForm)
        upgradeParams[formDefs.paymentFormAdminUpgradeSubmitName()] = ''
        #: we hope this will not work
        workshopUpgraded = self.app.post(
            url=str(compUpgradeForm.action),
            params=upgradeParams
        )
        #: currently, the appropriate response will be to reload the payment page, without the
        #: 'complimentary payment' button present.
        assert formDefs.paymentFormAdminUpgrade() not in workshopUpgraded, "complimentary upgrade button present on user's payment page"
        #: if the workshop is actually upgraded. how do we tell?
        #:  - there is no 'upgrade to professional' button on the preferences page
        #: we must log back in as the owner of this workshop in order to test this
        login(self, normalUser)
        normalUserSeeWorkshop = self.app.get(url=newWorkshop.request.url)
        preferencePage = workshop.getWorkshopPreferencesPage(self, normalUserSeeWorkshop)
        assert formDefs.upgradeWorkshop() in preferencePage, "workshop was upgraded with comp upgrade action by user"

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
        #: ||united-states||california||santa-cruz||santa-cruz|95060
        #: load a scoping object
        # default: state='california', county='santa-cruz', city='santa-cruz', postal='95060'
        scopeDict = {}
        scopeDict = content.scopeDict()
        #: create the scope string
        scopeString = workshop.createScope(self, state=scopeDict['state'], county=scopeDict['county'], city=scopeDict['city'], postal=scopeDict['postal'])
        #: set the workshop's scope
        workshop.setWorkshopScope(self, newWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, normalUser)
        #: now by reloading the workshop page, we will have a scope string present
        reloadWorkshop = self.app.get(url=newWorkshop.request.url)
        #: assert the workshop is listed on the all workshops page
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop how listed on all workshops page"

    """ How Scoping Works

        if I create a user in san fran or some other postal code, I should see that area designation 
        next to any objects I create

        currently, I do not see a scope browser in the interface. in order to test scope areas,
        therefore, I will need to create users in areas that encompass the zones to be tested.

        """
    def test_public_workshop_country_scope(self):
        """If I make a workshop scoped to united states, it and only it should be there when I 
        click the scope link for united states"""
        #: CREATE A WORKSHOP WITH THE SCOPE THIS TEST IS BUILT AROUND
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'COUNTRY workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, normalUser)
        #: the scope needs to be set before it will show up in the 'list all' page
        #: ||united-states|||||||
        scopeDict = {}
        #: NOTE - this style of scope area should end up being all lower-case with '-' instead of ' ',
        #: so when the code matures to this state, this line should break at which point I'll convert 
        #: the content accordingly
        scopeDict = content.scopeDict(country='United States', state='California')
        scopeString = workshop.createScope(self, country=scopeDict['country'])
        workshop.setWorkshopScope(self, newWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        # if I am logged in as a user, I will have a breadcrumb link list for clicking scope areas.
        # /workshops/geo/earth
        earthLink = linkDefs.createGeoLink()
        # /workshops/geo/earth/united-states
        usLink = linkDefs.createGeoLink(country='united-states')
        # /workshops/geo/earth/united-states/california
        stateLink = linkDefs.createGeoLink(country='united-states', state='california')
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitle not in earthView, "workshop scoped for United States showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitle in usView, "workshop scoped for United States not showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitle not in stateView, "workshop scoped for United States showing up on state-scoped list"
        # futher, I can make workshops that are above scope and below scope, and expect not to see
        # them in the scope of this workshop's designation

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL ABOVE THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeUp = 'EARTH workshop'
        earthWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeUp, login=False)
        assert workshopTitleScopeUp in earthWorkshop, "user not able to create earth workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, earthWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self)
        workshop.setWorkshopScope(self, earthWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, earthWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeUp in allWorkshops, "state workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitleScopeUp in earthView, "workshop scoped for earth not showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitleScopeUp not in usView, "workshop scoped for earth showing up on US-scoped list"
        assert workshopTitle in usView, "workshop scoped for country is not showing up on US-scoped list anymore"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitleScopeUp not in stateView, "workshop scoped for earth showing up on state-scoped list"

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL BELOW THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeDown = 'STATE workshop'
        stateWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeDown, login=False)
        assert workshopTitleScopeDown in stateWorkshop, "user not able to create state workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, stateWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, stateWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, stateWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeDown in allWorkshops, "state workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitleScopeDown not in earthView, "workshop scoped for state showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitleScopeDown not in usView, "workshop scoped for state showing up on US-scoped list"
        assert workshopTitle in usView, "workshop scoped for country now is not showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitleScopeDown in stateView, "workshop scoped for state not showing up on state-scoped list"

    def test_public_workshop_state_scope(self):
        """If I make a workshop scoped to a state, it and only it should be there when I 
        click the scope link for this state"""
        #: CREATE A WORKSHOP WITH THE SCOPE THIS TEST IS BUILT AROUND
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'STATE workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, normalUser)
        #: the scope needs to be set before it will show up in the 'list all' page
        #: ||united-states|california||||||
        scopeDict = {}
        #: NOTE - this style of scope area should end up being all lower-case with '-' instead of ' ',
        #: so when the code matures to this state, this line should break at which point I'll convert 
        #: the content accordingly
        scopeDict = content.scopeDict(country='United States', state='California')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, normalUser)
        #reloadW = self.app.get(url=newWorkshop.request.url)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        # if I am logged in as a user, I will have a breadcrumb link list for clicking scope areas.
        # /workshops/geo/earth
        earthLink = linkDefs.createGeoLink()
        # /workshops/geo/earth/united-states
        usLink = linkDefs.createGeoLink(country='united-states')
        # /workshops/geo/earth/united-states/california
        stateLink = linkDefs.createGeoLink(country='united-states', state='california')
        # /workshops/geo/earth/united-states/california/sacramento
        countyLink = linkDefs.createGeoLink(country='united-states', state='california', county='san-francisco')
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitle not in earthView, "workshop scoped for California showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitle not in usView, "workshop scoped for California showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitle in stateView, "workshop scoped for California not showing up on state-scoped list"
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitle not in countyView, "workshop scoped for California showing up on county-scoped list"
        # futher, I can make workshops that are above scope and below scope, and expect not to see
        # them in the scope of this workshop's designation

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL ABOVE THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeUp = 'COUNTRY workshop'
        countryWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeUp, login=False)
        assert workshopTitleScopeUp in countryWorkshop, "user not able to create country workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, countryWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self)
        workshop.setWorkshopScope(self, countryWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, countryWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeUp in allWorkshops, "state workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitleScopeUp in earthView, "workshop scoped for earth not showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitleScopeUp not in usView, "workshop scoped for earth showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitleScopeUp not in stateView, "workshop scoped for earth showing up on state-scoped list"
        assert workshopTitle in stateView, "workshop scoped for state is not showing up on US-scoped list anymore"

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL BELOW THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeDown = 'STATE workshop'
        stateWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeDown, login=False)
        assert workshopTitleScopeDown in stateWorkshop, "user not able to create state workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, stateWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, stateWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, stateWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeDown in allWorkshops, "state workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitleScopeDown not in earthView, "workshop scoped for state showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitleScopeDown not in usView, "workshop scoped for state showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitleScopeDown in stateView, "workshop scoped for state not showing up on state-scoped list"
        assert workshopTitle in stateView, "workshop scoped for state now is not showing up on US-scoped list"

    def test_public_workshop_county_scope(self):
        """If I make a workshop scoped to a county, it and only it should be there when I 
        click the scope link for this county"""
        #: CREATE A WORKSHOP WITH THE SCOPE THIS TEST IS BUILT AROUND
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'COUNTY workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, normalUser)
        #: the scope needs to be set before it will show up in the 'list all' page
        #: ||united-states|california||||||
        scopeDict = {}
        #: NOTE - this style of scope area should end up being all lower-case with '-' instead of ' ',
        #: so when the code matures to this state, this line should break at which point I'll convert 
        #: the content accordingly
        scopeDict = content.scopeDict(country='United States', state='California', county='San Francisco', city='San Francisco')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'], county=scopeDict['county'])
        workshop.setWorkshopScope(self, newWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, normalUser)
        #reloadW = self.app.get(url=newWorkshop.request.url)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        # if I am logged in as a user, I will have a breadcrumb link list for clicking scope areas.
        # /workshops/geo/earth
        earthLink = linkDefs.createGeoLink()
        # /workshops/geo/earth/united-states
        usLink = linkDefs.createGeoLink(country='united-states')
        # /workshops/geo/earth/united-states/california
        stateLink = linkDefs.createGeoLink(country='united-states', state='california')
        # /workshops/geo/earth/united-states/california/san-francisco
        countyLink = linkDefs.createGeoLink(country='united-states', state='california', county='san-francisco')
        # /workshops/geo/earth/united-states/california/san-francisco/san-francisco
        cityLink = linkDefs.createGeoLink(country='united-states', state='california', county='san-francisco', city='san-francisco')
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitle not in earthView, "workshop scoped for county showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitle not in usView, "workshop scoped for county showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitle not in stateView, "workshop scoped for county showing up on state-scoped list"
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitle in countyView, "workshop scoped for county not showing up on county-scoped list"
        cityView = allWorkshops.click(href=cityLink, index=0)
        assert workshopTitle not in cityView, "workshop scoped for county showing up on city-scoped list"
        # futher, I can make workshops that are above scope and below scope, and expect not to see
        # them in the scope of this workshop's designation

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL ABOVE THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeUp = 'STATE workshop'
        stateWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeUp, login=False)
        assert workshopTitleScopeUp in stateWorkshop, "user not able to create state workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, stateWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, stateWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, stateWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeUp in allWorkshops, "state workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitleScopeUp not in earthView, "workshop scoped for state showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitleScopeUp not in usView, "workshop scoped for state showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitleScopeUp in stateView, "workshop scoped for state not showing up on state-scoped list"
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitleScopeUp not in countyView, "workshop scoped for state showing up on county-scoped list"
        assert workshopTitle in countyView, "workshop scoped for county not showing up on county-scoped list"        

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL BELOW THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeDown = 'CITY workshop'
        cityWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeDown, login=False)
        assert workshopTitleScopeDown in cityWorkshop, "user not able to create city workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, cityWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'], county=scopeDict['county'], city=scopeDict['city'])
        workshop.setWorkshopScope(self, cityWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, cityWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeDown in allWorkshops, "city workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitleScopeDown not in countyView, "workshop scoped for city showing up on county-scoped list"
        cityView = allWorkshops.click(href=cityLink, index=0)
        assert workshopTitleScopeDown in cityView, "workshop scoped for city not showing up on city-scoped list"
        assert workshopTitle in countyView, "workshop scoped for county now is not showing up on county-scoped list"
        assert workshopTitle not in cityView, "workshop scoped for county is now showing up on city-scoped list"

    def test_public_workshop_city_scope(self):
        """If I make a workshop scoped to a city, it and only it should be there when I 
        click the scope link for this city"""
        #: CREATE A WORKSHOP WITH THE SCOPE THIS TEST IS BUILT AROUND
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'CITY workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, normalUser)
        #: the scope needs to be set before it will show up in the 'list all' page
        #: ||united-states|california||||||
        scopeDict = {}
        #: NOTE - this style of scope area should end up being all lower-case with '-' instead of ' ',
        #: so when the code matures to this state, this line should break at which point I'll convert 
        #: the content accordingly
        scopeDict = content.scopeDict(country='United States', state='California', county='San Francisco', city='San Francisco', postal='94122')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'], county=scopeDict['county'], city=scopeDict['city'])
        workshop.setWorkshopScope(self, newWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, normalUser)
        #reloadW = self.app.get(url=newWorkshop.request.url)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        # if I am logged in as a user, I will have a breadcrumb link list for clicking scope areas.
        # /workshops/geo/earth
        earthLink = linkDefs.createGeoLink()
        # /workshops/geo/earth/united-states
        usLink = linkDefs.createGeoLink(country='united-states')
        # /workshops/geo/earth/united-states/california
        stateLink = linkDefs.createGeoLink(country='united-states', state='california')
        # /workshops/geo/earth/united-states/california/san-francisco
        countyLink = linkDefs.createGeoLink(country='united-states', state='california', county='san-francisco')
        # /workshops/geo/earth/united-states/california/san-francisco/san-francisco
        cityLink = linkDefs.createGeoLink(country='united-states', state='california', county='san-francisco', city='san-francisco')
        # /workshops/geo/earth/united-states/california/san-francisco/san-francisco/94122
        postalLink = linkDefs.createGeoLink(country='united-states', state='california', county='san-francisco', city='san-francisco', postal='94122')
        #: test the scope views that this workshop is displayed in the correct one
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitle not in earthView, "workshop scoped for city showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitle not in usView, "workshop scoped for city showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitle not in stateView, "workshop scoped for city showing up on state-scoped list"
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitle not in countyView, "workshop scoped for city showing up on county-scoped list"
        cityView = allWorkshops.click(href=cityLink, index=0)
        assert workshopTitle in cityView, "workshop scoped for city not showing up on city-scoped list"
        postalView = allWorkshops.click(href=postalLink, index=0)
        assert workshopTitle not in postalView, "workshop scoped for city showing up on postal-scoped list"
        # futher, I can make workshops that are above scope and below scope, and expect not to see
        # them in the scope of this workshop's designation

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL ABOVE THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeUp = 'COUNTY workshop'
        countyWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeUp, login=False)
        assert workshopTitleScopeUp in countyWorkshop, "user not able to create county workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, countyWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'], county=scopeDict['county'])
        workshop.setWorkshopScope(self, countyWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, countyWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeUp in allWorkshops, "county workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitleScopeUp not in earthView, "workshop scoped for county showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitleScopeUp not in usView, "workshop scoped for county showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitleScopeUp not in stateView, "workshop scoped for county showing up on state-scoped list"
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitleScopeUp in countyView, "workshop scoped for county not showing up on county-scoped list"
        cityView = allWorkshops.click(href=cityLink, index=0)
        assert workshopTitleScopeUp not in cityView, "workshop scoped for county showing up in city-scoped list"
        assert workshopTitle in cityView, "workshop scoped for city not showing up on city-scoped list"

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL BELOW THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeDown = 'POSTAL CODE workshop'
        postalWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeDown, login=False)
        assert workshopTitleScopeDown in postalWorkshop, "user not able to create postal code workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, postalWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'], county=scopeDict['county'], city=scopeDict['city'], postal=scopeDict['postal'])
        workshop.setWorkshopScope(self, postalWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, postalWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeDown in allWorkshops, "postal workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitleScopeDown not in countyView, "workshop scoped for postal code showing up on county-scoped list"
        cityView = allWorkshops.click(href=cityLink, index=0)
        assert workshopTitleScopeDown not in cityView, "workshop scoped for postal code showing up on city-scoped list"
        postalView = allWorkshops.click(href=postalLink, index=0)
        assert workshopTitleScopeDown in postalView, "workshop scoped for postal code not showing up on postal-scoped list"
        assert workshopTitle in cityView, "workshop scoped for city is not showing up on city-scoped list anymore"
        assert workshopTitle not in countyView, "workshop scoped for city is now showing up on county-scoped list"


    def test_public_workshop_postal_scope(self):
        """If I make a workshop scoped to a postal code, it and only it should be there when I 
        click the scope link for this code"""
        #: CREATE A WORKSHOP WITH THE SCOPE THIS TEST IS BUILT AROUND
        normalUser = create_and_activate_a_user(self, postal='94122')
        workshopTitle = 'POSTAL CODE workshop by user'
        newWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "normal user not able to create new workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, normalUser)
        #: the scope needs to be set before it will show up in the 'list all' page
        #: ||united-states|california||||||
        scopeDict = {}
        #: NOTE - this style of scope area should end up being all lower-case with '-' instead of ' ',
        #: so when the code matures to this state, this line should break at which point I'll convert 
        #: the content accordingly
        scopeDict = content.scopeDict(country='United States', state='California', county='San Francisco', city='San Francisco', postal='94122')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'], county=scopeDict['county'], city=scopeDict['city'], postal=scopeDict['postal'])
        workshop.setWorkshopScope(self, newWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, normalUser)
        #reloadW = self.app.get(url=newWorkshop.request.url)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        # if I am logged in as a user, I will have a breadcrumb link list for clicking scope areas.
        # /workshops/geo/earth
        earthLink = linkDefs.createGeoLink()
        # /workshops/geo/earth/united-states
        usLink = linkDefs.createGeoLink(country='united-states')
        # /workshops/geo/earth/united-states/california
        stateLink = linkDefs.createGeoLink(country='united-states', state='california')
        # /workshops/geo/earth/united-states/california/san-francisco
        countyLink = linkDefs.createGeoLink(country='united-states', state='california', county='san-francisco')
        # /workshops/geo/earth/united-states/california/san-francisco/san-francisco
        cityLink = linkDefs.createGeoLink(country='united-states', state='california', county='san-francisco', city='san-francisco')
        # /workshops/geo/earth/united-states/california/san-francisco/san-francisco/94122
        postalLink = linkDefs.createGeoLink(country='united-states', state='california', county='san-francisco', city='san-francisco', postal='94122')
        #: test the scope views that this workshop is displayed in the correct one
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitle not in earthView, "workshop scoped for postal code showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitle not in usView, "workshop scoped for postal code showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitle not in stateView, "workshop scoped for postal code showing up on state-scoped list"
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitle not in countyView, "workshop scoped for postal code showing up on county-scoped list"
        cityView = allWorkshops.click(href=cityLink, index=0)
        assert workshopTitle not in cityView, "workshop scoped for postal code showing up on city-scoped list"
        postalView = allWorkshops.click(href=postalLink, index=0)
        assert workshopTitle in postalView, "workshop scoped for postal code not showing up on postal-scoped list"
        # futher, I can make workshops that are above scope and below scope, and expect not to see
        # them in the scope of this workshop's designation

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL ABOVE THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeUp = 'CITY workshop'
        countyWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeUp, login=False)
        assert workshopTitleScopeUp in countyWorkshop, "user not able to create county workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, countyWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'], county=scopeDict['county'])
        workshop.setWorkshopScope(self, countyWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, countyWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeUp in allWorkshops, "county workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        earthView = allWorkshops.click(href=earthLink, index=0)
        assert workshopTitleScopeUp not in earthView, "workshop scoped for county showing up on earth-scoped list"
        usView = allWorkshops.click(href=usLink, index=0)
        assert workshopTitleScopeUp not in usView, "workshop scoped for county showing up on US-scoped list"
        stateView = allWorkshops.click(href=stateLink, index=0)
        assert workshopTitleScopeUp not in stateView, "workshop scoped for county showing up on state-scoped list"
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitleScopeUp in countyView, "workshop scoped for county not showing up on county-scoped list"
        cityView = allWorkshops.click(href=cityLink, index=0)
        assert workshopTitleScopeUp not in cityView, "workshop scoped for county showing up in city-scoped list"
        assert workshopTitle in cityView, "workshop scoped for city not showing up on city-scoped list"

        #: CREATE A WORKSHOP SCOPED TO BE ONE LEVEL BELOW THE SCOPE WE'RE TESTING HERE
        workshopTitleScopeDown = 'POSTAL CODE workshop'
        postalWorkshop = workshop.create_new_workshop(self, normalUser, title=workshopTitleScopeDown, login=False)
        assert workshopTitleScopeDown in postalWorkshop, "user not able to create postal code workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, postalWorkshop, normalUser)
        #: scope this one a level below US: state
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'], county=scopeDict['county'], city=scopeDict['city'], postal=scopeDict['postal'])
        workshop.setWorkshopScope(self, postalWorkshop, normalUser, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, postalWorkshop, normalUser)
        #: first let's make sure the workshop is public and listed
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitleScopeDown in allWorkshops, "postal workshop not listed on all workshops page"
        #: test the views of workshops at each of these scopings
        countyView = allWorkshops.click(href=countyLink, index=0)
        assert workshopTitleScopeDown not in countyView, "workshop scoped for postal code showing up on county-scoped list"
        cityView = allWorkshops.click(href=cityLink, index=0)
        assert workshopTitleScopeDown not in cityView, "workshop scoped for postal code showing up on city-scoped list"
        postalView = allWorkshops.click(href=postalLink, index=0)
        assert workshopTitleScopeDown in postalView, "workshop scoped for postal code not showing up on postal-scoped list"
        assert workshopTitle in cityView, "workshop scoped for city is not showing up on city-scoped list anymore"
        assert workshopTitle not in countyView, "workshop scoped for city is now showing up on county-scoped list"