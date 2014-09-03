# -*- coding: utf-8 -*-
from pylowiki.tests import *
import re

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.link_definitions as linkDefs
import pylowiki.tests.helpers.workshops as workshop

import logging
log = logging.getLogger(__name__)


def resourceDeletedMessage():
    return 'Successfully deleted'

def resourceDisabledMessage():
    return 'This resource has been disabled'

def reourceEnabledMessage():
    return 'Successfully enabled'

def getAddPage(self, resourcesPage):
    """ returns the page for adding an idea """
    return resourcesPage.click(description=linkDefs.addResource())

def getResourcesPage(self, workshopPage):
    """ Returns the resources page by clicking on the Learn menu bar link. """
    return workshopPage.click(description=linkDefs.resourcesPage())

