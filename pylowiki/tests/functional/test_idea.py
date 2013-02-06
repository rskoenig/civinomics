# -*- coding: utf-8 -*-
from pylowiki.tests import *

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.link_definitions as linkDefs
from pylowiki.tests.helpers.authorization import login, logout
from pylowiki.tests.helpers.registration import create_and_activate_a_user
from pylowiki.tests.helpers.workshops import create_new_workshop, addIdeaToWorkshop

import logging
log = logging.getLogger(__name__)

class TestIdeaController(TestController):
    """This class tests the various aspects of ideas."""
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
        newWorkshop = create_new_workshop(
            self, 
            thisUser, 
            personal=True,
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        ideaAdded = addIdeaToWorkshop(self, newWorkshop, ideaText)
        
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
        # I would like to to a get request on this response object's url, 
        # but it doesn't have a url attribute or a refresh action. Instead,
        # the title of the idea page links to itself, so we click on that 
        # to get the desired refresh.
        canPublicSeeIdea = ideaAdded.click(description=ideaText, index=0)
        # assert we're viewing this page without being logged in
        assert linkDefs.login() in canPublicSeeIdea, "error before test complete: should not be logged in as someone at this point"
        # if this idea is visible, this is not good
        assert ideaText not in canPublicSeeIdea, "public user able to view idea in a private workshop"

    def test_see_private_idea_non_workshop_member(self):
        """Can a site member who is not an invitee of the private workshop 
        see this private idea? Create an idea in a private workshop, 
        then login as a new site member, and try to view it."""
        # create a idea in a private workshop
        ideaText = content.oneLine(3)
        ideaAdded = TestIdeaController.test_create_idea(
            self,
            ideaText=ideaText
        )
        # assert that it's there
        assert ideaText in ideaAdded, "error before test complete: not able to create idea in workshop"
        # logout, create a new user, and try to view this idea
        logout(self)
        # create a new user and login
        thisUser = create_and_activate_a_user(self)
        loggedIn = login(self, thisUser)
        canUserSeeIdea = ideaAdded.click(description=ideaText, index=0)
        # assert we're viewing this page without being logged in
        assert linkDefs.profile() in canUserSeeIdea, "error before test complete: should be logged in as someone at this point"
        # if this idea has been created, this is not good
        assert ideaText not in canUserSeeIdea, "site member who is not a member of a private workshop was able to view an idea in this workshop"

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
        addIdea = ideaAdded.click(description=linkDefs.addIdea(), index=0)

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
                params=params
            ).follow()
            # if the idea is present on the page, this is bad
            assert ideaText1 not in ideaAdded1, "public user was able to create a idea in a private workshop, using form on page"

    def test_create_idea_in_private_workshop_non_workshop_member(self):
        """Can a member create a idea within a private workshop who is not a member of the workshop?"""
        ideaText = content.oneLine(5)
        # create first user
        thisUser = create_and_activate_a_user(self)
        # create_workshop as this new user
        newWorkshop = create_new_workshop(
            self, 
            thisUser, 
            personal=True,
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        # go to the idea page
        ideasPage = newWorkshop.click(description=linkDefs.ideas_page(), index=0)
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
            params=params
        ).follow()
        # after trying to add the idea, it should not display on the following page.
        assert ideaText not in ideaAdded, "site member who is not a member of the private workshop, was able to make a idea in it"

    # NEXT SECTION
    #An admin, or a facilitor of a workshop can edit, delete, or make hidden (on first display) an idea.
    #def can_edit_idea_admin():

    def can_edit_idea_admin(self):
        #: create comment as random person
        thisUser = create_and_activate_a_user(self)
        ideaText = content.oneLine(1)
        ideaText2 = content.oneLine(2)
        #: create_workshop as this new user
        newWorkshop = create_new_workshop(
            self, 
            thisUser, 
            personal=True,
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        #: add idea to workshop
        ideaAdded = addIdeaToWorkshop(self, newWorkshop, ideaText)
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
        newWorkshop = create_new_workshop(
            self, 
            thisUser, 
            personal=True,
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        #: add idea to workshop
        ideaAdded = addIdeaToWorkshop(self, newWorkshop, ideaText)
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
        confirmDelete = ideaAdded.click(description=linkDefs.ideas_page(), index=0)
        #assert didDelete == 404
        assert ideaText not in confirmDelete, "admin not able to delete idea made by a user in their own workshop"
          

    