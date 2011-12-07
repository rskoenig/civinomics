# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

#from pylowiki.model import commit_comment, disable_comment, get_comment
from pylowiki.model import commit_comment, get_comment
import pylowiki.lib.helpers as h

class CommentController(BaseController):

    @h.login_required   
    def index(self, id):
        type = request.params['type']
        try:
            request.params['submit'] #Try submit, if false redirect back.
            data = request.params['comment-textarea']
            if type == "suggestion":
                url = [request.params['suggestionTitle'], int(request.params['issueID'])]
            elif type == "background":
                url = id
            if commit_comment( url, session['user'], data, type ):
                h.flash( "Your comment has gone into the moderation queue.", "success" )
            else:
                h.flash( "The comment was NOT saved.", "warning" )
        except:
            h.flash( "The comment was NOT saved.", "warning" )
        if type == "background":
            return redirect( "/issue/%s/background" %str(id) )
        elif type == "suggestion":
            return redirect('/issue/%s/suggestion/%s'%(str(id), str(url[0])))

    @h.login_required   
    def disable(self, id):
        """disable a comment by id"""
        comment = get_comment( id )
        if comment:
            if session['user'] == comment.event.user.name:
                comment.disable()
                h.flash( "The comment was disabled!", "success" )
            else:
                h.flash( "The comment was NOT disabled!", "warning" )
        else:
            h.flash( "Invalid comment id", "error" )
        return redirect( session['return_to'] )
