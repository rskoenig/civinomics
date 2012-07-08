# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.comments import addDiscussion, addComment, editComment
from pylowiki.lib.db.user import getUserByID, isAdmin
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.workshop import getWorkshop
#from pylowiki.model import commit, Event, get_page
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.event import Event, getParentEvents, getCommentEvent
from pylowiki.lib.db.page import get_page
from pylowiki.lib.db.comment import Comment, getComment, disableComment, enableComment
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.flag import Flag, isFlagged, getFlags

import simplejson as json

log = logging.getLogger(__name__)

import pylowiki.lib.helpers as h

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
    def modComment(self, id1, id2, id3, id4, id5, id6):
        c.wCode = id1
        c.wURL = id2
        w = getWorkshop(c.wCode, c.wURL)
        if id6 == 'background':
           c.commentID = id3
        elif id6 == 'feedback':
           c.commentID = id3
        else:
           c.oCode = id3
           c.oURL = id4
           c.commentID = id5

        c.commentType = id6
        c.comment = getComment(c.commentID)
        c.flags = getFlags(c.comment)
        c.events = getParentEvents(c.comment)
        c.user = getUserByID(c.comment.owner)

        if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, w.id):
            h.flash('You are not authorized', 'error')
            return redirect('/')

        return render('/derived/comment_admin.html')

    @h.login_required
    def modCommentHandler(self):
        backlink = '/'

        commentID = request.params['commentID']
        comment = getComment(commentID)

        commentType = request.params['commentType']

        workshopCode = request.params['workshopCode']
        workshopURL = request.params['workshopURL']
        w = getWorkshop(workshopCode, workshopURL)

        otherCode = request.params['otherCode']
        otherURL = request.params['otherURL']
    
        if commentType == 'resource':
           backlink = "/workshop/%s/%s/resource/%s/%s"%(workshopCode, workshopURL, otherCode, otherURL)
        elif commentType == 'suggestion':
           backlink = "/workshop/%s/%s/suggestion/%s/%s"%(workshopCode, workshopURL, otherCode, otherURL)
        elif commentType == 'background':
           backlink = "/workshop/%s/%s/background"%(workshopCode, workshopURL)
        elif commentType == 'feedback':
           backlink = "/workshop/%s/%s/feedback"%(workshopCode, workshopURL)
           
        try:
           modCommentReason = request.params['modCommentReason']
           verifyModComment = request.params['verifyModComment']

           modType = request.params['modType']

           if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, w.id):
              h.flash('You are not authorized', 'error')
              return redirect(backlink)    

        except:
           backlink += "/modComment/%s"%(commentID)
           "h.flash('All fields required', 'error')"
           alert = {'type':'error'}
           alert['title'] = 'All Fields Required'
           alert['content'] = ''
           "alert['content'] = 'Please check all Required Fields'"
           session['alert'] = alert
           session.save()
           return redirect(backlink)    

        if modCommentReason == "":
            modCommentReason = "No Reason Given"

        # disable or enable the comment, log the event        
        modTitle = "" 
        if modType == 'disable':
            if comment['disabled'] == '0':
               comment['disabled'] = True
               modTitle = "Comment Disabled"
            else:
               comment['disabled'] = False
               modTitle = "Comment Enabled"
            e = Event(modTitle, modCommentReason, comment, c.authuser)
           # events = getCommentEvent(comment.id)
           # latestEvent = events[len(events)-1]

            if 'disableEvents' not in comment.keys():
                comment['disableEvents'] = e.e.id
            else:
                comment['disableEvents'] = comment['disableEvents'] + ',' + str(e.e.id)
        # delete the object, take it out of the # of comments in a discussion
        elif modType == 'delete':
            dis = getDiscussionByID(int(comment['discussion_id']))
            if comment['deleted'] == '0':
               comment['deleted'] = True
               comment['disabled'] = False
               "dis['numComments'] = int(dis['numComments']) - 1"
               modTitle = "Comment Deleted"
               e = Event(modTitle, modCommentReason, comment, c.authuser)
               if 'deleteEvents' not in comment.keys():
                    comment['deleteEvents'] = e.e.id
               else:
                   "Should never need to be down here since anything can only be deleted once"
                   comment['deleteEvents'] = comment['deleteEvents'] + ',' + str(e.e.id)
        commit(comment)

        h.flash(modTitle, 'success')
        return redirect(backlink)
    
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
            h.flash('Do not access a handler directly', 'error')
        except:
            raise
            h.flash('Unknown error', 'error')
        
        if comType == 'background':
            return redirect('/workshop/%s/%s/background' % (workshopCode, workshopURL) )
        elif comType == 'feedback':
            return redirect('/workshop/%s/%s/feedback' % (workshopCode, workshopURL) )
        elif comType == 'resource':
            resourceCode = request.params['resourceCode']
            resourceURL = request.params['resourceURL']
            return redirect('/workshop/%s/%s/resource/%s/%s/' % (workshopCode, workshopURL, resourceCode, resourceURL ) )
        elif comType == 'suggestionMain':
            suggestionCode = request.params['suggestionCode']
            suggestionURL = request.params['suggestionURL']
            return redirect('/workshop/%s/%s/suggestion/%s/%s'%(workshopCode, workshopURL, suggestionCode, suggestionURL))
        else:
            return redirect('/')
            
    """ id1: the issue's URL.
    """
    @h.login_required
    def index(self, id):
        
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
        comment = getComment( id )
        if comment:
            if session['user'] == comment.event.user.name:
                comment.disable()
                h.flash( "The comment was disabled!", "success" )
            else:
                h.flash( "The comment was NOT disabled!", "warning" )
        else:
            h.flash( "Invalid comment id", "error" )
        return redirect( session['return_to'] )

    def adminCommentDelete(self, id):
        comment = getComment(id)
        deleteComment(comment)
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
        start = 1000 # starting of counter in commentsCustom.mako
        thisID = start + int(id)
        data = request.params['textarea' + str(thisID)]
        discussionID = request.params['discussionID']
        comment = editComment(commentID, discussionID, data)
        
        if not comment:
            h.flash('Comment edit was NOT saved!', 'error')
            return redirect('/issue/%s' % comment.page.url)
        else:
            h.flash('Comment edit saved!', 'success')
            return redirect('/issue/%s' % comment.page.url)
