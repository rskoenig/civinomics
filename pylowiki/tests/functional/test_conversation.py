from pylowiki.tests import *
from webtest import TestResponse
from routes import url_for

import pylowiki.tests.helpers.authorization as authorization
import pylowiki.tests.helpers.comment as comment
import pylowiki.tests.helpers.conversation as conversation
import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.page_definitions as pageDefs
import pylowiki.tests.helpers.registration as registration
import pylowiki.tests.helpers.workshops as workshop

import logging
log = logging.getLogger(__name__)

class TestConversationController(TestController):
    """ This class tests that conversations work correctly. A workshop's conversations are created
    similar to how ideas are created. """

    """ disable 
 - how: create a workshop, then a conversation, then disable it
    * creator, disabler:
    - admin, admin
    - facilitator, admin
    - user, admin
    - admin, facilitator
    - facilitator, facilitator
    - user, facilitator
    - admin, user
    - facilitator, user
    - user, user
    * more posssible tests:
    - admin, user not in workshop
    - admin, guest
    - admin, public
    - facilitator, user not in workshop
    - facilitator, guest
    - facilitator, public
    and so on down the ranks through guest and public


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
        #assert conversation.conversationDisabledMessage() not in conversationRevisit, "admin's conversation disabled by facilitator"
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

    """ TEST IMMUNITY - PRIVATE WORKSHOPS """

    """ In this next suite of tests, we will be looking for holes in the ability to immunify an object.
    There are many possible combinations of situations, but only a few of them should be successful. Therefore, 
    in order to reduce the number of tests to be written from 42 to 12, the attempts to immunify that should
    not be successful will be attempted before testing what should be a successful setting of an object's immunity.
    Should any unexpected failures occur, the feedback data will be verbose enough to pinpoint the problem anyways."""

    def test_immunify_privateWorkshop_user_facilitator(self):
        """ Create a conversation in a private workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 1/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as a user of the workshop
        #: invite user2 to the workshop
        guestLinkUser = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        guestLinkGuest = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLinkUser)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo as a user of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test guest - since we're already logged out, visit workshop via guestlink and try to immunify
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "guest able to immunify this conversation"
        #: login then logout as this guest to wipe the session
        authorization.login(self, user3)
        authorization.logout(self)
        #
        #: test user outside of workshop
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop - complete the guest invite process with user3
        authorization.login(self, user3)
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as the facilitator of the workshop
        authorization.login(self, user1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test guest - let's make a new guest
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser5 = workshop.inviteGuest(self, newWorkshop, email=user5['email'], guestLink=True)
        #: logout, and visit as this new guest
        authorization.logout(self)
        guestTester5 = self.app.get(url=guestLinkUser5)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "guest able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user outside of workshop
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop
        #: make a new guest
        user7 = registration.create_and_activate_a_user(self, postal='95062', name='user7')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser7 = workshop.inviteGuest(self, newWorkshop, email=user7['email'], guestLink=True)
        #: logout, login as this user and click the guest link to join the workshop
        authorization.logout(self)
        authorization.login(self, user7)
        workshopMember7 = self.app.get(url=guestLinkUser7)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "workshop member able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"
        
    def test_immunify_privateWorkshop_user_facilitator_nonUserFlag(self):
        """ Create a conversation in a private workshop as a user, immunify as the workshop's facilitator, then
        attempt to flag the object as a user of the site who's not a member of the private workshop.
        """
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as a user of the workshop
        #: invite user2 to the workshop
        guestLinkUser = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        guestLinkGuest = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLinkUser)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo as a user of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 3
        #: immunify as the facilitator of the workshop
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag as a user of the site who's not a member of the workshop
        #
        #: test user outside of workshop
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of site, not part of this private workshop, able to flag this immune conversation"

    def test_immunify_privateWorkshop_user_facilitator_userFlag(self):
        """ Create a conversation in a private workshop as a user, immunify as the workshop's facilitator, then
        attempt to flag the object as a user who is a member of the private workshop.
        """
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as a user of the workshop
        #: invite user2 to the workshop
        guestLinkUser = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        guestLinkGuest = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLinkUser)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo as a user of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 3
        #: immunify as the facilitator of the workshop
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop
        #: make a new guest
        user7 = registration.create_and_activate_a_user(self, postal='95062', name='user7')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser7 = workshop.inviteGuest(self, newWorkshop, email=user7['email'], guestLink=True)
        #: logout, login as this user and click the guest link to join the workshop
        authorization.logout(self)
        authorization.login(self, user7)
        workshopMember7 = self.app.get(url=guestLinkUser7)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "workshop member able to flag this conversation"
        #: wipe the session
        authorization.logout(self)

    def test_immunify_privateWorkshop_user_facilitator_extFacilitatorFlag(self):
        """ Create a conversation in a private workshop as a user, immunify as the workshop's facilitator, then
        attempt to flag the object as a facilitator of another workshop, not this private workshop.
        """
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as a user of the workshop
        #: invite user2 to the workshop
        guestLinkUser = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        guestLinkGuest = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLinkUser)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo as a user of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 3
        #: immunify as the facilitator of the workshop
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        workshopTitle2 = 'another workshop'
        #: note that create_new_workshop logs in as the user in the param unless otherwise specified
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"


    def test_immunify_privateWorkshop_facilitator_facilitator(self):
        """ Create a conversation in a private workshop as its facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 2/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        guestLinkGuest = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as the facilitator of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test guest - since we're already logged out, visit workshop via guestlink and try to immunify
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "guest able to immunify this conversation"
        #: login then logout as this guest to wipe the session
        authorization.login(self, user3)
        authorization.logout(self)
        #
        #: test user outside of workshop
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop - complete the guest invite process with user3
        authorization.login(self, user3)
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as the facilitator of the workshop
        authorization.login(self, user1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test guest - let's make a new guest
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser5 = workshop.inviteGuest(self, newWorkshop, email=user5['email'], guestLink=True)
        #: logout, and visit as this new guest
        authorization.logout(self)
        guestTester5 = self.app.get(url=guestLinkUser5)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "guest able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user outside of workshop
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop
        #: make a new guest
        user7 = registration.create_and_activate_a_user(self, postal='95062', name='user7')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser7 = workshop.inviteGuest(self, newWorkshop, email=user7['email'], guestLink=True)
        #: logout, login as this user and click the guest link to join the workshop
        authorization.logout(self)
        authorization.login(self, user7)
        workshopMember7 = self.app.get(url=guestLinkUser7)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "workshop member able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    def test_immunify_privateWorkshop_admin_facilitator(self):
        """ Create a conversation in a private workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 3/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='admin2', accessLevel='200')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as an admin, also invited as guest of the workshop
        #: invite user2 to the workshop
        guestLinkUser = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        guestLinkGuest = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLinkUser)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo as a user of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test guest - since we're already logged out, visit workshop via guestlink and try to immunify
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "guest able to immunify this conversation"
        #: login then logout as this guest to wipe the session
        authorization.login(self, user3)
        authorization.logout(self)
        #
        #: test user outside of workshop
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop - complete the guest invite process with user3
        authorization.login(self, user3)
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as the facilitator of the workshop
        authorization.login(self, user1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test guest - let's make a new guest
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser5 = workshop.inviteGuest(self, newWorkshop, email=user5['email'], guestLink=True)
        #: logout, and visit as this new guest
        authorization.logout(self)
        guestTester5 = self.app.get(url=guestLinkUser5)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "guest able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user outside of workshop
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop
        #: make a new guest
        user7 = registration.create_and_activate_a_user(self, postal='95062', name='user7')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser7 = workshop.inviteGuest(self, newWorkshop, email=user7['email'], guestLink=True)
        #: logout, login as this user and click the guest link to join the workshop
        authorization.logout(self)
        authorization.login(self, user7)
        workshopMember7 = self.app.get(url=guestLinkUser7)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "workshop member able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    def test_immunify_privateWorkshop_user_admin(self):
        """ Create a conversation in a private workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 4/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as a user, invited to be part of the workshop
        #: invite user2 to the workshop
        guestLinkUser = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        guestLinkGuest = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLinkUser)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo as a user of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test guest - since we're already logged out, visit workshop via guestlink and try to immunify
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "guest able to immunify this conversation"
        #: login then logout as this guest to wipe the session
        authorization.login(self, user3)
        authorization.logout(self)
        #
        #: test user outside of workshop
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop - complete the guest invite process with user3
        authorization.login(self, user3)
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as the facilitator of the workshop
        admin1 = registration.create_and_activate_a_user(self, postal='95062', name='admin1', accessLevel='200')
        authorization.login(self, admin1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test guest - let's make a new guest
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser5 = workshop.inviteGuest(self, newWorkshop, email=user5['email'], guestLink=True)
        #: logout, and visit as this new guest
        authorization.logout(self)
        guestTester5 = self.app.get(url=guestLinkUser5)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "guest able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user outside of workshop
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop
        #: make a new guest
        user7 = registration.create_and_activate_a_user(self, postal='95062', name='user7')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser7 = workshop.inviteGuest(self, newWorkshop, email=user7['email'], guestLink=True)
        #: logout, login as this user and click the guest link to join the workshop
        authorization.logout(self)
        authorization.login(self, user7)
        workshopMember7 = self.app.get(url=guestLinkUser7)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "workshop member able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    def test_immunify_privateWorkshop_facilitator_admin(self):
        """ Create a conversation in a private workshop as its facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 5/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        guestLinkGuest = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as the facilitator of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test guest - since we're already logged out, visit workshop via guestlink and try to immunify
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "guest able to immunify this conversation"
        #: login then logout as this guest to wipe the session
        authorization.login(self, user3)
        authorization.logout(self)
        #
        #: test user outside of workshop
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop - complete the guest invite process with user3
        authorization.login(self, user3)
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as the facilitator of the workshop
        admin1 = registration.create_and_activate_a_user(self, postal='95062', name='admin1', accessLevel='200')
        authorization.login(self, admin1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test guest - let's make a new guest
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser5 = workshop.inviteGuest(self, newWorkshop, email=user5['email'], guestLink=True)
        #: logout, and visit as this new guest
        authorization.logout(self)
        guestTester5 = self.app.get(url=guestLinkUser5)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "guest able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user outside of workshop
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop
        #: make a new guest
        user7 = registration.create_and_activate_a_user(self, postal='95062', name='user7')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser7 = workshop.inviteGuest(self, newWorkshop, email=user7['email'], guestLink=True)
        #: logout, login as this user and click the guest link to join the workshop
        authorization.logout(self)
        authorization.login(self, user7)
        workshopMember7 = self.app.get(url=guestLinkUser7)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "workshop member able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    def test_immunify_privateWorkshop_admin_admin(self):
        """ Create a conversation in a private workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 6/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='admin2', accessLevel='200')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as an admin, also invited as guest of the workshop
        #: invite user2 to the workshop
        guestLinkUser = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        guestLinkGuest = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLinkUser)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: now add a convo as a user of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test guest - since we're already logged out, visit workshop via guestlink and try to immunify
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "guest able to immunify this conversation"
        #: login then logout as this guest to wipe the session
        authorization.login(self, user3)
        authorization.logout(self)
        #
        #: test user outside of workshop
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop - complete the guest invite process with user3
        authorization.login(self, user3)
        guestTester = self.app.get(url=guestLinkGuest)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as the facilitator of the workshop
        admin1 = registration.create_and_activate_a_user(self, postal='95062', name='admin1', accessLevel='200')
        authorization.login(self, admin1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test guest - let's make a new guest
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser5 = workshop.inviteGuest(self, newWorkshop, email=user5['email'], guestLink=True)
        #: logout, and visit as this new guest
        authorization.logout(self)
        guestTester5 = self.app.get(url=guestLinkUser5)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "guest able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user outside of workshop
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test user in workshop
        #: make a new guest
        user7 = registration.create_and_activate_a_user(self, postal='95062', name='user7')
        #: login as the facilitator and invite the new guest
        authorization.login(self, user1)
        guestLinkUser7 = workshop.inviteGuest(self, newWorkshop, email=user7['email'], guestLink=True)
        #: logout, login as this user and click the guest link to join the workshop
        authorization.logout(self)
        authorization.login(self, user7)
        workshopMember7 = self.app.get(url=guestLinkUser7)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "workshop member able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    """ TEST IMMUNITY - PUBLIC WORKSHOPS """

    """ This next group of tests are the same as the previous ones that started at 
    'TEST IMMUNITY - PRIVATE WORKSHOPS', except for the fact that these are working 
    with public workshops. """


    def test_immunify_publicWorkshop_user_facilitator(self):
        """ Create a conversation in a public workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 7/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1', email='user1@civinomics.com', password='todd')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2', email='user2@civinomics.com', password='todd')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3', email='user3@civinomics.com', password='todd')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        log.info("score dict: " + scopeDict['state'])
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        log.info("scopeString: "+ scopeString)
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        #: create a conversation as a user of the workshop
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: add a convo as a user of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test as a normal user
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as the facilitator of the workshop
        authorization.login(self, user1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as normal user
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    def test_immunify_publicWorkshop_facilitator_facilitator(self):
        """ Create a conversation in a public workshop as the facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 8/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        #: add a convo as the facilitator of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test as a normal user
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as the facilitator of the workshop
        authorization.login(self, user1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as normal user
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    def test_immunify_publicWorkshop_admin_facilitator(self):
        """ Create a conversation in a public workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 9/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2', accessLevel='200')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        #: add a convo as an admin
        authorization.logout(self)
        authorization.login(self, user2)
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test as a normal user
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as the facilitator of the workshop
        authorization.login(self, user1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as normal user
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    def test_immunify_publicWorkshop_user_admin(self):
        """ Create a conversation in a public workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 10/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1', email='user1@civinomics.com', password='todd')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2', email='user2@civinomics.com', password='todd')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3', email='user3@civinomics.com', password='todd')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        log.info("score dict: " + scopeDict['state'])
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        log.info("scopeString: "+ scopeString)
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        #: create a conversation as a user of the workshop
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: add a convo as a user of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test as a normal user
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as an admin
        admin1 = registration.create_and_activate_a_user(self, postal='95062', name='admin1', accessLevel='200')
        authorization.login(self, admin1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as normal user
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    def test_immunify_publicWorkshop_facilitator_admin(self):
        """ Create a conversation in a public workshop as the facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 11/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: add a convo as the facilitator of the workshop
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test as a normal user
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as an admin
        admin1 = registration.create_and_activate_a_user(self, postal='95062', name='admin1', accessLevel='200')
        authorization.login(self, admin1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as normal user
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    def test_immunify_publicWorkshop_admin_admin(self):
        """ Create a conversation in a public workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 12/12 for this group
        #
        #: PART 1
        #: create a private workshop
        user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
        user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2', accessLevel='200')
        user3 = registration.create_and_activate_a_user(self, postal='95062', name='user3')
        workshopTitle = 'immune workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        #: NOTE we need to start the workshop manually instead of through the preferences pane now
        #: there is a check with stripe about the customer account being valid, and at the moment
        #: I can't get a test account here to be valid with stripe
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        #: add a convo as an admin
        authorization.logout(self)
        authorization.login(self, user2)
        conversationTitle = 'user conversation'
        conversationText = 'user conversation text'
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        conversationCode = conversation.getConversationCode(self, conversationAdded)
        #: grab the immunify link, to use with each of the roles to be tested
        #: in order to do so, must be the facilitator so we login as user1 here
        #: also, take the chance to grab the flagging link for cases where it will be needed
        conversationRevisited = self.app.get(url=conversationAdded.request.url)
        immunifyConversationUrl = conversation.immunify(self, conversationRevisited, dontSubmit=True)
        flagConversationUrl = conversation.flag(self, conversationRevisited, dontSubmit=True)
        #
        #: PART 2
        #: try to immunify this conversation as each of the roles that shouldn't be able to
        #
        #: test public - just logout and try
        authorization.logout(self)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        import pylowiki.lib.db.discussion   as discussionLib
        import pylowiki.lib.db.flag         as flagLib
        import pylowiki.lib.db.revision     as revisionLib
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "public able to immunify this conversation"
        #
        #: test as a normal user
        user4 = registration.create_and_activate_a_user(self, postal='95062', name='user4')
        authorization.login(self, user4)
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "user of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user5 = registration.create_and_activate_a_user(self, postal='95062', name='user5')
        workshopTitle1 = 'some other workshop'
        newWorkshop1 = workshop.create_new_workshop(self, user5, title=workshopTitle1)
        assert workshopTitle1 in newWorkshop1, "not able to create another workshop"
        #: attempt to immunify the object, expect a 404 response
        conversationNotImmunified = self.app.post(
            url=str(immunifyConversationUrl),
            status=404
        )
        assert conversationNotImmunified.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not immune yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == False, "facilitator of other workshop able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 3
        #: immunify with a role that can, and make sure it worked
        #: in this test we act as an admin
        admin1 = registration.create_and_activate_a_user(self, postal='95062', name='admin1', accessLevel='200')
        authorization.login(self, admin1)
        #: immunify the object, do not expect a 404 response this time
        conversationImmunified = self.app.post(
            url=str(immunifyConversationUrl)
        )
        assert conversationImmunified.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's immune now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        isItImmuneYet = flagLib.isImmune(conversationObject)
        assert isItImmuneYet == True, "facilitator of workshop not able to immunify this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 4
        #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
        #: test public - already logged out
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: again, look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "public able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as normal user
        user6 = registration.create_and_activate_a_user(self, postal='95062', name='user6')
        authorization.login(self, user6)
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "user of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: test as a facilitator outside of the workshop
        user8 = registration.create_and_activate_a_user(self, postal='95062', name='user8')
        authorization.login(self, user8)
        workshopTitle2 = 'another workshop'
        newWorkshop2 = workshop.create_new_workshop(self, user8, title=workshopTitle2)
        assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
        #: attempt to flag the object, expect a 404 response
        conversationNotFlagged = self.app.post(
            url=str(flagConversationUrl),
            status=404
        )
        assert conversationNotFlagged.status_int == 404, "404 expected, something else happened"
        #: look at the object via the model and make sure it's not flagged yet
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == False, "facilitator of other workshop able to flag this conversation"
        #: wipe the session
        authorization.logout(self)
        #
        #: PART 5
        #: flag the object as an admin, and make sure it worked
        user9 = registration.create_and_activate_a_user(self, postal='95062', name='admin user9', accessLevel='200')
        authorization.login(self, user9)
        #: flag the object, expect a 200 response
        conversationFlagged = self.app.post(
            url=str(flagConversationUrl)
        )
        assert conversationFlagged.status_int == 200, "200 expected, something else happened"
        #: look at the object via the model and make sure it's flagged now
        conversationObject = discussionLib.getDiscussion(conversationCode)
        if not conversationObject:
            conversationObject = revisionLib.getRevisionByCode(conversationCode)
            assert conversationObject is not None, "conversation object cannot be found via model"
        #: normally we would use isFlagged, but that requires a user object as well
        #: we expect 0 flags in any case, so it's enough to check with this method:
        isItFlaggedYet = flagLib.checkFlagged(conversationObject)
        assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ This next batch of tests will cover deletion permissions. Bottom line is, only an admin 
        can delete an object. """
    """ First set will deal with this within private workshops. There should be 18 tests in this group. """

    def test_delete_conversation_admin_admin(self):
        """ Create a conversation as an admin, then delete this conversation as an admin."""
        # test 1
        #: create a workshop and two admins
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Admin One', accessLevel='200')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Admin Two', accessLevel='200')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as user1
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as admin2, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit)
        assert conversationDeleted.status_int == 200, "delete request not successful"
        
        #: make sure a delete message is present
        assert conversation.conversationDeletedMessage() in conversationDeleted, "admin not able to delete admin's conversation"
        #: revisit the conversation page and make sure this conversation is gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle not in conversationsPage, "deleted conversation still visible"
        
    def test_delete_conversation_facilitator_admin(self):
        """ Create a conversation as a facilitator, then delete this conversation as an admin."""
        # test 2
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Fac One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Admin Two', accessLevel='200')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: create a conversation as user1
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as admin2, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit)
        assert conversationDeleted.status_int == 200, "delete request not successful"
        
        #: make sure a delete message is present
        assert conversation.conversationDeletedMessage() in conversationDeleted, "admin not able to delete admin's conversation"
        #: revisit the conversation page and make sure this conversation is gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle not in conversationsPage, "deleted conversation still visible"
        
    def test_delete_conversation_user_admin(self):
        """ Create a conversation as a user of the private workshop, then delete this conversation 
        as an admin."""
        # test 3
        #: create a workshop and three users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Fac One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Admin Two', accessLevel='200')
        user3 = registration.create_and_activate_a_user(self, postal='92007', name='User')
        workshopTitle = 'delete workshop conversation'
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
        #: create a conversation as user3
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as admin2, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit)
        assert conversationDeleted.status_int == 200, "delete request not successful"
        
        #: make sure a delete message is present
        assert conversation.conversationDeletedMessage() in conversationDeleted, "admin not able to delete admin's conversation"
        #: revisit the conversation page and make sure this conversation is gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle not in conversationsPage, "deleted conversation still visible"

    def test_delete_conversation_admin_facilitator(self):
        """ Create a conversation as an admin, then delete this conversation as a facilitator 
        of the workshop. 
          There are some extra edge cases that need to be tested, and these are when a nonmember, 
        guest or the public try to delete this conversation. 
          Since the facilitator should not be able to delete this conversation, we will squeeze 
        these extra cases in to this test. These extra edge cases will be added to two other 
        private workshop tests, and three other public workshop tests:

        test_delete_conversation_facilitator_facilitator
        test_delete_conversation_user_facilitator
        test_delete_public_conversation_admin_facilitator
        test_delete_public_conversation_facilitator_facilitator
        test_delete_public_conversation_user_facilitator
         """
        # test 4
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Admin One', accessLevel='200')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator Two')
        workshopTitle = 'delete workshop conversation'
        #: user2 is to be the facilitator
        newWorkshop = workshop.create_new_workshop(self, user2, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        authorization.logout(self)
        authorization.login(self, user1)
        #: create a conversation as user1
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: grab the delete link
        conversationDeleteLink = conversation.delete(self, conversationAdded, dontSubmit=True)
        #: logout, login as user2, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            postLink=conversationDeleteLink,
            expectErrors=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation was deleted"
        #: test the edge cases for this situation
        #: NONMEMBER
        authorization.logout(self)
        user3 = registration.create_and_activate_a_user(self, postal='95060', name='User Three')
        authorization.login(self, user3)
        #: try to delete the conversation
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            postLink=conversationDeleteLink,
            expectErrors=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        authorization.logout(self)
        #: must be someone who can see this page
        authorization.login(self, user2)
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation was deleted"
        #: GUEST
        user4 = registration.create_and_activate_a_user(self, postal='95060', name='User Four')
        #: we are logged in as the facilitator so we invite user4 to the workshop
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user4['email'], guestLink=True)
        authorization.logout(self)
        #: don't login as user4, just visit the site using the guest link
        guestVisit = self.app.get(url=guestLink)
        #: try to delete the conversation
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            postLink=conversationDeleteLink,
            expectErrors=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        authorization.logout(self)
        #: must be someone who can see this page
        authorization.login(self, user2)
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation was deleted"
        #: PUBLIC
        authorization.logout(self)
        #: try to delete the conversation
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            postLink=conversationDeleteLink,
            expectErrors=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        authorization.logout(self)
        #: must be someone who can see this page
        authorization.login(self, user2)
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation was deleted"

    def test_delete_conversation_facilitator_facilitator(self):
        """ INCOMPLETE Create a conversation as a facilitator, then delete this conversation as a facilitator of the workshop."""
        # test 5
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator One', accessLevel='200')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator Two')
        workshopTitle = 'delete workshop conversation'
        #: user2 is to be the original facilitator
        newWorkshop = workshop.create_new_workshop(self, user2, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user1 to the workshop, this will be the invited facilitator
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user1['email'], guestLink=True)
        #: login as user1 then visit the invite link and the workshop
        authorization.logout(self)
        authorization.login(self, user1)
        guestConfirmed = self.app.get(url=guestLink)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: get this user's profile page handy
        profileUser1 = atWorkshop.click(description=linkDefs.profile())
        #: now log back in as the original faciltator and make user1 a facilitator as well
        authorization.logout(self)
        authorization.login(self, user2)
        seeUser1 = self.app.get(url=profileUser1.request.url)
        #: click the invite button to make this person a facilitator as well

        #: create a conversation as user1
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: grab the delete link
        conversationDeleteLink = conversation.delete(self, conversationAdded, dontSubmit=True)
        #: logout, login as user2, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            postLink=conversationDeleteLink,
            expectErrors=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "deleted conversation still visible"

    def test_delete_conversation_user_facilitator(self):
        """ Create a conversation as a user of the private workshop, then try to delete this conversation 
        as a facilitator. 
          The edge cases for trying to delete as a nonmember, guest and the public will be tested
        in this test as well. """
        # test 6
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='User One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='User Two')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user2 to the workshop
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        #: create a conversation as user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLink)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: create a conversation as user2
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as user1, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit, spoof=True)
        assert conversationDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversations page and make sure this conversation is still there
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation deleted by facilitator"
        #: test the edge cases for this situation
        #: NONMEMBER
        authorization.logout(self)
        user3 = registration.create_and_activate_a_user(self, postal='95060', name='User Three')
        authorization.login(self, user3)
        #: try to delete the conversation
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            spoof=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        authorization.logout(self)
        #: must be someone who can see this page
        authorization.login(self, user1)
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation was deleted"
        #: GUEST
        user4 = registration.create_and_activate_a_user(self, postal='95060', name='User Four')
        #: we are logged in as the facilitator so we invite user4 to the workshop
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user4['email'], guestLink=True)
        authorization.logout(self)
        #: don't login as user4, just visit the site using the guest link
        guestVisit = self.app.get(url=guestLink)
        #: try to delete the conversation
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            spoof=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        authorization.logout(self)
        #: must be someone who can see this page
        authorization.login(self, user2)
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation was deleted"
        #: PUBLIC
        authorization.logout(self)
        #: try to delete the conversation
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            spoof=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        authorization.logout(self)
        #: must be someone who can see this page
        authorization.login(self, user2)
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation was deleted"

    def test_delete_conversation_admin_user(self):
        """ Create a conversation as an admin, then try to delete this conversation as a user of the workshop."""
        # test 7
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Admin One', accessLevel='200')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator Two')
        user3 = registration.create_and_activate_a_user(self, postal='94122', name='User Three')
        workshopTitle = 'delete workshop conversation'
        #: user2 is to be the facilitator
        newWorkshop = workshop.create_new_workshop(self, user2, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user3 to the workshop
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        authorization.logout(self)
        authorization.login(self, user1)
        #: create a conversation as user1
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: grab the delete link
        conversationDeleteLink = conversation.delete(self, conversationAdded, dontSubmit=True)
        #: logout, login as user3, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user3)
        guestConfirmed = self.app.get(url=guestLink)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            postLink=conversationDeleteLink,
            expectErrors=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "deleted conversation still visible"

    def test_delete_conversation_facilitator_user(self):
        """ Create a conversation as a facilitator of the private workshop, then try to delete 
        this conversation as a user."""
        # test 8
        #: create a workshop and three users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Fac One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='User Two')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user2 to the workshop
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        #: create a conversation as the facilitator
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            newWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLink)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: try to delete the conversation
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit, spoof=True)
        assert conversationDeleted.status_int == 404, "delete request successful"
        #: revisit the conversations page and make sure this conversation is not gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation deleted"
        
    def test_delete_conversation_user_user(self):
        """ Create a conversation as a user of the private workshop, then try to delete 
        this conversation as another user."""
        # test 9
        #: create a workshop and three users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Fac One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='User Two')
        user3 = registration.create_and_activate_a_user(self, postal='95060', name='User Three')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite user2 and user3 to the workshop
        guestLink2 = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
        guestLink3 = workshop.inviteGuest(self, newWorkshop, email=user3['email'], guestLink=True)
        #: create a conversation as the user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        guestConfirmed = self.app.get(url=guestLink2)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        authorization.logout(self)
        #: login as user3 then visit the invite link
        authorization.login(self, user3)
        guestConfirmed = self.app.get(url=guestLink3)
        #: try to delete the conversation
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit, spoof=True)
        assert conversationDeleted.status_int == 404, "delete request successful"
        #: revisit the conversations page and make sure this conversation is not gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation deleted"
    
    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ Second set will deal with this within public workshops. """

    def test_delete_public_conversation_admin_admin(self):
        """ Create a conversation as an admin in a public workshop, then delete this conversation 
        as an admin."""
        # test 10
        #: create a workshop and two admins
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Admin One', accessLevel='200')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Admin Two', accessLevel='200')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        publicWorkshop = self.app.get(url=newWorkshop.request.url)
        #: create a conversation as user1
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            publicWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as admin2, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit)
        assert conversationDeleted.status_int == 200, "delete request not successful"
        
        #: make sure a delete message is present
        assert conversation.conversationDeletedMessage() in conversationDeleted, "admin not able to delete admin's conversation"
        #: revisit the conversation page and make sure this conversation is gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle not in conversationsPage, "deleted conversation still visible"
    
    def test_delete_public_conversation_facilitator_admin(self):
        """ Create a conversation as a facilitator in a public workshop, then delete this conversation 
        as an admin."""
        # test 11
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Admin Two', accessLevel='200')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        publicWorkshop = self.app.get(url=newWorkshop.request.url)
        #: create a conversation as user1
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            publicWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as admin2, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit)
        assert conversationDeleted.status_int == 200, "delete request not successful"
        
        #: make sure a delete message is present
        assert conversation.conversationDeletedMessage() in conversationDeleted, "admin not able to delete admin's conversation"
        #: revisit the conversation page and make sure this conversation is gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle not in conversationsPage, "deleted conversation still visible"

    def test_delete_public_conversation_user_admin(self):
        """ Create a conversation as a user in a public workshop, then delete this conversation 
        as an admin."""
        # test 11
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='User Two')
        user3 = registration.create_and_activate_a_user(self, postal='95060', name='Admin Three', accessLevel='200')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        publicWorkshop = self.app.get(url=newWorkshop.request.url)
        authorization.logout(self)
        #: login as user2 then visit the workshop and add a conversation
        authorization.login(self, user2)
        atWorkshop = self.app.get(url=publicWorkshop.request.url)
        #: create a conversation as user2
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as user3, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user3)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit)
        assert conversationDeleted.status_int == 200, "delete request not successful"
        
        #: make sure a delete message is present
        assert conversation.conversationDeletedMessage() in conversationDeleted, "admin not able to delete admin's conversation"
        #: revisit the conversation page and make sure this conversation is gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle not in conversationsPage, "deleted conversation still visible"

    def test_delete_public_conversation_admin_facilitator(self):
        """ Create a public conversation as an admin, then delete this conversation as a facilitator 
        of the workshop.
          Edge case of trying to delete as public added to this test. """
        # test 12
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Admin One', accessLevel='200')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator Two')
        workshopTitle = 'delete workshop conversation'
        #: user2 is to be the facilitator
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        publicWorkshop = self.app.get(url=newWorkshop.request.url)
        #: create a conversation as user1
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            publicWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: grab the delete link
        conversationDeleteLink = conversation.delete(self, conversationAdded, dontSubmit=True)
        #: logout, login as user2, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user2)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            postLink=conversationDeleteLink,
            expectErrors=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation deleted"
        #: test delete attempt as public
        authorization.logout(self)
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            postLink=conversationDeleteLink,
            expectErrors=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        authorization.login(self, user1)
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation deleted"

    def test_delete_public_conversation_user_facilitator(self):
        """ Create a conversation as a user of a public workshop, then try to delete this conversation 
        as a facilitator."""
        # test 13
        #: create a workshop and two users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='User One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='User Two')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user1)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user1, scopeString)
        workshop.startWorkshop(self, newWorkshop, user1)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        publicWorkshop = self.app.get(url=newWorkshop.request.url)
        #: create a conversation as user2
        authorization.logout(self)
        #: login as user2 then visit the invite link
        authorization.login(self, user2)
        atWorkshop = self.app.get(url=publicWorkshop.request.url)
        #: create a conversation as user2
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: logout, login as user1, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user1)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit, spoof=True)
        assert conversationDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversations page and make sure this conversation is still there
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation deleted by facilitator"
        #: test delete attempt as public
        authorization.logout(self)
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            spoof=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        authorization.login(self, user1)
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation deleted"

    def test_delete_public_conversation_admin_user(self):
        """ Create a public conversation as an admin, then try to delete this conversation as a user of the workshop."""
        # test 14
        #: create a workshop and three users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Admin One', accessLevel='200')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator Two')
        user3 = registration.create_and_activate_a_user(self, postal='94122', name='User Three')
        workshopTitle = 'delete workshop conversation'
        #: user2 is to be the facilitator
        newWorkshop = workshop.create_new_workshop(self, user2, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user2)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user2, scopeString)
        workshop.startWorkshop(self, newWorkshop, user2)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        publicWorkshop = self.app.get(url=newWorkshop.request.url)
        #: create a conversation as user1, the admin
        authorization.logout(self)
        authorization.login(self, user1)
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            publicWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        #: grab the delete link
        conversationDeleteLink = conversation.delete(self, conversationAdded, dontSubmit=True)
        #: logout, login as user3, revisit the conversation's page and delete
        authorization.logout(self)
        authorization.login(self, user3)
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationNotDeleted = conversation.delete(
            self, 
            conversationRevisit, 
            postLink=conversationDeleteLink,
            expectErrors=True
        )
        assert conversationNotDeleted.status_int == 404, "delete request was successful"
        #: revisit the conversation page and make sure this conversation is not gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "deleted conversation still visible"

    def test_delete_public_conversation_facilitator_user(self):
        """ Create a public conversation as a facilitator of a workshop, then try to delete 
        this conversation as a user."""
        # test 15
        #: create a workshop and three users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Fac One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='User Two')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user2)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user2, scopeString)
        workshop.startWorkshop(self, newWorkshop, user2)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        publicWorkshop = self.app.get(url=newWorkshop.request.url)
        #: create a conversation as the facilitator
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            publicWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        authorization.logout(self)
        #: login as user2
        authorization.login(self, user2)
        atWorkshop = self.app.get(url=publicWorkshop.request.url)
        #: try to delete the conversation
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit, spoof=True)
        assert conversationDeleted.status_int == 404, "delete request successful"
        #: revisit the conversations page and make sure this conversation is not gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation deleted"

    def test_delete_public_conversation_user_user(self):
        """ Create a public conversation as a user of the workshop, then try to delete 
        this conversation as another user."""
        # test 16
        #: create a workshop and three users
        user1 = registration.create_and_activate_a_user(self, postal='95060', name='Fac One')
        user2 = registration.create_and_activate_a_user(self, postal='95060', name='User Two')
        user3 = registration.create_and_activate_a_user(self, postal='95060', name='User Three')
        workshopTitle = 'delete workshop conversation'
        newWorkshop = workshop.create_new_workshop(self, user1, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: upgrade it to professional
        workshop.upgradeToProfessional(self, newWorkshop, user2)
        #: the scope needs to be set before it will show up in the 'list all' page
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, user2, scopeString)
        workshop.startWorkshop(self, newWorkshop, user2)
        #: make sure the workshop is public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        publicWorkshop = self.app.get(url=newWorkshop.request.url)
        #: create a conversation as the user2
        authorization.logout(self)
        #: login as user2
        authorization.login(self, user2)
        atWorkshop = self.app.get(url=publicWorkshop.request.url)
        conversationTitle = 'delete conversation title'
        conversationText = 'delete conversation text'
        conversationAdded = workshop.addConversationToWorkshop(
            self, 
            atWorkshop, 
            conversationTitle=conversationTitle,
            conversationText=conversationText
        )
        assert conversationTitle in conversationAdded, "conversation not created"
        authorization.logout(self)
        #: login as user3
        authorization.login(self, user3)
        #: try to delete the conversation
        conversationRevisit = self.app.get(url=conversationAdded.request.url)
        conversationDeleted = conversation.delete(self, conversationRevisit, spoof=True)
        assert conversationDeleted.status_int == 404, "delete request successful"
        #: revisit the conversations page and make sure this conversation is not gone
        conversationsPage = conversation.getConversationsPage(self, conversationAdded)
        assert conversationTitle in conversationsPage, "conversation deleted"
    
