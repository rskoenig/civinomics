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

def delete(self, conversation, **kwargs):
    """deletes a conversation, or return the url needed for doing so """
    #: if we've been provided with the link to post to, we do just that
    if 'postLink' in kwargs:
        #: if we should expect errors, the post looks a bit different
        if 'expectErrors' in kwargs:
            if kwargs['expectErrors'] == True:
                deleteResponse = self.app.post(
                    url=str(kwargs['postLink']),
                    status=404,
                    expect_errors=True
                )
                return deleteResponse
            else:
                deleteResponse = self.app.post(url=str(kwargs['postLink']))
                return deleteResponse
        else:
            deleteResponse = self.app.post(url=str(kwargs['postLink']))
            return deleteResponse

    #: we have not been given the link to post to, so we find it
    convoForms = conversation.forms__get()
    deleteUrl = None

    if 'spoof' in kwargs:
        if kwargs['spoof'] == True:
            conversationSoup = conversation.html
            flagUrl = None
            pageLink = conversationSoup.find('a', attrs={'href' : re.compile("flag")})
            #: change the flag url to a delete url 
            if pageLink is not None:
                flagUrl = pageLink['href']
                deleteUrl = str.replace(str(flagUrl), 'flag', 'delete')
                deleteResponse = self.app.post(
                    url=str(deleteUrl),
                    status=404,
                    expect_errors=True
                )
                return deleteResponse
            else:
                #: couldn't find a flag link for the spoof move
                return False

    #: go through the conversation page's forms and look for the one with delete in its action
    for formIndex in convoForms:
        #: does it have 'delete' in the action?
        # log.info("actions: "+str(convoForms[formIndex].action))
        if convoForms[formIndex].action.find('delete') >= 0:
            deleteUrl = convoForms[formIndex].action

    #: post to the form's url to delete the conversation
    if deleteUrl is not None:
        if 'dontSubmit' in kwargs:
            if kwargs['dontSubmit'] == True:
                return deleteUrl
            else:
                deleteResponse = self.app.post(url=str(deleteUrl))
                return deleteResponse
        else:
            deleteResponse = self.app.post(url=str(deleteUrl))
            return deleteResponse
    else:
        return False

def disable(self, conversation, **kwargs):
    """disables a conversation, or return the url needed for doing so """
    #: if we've been provided with the link to post to, we do just that
    if 'postLink' in kwargs:
        #: if we should expect errors, the post looks a bit different
        if 'expectErrors' in kwargs:
            if kwargs['expectErrors'] == True:
                disableResponse = self.app.post(
                    url=str(kwargs['postLink']),
                    status=404,
                    expect_errors=True
                )
                return disableResponse
            else:
                disableResponse = self.app.post(url=str(kwargs['postLink']))
                return disableResponse
        else:
            disableResponse = self.app.post(url=str(kwargs['postLink']))
            return disableResponse

    #: go through the conversation page's forms and look for the one with disable in its action
    convoForms = conversation.forms__get()
    disableUrl = None
    for formIndex in convoForms:
        #: does it have 'disable' in the action?
        if convoForms[formIndex].action.find('disable') >= 0:
            disableUrl = convoForms[formIndex].action

    #: post to the form's url to disable the conversation
    if disableUrl is not None:
        if 'dontSubmit' in kwargs:
            if kwargs['dontSubmit'] == True:
                return disableUrl
            else:
                disableResponse = self.app.post(url=str(disableUrl))
                return disableResponse
        else:
            disableResponse = self.app.post(url=str(disableUrl))
            return disableResponse
    else:
        return False

def flag(self, conversation, **kwargs):
    """ flag a conversation, or return the url needed for doing so """
    #: find the flagging link in the conversation's page
    conversationSoup = conversation.html
    flagUrl = None
    pageLink = conversationSoup.find('a', attrs={'href' : re.compile("flag")})

    #: post to the form's url to disable the conversation
    if pageLink is not None:
        flagUrl = pageLink['href']
        if 'dontSubmit' in kwargs:
            if kwargs['dontSubmit'] == True:
                return flagUrl
            else:
                flagResponse = self.app.post(url=str(flagUrl))
                return flagResponse
        else:
            flagResponse = self.app.post(url=str(flagUrl))
            return flagResponse
    else:
        return False

def getAddPage(self, conversationsPage):
    return conversationsPage.click(description=linkDefs.addConversation(), index=0)

def getConversationCode(self, conversation):
    """returns the conversation's code """
    # structure: http://test.civinomics.org/workshop/{workshopCode}/{workshopName}/
    # discussion/{conversationCode}/{conversationName}
    parts = conversation.request.url.split('/')
    codeIndex = len(parts)-2
    convoCode = parts[codeIndex]
    return convoCode

def getConversationsPage(self, workshopPage):
    """ Returns the conversations page by clicking on the conversations menu bar link. """
    return workshopPage.click(description=linkDefs.conversationsPage())

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












