# -*- coding: utf-8 -*-
from pylowiki.tests import *
import re

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.link_definitions as linkDefs

import logging
log = logging.getLogger(__name__)


def conversationDeletedMessage():
    return 'Successfully deleted'

def conversationDisabledMessage():
    return 'This discussion has been disabled'

def conversationEnabledMessage():
    return 'Successfully enabled'

def editProfile(self, params, **kwargs):
    #: set the profile's edit form's parameters and return the parameters
    if 'name' in kwargs:
        name = kwargs['name']
    else:
        name = content.generateText(6)
    if 'email' in kwargs:
        email = kwargs['email']
    else:
        email = content.generateText(6) + '@' + content.generateText(7) + '.com'
    if 'greeting' in kwargs:
        greeting = kwargs['greeting']
    else:
        greeting = content.generateText(18)            
    if 'website' in kwargs:
        website = kwargs['website']
    else:
        website = 'www.' + content.generateText(12) + '.com'
    if 'websiteDesc' in kwargs:
        websiteDesc = kwargs['websiteDesc']
    else:
        websiteDesc = content.generateText(24)
    #: put these new values in the profile parameters
    params['member_name'] = name
    params['email'] = email
    params['greetingMsg'] = greeting
    params['websiteLink'] = website
    params['websiteDesc'] = websiteDesc

    #: should we return the parameters?
    if 'returnParams' in kwargs:
        if kwargs['returnParams'] == True:
            return params

    #: if the parameters aren't wanted, it's time to edit the profile
    if 'expectErrors' in kwargs:
        if kwargs['expectErrors'] == True:
            #: try to update the profile, expect it not to work
            profileNotUpdated = self.app.post(
                url=str(kwargs['editForm'].action),
                params=params,
                status=404,
                expect_errors=True
            ).follow()
            return profileNotUpdated
        else:
            #: update the profile
            profileUpdated = self.app.post(
                url=str(kwargs['editForm'].action),
                params=params
            ).follow()
            return profileUpdated
    #: update the profile
    profileUpdated = self.app.post(
        url=str(kwargs['editForm'].action),
        params=params
    ).follow()
    return profileUpdated

def getResources(self, profilePage):
    return profilePage.click(description=linkDefs.profileResources(), index=0)

def getConversations(self, profilePage):
    return profilePage.click(description=linkDefs.profileConversations(), index=0)

def getIdeas(self, profilePage):
    return profilePage.click(description=linkDefs.profileIdeas(), index=0)

def getObjectsPage(self, profilePage):
    """ figure out which object, go to that listing page and return it """
    return thatObjectPage.click(description=linkDefs.addConversation(), index=0)

def getEditPage(self, profilePage):
    """ return the profile editing page """
    return profilePage.click(description=linkDefs.profileEditPage())

def getProfilePage(self, aPage):
    """ Returns the profile page by clicking on the profile link up top. """
    return aPage.click(description=linkDefs.profilePage())

def immunify(self, conversation, **kwargs):
    """ immunify a conversation, or return the url needed for doing so """
    #: go through the conversation page's forms and look for the one with disable in its action
    convoForms = conversation.forms__get()
    immunifyUrl = None
    for formIndex in convoForms:
        #: does it have 'disable' in the action?
        if convoForms[formIndex].action.find('immunify') >= 0:
            immunifyUrl = convoForms[formIndex].action

    #: post to the form's url to disable the conversation
    if immunifyUrl is not None:
        if 'dontSubmit' in kwargs:
            if kwargs['dontSubmit'] == True:
                return immunifyUrl
            else:
                immunifyResponse = self.app.post(url=str(immunifyUrl))
                return immunifyResponse
        else:
            immunifyResponse = self.app.post(url=str(immunifyUrl))
            return immunifyResponse
    else:
        return False












