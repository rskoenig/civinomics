# -*- coding: utf-8 -*-
from pylowiki.tests import *
import re

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.workshops as workshop

import logging
log = logging.getLogger(__name__)


def conversationDisabledMessage():
    return 'This discussion has been disabled'

def disable(self, conversation, **kwargs):
    """disables a conversation, or return the url needed for doing so """
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

def getConversationCode(self, conversation):
    """returns the conversation's code """
    # structure: http://test.civinomics.org/workshop/{workshopCode}/{workshopName}/
    # discussion/{conversationCode}/{conversationName}
    parts = conversation.request.url.split('/')
    codeIndex = len(parts)-2
    convoCode = parts[codeIndex]
    return convoCode

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












