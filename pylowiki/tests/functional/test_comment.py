# -*- coding: utf-8 -*-
from pylowiki.tests import *

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
        ideaPage = newWorkshop.click(description=linkDefs.ideas_page(), index=0)

        addIdea = ideaPage.click(description=linkDefs.addIdea(), index=0)

        addForm = addIdea.forms[formDefs.addIdea()]

        # this form does not include submit as a parameter, but it must be included in the postdata
        #NOTE either find a way to add this to the submit fields, or create a post that includes this in the postdata

        ideaAdded = self.app.post(
            url=str(addForm.action), 
            content_type=addForm.enctype,
            params={ formDefs.addIdea_ideaText() : 'this is a test idea',
                formDefs.addIdea_ideaSubmit() : ''
            }
        ).follow()
        


        assert newWorkshop == 404
         # login as john
         # create workshop page:
            # - name, fill out next page's form1, submit, fill out form 2, submit, check both boxes, submit
            # confirm success message
        # create discussion

        # comment on discussion

        # at this point we have a comment on a discussion. we can begin testing various role's abilities