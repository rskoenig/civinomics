# -*- coding: utf-8 -*-
from pylowiki.tests import *
from nose.plugins.skip import Skip, SkipTest

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.link_definitions as linkDefs
import pylowiki.tests.helpers.noun_verb_tests as nounVerbTest
import pylowiki.tests.helpers.workshops as  workshop
from pylowiki.tests.helpers.authorization import login, logout
from pylowiki.tests.helpers.registration import create_and_activate_a_user


import logging
log = logging.getLogger(__name__)

class TestIdeaController(TestController):
    """ This class tests that ideas work correctly. A workshop's ideas are created
    similar to how ideas and resources are created, so there is a helper file, noun_verb_tests.py
    that hosts most of the tests for these objects. Any tests that are not in this file either
    have not been refactored to apply to all three of these types, or applies to a situation 
    specific to that type of workshop object. """

    #: Can an idea be created?
    #: Can an idea in a private workshop be seen by a user who is not a participant in this workshop?
    #: Can a user who is not a participant in this workshop create an idea in it?
	#: An admin, or a facilitor of a workshop can edit, delete, or make hidden an idea.

    def test_create_idea(self, **kwargs):
        """Can we create an idea in a workshop?"""
        if 'ideaText' in kwargs:
            ideaText = kwargs['ideaText']
        else:
            ideaText = content.oneLine()

        # create a new user
        thisUser = create_and_activate_a_user(self)
        # create_workshop as this new user
        newWorkshop = workshop.create_new_workshop(
            self, 
            thisUser, 
            personal=True,
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        ideaAdded = workshop.addIdeaToWorkshop(self, newWorkshop, ideaText)
        
        # after adding the idea, it should display on the following page.
        # be sure not to make too long of an idea for this test, in order for the assertion to reliably pass
        assert ideaText in ideaAdded, "Not able to add idea to workshop"
        return ideaAdded

    def test_see_private_idea_public(self):
        """Can the public see this private idea? Create an idea in a private workshop, 
        then try to view it as someone who is not logged in to the site."""
        # create an idea in a private workshop
        ideaText = content.oneLine(2)
        
        ideaAdded = TestIdeaController.test_create_idea(
            self,
            ideaText=ideaText
        )
        # assert that it's there
        assert ideaText in ideaAdded, "error before test complete: not able to create idea in workshop"
        # now logout, and try to view this idea
        logout(self)
        #: ideaAdded is the idea's own page, so we reload it to see if the public can view it.
        #: we expect a 404 instead though.
        canPublicSeeIdea = self.app.get(url=ideaAdded.request.url, status=404)
        # if this idea is visible, this is not good
        assert ideaText not in canPublicSeeIdea, "public user can view idea in private workshop"

    def test_see_private_idea_non_workshop_member(self):
        """Can a site member who is not an invitee of the private workshop 
        see this private idea? Create an idea in a private workshop, 
        then login as a new site member, and try to view it."""
        #: create a idea in a private workshop
        ideaText = content.oneLine(3)
        ideaAdded = TestIdeaController.test_create_idea(
            self,
            ideaText=ideaText
        )
        #: assert that it's there
        assert ideaText in ideaAdded, "error before test complete: not able to create idea in workshop"
        #: logout, create a new user, and try to view this idea
        logout(self)
        #: create a new user and login
        thisUser = create_and_activate_a_user(self)
        loggedIn = login(self, thisUser)
        #: ideaAdded is the idea's own page, so we reload it to see if this other user can view it.
        #: we expect a 404 instead though.
        canUserSeeIdea = self.app.get(url=ideaAdded.request.url, status=404)
        # if we can see the idea, this is not good
        assert ideaText not in canUserSeeIdea, "site member, not a member of a private workshop, able to view an idea in the workshop"

    def test_create_idea_in_private_workshop_public(self):
        """Can a non-logged in visitor create an idea within a private workshop?"""
        # create a workshop
        ideaText = content.oneLine(4)
        ideaText1 = content.oneLine(5)
        ideaAdded = TestIdeaController.test_create_idea(
            self,
            ideaText=ideaText
        )
        # assert that it's there
        assert ideaText in ideaAdded, "error before test complete: not able to create idea in workshop"
        # get the add idea form
        ideaPage = ideaAdded.click(description=linkDefs.vote_page(), index=0)
        addIdea = ideaPage.click(description=linkDefs.addIdea(), index=0)

        logout(self)

        # is the add idea form here?
        if formDefs.addIdea() in addIdea.forms:
            addIdeaForm = addIdea.forms[formDefs.addIdea()]
            # this form does not include submit as a parameter, but it must be included in the postdata
            params = {}
            params = formHelpers.loadWithSubmitFields(addIdeaForm)
            params[formDefs.parameter_submit()] = content.noChars()
            ideaAdded1 = self.app.post(
                url=str(addIdeaForm.action), 
                content_type=addIdeaForm.enctype,
                params=params,
                status=404,
                expect_errors=True
            )
            # if the idea is present on the page, this is bad
            assert ideaText1 not in ideaAdded1, "public user was able to create a idea in a private workshop, using form on page"

    def test_create_idea_in_private_workshop_non_workshop_member(self):
        """Can a member create a idea within a private workshop who is not a member of the workshop?"""
        ideaText = content.oneLine(5)
        # create first user
        thisUser = create_and_activate_a_user(self)
        # create_workshop as this new user
        newWorkshop = workshop.create_new_workshop(
            self, 
            thisUser, 
            personal=True,
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        # go to the idea page
        ideasPage = newWorkshop.click(description=linkDefs.vote_page(), index=0)
        # click the 'add idea' link
        addIdea = ideasPage.click(description=linkDefs.addIdea(), index=0)
        # obtain the form for this
        addForm = addIdea.forms[formDefs.addIdea()]
        addForm.set(formDefs.addIdea_text(), ideaText)
        # this form does not include submit as a parameter, but it must be included in the postdata
        params = {}
        params = formHelpers.loadWithSubmitFields(addForm)
        params[formDefs.parameter_submit()] = content.noChars()
        # now, before submitting this form let's logout, create a new user, login as that person, 
        # then submit the form
        logout(self)
        newUser = create_and_activate_a_user(self)
        login(self, newUser)
        ideaAdded = self.app.post(
            url=str(addForm.action), 
            content_type=addForm.enctype,
            params=params,
            status=404,
            expect_errors=True
        )
        # after trying to add the idea, it should not display on the following page.
        assert ideaText not in ideaAdded, "site member who is not a member of the private workshop, was able to make a idea in it"
        assert ideaAdded.status_int == 404

    # NEXT SECTION
    #An admin, or a facilitor of a workshop can edit, delete, or make hidden (on first display) an idea.
    #def can_edit_idea_admin():

    def can_edit_idea_admin(self):
        #: create comment as random person
        thisUser = create_and_activate_a_user(self)
        ideaText = content.oneLine(1)
        ideaText2 = content.oneLine(2)
        #: create_workshop as this new user
        newWorkshop = workshop.create_new_workshop(
            self, 
            thisUser, 
            personal=True,
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        #: add idea to workshop
        ideaAdded = workshop.addIdeaToWorkshop(self, newWorkshop, ideaText)
        # assert that it's there
        assert ideaText in ideaAdded, "error before test complete: not able to create idea in workshop"
        # NOTE for now, login as super admin. next, make a normal user an admin for this
        logout(self)
        admin = {}
        # conf = config['app_conf']
        # admin['email'] = conf['admin.email']
        # NOTE - get these two lines working with the conf method
        admin['email'] = 'username@civinomics.com'
        # admin['password'] = conf['admin.pass']
        admin['password'] = 'password'

        loggedIn = login(self, admin)
        #: find the idea that we want to edit
        for form in ideaAdded.forms:
            thisForm = ideaAdded.forms[form]
            for field in thisForm.submit_fields():
                # field is actually a tuple
                log.info("field %s value %s"%(field[0], field[1]))
                if ideaText in field[1]:
                    #edit idea and submit this form
                    thisForm.set(field[0], ideaText2)
                    params = {}
                    params = formHelpers.loadWithSubmitFields(thisForm)
                    params[formDefs.parameter_submit()] = formDefs.editIdea_submit()
                    didWork = self.app.put(
                        url = str.strip(str(thisForm.action)),
                        content_type=thisForm.enctype,
                        params=params
                    ).follow()

        assert ideaText2 in didWork, "admin not able to edit idea in workshop made by a user"
        assert ideaText not in didWork, "admin not able to edit idea in workshop made by a user"


    def can_delete_idea_admin(self):
        # create idea as random person
        thisUser = create_and_activate_a_user(self)
        ideaText = content.oneLine(1)
        #: create_workshop as this new user
        newWorkshop = workshop.create_new_workshop(
            self, 
            thisUser, 
            personal=True,
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        #: add idea to workshop
        ideaAdded = workshop.addIdeaToWorkshop(self, newWorkshop, ideaText)
        # assert that it's there
        assert ideaText in ideaAdded, "error before test complete: not able to create idea in workshop"
        # NOTE for now, login as super admin. next, make a normal user an admin for this
        admin = {}
        # conf = config['app_conf']
        # admin['email'] = conf['admin.email']
        # NOTE - get these two lines working with the conf method
        admin['email'] = 'username@civinomics.com'
        # admin['password'] = conf['admin.pass']
        admin['password'] = 'password'
        # login as this new admin
        loggedIn = login(self, admin)
        #: find the idea that we want to delete
        # we need the code of the idea
        # find the idea text in a link, parse the link to get the idea object code
        # we're using beautifulsoup4, which is what the response object's .html attribute returns:
        soup = ideaAdded.html
        theIdea = soup.find("a", text=ideaText)
        ideaLink = theIdea['href']
        # grab the idea code
        ideaCode = content.ideaTitleLink_getCode(ideaLink)
        # we're looking for this code in this form: <form action = 'delete/objectType/objectCode
        deleteForm = content.deleteObjectForm_findByCode(soup, ideaCode)
        # with the delete form in a beautifulsoup object, we can now get the values out and into action
        formParts = content.getFormParts_soup(deleteForm)
        # submit the delete form
        didDelete = self.app.post(
            url = str.strip(str(formParts['action']))
        )
        # reload the page by clicking the ideas menu and the idea should no longer be visible
        confirmDelete = ideaAdded.click(description=linkDefs.vote_page(), index=0)
        #assert didDelete == 404
        assert ideaText not in confirmDelete, "admin not able to delete idea made by a user in their own workshop"
          

    """ ****************************************************************************************** """
    """ ****************************************************************************************** """
    """ This group of tests focuses on permissions for disabling and enabling. In the tests
    where there should be a successful disabling of the idea, the cases for enabling will
    be tested as well. """
    
    def test_disable_idea_admin_admin(self):
        """ Create a idea as an admin, then disable this idea as an admin. 
        In order to test a more realistic situation, these admins will be different users. """
        #: create a workshop and two admins
        nounVerbTest.test_disable_noun_admin_admin(self, 'idea')

    def test_disable_idea_facilitator_admin(self):
        """ Create a idea as a facilitator, then disable this idea as an admin. """
        #: create a workshop and two users
        nounVerbTest.test_disable_noun_facilitator_admin(self, 'idea')

    def test_disable_idea_user_admin(self):
        """ Create a idea as a user of the workshop, then disable this idea as an admin. """
        #: create a workshop and two users
        nounVerbTest.test_disable_noun_user_admin(self, 'idea')

    def test_disable_idea_admin_facilitator(self):
        """ Create a idea as an admin, then try to disable it as a facilitator. """
        #: create a workshop and two users
        nounVerbTest.test_disable_noun_admin_facilitator(self, 'idea')

    def test_disable_idea_facilitator_facilitator(self):
        """ Create an idea as a facilitator, then disable it as a facilitator. """
        nounVerbTest.test_disable_noun_facilitator_facilitator(self, 'idea')
        
    def test_disable_idea_user_facilitator(self):
        """ Create a idea as a user of the workshop, then disable this idea as its facilitator. """
        #: create a workshop and two users
        nounVerbTest.test_disable_noun_user_facilitator(self, 'idea')
        
    def test_disable_idea_admin_user(self):
        """ Create a idea as an admin, then disable this idea as a user of the workshop. """
        #: create a workshop and two users
        nounVerbTest.test_disable_noun_admin_user(self, 'idea')

    def test_disable_idea_facilitator_user(self):
        """ Create a idea as a facilitator, then disable this idea as a user of the workshop. """
        #: create a workshop and two users
        nounVerbTest.test_disable_noun_facilitator_user(self, 'idea')

    def test_disable_idea_user_user(self):
        """ Create a idea as a user, then disable this idea as a user of the workshop. """
        #: create a workshop and two users
        nounVerbTest.test_disable_noun_user_user(self, 'idea')

    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ TEST IMMUNITY - PRIVATE WORKSHOPS """
    """ In this next group, we will be looking for holes in the ability to immunify an object.
    There are many possible combinations of situations, but only a few of them should be successful. Therefore, 
    in order to reduce the number of tests here, the attempts to immunify that should
    not be successful will be attempted before testing what should be a successful setting of an object's immunity. """

    "admin not able to flag an immune conversation"
    def test_immunify_privateWorkshop_user_facilitator(self):
        """ Create a idea in a private workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 1/12 for this group
        nounVerbTest.test_immunify_private_noun_user_facilitator(self, 'idea')
        
    "admin not able to flag an immune conversation"
    def test_immunify_privateWorkshop_facilitator_facilitator(self):
        """ Create a idea in a private workshop as its facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 2/12 for this group
        nounVerbTest.test_immunify_private_noun_facilitator_facilitator(self, 'idea')
        
    "OK"
    def test_immunify_privateWorkshop_admin_facilitator(self):
        """ Create a idea in a private workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 3/12 for this group
        nounVerbTest.test_immunify_private_noun_admin_facilitator(self, 'idea')

    "admin not able to flag an immune conversation"
    def test_immunify_privateWorkshop_user_admin(self):
        """ Create a idea in a private workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 4/12 for this group
        nounVerbTest.test_immunify_noun_user_admin(self, 'idea')

    "admin not able to flag an immune conversation"
    def test_immunify_privateWorkshop_facilitator_admin(self):
        """ Create a idea in a private workshop as its facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 5/12 for this group
        nounVerbTest.test_immunify_private_noun_facilitator_admin(self, 'idea')

    "admin not able to flag an immune conversation"
    def test_immunify_privateWorkshop_admin_admin(self):
        """ Create a idea in a private workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 6/12 for this group
        nounVerbTest.test_immunify_private_noun_admin_admin(self, 'idea')

    """ ****************************************************************************************** """
    """ This next group of tests are the same as the previous ones that started at 
    'TEST IMMUNITY - PRIVATE WORKSHOPS', except for the fact that these are working 
    with public workshops. """

    "OK"
    def test_immunify_publicWorkshop_user_facilitator(self):
        """ Create a idea in a public workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 7/12 for this group
        nounVerbTest.test_immunify_public_noun_user_facilitator(self, 'idea')

    "OK"
    def test_immunify_publicWorkshop_facilitator_facilitator(self):
        """ Create a idea in a public workshop as the facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 8/12 for this group
        nounVerbTest.test_immunify_public_noun_facilitator_facilitator(self, 'idea')
        
    "OK"
    def test_immunify_publicWorkshop_admin_facilitator(self):
        """ Create a idea in a public workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 9/12 for this group
        nounVerbTest.test_immunify_public_noun_admin_facilitator(self, 'idea')

    "OK"
    def test_immunify_publicWorkshop_user_admin(self):
        """ Create a idea in a public workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 10/12 for this group
        nounVerbTest.test_immunify_public_noun_user_admin(self, 'idea')

    "OK"
    def test_immunify_publicWorkshop_facilitator_admin(self):
        """ Create a idea in a public workshop as the facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 11/12 for this group
        nounVerbTest.test_immunify_public_noun_facilitator_admin(self, 'idea')

    "OK"
    def test_immunify_publicWorkshop_admin_admin(self):
        """ Create a idea in a public workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 12/12 for this group
        nounVerbTest.test_immunify_public_noun_admin_admin(self, 'idea')

    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ This next group of tests will cover deletion permissions. Bottom line is, only an admin 
        can delete an object. """

    def test_delete_idea_admin_admin(self):
        """ Create a idea as an admin, then delete this idea as an admin."""
        # test 1
        nounVerbTest.test_delete_noun_admin_admin(self, 'idea')
        
    def test_delete_idea_facilitator_admin(self):
        """ Create a idea as a facilitator, then delete this idea as an admin."""
        # test 2
        nounVerbTest.test_delete_noun_facilitator_admin(self, 'idea')
        
    def test_delete_idea_user_admin(self):
        """ Create a idea as a user of the private workshop, then delete this idea 
        as an admin."""
        # test 3
        nounVerbTest.test_delete_noun_user_admin(self, 'idea')

    """ ****************************************************************************************** """ 
    """ Second set will deal with this within public workshops. """

    def test_delete_public_idea_admin_admin(self):
        """ Create a idea as an admin in a public workshop, then delete this idea 
        as an admin."""
        # test 4
        nounVerbTest.test_delete_public_noun_admin_admin(self, 'idea')
    
    def test_delete_public_idea_facilitator_admin(self):
        """ Create a idea as a facilitator in a public workshop, then delete this idea 
        as an admin."""
        # test 5
        nounVerbTest.test_delete_public_noun_facilitator_admin(self, 'idea')
        
    def test_delete_public_idea_user_admin(self):
        """ Create a idea as a user in a public workshop, then delete this idea 
        as an admin."""
        # test 6
        nounVerbTest.test_delete_public_noun_user_admin(self, 'idea')
        
