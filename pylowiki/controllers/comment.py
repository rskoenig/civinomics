# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.utils import urlify
from pylowiki.lib.base import BaseController, render
from pylowiki.lib.comments import addDiscussion, addComment
from pylowiki.lib.db.user import getUserByID, isAdmin
from pylowiki.lib.db.facilitator import isFacilitator, getFacilitatorsByWorkshop
from pylowiki.lib.db.workshop import getWorkshop, isScoped
#from pylowiki.model import commit, Event, get_page
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.event import Event, getParentEvents, getCommentEvent
from pylowiki.lib.db.page import get_page
from pylowiki.lib.db.comment import Comment, getComment, disableComment, enableComment, getCommentByCode, editComment
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.flag import Flag, isFlagged, getFlags, clearFlags
from pylowiki.lib.db.revision import getRevisionByCode

import simplejson as json

log = logging.getLogger(__name__)

import pylowiki.lib.helpers as h

class CommentController(BaseController):

    @h.login_required
    def flagComment(self, id1):
        commentID = id1
        comment = getComment(commentID)
        commentCode = comment['urlCode']
        if not comment:
            return json.dumps({'id':commentCode, 'result':'ERROR'})
        if not isFlagged(comment, c.authuser):
            f = Flag(comment, c.authuser)
            return json.dumps({'id':commentCode, 'result':"Successfully flagged!"})
        else:
            return json.dumps({'id':commentCode, 'result':"Already flagged!"})

    @h.login_required
    def adminComment(self, id1):
        code = id1
        c.comment = getCommentByCode(code)
        c.discussion = getDiscussionByID(c.comment['discussion_id'])
        c.w = getWorkshop(c.discussion['workshopCode'], c.discussion['workshopURL'])
        c.commentType = c.discussion['discType']
        c.flags = getFlags(c.comment)
        log.info('len of c.flags is %s'%len(c.flags))
        c.events = getParentEvents(c.comment)
        c.user = getUserByID(c.comment.owner)

        if not isAdmin(c.authuser.id) and not isFacilitator(c.authuser.id, c.w.id):
            h.flash('You are not authorized', 'error')
            return redirect('/')

        return render('/derived/comment_admin.bootstrap')

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

        return render('/derived/comment_admin.bootstrap')

    @h.login_required
    def clearCommentFlagsHandler(self, id1):
        code = id1

        c.comment = getCommentByCode(code)
        fList = getFlags(c.comment)

        clearError = 0
        clearMessage = ""
        c.discussion = getDiscussionByID(c.comment['discussion_id'])

        if 'clearCommentFlagsReason' in request.params:
            clearReason = request.params['clearCommentFlagsReason']
            if clearReason != '':
                clearFlags(c.comment)
                clearTitle = "Flags cleared"
                e = Event(clearTitle, clearReason, c.comment, c.authuser)
            else:
                clearError = 1
                clearMessage = "Please include a reason for your action"
        else:
            clearError = 1
            clearMessage = "Please include a reason for your action"

        if clearError:
            alert = {'type':'error'}
            alert['title'] = "Flags not cleared"
            alert['content'] = clearMessage
            session['alert'] = alert
            session.save()
        else:
            clearMessage = "Flags cleared from this comment"
            alert = {'type':'success'}
            alert['title'] = 'Flags cleared!'
            alert['content'] = clearMessage
            session['alert'] = alert
            session.save()

        returnURL = "/adminComment/" + code
        return redirect(returnURL)

     

    @h.login_required
    def modCommentHandler(self, id1):
        code = id1
        backlink = '/'

        comment = getCommentByCode(code)
        discussion = getDiscussionByID(comment['discussion_id'])

        commentType = discussion['discType']

        workshopCode = discussion['workshopCode']
        workshopURL = discussion['workshopURL']
        w = getWorkshop(workshopCode, workshopURL)

        if commentType == 'resource':
           backlink = "/workshop/%s/%s/resource/%s/%s"%(workshopCode, workshopURL, discussion['resourceCode'], discussion['resourceURL'])
        elif commentType == 'suggestion':
           backlink = "/workshop/%s/%s/suggestion/%s/%s"%(workshopCode, workshopURL, discussion['suggestionCode'], discussion['suggestionURL'])
        elif commentType == 'general':
           backlink = "/workshop/%s/%s/discussion/%s/%s"%(workshopCode, workshopURL, discussion['urlCode'], discussion['url'])
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
           alert = {'type':'error'}
           alert['title'] = 'All Fields Required'
           alert['content'] = ''
           "alert['content'] = 'Please check all Required Fields'"
           session['alert'] = alert
           session.save()
           return redirect(session['return_to'])

        if modCommentReason == "":
            modCommentReason = "No Reason Given"

        # disable or enable the comment, log the event        
        modTitle = "" 
        if modType == 'disable':
            if comment['disabled'] == '0':
               comment['disabled'] = '1'
               modTitle = "Comment Disabled"
            else:
               comment['disabled'] = '0'
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
               comment['deleted'] = '1'
               comment['disabled'] = '0'
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
        cError = 0
        try:
            request.params['submit']
            discussionID = request.params['discussionID']
            parentCommentID = request.params['parentID']
            comType = request.params['type']
            data = request.params['comment-textarea']
            data = data.lstrip()
            data = data.rstrip()
            if data == '':
                alert = {'type':'error'}
                alert['title'] = 'Add Comment failed.'
                alert['content'] = 'No comment text entered.'
                session['alert'] = alert
                session.save()
                cError = 1
            
            workshopCode = request.params['workshopCode']
            workshopURL = request.params['workshopURL']
            
            discussion = getDiscussionByID(discussionID)

            log.info('parent comment = %s' % parentCommentID)
            if parentCommentID and parentCommentID != '0' and parentCommentID != '':
                parentComment = getCommentByCode(parentCommentID)
                parentCommentID = parentComment.id

            if cError == 0:
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
        elif comType == 'discussion':
            discussionCode = discussion['urlCode']
            discussionURL = discussion['url']
            return redirect('/workshop/%s/%s/discussion/%s/%s'%(workshopCode, workshopURL, discussionCode, discussionURL))
        elif comType == 'thread':
            return redirect(session['return_to'])
        else:
            return redirect('/')
            
    """ id1: the issue's URL.
    """
    ##@h.login_required
    def index(self, id):
        
        #for key in request.params:
        #        log.info("key:::value ---> %s:::%s"%(key, request.params[key]))
        
        c.comment = getCommentByCode(id)
        d = getDiscussionByID(c.comment['discussion_id'])
        wLink = '/workshop/' + d['workshopCode'] + '/' + d['workshopURL']
        if d['discType'] == 'background':
           oLink = wLink + '/background'
        elif d['discType'] == 'suggestion':
           oLink = wLink + '/suggestion/' + d['suggestionCode'] + '/' + d['suggestionURL']
        elif d['discType'] == 'general':
           oLink = wLink + '/discussion/' + d['urlCode'] + '/' + d['url']
        elif d['discType'] == 'resource':
           oLink = wLink + '/resource/' + d['resourceCode'] + '/' + d['resourceURL']
        elif d['discType'] == 'sresource':
           oLink = wLink + '/resource/' + d['resourceCode'] + '/' + d['resourceURL']
    
        return redirect( oLink )

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
    def edit(self, id1):
        """
            Edits a comment by replacing the current revision with a new revision.  Just grabs relevant info
            and then uses the editComment() function in the comments library.
            
            Inputs:
                        id1    ->    The comment hash
        """
        commentCode = id1
        cError = 0
        data = request.params['textarea' + commentCode]
        data = data.lstrip()
        data = data.rstrip()
        if data == '':
            alert = {'type':'error'}
            alert['title'] = 'Edit Comment failed.'
            alert['content'] = 'No comment text entered.'
            session['alert'] = alert
            session.save()
            cError = 1

        comment = getCommentByCode(commentCode)
        discussionID = comment['discussion_id']
        d = getDiscussionByID(discussionID)
        if d['discType'] == 'suggestion':
            backlink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + "/suggestion/" + d['suggestionCode'] + "/" + d['suggestionURL']
        elif d['discType'] == 'resource':
            backlink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + "/resource/" + d['resourceCode'] + "/" + d['resourceURL']
        elif d['discType'] == 'sresource':
            backlink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + + "/suggestion/" + d['suggestionCode'] + "/" + d['suggestionURL'] + "/resource/" + "/resource/" + d['resourceCode'] + "/" + d['resourceURL']
        elif d['discType'] == 'general':
            backlink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + "/discussion/" + d['urlCode'] + "/" + d['url']
        elif d['discType'] == 'background':
            backlink = "/workshop/" + d['workshopCode'] + "/" + d['workshopURL'] + "/background"

        if 'discType' in request.params:
          if request.params['discType'] == 'thread':
            backlink = session['return_to']

        if cError == 0:
           comment = editComment(commentCode, discussionID, data)
           if not comment:
               alert = {'type':'error'}
               alert['title'] = 'Edit Comment failed.'
               alert['content'] = 'Unknown error in editComment.'
               session['alert'] = alert
               session.save()
           else:
               alert = {'type':'success'}
               alert['title'] = 'Edit Comment.'
               alert['content'] = 'Edit comment successful.'
               session['alert'] = alert
               session.save()
               #eMsg = "Comment data updated. " + remark
               #Event('Comment edited by %s'%c.authuser['name'], eMsg, comment, c.authuser)
               Event('Comment edited by %s'%c.authuser['name'], comment, c.authuser)

        return redirect(backlink)


    def permalink(self, id1, id2, id3):
      workshopCode = id1
      workshopURL = id2
      revisionCode = id3

      c.w = getWorkshop(workshopCode, workshopURL)
      c.r = getRevisionByCode(revisionCode)
      c.u = getUserByID(c.r.owner)

      return render('/derived/permaComment.bootstrap')

    def showThread(self, id1, id2, id3):
      workshopCode = id1
      workshopURL = id2
      commentCode = id3

      c.w = getWorkshop(workshopCode, workshopURL)
      c.rootComment = getCommentByCode(commentCode)
      c.discussion = getDiscussionByID(int(c.rootComment['discussion_id']))
      if 'user' in session:
        c.isScoped = isScoped(c.authuser, c.w)
        c.isFacilitator = isFacilitator(c.authuser.id, c.w.id)
      c.facilitators = getFacilitatorsByWorkshop(c.w.id)

      return render('/derived/commentThread.bootstrap')
