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
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.event import Event, getParentEvents, getCommentEvent
from pylowiki.lib.db.page import get_page
from pylowiki.lib.db.comment import Comment, getComment, isDisabled, disableComment, enableComment, getCommentByCode, editComment
from pylowiki.lib.db.discussion import getDiscussionByID, getDiscussion as getDiscussionByCode
from pylowiki.lib.db.flag import Flag, isFlagged, getFlags, clearFlags
from pylowiki.lib.db.revision import getRevisionByCode

import simplejson as json

log = logging.getLogger(__name__)

import pylowiki.lib.helpers as h

class CommentController(BaseController):

    @h.login_required
    def adminComment(self, id1):
        code = id1
        c.comment = getCommentByCode(code)
        c.discussion = getDiscussionByID(c.comment['discussion_id'])
        c.w = getWorkshop(c.discussion['workshopCode'], c.discussion['workshopURL'])
        c.commentType = c.discussion['discType']
        c.flags = getFlags(c.comment)
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
    def commentAddHandler(self):
        try:
            request.params['submit']
            parentCommentCode = request.params['parentCode']
            data = request.params['comment-textarea']
            data = data.strip()
            if data == '':
                alert = {'type':'error'}
                alert['title'] = 'Add Comment failed.'
                alert['content'] = 'No comment text entered.'
                session['alert'] = alert
                session.save()
                return redirect(session['return_to'])
            if parentCommentCode and parentCommentCode != '0' and parentCommentCode != '':
                # Reply to an existing comment
                parentComment = getCommentByCode(parentCommentCode)
                parentCommentID = parentComment.id
                discussion = getDiscussionByCode(parentComment['discussionCode'])
            elif 'discussionCode' in request.params:
                # Root level comment
                discussion = getDiscussionByCode(request.params['discussionCode'])
                parentCommentID = 0
            comment = Comment(data, c.authuser, discussion, parentCommentID)
            return redirect(session['return_to'])
                
        except KeyError:
            # Check if the 'submit' variable is in the posted variables.
            return redirect(session['return_to'])
        return redirect(session['return_to'])
    
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

    def permalink(self, id1, id2, id3):
      workshopCode = id1
      workshopURL = id2
      revisionCode = id3

      c.w = getWorkshop(workshopCode, workshopURL)
      c.r = getRevisionByCode(revisionCode)
      c.u = getUserByID(c.r.owner)
      c.comment = getComment(c.r['parent_id'])

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
