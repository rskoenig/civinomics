# -*- coding: utf-8 -*-
from pylowiki.tests import *
import re

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.conversation as conversation
import pylowiki.tests.helpers.idea as idea
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.resource as resource

import logging
log = logging.getLogger(__name__)

""" generalized actions that can be used on the three main object types of the site: 
    conversations, resources and ideas """

def addNounToWorkshop(self, objectType, workshop, **kwargs):
    """Add a conversation/idea/resource to a workshop"""
    #: load the necessary info
    if 'title' in kwargs:
        title = kwargs['title']
    else:
        title = content.oneLine(2)
    if 'text' in kwargs:
        text = kwargs['text']
    else:
        text = content.oneLine(3)
    if 'link' in kwargs:
        link = kwargs['link']
    else:
        link = content.oneLine(4)
    #: go to the correct page and click the add link and get the form and set the fields
    if objectType == 'conversation':
        listingPage = conversation.getConversationsPage(self, workshop)
        addObject = conversation.getAddPage(self, listingPage)
        addForm = addObject.forms[formDefs.addConversation()]
        addForm.set(formDefs.addConversation_title(), title)
        addForm.set(formDefs.addConversation_text(), text)
    elif objectType == 'idea':
        listingPage = idea.getIdeasPage(self, workshop)
        addObject = idea.getAddPage(self, listingPage)
        addForm = addObject.forms[formDefs.addIdea()]
        addForm.set(idea.setIdea(), title)
    elif objectType == 'resource':
        listingPage = resource.getResourcesPage(self, workshop)
        addObject = resource.getAddPage(self, listingPage)
        addForm = addObject.forms[formDefs.addResource()]    
        addForm.set(formDefs.addResource_title(), title)
        addForm.set(formDefs.addResource_link(), link)
        addForm.set(formDefs.addResource_text(), text)
    #: this is the easiest way to set up a custom set of submit fields for the form.
    #: this is only needed because of needing to include submit='' in the parameters
    params = {}
    params = formHelpers.loadWithSubmitFields(addForm)
    #: this form does not include submit as a parameter, but it must be included in the postdata
    params[formDefs.parameter_submit()] = content.noChars()
    #: submit the form and follow the response
    objectAdded = self.app.post(
        url=str(addForm.action), 
        content_type=addForm.enctype,
        params=params
    ).follow()
    #: return the object's page.
    return objectAdded

def flag(self, noun, **kwargs):
    """ flag a noun (conversation, idea or resource), or return the url needed for doing so """
    #: find the flagging link in the conversation's page
    nounSoup = noun.html
    flagUrl = None
    pageLink = nounSoup.find('a', attrs={'href' : re.compile("flag")})
    log.info("found page link: "+pageLink['href'])
    #: post to the form's url to disable the conversation
    if pageLink is not None:
        flagUrl = pageLink['href']
        if 'expectErrors' in kwargs:
            if kwargs['expectErrors'] == True:
                flagResponse = self.app.post(
                    url=str(flagUrl),
                    status=404,
                    expect_errors=True
                )
                return flagResponse

        if 'dontSubmit' in kwargs:
            if kwargs['dontSubmit'] == True:
                return flagUrl
            else:
                flagResponse = self.app.post(url=str(flagUrl))
                return flagResponse
        else:
            log.info("posting to flag url: "+flagUrl)
            flagResponse = self.app.post(url=str(flagUrl))
            return flagResponse
    else:
        return False

def verbAdmin(self, noun, verb, **kwargs):
    """ Act on a noun (conversation, idea or resource), using the verb 
    (disable, enable, immunify, delete). 

    Options are available with kwargs:
     - postLink: use a provided link to post the action to a custom url
     - expectErrors: modify the post to expect a 404 flagResponse
     - spoof: create the action to post to, using the flag link
     - dontSubmit: do not post to the desired link, just return it """

    #log.info("in verb admin "+verb)
    #: if we've been provided with the link to post to, we do just that
    if 'postLink' in kwargs:
        #: if we should expect errors, the post looks a bit different
        if 'expectErrors' in kwargs:
            if kwargs['expectErrors'] == True:
                verbResponse = self.app.post(
                    url=str(kwargs['postLink']),
                    status=404,
                    expect_errors=True
                )
                return verbResponse
            else:
                verbResponse = self.app.post(url=str(kwargs['postLink']))
                return verbResponse
        else:
            verbResponse = self.app.post(url=str(kwargs['postLink']))
            return verbResponse

    #: we have not been given the link to post to, so we find it
    nounForms = noun.forms__get()
    verbUrl = None

    if 'spoof' in kwargs:
        if kwargs['spoof'] == True:
            nounSoup = noun.html
            flagUrl = None
            nounLink = nounSoup.find('a', attrs={'href' : re.compile("flag")})
            #: change the flag url to a verb url 
            if nounLink is not None:
                flagUrl = nounLink['href']
                verbUrl = str.replace(str(flagUrl), 'flag', verb)
                verbResponse = self.app.post(
                    url=str(verbUrl),
                    status=404,
                    expect_errors=True
                )
                return verbResponse
            else:
                #: couldn't find a flag link for the spoof move
                return False

    #: go through the noun page's forms and look for the one with verb in its action
    for formIndex in nounForms:
        #: does it have the verb in the action?
        #log.info("actions: "+str(nounForms[formIndex].action))
        if nounForms[formIndex].action.find(verb) >= 0:
            #log.info("getting verb url: "+str(nounForms[formIndex].action))
            verbUrl = nounForms[formIndex].action

    #: post to the form's url to act on the noun with the verb
    if verbUrl is not None:
        if 'dontSubmit' in kwargs:
            if kwargs['dontSubmit'] == True:
                return verbUrl
            else:
                verbResponse = self.app.post(url=str(verbUrl))
                return verbResponse
        else:
            #log.info("posting "+verbUrl)
            verbResponse = self.app.post(url=str(verbUrl))
            return verbResponse
    else:
        return False
