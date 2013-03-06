from pylowiki.tests import *
from webtest import TestResponse
from routes import url_for

import pylowiki.tests.helpers.authorization as authorization
import pylowiki.tests.helpers.comment as comment
import pylowiki.tests.helpers.conversation as conversation
import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.registration as registration
import pylowiki.tests.helpers.workshops as workshop

class TestConversationController(TestController):
    """ This class tests that conversations work correctly. A workshop's conversations are created
    similar to how ideas are created. """

    """ disable 
 - how: create a workshop, then a conversation, then disable it
    - creator: admin, disabler: admin
    - creator: facilitator, disabler: admin
    - creator: user, disabler: admin
    - creator: admin, disabler: facilitator
    - creator: facilitator, disabler: facilitator
    - creator: user, disabler: facilitator
    - creator: admin, disabler: user
    - creator: facilitator, disabler: user
    - creator: user, disabler: user
 - prove: visit the object and confirm there is no comment form, and that the word 'disabled' is present
    - CAN: facilitator, admin
        - make sure admin button is present
    - CAN'T: user, guest, public
        - aside from spoof attempts, make sure the 'admin' button isn't present """
    
    def test_disable_conversation_admin_admin(self):
        """ Create a conversation as an admin, then disable this conversation as an admin. 
        In order to test a more realistic situation, these admins will be different users. """
        #: create a workshop and two admins
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='Admin One', accessLevel='200')
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
        workshopTitle = 'workshop conversations'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as user1
        conversationTitle = 'conversation title'
        conversationText = 'conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as admin2, revisit the conversation's page and disable
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDisabled = conversation.disable(self, conversationRevisit)
        assert conversationDisabled.status_int == 200, "disable request not successful"
        #: revisit the conversation page
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: make sure a disable message is present
        assert conversation.conversationDisabledMessage() in conversationRevisit, "admin not able to disable admin's conversation"
        #: make sure a comment form is not present
        assert formHelpers.isFormPresentByAction(conversationRevisit, 'comment') == False, "admin not able to disable admin's conversation, comment form present"
        #: Here is an extra test, making sure a comment submitted to the disabled conversation will be rejected.
        #: However, I can't get the test harness to work with the 404 rejection so for now this is disabled.
        #: In testing by hand, I've confirmed a comment is not allowed.
        #result = comment.addCommentToObject(self, conversationAdded, 'should not be able to comment', expect_errors=True)
        #assert result.status_int == 404

    def test_disable_conversation_facilitator_admin(self):
        """ Create a conversation as a facilitator, then disable this conversation as an admin. """
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
        workshopTitle = 'workshop conversations'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as user1
        conversationTitle = 'conversation title'
        conversationText = 'conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as admin2, revisit the conversation's page and disable
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDisabled = conversation.disable(self, conversationRevisit)
        assert conversationDisabled.status_int == 200, "disable request not successful"
        #: revisit the conversation page
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: make sure a disable message is present
        assert conversation.conversationDisabledMessage() in conversationRevisit, "admin not able to disable facilitator's conversation"
        #: make sure a comment form is not present
        assert formHelpers.isFormPresentByAction(conversationRevisit, 'comment') == False, "admin not able to disable facilitator's conversation, comment form present"
        
    def test_disable_conversation_user_admin(self):
        """ Create a conversation as a user of the workshop, then disable this conversation as an admin. """
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
        user3 = registration.create_and_activate_a_user(self, postal='92007', name='User')
        workshopTitle = 'workshop conversations'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user3 to the workshop
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user3
        authorization.logout(self)
        #: login as user3 then visit the invite link
        authorization.login(self, user3)
        guestConfirmed = self.app.get(url=guestLink)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo as a user of the workshop
        conversationTitle = 'conversation title'
        conversationText = 'conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: now make sure an admin can disable
        #: logout, login as admin2, revisit the conversation's page and disable
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDisabled = conversation.disable(self, conversationRevisit)
        assert conversationDisabled.status_int == 200, "disable request not successful"
        #: revisit the conversation page
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: make sure a disable message is present
        assert conversation.conversationDisabledMessage() in conversationRevisit, "admin not able to disable user's conversation"
        #: make sure a comment form is not present
        assert formHelpers.isFormPresentByAction(conversationRevisit, 'comment') == False, "admin not able to disable user's conversation, comment form present"
        
    def test_disable_conversation_admin_facilitator(self):
        """ Create a conversation as an admin, then try to disable it as a facilitator. """
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator One')
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
        workshopTitle = 'workshop conversations'
        #: user1 creates the workshop
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: user2, an admin, creates a conversation in it
        authorization.logout(self)
        authorization.login(self, user2)
        conversationTitle = 'conversation title'
        conversationText = 'conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: now log back is as the facilitator (user1), revisit the conversation's page and 
        #: attempt to disable it
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDisabled = conversation.disable(self, conversationRevisit)
        # NOTE: not sure what status will be returned when this is fixed
        # assert conversationDisabled.status_int == 200
        #: revisit the conversation page
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: make sure a disable message is not present
        assert conversation.conversationDisabledMessage() not in conversationRevisit, "admin's conversation disabled by facilitator"
        #: make sure a comment form is present
        assert formHelpers.isFormPresentByAction(conversationRevisit, 'comment') == True, "admin's conversation disabled by facilitator, comment form not present"

    def test_disable_conversation_facilitator_facilitator(self):
        """ INCOMPLETE """
        """ Create a conversation as a facilitator, then try to disable it as a facilitator. """
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator One')
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator Two')
        # LEFT OFF HERE
        workshopTitle = 'workshop conversations'
        #: user1 creates the workshop
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: user2, an admin, creates a conversation in it
        authorization.logout(self)
        authorization.login(self, user2)
        conversationTitle = 'conversation title'
        conversationText = 'conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: now log back is as the facilitator (user1), revisit the conversation's page and 
        #: attempt to disable it
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDisabled = conversation.disable(self, conversationRevisit)
        assert conversationDisabled.status_int == 200, "disable request not successful"
        #: revisit the conversation page
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: make sure a disable message is present
        assert conversation.conversationDisabledMessage() in conversationRevisit, "facilitator not able to disable facilitator's conversation"
        #: make sure a comment form is not present
        assert formHelpers.isFormPresentByAction(conversationRevisit, 'comment') == False, "facilitator not able to disable facilitator's conversation, comment form present"

    def test_disable_conversation_user_facilitator(self):
        """ Create a conversation as a user of the workshop, then disable this conversation as its facilitator. """
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='User')
        workshopTitle = 'workshop conversations'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user2 to the workshop
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        #: create a conversation as user2
        #: logout, then login as user2 and visit the invite link
        authorization.logout(self)
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLink)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo as a user of the workshop
        conversationTitle = 'conversation title'
        conversationText = 'conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: now make sure the facilitator can disable
        #: logout, login as user1, revisit the conversation's page and disable
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDisabled = conversation.disable(self, conversationRevisit)
        assert conversationDisabled.status_int == 200, "disable request not successful"
        #: revisit the conversation page
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: make sure a disable message is present
        assert conversation.conversationDisabledMessage() in conversationRevisit, "facilitator not able to disable user's conversation"
        #: make sure a comment form is not present
        assert formHelpers.isFormPresentByAction(conversationRevisit, 'comment') == False, "facilitator not able to disable user's conversation, comment form present"

    def test_disable_conversation_admin_user(self):
        """ Create a conversation as an admin, then disable this conversation as a user of the workshop. """
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
        user3 = registration.create_and_activate_a_user(self, postal='92007', name='User')
        workshopTitle = 'workshop conversations'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user3 to the workshop
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user2, the admin
        authorization.logout(self)
        authorization.login(self, user2)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo to the workshop
        conversationTitle = 'conversation title'
        conversationText = 'conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: As a user, there will not be a disable form available. we should still try though.
        #: Take advantage of being an admin and save the url necessary for this action. 
        #: use it next when logged in as a user.
        conversationDisableUrl = conversation.disable(self, conversationAdded, dontSubmit=True)
        #: now make sure a user cannot disable the admin's comment
        #: logout, login as user3, revisit the conversation's page and disable
        authorization.logout(self)
        authorization.login(self, user3)
        guestConfirmed = self.app.get(url=guestLink)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: can the user spoof the server with this disable post? we hope not
        #: expect a 404 response
        conversationDisabled = self.app.post(
            url=str(conversationDisableUrl),
            status=404
        )
        assert conversationDisabled.status_int == 404, "404 expected, something else happened"
        #: revisit the conversation page
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: make sure a disable message is not present
        assert conversation.conversationDisabledMessage() not in conversationRevisit, "admin's conversation disabled by user"
        #: make sure a comment form is present
        assert formHelpers.isFormPresentByAction(conversationRevisit, 'comment') == True, "admin's conversation disabled by user, comment form not present"

    def test_disable_conversation_facilitator_user(self):
        """ Create a conversation as a facilitator, then disable this conversation as a user of the workshop. """
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='User')
        workshopTitle = 'workshop conversations'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user2 to the workshop
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        #: create a conversation
        conversationTitle = 'conversation title'
        conversationText = 'conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: As a user, there will not be a disable form available. we should still try though.
        #: Take advantage of being a facilitator and save the url necessary for this action. 
        #: use it next when logged in as a user.
        conversationDisableUrl = conversation.disable(self, conversationAdded, dontSubmit=True)
        #: now make sure a user cannot disable the admin's comment
        #: logout, login as user2, revisit the conversation's page and disable
        authorization.logout(self)
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLink)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: can the user spoof the server with this disable post? we hope not
        #: expect a 404 response
        conversationDisabled = self.app.post(
            url=str(conversationDisableUrl),
            status=404
        )
        assert conversationDisabled.status_int == 404, "404 expected, something else happened"
        #: revisit the conversation page
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: make sure a disable message is not present
        assert conversation.conversationDisabledMessage() not in conversationRevisit, "facilitator's conversation disabled by user"
        #: make sure a comment form is present
        assert formHelpers.isFormPresentByAction(conversationRevisit, 'comment') == True, "facilitator's conversation disabled by user, comment form not present"

    def test_disable_conversation_user_user(self):
        """ Create a conversation as a user, then disable this conversation as a user of the workshop. """
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='User2')
        user3 = registration.create_and_activate_a_user(self, postal='92007', name='User3')
        workshopTitle = 'workshop conversations'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user2 and user3 to the workshop
        guestLink2 = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        guestLink3 = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user2
        authorization.logout(self)
        authorization.login(self, user2)
        guestConfirmed2 = self.app.get(url=guestLink2)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        conversationTitle = 'conversation title'
        conversationText = 'conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop,
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: As a user, there will not be a disable form available. we should still try though.
        #: Take advantage of being a facilitator and save the url necessary for this action. 
        #: use it next when logged in as a user.
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDisableUrl = conversation.disable(self, conversationRevisit, dontSubmit=True)
        #: now make sure a user cannot disable another user's comment
        #: logout, login as user3, revisit the conversation's page and disable
        authorization.logout(self)
        authorization.login(self, user3)
        guestConfirmed3 = self.app.get(url=guestLink3)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: can the user spoof the server with this disable post? we hope not
        #: expect a 404 response
        conversationDisabled = self.app.post(
            url=str(conversationDisableUrl),
            status=404
        )
        assert conversationDisabled.status_int == 404, "404 expected, something else happened"
        #: revisit the conversation page
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        #: make sure a disable message is not present
        assert conversation.conversationDisabledMessage() not in conversationRevisit, "user's conversation disabled by user"
        #: make sure a comment form is present
        assert formHelpers.isFormPresentByAction(conversationRevisit, 'comment') == True, "user's conversation disabled by user, comment form not present"

















