# -*- coding: utf-8 -*-
from pylowiki.tests import *

import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.workshops as workshop

import logging
log = logging.getLogger(__name__)

def addCommentToIdeaPage(self, ideaPage, commentText):
    """ adds a comment to an idea page """
    # comment on this idea
    addCommentForm = ideaPage.forms[formDefs.addComment()]
    addCommentForm.set(formDefs.addComment_text(), commentText)
    # the form for submitting an idea has an extra parameter added to it as well.
    # this is an easy way to add the extra parameter
    params = {}
    params = formHelpers.loadWithSubmitFields(addCommentForm)
    params[formDefs.parameter_submit()] = formDefs.addComment_submit()
    commentAdded = self.app.get(
        url = str(addCommentForm.action),
        params=params
    ).follow()
    return commentAdded

def addCommentToObject(self, objectPage, commentText, **kwargs):
    """ adds a comment to the page for a conversation, idea or resource """
    # comment on this idea
    addCommentForm = objectPage.forms[formDefs.addComment()]
    addCommentForm.set(formDefs.addComment_text(), commentText)
    # the form for submitting an idea has an extra parameter added to it as well.
    # this is an easy way to add the extra parameter
    params = {}
    params = formHelpers.loadWithSubmitFields(addCommentForm)
    params[formDefs.parameter_submit()] = formDefs.addComment_submit()
    
    if 'expect_errors' in kwargs:
        if kwargs['expect_errors'] == True:
            commentAdded = self.app.get(
                url = str(addCommentForm.action),
                params=params,
                status=404,
                expect_errors=True
            ).follow()
        else:
            commentAdded = self.app.get(
                url = str(addCommentForm.action),
                params=params
            ).follow()
    else:
        commentAdded = self.app.get(
            url = str(addCommentForm.action),
            params=params
        ).follow()
    return commentAdded
