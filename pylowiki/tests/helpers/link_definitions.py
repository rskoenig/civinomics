# -*- coding: utf-8 -*-
from pylowiki.tests import *

import logging
log = logging.getLogger(__name__)

def addConversation():
    return 'Add a conversation'

def addIdea():
    return 'Add an idea'

def conversationsPage():
    return talk_page()

def createGeoLink(**kwargs):
    """returns the href of a geo scope breadcrumb link that could be expected on the
    page for a logged-in user"""
    #: all geo scope links start with this
    geoBase = '/workshops/geo/earth'
    #: create the parts of a scoped link, depending on the args involved
    if 'country' in kwargs:
        country = kwargs['country']
    else:
        country = None
    if 'state' in kwargs:
        state = kwargs['state']
    else:
        state = None
    if 'county' in kwargs:
        county = kwargs['county']
    else:
        county = None
    if 'city' in kwargs:
        city = kwargs['city']
    else:
        city = None
    if 'postal' in kwargs:
        postal = kwargs['postal']
    else:
        postal = None

    #: with the parts loaded, build the string 
    if country is not None:
        geoBase += '/' + country
    if state is not None:
        geoBase += '/' + state
    if county is not None:
        geoBase += '/' + county
    if city is not None:
        geoBase += '/' + city
    if postal is not None:
        geoBase += '/' + postal

    return geoBase

def vote_page():
    return 'Vote'

def login():
	return 'login'

def login_homePage():
	return u'Log In'

def profile():
    return 'profile'

def profile_edit():
    return 'Edit'

def talk_page():
    return 'Talk'

def workshopListingPage():
	return u'workshops'

def workshopSettings():
	return u'preferences'