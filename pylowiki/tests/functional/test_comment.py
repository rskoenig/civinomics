# -*- coding: utf-8 -*-
from pylowiki.tests import *

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.link_definitions as linkDefs
from pylowiki.tests.helpers.authorization import login, logout
from pylowiki.tests.helpers.registration import create_and_activate_a_user
from pylowiki.tests.helpers.workshops import create_new_workshop

class TestCommentController(TestController):
    """This class tests the various aspects of comments."""
    #: Can a comment be created?
    #: Can a comment in a private workshop be seen by a user who is not a participant in this workshop?
    #: Can a user who is not a participant in this workshop create a comment in it?
	#: An admin, or a facilitor of a workshop can edit, delete, or make hidden a comment.

    def test_create_a_comment(self, **kwargs):
        """This test creates a comment on a standard workshop object"""
        # set the identifying text to be used in creating the objects necessary for a comment
        if 'ideaText' in kwargs:
            ideaText = kwargs['ideaText']
        else:
            ideaText = content.oneLine()
        if 'commentText' in kwargs:
            commentText = kwargs['commentText']
        else:
            commentText = content.oneLine(1)

        # create a new user
        thisUser = create_and_activate_a_user(self)
        # create_workshop as this new user
        newWorkshop = create_new_workshop(
            self, 
            thisUser, 
            private=True,
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        # comments can exist on discussion, idea or resource objects.
        #: commenting on an idea
        # go to the ideas page
        ideasPage = newWorkshop.click(description=linkDefs.ideas_page(), index=0)
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
        # after adding the idea, it should display on the following page.
        # be sure not to make too long of an idea for this test, in order for the assertion to reliably pass
        assert ideaText in ideaAdded, "idea not added to ideas page"
        # visit this idea's page
        ideaPage = ideaAdded.click(description=ideaText, index=0)
        # comment on this idea
        addCommentForm = ideaPage.forms[formDefs.addComment()]
        addCommentForm.set(formDefs.addComment_text(), commentText)
        # the form for submitting an idea has an extra parameter added to it as well.
        # this is an easy way to add the extra parameter
        params = {}
        #for key, value in addCommentForm.submit_fields():
        #    params[key] = value
        params = formHelpers.loadWithSubmitFields(addCommentForm)
        params[formDefs.parameter_submit()] = formDefs.addComment_submit()

        commentAdded = self.app.get(
            url = str(addCommentForm.action),
            params=params
        ).follow()

        assert commentText in commentAdded, "comment not visible here"
        return commentAdded

    def test_public_see_private_comment(self):
        """Can the public see this private comment? Create a comment in a private workshop, 
        then try to view it as someone who is not logged in to the site."""
        # create a comment in a private workshop
        ideaText = content.oneLine(2)
        commentText = content.oneLine(3)
        commentAdded = TestCommentController.test_create_a_comment(
            self,
            ideaText=ideaText,
            commentText=commentText
        )
        # assert that it's there
        assert commentText in commentAdded, "comment not visible here"
        # now logout, and try to view this comment
        logout(self)
        # I would like to to a get request on this response object's url, 
        # but it doesn't have a url attribute or a refresh action. Instead,
        # the title of the idea page links to itself, so we click on that 
        # to get the desired refresh.
        canPublicSeeComment = commentAdded.click(description=ideaText, index=0)
        # assert we're viewing this page without being logged in
        assert linkDefs.login() in canPublicSeeComment, "logged in as someone" 
        assert commentText not in canPublicSeeComment, "comment in private workshop is visible to public"
    
    def test_non_workshop_member_see_private_comment(self):
        """Can a site member who is not an invitee of the private workshop 
        see this private comment? Create a comment in a private workshop, 
        then login as a new site member, and try to view it."""
        # create a comment in a private workshop
        ideaText = content.oneLine(3)
        commentText = content.oneLine(4)
        commentAdded = TestCommentController.test_create_a_comment(
            self,
            ideaText=ideaText,
            commentText=commentText
        )
        # assert that it's there
        assert commentText in commentAdded, "comment not visible here"
        # logout, create a new user, and try to view this comment
        logout(self)
        # create a new user and login
        thisUser = create_and_activate_a_user(self)
        loggedIn = login(self, thisUser)
        canUserSeeComment = commentAdded.click(description=ideaText, index=0)
        # assert we're viewing this page without being logged in
        assert linkDefs.profile() in canUserSeeComment, "not logged in as who we should be" 
        assert commentText not in canUserSeeComment, "comment in private workshop visible to member outside of private workshop"
