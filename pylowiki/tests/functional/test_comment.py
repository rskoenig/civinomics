# -*- coding: utf-8 -*-
from pylowiki.tests import *

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.link_definitions as linkDefs
from pylowiki.tests.helpers.registration import create_and_activate_a_user
from pylowiki.tests.helpers.workshops import create_new_workshop

class TestCommentController(TestController):

	# 	- an admin or facilitor of this workshop
	#		-  can edit, delete, or make hidden on first display
	#	    :" a comment"


    def test_create_a_comment(self):
        # create_and_activate_normal_john
        thisUser = create_and_activate_a_user(self, email='toddy@civ.io', first='Toddley')
        # create_workshop as this new user
        newWorkshop = create_new_workshop(self, thisUser, 
            allowIdeas=formDefs.workshopSettings_allowIdeas(True),
            allowResourceLinks=formDefs.workshopSettings_allowResourceLinks(True)
        )
        ideasPage = newWorkshop.click(description=linkDefs.ideas_page(), index=0)

        addIdea = ideasPage.click(description=linkDefs.addIdea(), index=0)

        addForm = addIdea.forms[formDefs.addIdea()]
        # this form does not include submit as a parameter, but it must be included in the postdata
        ideaAdded = self.app.post(
            url=str(addForm.action), 
            content_type=addForm.enctype,
            params={ formDefs.addIdea_text() : content.oneLine(),
                formDefs.parameter_submit() : content.noChars()
            }
        ).follow()
        
        assert content.oneLine() in ideaAdded
        # visit this idea's page
        ideaPage = ideaAdded.click(description=content.oneLine(), index=0, verbose=True)
        # comment on this idea
        addCommentForm = ideaPage.forms[formDefs.addComment()]
        addCommentForm.set(formDefs.addComment_text(), content.oneLine(1))
        #URL=http://todd.civinomics.org/comment/add/handler?
        #type=idea
        #&discussionCode=4ICP
        #&parentCode=0
        #&comment-textarea=something+to+say%3F
        #&submit=reply
        params = {}
        for key, value in addCommentForm.submit_fields():
            params[key] = value
        
        params[formDefs.parameter_submit()] = formDefs.addComment_submit()

        commentAdded = self.app.get(
            url = str(addCommentForm.action),
            params=params
        ).follow()

        assert content.oneLine(1) in commentAdded