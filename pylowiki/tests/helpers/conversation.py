# -*- coding: utf-8 -*-
from pylowiki.tests import *
    
import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.workshops as workshop

import logging
log = logging.getLogger(__name__)


def conversationDisabledMessage():
    return 'This discussion has been disabled'

def disable(self, conversation, **kwargs):
    """disables a conversation """
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
        else:
            disableResponse = self.app.post(url=str(disableUrl))
            return disableResponse
    else:
        return False