# -*- coding: utf-8 -*-
from pylowiki.tests import *


def getNounCode(noun):
    """returns the noun's code """
    # structure: http://test.civinomics.org/workshop/{workshopCode}/{workshopName}/
    # discussion/{conversationCode}/{conversationName}
    parts = noun.request.url.split('/')
    codeIndex = len(parts)-2
    nounCode = parts[codeIndex]
    return nounCode
