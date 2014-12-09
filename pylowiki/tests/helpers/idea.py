# -*- coding: utf-8 -*-
from pylowiki.tests import *
import re

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.link_definitions as linkDefs


import logging
log = logging.getLogger(__name__)


def addIdea(self, ideasPage):
    return ideasPage.click(description=linkDefs.addIdea(), index=0)

def conversationDeletedMessage():
    return 'Successfully deleted'

def conversationDisabledMessage():
    return 'This discussion has been disabled'

def conversationEnabledMessage():
    return 'Successfully enabled'

def getAddPage(self, ideasPage):
    """ returns the page for adding an idea """
    return ideasPage.click(description=linkDefs.addIdea())

def getIdeasPage(self, workshopPage):
    """ Returns the ideas page by clicking on the ideas menu bar link. """
    return workshopPage.click(description=linkDefs.ideasPage(), index=0)

def setIdea():
    return formDefs.addIdea_text()









