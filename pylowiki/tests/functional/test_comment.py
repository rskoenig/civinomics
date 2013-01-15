# -*- coding: utf-8 -*-
from pylowiki.tests import *

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.link_definitions as linkDefs
from pylowiki.tests.helpers.registration import create_and_activate_a_user
from pylowiki.tests.helpers.workshops import create_new_workshop

class TestCommentController(TestController):
    """This class tests the various aspects of comments."""
    #: Can a comment be created?
    #: Can a comment in a private workshop be seen by a user who is not a participant in this workshop?
    #: Can a user who is not a participant in this workshop create a comment in it?
	#: An admin, or a facilitor of a workshop can edit, delete, or make hidden a comment.

    def test_create_a_comment(self):
        """This test creates a comment on a standard workshop object"""
        # create_and_activate_normal_john
        thisUser = create_and_activate_a_user(self, email='toddy@civ.io', first='Toddley')
        # create_workshop as this new user
        newWorkshop = create_new_workshop(self, thisUser, 
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
        addForm.set(formDefs.addIdea_text(), content.oneLine())
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
        assert content.oneLine() in ideaAdded, "idea added to ideas page"
        # visit this idea's page
        ideaPage = ideaAdded.click(description=content.oneLine(), index=0, verbose=True)
        # comment on this idea
        addCommentForm = ideaPage.forms[formDefs.addComment()]
        addCommentForm.set(formDefs.addComment_text(), content.oneLine(1))
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

        assert content.oneLine(1) in commentAdded, "comment added to idea"