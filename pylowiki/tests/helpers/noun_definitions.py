# -*- coding: utf-8 -*-
from pylowiki.tests import *


def objectDisabledMessage(objectType):
    if objectType == 'conversation':
        return 'This conversation has been disabled'
    elif objectType == 'idea':
        return 'This idea has been disabled'
    elif objectType == 'resource':
        return 'This resource has been disabled'

def allWorkshops():
	return '/workshops'