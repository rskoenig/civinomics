# -*- coding: utf-8 -*-
from pylowiki.tests import *
import re

import pylowiki.tests.helpers.authorization as authorization
import pylowiki.tests.helpers.conversation as conversation
import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.idea as idea
import pylowiki.tests.helpers.noun_definitions as nounDefs
import pylowiki.tests.helpers.noun_helpers as nounHelp
import pylowiki.tests.helpers.noun_verb_actions as nounAction
import pylowiki.tests.helpers.page_definitions as pageDefs
import pylowiki.tests.helpers.resource as resource
import pylowiki.tests.helpers.registration as registration
import pylowiki.tests.helpers.workshops as workshop


import logging
log = logging.getLogger(__name__)

""" generalized tests that can be used for the three main object types of the site: 
    conversations, resources and ideas """

#NOTE - in the case where a facilitator can, add code that will flag/immunfy the object 
#and assert it happened .. I may just need to run another gamut of tests where the 
#final flagger is a facilitator

def runDeleteTests(self, objectType, objectPage, objectTitle, workshopPage, facilitator, **kwargs):
    """ Test cases for deleting an object that should not work. """
    #: create the roles and links we'll need
    authorization.login(self, facilitator)
    guest = registration.create_and_activate_a_user(self, postal='95062', name='Guest')
    nonMember = registration.create_and_activate_a_user(self, postal='95062', name='Non member')
    member = registration.create_and_activate_a_user(self, postal='95062', name='Member')
    outsideFacilitator = registration.create_and_activate_a_user(self, postal='95062', name='Outside facilitator')
    guestLink = workshop.inviteGuest(self, workshopPage, email=guest['email'], guestLink=True)
    memberLink = workshop.inviteGuest(self, workshopPage, email=member['email'], guestLink=True)
    authorization.logout(self)
    #
    #: test as the public
    objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'delete', spoof=True)
    #: make sure the object has not been deleted
    authorization.login(self, facilitator)
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectPage)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectPage)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectPage)
    assert objectTitle in listingPage, "object has been deleted"
    authorization.logout(self)
    #
    #: test as a guest
    guestVisit = self.app.get(url=guestLink)
    #: try to delete
    objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'delete', spoof=True)
    #: make sure the object has not been deleted
    authorization.logout(self)
    authorization.login(self, facilitator)
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectPage)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectPage)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectPage)
    assert objectTitle in listingPage, "object has been deleted"
    #
    #: test as a site user who is not a member of the private workshop
    authorization.logout(self)
    authorization.login(self, nonMember)
    #: try to delete
    objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'delete', spoof=True)
    #: make sure the object has not been deleted
    authorization.logout(self)
    authorization.login(self, facilitator)
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectPage)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectPage)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectPage)
    assert objectTitle in listingPage, "object has been deleted"
    authorization.logout(self)
    #
    #: test as a site user who is a member of the private workshop
    authorization.login(self, member)
    memberConfirmed = self.app.get(url=memberLink)
    #: try to delete
    objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'delete', spoof=True)
    #: make sure the object has not been deleted
    authorization.logout(self)
    authorization.login(self, facilitator)
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectPage)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectPage)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectPage)
    assert objectTitle in listingPage, "object has been deleted"
    authorization.logout(self)
    #
    #: test as the facilitator
    authorization.login(self, facilitator)
    if 'facilitatorCan' in kwargs:
        if kwargs['facilitatorCan'] == True:
            #: in this case the factilitator can delete this object, 
            #: so we let the originating test handle that case
            return True
    #: try to delete
    objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'delete', spoof=True)
    #: make sure the object has not been deleted
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectPage)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectPage)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectPage)
    assert objectTitle in listingPage, "object has been deleted"
    authorization.logout(self)
    return True    

def runEnableTests(self, objectType, objectPage, workshopPage, facilitator, admin, **kwargs):
    """ Test cases for enabling this object. The only roles that should be able to 
    enable this will be an admin or a facilitator. No other roles should be able to do this, 
    so they will be tested first. Finally, the facilitator and admin roles will enable the 
    object. """
    #: can't enable: public, guest, nonmember, member, facilitator
    #
    #: test public enable action
    authorization.logout(self)
    objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'enable', spoof=True)
    #: make sure the object has not been enabled
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectPage.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "disabled object has been enabled"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "disabled object has been enabled"
    #
    #: test guest enable action
    guest = registration.create_and_activate_a_user(self, postal='92007', name='Guest')
    authorization.logout(self)
    authorization.login(self, facilitator)
    guestLink = workshop.inviteGuest(self, workshopPage, email=guest['email'], guestLink=True)
    authorization.logout(self)
    visitAsGuest = self.app.get(url=guestLink)
    objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'enable', spoof=True)
    #: make sure the object has not been enabled
    authorization.login(self, guest)
    authorization.logout(self)
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectPage.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "disabled object has been enabled"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "disabled object has been enabled"
    authorization.logout(self)
    #
    #: test nonmember enable action
    nonMember = registration.create_and_activate_a_user(self, postal='92007', name='Nonmember')
    authorization.login(self, nonMember)
    objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'enable', spoof=True)
    #: make sure the object has not been enabled
    authorization.logout(self)
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectPage.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "disabled object has been enabled"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "admin-disabled object has been enabled"
    authorization.logout(self)
    #
    #: test member enable action
    member = registration.create_and_activate_a_user(self, postal='92007', name='Member')
    authorization.login(self, facilitator)
    memberInviteLink = workshop.inviteGuest(self, workshopPage, email=member['email'], guestLink=True)
    authorization.logout(self)
    authorization.login(self, member)
    becomeMember = self.app.get(url=memberInviteLink)
    objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'enable', spoof=True)
    #: make sure the object has not been enabled
    authorization.logout(self)
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectPage.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "disabled object has been enabled"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "disabled object has been enabled"
    #
    if 'facilitatorCan' in kwargs:
        if kwargs['facilitatorCan'] == True:
            # already logged in as a facilitator, show it's possible:
            objectRevisit = self.app.get(url=objectPage.request.url)
            #: make sure a disable message is present
            assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "disabled object has been enabled"
            #: make sure a comment form is not present
            assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "disabled object has already been enabled"
            #: enable it
            objectEnabled = nounAction.verbAdmin(self, objectRevisit, 'enable')
            #: make sure the object has been enabled
            objectRevisitAgain = self.app.get(url=objectRevisit.request.url)
            #: make sure a disable message is not present
            assert nounDefs.objectDisabledMessage(objectType) not in objectRevisitAgain, "facilitator not able to enable the disabled object"
            #: make sure a comment form is present
            assert formHelpers.isFormPresentByAction(objectRevisitAgain, 'comment') == True, "facilitator not able to enable the disabled object"
            #: now disable it again, so we can make sure the admin can enable this as well
            objectDisabled = nounAction.verbAdmin(self, objectRevisitAgain, 'disable')
            assert objectDisabled.status_int == 200, "disable request not successful"
            #: revisit the object page
            objectReloaded = self.app.get(url=objectRevisitAgain.request.url)
            #: make sure a disable message is present
            assert nounDefs.objectDisabledMessage(objectType) in objectReloaded, "not able to disable object"
            #: make sure a comment form is not present
            assert formHelpers.isFormPresentByAction(objectReloaded, 'comment') == False, "not able to disable object, comment form present"
        else:
            #: visit as facilitator and try to enable (already logged in as facilitator)
            objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'enable', spoof=True)
            #: make sure the object has not been enabled
            objectRevisit = self.app.get(url=objectPage.request.url)
            #: make sure a disable message is present
            assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "disabled object has been enabled"
            #: make sure a comment form is not present
            assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "disabled object has been enabled"
    else:
        #: visit as facilitator and try to enable (already logged in as facilitator)
        objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'enable', spoof=True)
        #: make sure the object has not been enabled
        objectRevisit = self.app.get(url=objectPage.request.url)
        #: make sure a disable message is present
        assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "disabled object has been enabled"
        #: make sure a comment form is not present
        assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "disabled object has been enabled"
    #
    # can enable: admin
    #: Finally, visit as an admin and enable the object.
    authorization.logout(self)
    authorization.login(self, admin)
    objectAdminView = self.app.get(url=objectPage.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectAdminView, "disabled object has already been enabled"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "disabled object has already been enabled"
    #: enable the object
    objectEnabled = nounAction.verbAdmin(self, objectAdminView, 'enable')
    #: make sure the object has been enabled
    objectAdminReload = self.app.get(url=objectAdminView.request.url)
    #: make sure a disable message is not present
    assert nounDefs.objectDisabledMessage(objectType) not in objectAdminReload, "admin not able to enable an admin-disabled object"
    #: make sure a comment form is present
    assert formHelpers.isFormPresentByAction(objectAdminReload, 'comment') == True, "admin not able to enable an admin-disabled object"


def runFlaggingTests(
        self, 
        objectType,
        objectCode, 
        objectPage,
        workshopPage,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib, 
        flagLib, 
        revisionLib,
        **kwargs):
    """ Test cases that should not work for flagging an immune object. """
    #
    # test public
    authorization.logout(self)
    objectNotFlagged = nounAction.flag(self, objectPage, expectErrors=True)
    #: look at the object via the model and make sure it's not flagged yet
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    #: normally we would use isFlagged, but that requires a user object as well
    #: we expect 0 flags in any case, so it's enough to check with this method:
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == False, "public able to flag this object"
    #: wipe the session
    authorization.logout(self)
    #
    #: test guest - let's make a new guest
    guest = registration.create_and_activate_a_user(self, postal='95062', name='guest flagger')
    #: login as the facilitator and invite the new guest
    authorization.login(self, facilitator)
    guestLink = workshop.inviteGuest(self, workshopPage, email=guest['email'], guestLink=True)
    #: logout, and visit as this new guest
    authorization.logout(self)
    guestTester = self.app.get(url=guestLink)
    #: attempt to flag the object, expect a 404 response
    objectNotFlagged = nounAction.flag(self, objectPage, expectErrors=True)
    #: look at the object via the model and make sure it's not flagged yet
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect there to be 0 flags on this object:
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == False, "guest able to flag this object"
    #: wipe the session
    authorization.logout(self)
    #
    #: test user outside of workshop
    nonMember = registration.create_and_activate_a_user(self, postal='95062', name='non member')
    authorization.login(self, nonMember)
    #: attempt to flag the object, expect a 404 response
    objectNotFlagged = nounAction.flag(self, objectPage, expectErrors=True)
    #: look at the object via the model and make sure it's not flagged yet
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect there to be 0 flags on this object:
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == False, "user of site, not of this private workshop, able to flag this object"
    #: wipe the session
    authorization.logout(self)
    #
    #: test user in workshop
    #: make a new guest
    member = registration.create_and_activate_a_user(self, postal='95062', name='member')
    #: login as the facilitator and invite the new guest
    authorization.login(self, facilitator)
    guestLinkMember = workshop.inviteGuest(self, workshopPage, email=member['email'], guestLink=True)
    #: logout, login as this user and click the guest link to join the workshop
    authorization.logout(self)
    authorization.login(self, member)
    workshopMember = self.app.get(url=guestLinkMember)
    #: attempt to flag the object, expect a 404 response
    objectNotFlagged = nounAction.flag(self, objectPage, expectErrors=True)
    #: look at the object via the model and make sure it's not flagged yet
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect there to be 0 flags on this object:
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == False, "user of private workshop able to flag this object"
    #: wipe the session
    authorization.logout(self)
    #
    #: test as a facilitator outside of the workshop
    ousideFacilitator = registration.create_and_activate_a_user(self, postal='95062', name='Outside Facilitator')
    authorization.login(self, ousideFacilitator)
    workshopTitle2 = 'another workshop'
    #: create a separate workshop - note the login parameter, we're already logged in
    newWorkshop2 = workshop.create_new_workshop(self, ousideFacilitator, title=workshopTitle2, login=False)
    assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
    #: attempt to flag the object, expect a 404 response
    objectNotFlagged = nounAction.flag(self, objectPage, expectErrors=True)
    #: look at the object via the model and make sure it's not flagged yet
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect there to be 0 flags on this object:
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == False, "facilitator of a different workshop is able to flag this object"
    #: wipe the session
    authorization.logout(self)
    #
    if 'facilitatorCant' in kwargs:
        if kwargs['facilitatorCant'] == True:
            #: visit as facilitator and try to flag
            authorization.login(self, facilitator)
            objectNotFlagged = nounAction.flag(self, objectPage, expectErrors=True)
            #: look at the object via the model and make sure it's not flagged
            if objectType == 'conversation':
                nounObject = discussionLib.getDiscussion(objectCode)
            elif objectType == 'idea':
                nounObject = ideaLib.getIdea(objectCode)
            elif objectType == 'resource':
                nounObject = resourceLib.getResourceByCode(objectCode)
            if not nounObject:
                nounObject = revisionLib.getRevisionByCode(objectCode)
                assert nounObject is not None, "object cannot be found via model"
            #: we expect there to be 0 flags on this object:
            isItFlaggedYet = flagLib.checkFlagged(nounObject)
            assert isItFlaggedYet == False, "facilitator able to flag this object"
            #: wipe the session
            authorization.logout(self) 
    #: this part of flag testing is done
    return True


def runImmunifyTests(
        self, 
        objectType, 
        objectCode,
        objectPage,
        workshopPage,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        **kwargs
    ):
    """ Test cases that should not work for making this object immune to flagging. """
    #
    #: test public - just logout and try
    authorization.logout(self)
    objectNotImmunified = nounAction.verbAdmin(self, objectPage, 'immunify', spoof=True)
    #: look at the object via the model and make sure it's not immune yet
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == False, "public able to immunify this object"
    #
    #: test guest
    newGuest = registration.create_and_activate_a_user(self, postal='92007', name='New Guest')
    authorization.login(self, facilitator)
    guestInviteLink = workshop.inviteGuest(self, workshopPage, email=newGuest['email'], guestLink=True)
    authorization.logout(self)
    guestTester = self.app.get(url=guestInviteLink)
    #: attempt to immunify the object, expect a 404 response
    objectNotImmunified = nounAction.verbAdmin(self, objectPage, 'immunify', spoof=True)
    #: look at the object via the model and make sure it's not immune yet
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == False, "guest able to immunify this object"
    #: login then logout as this guest to wipe the session
    authorization.login(self, newGuest)
    authorization.logout(self)
    #
    #: test user outside of workshop
    outsideUser = registration.create_and_activate_a_user(self, postal='95062', name='Outside User')
    authorization.login(self, outsideUser)
    #: attempt to immunify the object
    objectNotImmunified = nounAction.verbAdmin(self, objectPage, 'immunify', spoof=True)
    #: look at the object via the model and make sure it's not immune yet
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == False, "user outside of workshop able to immunify this object"
    #: wipe the session
    authorization.logout(self)
    #
    #: test user in workshop - complete the guest invite process with user3
    newerGuest = registration.create_and_activate_a_user(self, postal='92007', name='New Guest')
    authorization.login(self, facilitator)
    newerGuestInviteLink = workshop.inviteGuest(self, workshopPage, email=newerGuest['email'], guestLink=True)
    authorization.logout(self)
    authorization.login(self, newerGuest)
    memberConfirmed = self.app.get(url=newerGuestInviteLink)
    #: attempt to immunify the object, expect a 404 response
    objectNotImmunified = nounAction.verbAdmin(self, objectPage, 'immunify', spoof=True)
    #: look at the object via the model and make sure it's not immune yet
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == False, "member of workshop able to immunify this object"
    #: login then logout as this guest to wipe the session
    authorization.logout(self)
    #
    #: attempt to immunify the object as the facilitator of another workshop
    ousideFacilitator = registration.create_and_activate_a_user(self, postal='95062', name='Outside Facilitator')
    authorization.login(self, ousideFacilitator)
    workshopTitle2 = 'another workshop'
    #: create a separate workshop - note the login parameter, we're already logged in
    newWorkshop2 = workshop.create_new_workshop(self, ousideFacilitator, title=workshopTitle2, login=False)
    assert workshopTitle2 in newWorkshop2, "not able to create another workshop"
    objectNotImmunified = nounAction.verbAdmin(self, objectPage, 'immunify', spoof=True)
    #: look at the object via the model and make sure it's not immune yet
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(objectCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(objectCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(objectCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(objectCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == False, "facilitator of other workshop able to immunify this object"
    authorization.logout(self)
    #
    if 'facilitatorCant' in kwargs:
        if kwargs['facilitatorCant'] == True:
            #: visit as facilitator and try to immunify
            authorization.login(self, facilitator)
            objectNotEnabled = nounAction.verbAdmin(self, objectPage, 'immunify', spoof=True)
            #: look at the object via the model and make sure it's not immune yet
            if objectType == 'conversation':
                nounObject = discussionLib.getDiscussion(objectCode)
            elif objectType == 'idea':
                nounObject = ideaLib.getIdea(objectCode)
            elif objectType == 'resource':
                nounObject = resourceLib.getResourceByCode(objectCode)
            if not nounObject:
                nounObject = revisionLib.getRevisionByCode(objectCode)
                assert nounObject is not None, "object cannot be found via model"
            isItImmuneYet = flagLib.isImmune(nounObject)
            assert isItImmuneYet == False, "facilitator of workshop able to immunify this object"
            #: wipe the session
            authorization.logout(self)
    #
    #: done with these imunify tests
    return True


def test_disable_noun_admin_admin(self, objectType):
    """ Create a conversation/idea/resource as an admin, then disable this object as an admin. 
    In order to test a more realistic situation, these admins will be different users. """
    #: create a workshop and two admins
    facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
    admin1 = registration.create_and_activate_a_user(self, postal='92007', name='Admin One', accessLevel='200')
    admin2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
    workshopTitle = 'workshop objects'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    authorization.logout(self)
    authorization.login(self, admin1)
    #: create a object as user1
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    #: logout, login as admin2, revisit the object's page and disable
    authorization.logout(self)
    authorization.login(self, admin2)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDisabled = nounAction.verbAdmin(self, objectRevisit, 'disable')
    assert objectDisabled.status_int == 200, "disable request not successful"
    #: revisit the object page
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "admin not able to disable admin's object"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "admin not able to disable admin's object, comment form present"
    runEnableTests(self, objectType, objectAdded, newWorkshop, facilitator, admin2)

def test_disable_noun_facilitator_admin(self, objectType):
    """ Create a conversation/idea/resource as a facilitator, then disable this object as an admin. """
    facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
    admin2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
    workshopTitle = 'workshop objects'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: create a object as facilitator
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    #: logout, login as admin2, revisit the object's page and disable
    authorization.logout(self)
    authorization.login(self, admin2)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDisabled = nounAction.verbAdmin(self, objectRevisit, 'disable')
    assert objectDisabled.status_int == 200, "disable request not successful"
    #: revisit the object page
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "admin not able to disable facilitator's object"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "admin not able to disable facilitator's object, comment form present"
    runEnableTests(self, objectType, objectAdded, newWorkshop, facilitator, admin2)

def test_disable_noun_user_admin(self, objectType):
    """ Create a conversation/idea/resource as a user of the workshop, then disable this conversation as an admin. """
    facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
    user1 = registration.create_and_activate_a_user(self, postal='92007', name='User')
    admin2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
    #: create a workshop and two users
    workshopTitle = 'workshop objects'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: invite user1 to the workshop
    guestLink = workshop.inviteGuest(self, newWorkshop, email=user1['email'], guestLink=True)
    #: create a conversation as user1
    authorization.logout(self)
    #: login as user1 then visit the invite link
    authorization.login(self, user1)
    guestConfirmed = self.app.get(url=guestLink)
    newWorkshop = self.app.get(url=newWorkshop.request.url)
    #: create a object as user1
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    #: logout, login as admin2, revisit the object's page and disable
    authorization.logout(self)
    authorization.login(self, admin2)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDisabled = nounAction.verbAdmin(self, objectRevisit, 'disable')
    assert objectDisabled.status_int == 200, "disable request not successful"
    #: revisit the object page
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "admin not able to disable facilitator's object"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "admin not able to disable facilitator's object, comment form present"
    runEnableTests(self, objectType, objectAdded, newWorkshop, facilitator, admin2)

def test_disable_noun_admin_facilitator(self, objectType):
    """ Create a conversation/idea/resource as an admin, then try to disable it as a facilitator. """
    facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator One')
    admin = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
    #: create a workshop
    workshopTitle = 'workshop objects'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: create a conversation as admin
    authorization.logout(self)
    #: login as user1 then visit the invite link
    authorization.login(self, admin)
    #: create a object as admin
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    #: logout, login as facilitator, revisit the object's page and try to disable
    authorization.logout(self)
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectNotDisabled = nounAction.verbAdmin(self, objectRevisit, 'disable', spoof=True)
    #: revisit the object page
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: make sure a disable message is not present
    assert nounDefs.objectDisabledMessage(objectType) not in objectRevisit, "facilitator able to disable admin's object"
    #: make sure a comment form is present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == True, "facilitator able to disable admin's object, comment form present"

def test_disable_noun_facilitator_facilitator(self, objectType):
    """ Create a conversation/idea/resource as a facilitator, then try to disable it as a facilitator. """
    facilitator = registration.create_and_activate_a_user(self, postal='92007', email='fac@civinomics.com', password='pass', name='Facilitator')
    admin = registration.create_and_activate_a_user(self, postal='92007', name='Admin', accessLevel='200')
    #: create a workshop
    workshopTitle = 'workshop objects'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: create a conversation
    newWorkshop = self.app.get(url=newWorkshop.request.url)
    #: create an object
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    #: disable the object
    objectDisabled = nounAction.verbAdmin(self, objectAdded, 'disable')
    assert objectDisabled.status_int == 200, "disable request not successful"
    #: revisit the object page
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "facilitator not able to disable own object"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "facilitator not able to disable own object, comment form present"
    runEnableTests(self, objectType, objectAdded, newWorkshop, facilitator, admin, facilitatorCan=True)


def test_disable_noun_user_facilitator(self, objectType):
    """ Create a conversation/idea/resource as a user of the workshop, then disable this conversation as its facilitator. """
    facilitator = registration.create_and_activate_a_user(self, postal='92007', email='fac@civinomics.com', password='pass', name='Facilitator')
    user1 = registration.create_and_activate_a_user(self, postal='92007', name='User')
    admin2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
    #: create a workshop
    workshopTitle = 'workshop objects'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: invite user1 to the workshop
    guestLink = workshop.inviteGuest(self, newWorkshop, email=user1['email'], guestLink=True)
    #: create a conversation as user1
    authorization.logout(self)
    #: login as user1 then visit the invite link
    authorization.login(self, user1)
    guestConfirmed = self.app.get(url=guestLink)
    newWorkshop = self.app.get(url=newWorkshop.request.url)
    #: create a object as user1
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    #: logout, login as facilitator, revisit the object's page and disable
    authorization.logout(self)
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDisabled = nounAction.verbAdmin(self, objectRevisit, 'disable')
    assert objectDisabled.status_int == 200, "disable request not successful"
    #: revisit the object page
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: make sure a disable message is present
    assert nounDefs.objectDisabledMessage(objectType) in objectRevisit, "facilitator not able to disable user's object"
    #: make sure a comment form is not present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == False, "facilitator not able to disable user's object, comment form present"
    runEnableTests(self, objectType, objectAdded, newWorkshop, facilitator, admin2, facilitatorCan=True)

def test_disable_noun_admin_user(self, objectType):
    """ Create a conversation/idea/resource as an admin, then try to disable it as a user of the workshop. """
    facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
    user1 = registration.create_and_activate_a_user(self, postal='92007', name='User')
    admin2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
    #: create a workshop
    workshopTitle = 'workshop objects'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: invite user1 to the workshop
    guestLink = workshop.inviteGuest(self, newWorkshop, email=user1['email'], guestLink=True)
    #: create a conversation as admin
    authorization.logout(self)
    authorization.login(self, admin2)
    #: create a object as admin
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    #: logout, login as user1, revisit the object's page and try to disable
    authorization.logout(self)
    authorization.login(self, user1)
    guestConfirmed = self.app.get(url=guestLink)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectNotDisabled = nounAction.verbAdmin(self, objectRevisit, 'disable', spoof=True)
    #: revisit the object page
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: make sure a disable message is not present
    assert nounDefs.objectDisabledMessage(objectType) not in objectRevisit, "user able to disable admin's object"
    #: make sure a comment form is present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == True, "user able to disable admin's object, comment form present"
    

def test_disable_noun_facilitator_user(self, objectType):
    """ Create a conversation/idea/resource as a facilitator, then try to disable it as a user of the workshop. """
    facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
    user1 = registration.create_and_activate_a_user(self, postal='92007', name='User')
    #: create a workshop
    workshopTitle = 'workshop objects'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: invite user1 to the workshop
    guestLink = workshop.inviteGuest(self, newWorkshop, email=user1['email'], guestLink=True)
    #: create a conversation as the facilitator
    #: create a object as admin
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    #: logout, login as user1, revisit the object's page and try to disable
    authorization.logout(self)
    authorization.login(self, user1)
    guestConfirmed = self.app.get(url=guestLink)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectNotDisabled = nounAction.verbAdmin(self, objectRevisit, 'disable', spoof=True)
    #: revisit the object page
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: make sure a disable message is not present
    assert nounDefs.objectDisabledMessage(objectType) not in objectRevisit, "user able to disable facilitator's object"
    #: make sure a comment form is present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == True, "user able to disable facilitator's object, comment form present"
    

def test_disable_noun_user_user(self, objectType):
    """ Create a conversation/idea/resource as a user, then try to disable this conversation 
    as a user of the workshop. """
    facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
    user1 = registration.create_and_activate_a_user(self, postal='92007', name='User1')
    user2 = registration.create_and_activate_a_user(self, postal='92007', name='User2')
    #: create a workshop
    workshopTitle = 'workshop objects'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: invite user1 to the workshop
    guestLink1 = workshop.inviteGuest(self, newWorkshop, email=user1['email'], guestLink=True)
    guestLink2 = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
    #: create a conversation as user1
    authorization.logout(self)
    authorization.login(self, user1)
    guestConfirmed1 = self.app.get(url=guestLink1)
    #: create a object as user1
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    #: logout, login as user2, revisit the object's page and try to disable
    authorization.logout(self)
    authorization.login(self, user2)
    guestConfirmed2 = self.app.get(url=guestLink2)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectNotDisabled = nounAction.verbAdmin(self, objectRevisit, 'disable', spoof=True)
    #: revisit the object page
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: make sure a disable message is not present
    assert nounDefs.objectDisabledMessage(objectType) not in objectRevisit, "user able to disable user's object"
    #: make sure a comment form is present
    assert formHelpers.isFormPresentByAction(objectRevisit, 'comment') == True, "user able to disable user's object, comment form present"
    
def test_immunify_private_noun_user_facilitator(self, objectType):
    """ Create a conversation/idea/resource in a private workshop as a user, try to immunify and 
    confirm it hasn't happened with each role that shouldn't be able to, then immunify the object 
    as the workshop's facilitator.
     At this point, confirm that it is immune by attempting to flag the object as each of the roles 
    that shouldn't be able to, confirming after each attempt this is true. Finally, flag the object 
    as an admin and assert this has been successful. """
    # test 1/12 for this group
    #
    #: PART 1
    #: create a workshop
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    user1 = registration.create_and_activate_a_user(self, postal='95062', name='user1')
    user2 = registration.create_and_activate_a_user(self, postal='95062', name='user2')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: invite user1 to the workshop
    guestLink1 = workshop.inviteGuest(self, newWorkshop, email=user1['email'], guestLink=True)
    guestLink2 = workshop.inviteGuest(self, newWorkshop, email=user2['email'], guestLink=True)
    #: create a conversation as user1
    authorization.logout(self)
    authorization.login(self, user1)
    guestConfirmed1 = self.app.get(url=guestLink1)
    #: create a object as user1
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunify this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    #: in this test we act as the facilitator of the workshop
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object, do not expect a 404 response this time
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "facilitator of workshop not able to immunify this object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    adminUser = registration.create_and_activate_a_user(self, postal='95062', name='admin user', accessLevel='200')
    authorization.login(self, adminUser)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation"    

def test_immunify_private_noun_facilitator_facilitator(self, objectType):
    """ Create a conversation/idea/resource in a private workshop as its facilitator, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
    has been successful. """
    # test 2/12 for this group
    #
    #: PART 1
    #: create a workshop
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: create a conversation as the facilitator
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    #: in this test we act as the facilitator of the workshop
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object, do not expect a 404 response this time
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "facilitator of workshop not able to immunify own object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    adminUser = registration.create_and_activate_a_user(self, postal='95062', name='admin user', accessLevel='200')
    authorization.login(self, adminUser)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation"  

def test_immunify_private_noun_admin_facilitator(self, objectType):
    """ Create a conversation/idea/resource in a private workshop as an admin, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, including the workshop's facilitator.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. 
    Because the facilitator should not be able to make this object immune, the last step of flagging
    the object as an admin is not performed, since the object is not immunified. """
    # test 3/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: create a conversation as the admin
    authorization.logout(self)
    authorization.login(self, admin)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    #: This test is about seeing permissions are correct for if a facilitator can immunify
    #: an admin's conversation/idea/resource. Since a facilitator shouldn't be able to, the 
    #: test stops here.
    #: In other tests where the case is that an immunify action will be successful, we test the
    #: other side of the coin - cases for flagging the immune object.

def test_immunify_noun_user_admin(self, objectType):
    """ Create a conversation/idea/resource in a private workshop as a user, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, then immunify the object as an admin.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
    has been successful. """
    # test 4/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    user = registration.create_and_activate_a_user(self, postal='95062', name='user')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: create a conversation as the user
    guestLink = workshop.inviteGuest(self, newWorkshop, email=user['email'], guestLink=True)
    authorization.logout(self)
    authorization.login(self, user)
    guestConfirmed = self.app.get(url=guestLink)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "admin not able to immunify object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    authorization.login(self, admin)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation" 

def test_immunify_private_noun_facilitator_admin(self, objectType):
    """ Create a conversation/idea/resource in a private workshop as its facilitator, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, then immunify the object as an admin.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
    has been successful. """
    # test 5/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: create a conversation as the facilitator
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "admin not able to immunify object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    authorization.login(self, admin)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation"     

def test_immunify_private_noun_admin_admin(self, objectType):
    """ Create a conversation/idea/resource in a private workshop as an admin, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, then immunify the object as an admin.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
    has been successful. """
    # test 6/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: create a conversation as the admin
    authorization.logout(self)
    authorization.login(self, admin)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "admin not able to immunify object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    authorization.login(self, admin)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation"  

""" TEST IMMUNITY - PUBLIC WORKSHOPS """

""" This next group of tests are the same as the previous ones that started at 
'TEST IMMUNITY - PRIVATE WORKSHOPS', except for the fact that these are working 
with public workshops. """


def test_immunify_public_noun_user_facilitator(self, objectType):
    """ Create a conversation/idea/resource in a public workshop as a user, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
    has been successful. """
    # test 7/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: upgrade it to professional
    workshop.upgradeToProfessional(self, newWorkshop, facilitator)
    #: the scope needs to be set before it will show up in the 'list all' page
    scopeDict = {}
    scopeDict = content.scopeDict(country='united-states', state='california')
    scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
    workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
    workshop.startWorkshop(self, newWorkshop, facilitator)
    #: make sure the workshop is public
    allWorkshops = self.app.get(pageDefs.allWorkshops())
    assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
    #: create a conversation as a user
    authorization.logout(self)
    user = registration.create_and_activate_a_user(self, postal='95060', name='user')
    authorization.login(self, user)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "admin not able to immunify object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    authorization.login(self, admin)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation"      

def test_immunify_public_noun_facilitator_facilitator(self, objectType):
    """ Create a conversation/idea/resource in a public workshop as the facilitator, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
    has been successful. """
    # test 8/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: upgrade it to professional
    workshop.upgradeToProfessional(self, newWorkshop, facilitator)
    #: the scope needs to be set before it will show up in the 'list all' page
    scopeDict = {}
    scopeDict = content.scopeDict(country='united-states', state='california')
    scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
    workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
    workshop.startWorkshop(self, newWorkshop, facilitator)
    #: make sure the workshop is public
    allWorkshops = self.app.get(pageDefs.allWorkshops())
    assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
    #: create a conversation as the facilitator
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    authorization.login(self, facilitator)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "admin not able to immunify object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    authorization.login(self, admin)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation"   

def test_immunify_public_noun_admin_facilitator(self, objectType):
    """ Create a conversation/idea/resource in a public workshop as an admin, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, including the workshop's facilitator.
    At this point, the test is done, since a state of immunity shouldn't be arrived at for this object."""
    # test 9/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: upgrade it to professional
    workshop.upgradeToProfessional(self, newWorkshop, facilitator)
    #: the scope needs to be set before it will show up in the 'list all' page
    scopeDict = {}
    scopeDict = content.scopeDict(country='united-states', state='california')
    scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
    workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
    workshop.startWorkshop(self, newWorkshop, facilitator)
    #: make sure the workshop is public
    allWorkshops = self.app.get(pageDefs.allWorkshops())
    assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
    #: create a conversation as the admin
    authorization.logout(self)
    authorization.login(self, admin)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    
def test_immunify_public_noun_user_admin(self, objectType):
    """ Create a conversation/idea/resource in a public workshop as a user, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, then immunify the object as an admin.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
    has been successful. """
    # test 10/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: upgrade it to professional
    workshop.upgradeToProfessional(self, newWorkshop, facilitator)
    #: the scope needs to be set before it will show up in the 'list all' page
    scopeDict = {}
    scopeDict = content.scopeDict(country='united-states', state='california')
    scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
    workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
    workshop.startWorkshop(self, newWorkshop, facilitator)
    #: make sure the workshop is public
    allWorkshops = self.app.get(pageDefs.allWorkshops())
    assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
    #: create a conversation as a user
    authorization.logout(self)
    user = registration.create_and_activate_a_user(self, postal='95060', name='user')
    authorization.login(self, user)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "admin not able to immunify object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    authorization.login(self, admin)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation" 

def test_immunify_public_noun_facilitator_admin(self, objectType):
    """ Create a conversation/idea/resource in a public workshop as the facilitator, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, then immunify the object as an admin.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
    has been successful. """
    # test 11/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: upgrade it to professional
    workshop.upgradeToProfessional(self, newWorkshop, facilitator)
    #: the scope needs to be set before it will show up in the 'list all' page
    scopeDict = {}
    scopeDict = content.scopeDict(country='united-states', state='california')
    scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
    workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
    workshop.startWorkshop(self, newWorkshop, facilitator)
    #: make sure the workshop is public
    allWorkshops = self.app.get(pageDefs.allWorkshops())
    assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
    #: create a conversation
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "admin not able to immunify object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    authorization.login(self, admin)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation" 

def test_immunify_public_noun_admin_admin(self, objectType):
    """ Create a conversation/idea/resource in a public workshop as an admin, try to immunify and confirm it hasn't
    happened with each role that shouldn't be able to, then immunify the object as an admin.
    At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
    be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
    has been successful. """
    # test 12/12 for this group
    #
    #: PART 1
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95062', name='admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95062', name='facilitator')
    workshopTitle = 'workshop objects immune conversation'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: upgrade it to professional
    workshop.upgradeToProfessional(self, newWorkshop, facilitator)
    #: the scope needs to be set before it will show up in the 'list all' page
    scopeDict = {}
    scopeDict = content.scopeDict(country='united-states', state='california')
    scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
    workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
    workshop.startWorkshop(self, newWorkshop, facilitator)
    #: make sure the workshop is public
    allWorkshops = self.app.get(pageDefs.allWorkshops())
    assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
    #: create a conversation
    authorization.logout(self)
    authorization.login(self, admin)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: prep for the coming tests by loading the needed models
    import pylowiki.lib.db.discussion   as discussionLib
    import pylowiki.lib.db.idea         as ideaLib
    import pylowiki.lib.db.resource     as resourceLib
    import pylowiki.lib.db.flag         as flagLib
    import pylowiki.lib.db.revision     as revisionLib
    #
    #: PART 2
    #: try to immunize this noun as each of the roles that shouldn't be able to
    runImmunifyTests(
        self, 
        objectType, 
        nounCode, 
        objectAdded,
        newWorkshop,
        facilitator, 
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    #
    #: PART 3
    #: immunify with a role that can, and make sure it worked
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    #: immunify the object
    objectImmunified = nounAction.verbAdmin(self, objectRevisit, 'immunify')
    #: look at the object via the model and make sure it's immune now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    isItImmuneYet = flagLib.isImmune(nounObject)
    assert isItImmuneYet == True, "admin not able to immunify object"
    #: wipe the session
    authorization.logout(self)
    #
    #: PART 4
    #: attempt to flag with all the roles that now cannot flag the object, and make sure they can't
    runFlaggingTests(
        self,
        objectType,
        nounCode, 
        objectRevisit, 
        newWorkshop, 
        facilitator,
        discussionLib, 
        ideaLib, 
        resourceLib,
        flagLib,
        revisionLib,
        facilitatorCant=True
    )
    #
    #: PART 5
    #: flag the object as an admin, and make sure it worked
    authorization.login(self, admin)
    objectRevisited = self.app.get(url=objectRevisit.request.url)
    #: flag the object, expect it to be successful
    objectFlagged = nounAction.flag(self, objectRevisited)
    #: look at the object via the model and make sure it's flagged now
    if objectType == 'conversation':
        nounObject = discussionLib.getDiscussion(nounCode)
    elif objectType == 'idea':
        nounObject = ideaLib.getIdea(nounCode)
    elif objectType == 'resource':
        nounObject = resourceLib.getResourceByCode(nounCode)
    if not nounObject:
        nounObject = revisionLib.getRevisionByCode(nounCode)
        assert nounObject is not None, "object cannot be found via model"
    #: we expect to see a flag now
    isItFlaggedYet = flagLib.checkFlagged(nounObject)
    assert isItFlaggedYet == True, "admin not able to flag an immune conversation"

""" ****************************************************************************************** """ 
""" ****************************************************************************************** """ 
""" ****************************************************************************************** """ 
""" ****************************************************************************************** """ 
""" ****************************************************************************************** """ 
""" This next batch of tests will cover deletion permissions. Bottom line is, only an admin 
    can delete an object. """
""" First set will deal with this within private workshops. There should be 18 tests in this group. """

def test_delete_noun_admin_admin(self, objectType):
    """ Create a conversation/idea/resource as an admin, then delete this conversation as an admin."""
    # test 1
    #: create a workshop
    facilitator = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator')
    admin1 = registration.create_and_activate_a_user(self, postal='95060', name='Admin One', accessLevel='200')
    admin2 = registration.create_and_activate_a_user(self, postal='95060', name='Admin Two', accessLevel='200')
    workshopTitle = 'delete workshop object'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: create the object as an admin
    authorization.logout(self)
    authorization.login(self, admin1)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: run the delete tests that shouldn't work
    runDeleteTests(self, objectType, objectAdded, objectTitle, newWorkshop, facilitator)
    #: delete the object as the other admin
    authorization.login(self, admin2)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDeleted = nounAction.verbAdmin(self, objectRevisit, 'delete')
    #: make sure the object has been deleted, revisit the object's listing page
    #: to make sure it is gone
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectAdded)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectAdded)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectAdded)
    assert objectTitle not in listingPage, "deleted object still visible"

def test_delete_noun_facilitator_admin(self, objectType):
    """ Create a conversation/idea/resource as a facilitator, then delete this conversation as an admin."""
    # test 2
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95060', name='Admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator')
    workshopTitle = 'delete workshop object'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: run the delete tests that shouldn't work
    runDeleteTests(self, objectType, objectAdded, objectTitle, newWorkshop, facilitator)
    #: delete the object as the other admin
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDeleted = nounAction.verbAdmin(self, objectRevisit, 'delete')
    #: make sure the object has been deleted, revisit the object's listing page
    #: to make sure it is gone
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectAdded)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectAdded)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectAdded)
    assert objectTitle not in listingPage, "deleted object still visible"

def test_delete_noun_user_admin(self, objectType):
    """ Create a conversation/idea/resource as a user of the private workshop, then delete this conversation 
    as an admin."""
    # test 3
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95060', name='Admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator')
    user = registration.create_and_activate_a_user(self, postal='95060', name='User')
    workshopTitle = 'delete workshop object'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: invite the user
    guestLink = workshop.inviteGuest(self, newWorkshop, email=user['email'], guestLink=True)
    authorization.logout(self)
    authorization.login(self, user)
    guestConfirmed = self.app.get(url=guestLink)
    #: create the object
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: run the delete tests that shouldn't work
    runDeleteTests(self, objectType, objectAdded, objectTitle, newWorkshop, facilitator)
    #: delete the object as an admin
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDeleted = nounAction.verbAdmin(self, objectRevisit, 'delete')
    #: make sure the object has been deleted, revisit the object's listing page
    #: to make sure it is gone
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectAdded)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectAdded)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectAdded)
    assert objectTitle not in listingPage, "deleted object still visible"

def test_delete_public_noun_admin_admin(self, objectType):
    """ Create a public conversation/idea/resource as an admin, then delete this conversation as an admin."""
    # test 4
    #: create a workshop
    facilitator = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator')
    admin1 = registration.create_and_activate_a_user(self, postal='95060', name='Admin One', accessLevel='200')
    admin2 = registration.create_and_activate_a_user(self, postal='95060', name='Admin Two', accessLevel='200')
    workshopTitle = 'delete workshop object'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: upgrade it to professional
    workshop.upgradeToProfessional(self, newWorkshop, facilitator)
    #: the scope needs to be set before it will show up in the 'list all' page
    scopeDict = {}
    scopeDict = content.scopeDict(country='united-states', state='california')
    scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
    workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
    workshop.startWorkshop(self, newWorkshop, facilitator)
    #: make sure the workshop is public
    allWorkshops = self.app.get(pageDefs.allWorkshops())
    assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
    #: create the object as an admin
    authorization.logout(self)
    authorization.login(self, admin1)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: run the delete tests that shouldn't work
    runDeleteTests(self, objectType, objectAdded, objectTitle, newWorkshop, facilitator)
    #: delete the object as the other admin
    authorization.login(self, admin2)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDeleted = nounAction.verbAdmin(self, objectRevisit, 'delete')
    #: make sure the object has been deleted, revisit the object's listing page
    #: to make sure it is gone
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectAdded)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectAdded)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectAdded)
    assert objectTitle not in listingPage, "deleted object still visible"

def test_delete_public_noun_facilitator_admin(self, objectType):
    """ Create a public conversation/idea/resource as a facilitator, then delete this conversation as an admin."""
    # test 5
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95060', name='Admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator')
    workshopTitle = 'delete workshop object'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: upgrade it to professional
    workshop.upgradeToProfessional(self, newWorkshop, facilitator)
    #: the scope needs to be set before it will show up in the 'list all' page
    scopeDict = {}
    scopeDict = content.scopeDict(country='united-states', state='california')
    scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
    workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
    workshop.startWorkshop(self, newWorkshop, facilitator)
    #: make sure the workshop is public
    allWorkshops = self.app.get(pageDefs.allWorkshops())
    assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
    #: create the object
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: run the delete tests that shouldn't work
    runDeleteTests(self, objectType, objectAdded, objectTitle, newWorkshop, facilitator)
    #: delete the object as the other admin
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDeleted = nounAction.verbAdmin(self, objectRevisit, 'delete')
    #: make sure the object has been deleted, revisit the object's listing page
    #: to make sure it is gone
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectAdded)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectAdded)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectAdded)
    assert objectTitle not in listingPage, "deleted object still visible"

def test_delete_public_noun_user_admin(self, objectType):
    """ Create a public conversation/idea/resource as a user of the private workshop, then delete this conversation 
    as an admin."""
    # test 6
    #: create a workshop
    admin = registration.create_and_activate_a_user(self, postal='95060', name='Admin', accessLevel='200')
    facilitator = registration.create_and_activate_a_user(self, postal='95060', name='Facilitator')
    user = registration.create_and_activate_a_user(self, postal='95060', name='User')
    workshopTitle = 'delete workshop object'
    newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
    assert workshopTitle in newWorkshop, "not able to create workshop"
    #: invite the user
    guestLink = workshop.inviteGuest(self, newWorkshop, email=user['email'], guestLink=True)
    #: upgrade it to professional
    workshop.upgradeToProfessional(self, newWorkshop, facilitator)
    #: the scope needs to be set before it will show up in the 'list all' page
    scopeDict = {}
    scopeDict = content.scopeDict(country='united-states', state='california')
    scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
    workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
    workshop.startWorkshop(self, newWorkshop, facilitator)
    #: make sure the workshop is public
    allWorkshops = self.app.get(pageDefs.allWorkshops())
    assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
    #: create the object
    authorization.logout(self)
    authorization.login(self, user)
    guestConfirmed = self.app.get(url=guestLink)
    objectTitle = 'object title'
    objectText = 'object text'
    objectAdded = nounAction.addNounToWorkshop(
        self, 
        objectType, 
        newWorkshop, 
        title=objectTitle,
        text=objectText
    )
    assert objectTitle in objectAdded, "object not created"
    nounCode = nounHelp.getNounCode(objectAdded)
    #: wipe the session
    authorization.logout(self)
    #: run the delete tests that shouldn't work
    runDeleteTests(self, objectType, objectAdded, objectTitle, newWorkshop, facilitator)
    #: delete the object as an admin
    authorization.login(self, admin)
    objectRevisit = self.app.get(url=objectAdded.request.url)
    objectDeleted = nounAction.verbAdmin(self, objectRevisit, 'delete')
    #: make sure the object has been deleted, revisit the object's listing page
    #: to make sure it is gone
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, objectAdded)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, objectAdded)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, objectAdded)
    assert objectTitle not in listingPage, "deleted object still visible"
