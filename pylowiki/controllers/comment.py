# -*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.event import Event
from pylowiki.lib.db.page import get_page
from pylowiki.lib.db.comment import Comment, getComment
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.comment import getComment, editComment
from pylowiki.lib.db.flag import Flag, isFlagged

import pylowiki.lib.helpers as h

import simplejson as json

class CommentController(BaseController):

    @h.login_required
    def flagComment(self, id1):
        commentID = id1
        comment = getComment(commentID)
        if not comment:
            return json.dumps({'id':commentID, 'result':'ERROR'})
        if not isFlagged(comment, c.authuser):
            f = Flag(comment, c.authuser)
            return json.dumps({'id':commentID, 'result':"Successfully flagged!"})
        else:
            return json.dumps({'id':commentID, 'result':"Already flagged!"})

    @h.login_required
    def addComment(self):
        try:
            request.params['submit']
            discussionID = request.params['discussionID']
            parentCommentID = request.params['parentID']
            comType = request.params['type']
            data = request.params['comment-textarea']
            workshopCode = request.params['workshopCode']
            workshopURL = request.params['workshopURL']
            
            discussion = getDiscussionByID(discussionID)
            log.info('parent comment = %s' % parentCommentID)
            comment = Comment(data, c.authuser, discussion, int(parentCommentID))
        except KeyError:
            # Check if the 'submit' variable is in the posted variables.
            raise
            h.flash('Do not access a handler directly', 'error')
        except:
            raise
            h.flash('Unknown error', 'error')
        
        if comType == 'background':
            return redirect('/workshop/%s/%s/background' % (workshopCode, workshopURL) )
        elif comType == 'feedback':
            return redirect('/workshop/%s/%s/feedback' % (workshopCode, workshopURL) )
        elif comType == 'suggestionMain':
            suggestionCode = request.params['suggestionCode']
            suggestionURL = request.params['suggestionURL']
            return redirect('/workshop/%s/%s/suggestion/%s/%s'%(workshopCode, workshopURL, suggestionCode, suggestionURL))
        else:
            return redirect('/')
            
    
    
    @h.login_required
    def index(self, id):
        """ 
            id1: the issue's URL.
        """
        #for key in request.params:
        #        log.info("key:::value ---> %s:::%s"%(key, request.params[key]))
        
        try:
            request.params['submit']
            discussionID = request.params['discussionID']
            parentCommentID = request.params['parentID']
            type = request.params['type']
            data = request.params['comment-textarea']
            p = get_page(id)
            i = p.issue
            if type == "suggestionMain": 
                suggestionURL = request.params['url']
            c = addComment(discussionID, data, parentCommentID, type)
        except KeyError:
            # Check if the 'submit' variable is in the posted variables.
            h.flash('Do not access a handler directly', 'error')
        except:
            h.flash('Unknown error', 'error')
        if request.params['type'] == 'background':
            return redirect( "/issue/%s/background" %str(id) )
        elif request.params['type'] == 'suggestionMain':
            return redirect( "/issue/%s/suggestion/%s" %(str(id), suggestionURL) )

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

    @h.login_required
    def edit(self, id):
        """
            Edits a comment by replacing the current revision with a new revision.  Just grabs relevant info
            and then uses the editComment() function in the comments library.
            
            Inputs:
                        id    ->    The comment id
        """
        commentID = id
        start = 0 # starting of counter in commentsCustom.mako
        thisID = start + int(id)
        data = request.params['textarea' + str(thisID)]
        discussionID = request.params['discussionID']
        comment = editComment(commentID, discussionID, data)
        d = getDiscussionByID(discussionID)
        
        if not comment:
            h.flash('Comment edit was NOT saved!', 'error')
            return redirect('/workshop/%s/%s' % (d['workshopCode'], d['workshopURL']))
        else:
            h.flash('Comment edit saved!', 'success')
            if d['discType'] == 'background':
                return redirect('/workshop/%s/%s/background' %(d['workshopCode'], d['workshopURL']))
            elif d['discType'] == 'feedback':
                return redirect('/workshop/%s/%s/feedback' %(d['workshopCode'], d['workshopURL']))
            elif d['discType'] == 'suggestion':
                return redirect('/workshop/%s/%s/suggestion/%s/%s' %(d['workshopCode'], d['workshopURL'], d['suggestionCode'], d['suggestionURL']))
            else:
                return redirect('/')