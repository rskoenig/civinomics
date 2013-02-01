# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.db.user         as  userLib
import pylowiki.lib.db.facilitator  as  facilitatorLib
import pylowiki.lib.db.workshop     as  workshopLib
import pylowiki.lib.db.comment      as  commentLib 
import pylowiki.lib.db.discussion   as  discussionLib 
import pylowiki.lib.db.revision     as  revisionLib
import pylowiki.lib.db.generic      as  genericLib

log = logging.getLogger(__name__)
import pylowiki.lib.helpers as h

class CommentController(BaseController):
    
    def __before__(self, action, workshopCode = None, workshopURL = None):
        if action in ['permalink', 'showThread']:
            c.w = workshopLib.getWorkshop(workshopCode, workshopURL)
            if not c.w:
                abort(404)
    
    @h.login_required
    def commentAddHandler(self):
        try:
            request.params['submit']
            parentCommentCode = request.params['parentCode']
            thingCode = request.params['thingCode']
            thing = genericLib.getThing(thingCode)
            if not thing:
                return False
            if thing['disabled'] == '1':
                return False
            workshop = workshopLib.getWorkshopByCode(thing['workshopCode'])
            if not workshop:
                return False
            else:
                workshopLib.setWorkshopPrivs(workshop)
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
                parentComment = commentLib.getCommentByCode(parentCommentCode)
                parentCommentID = parentComment.id
                discussion = discussionLib.getDiscussion(parentComment['discussionCode'])
            elif 'discussionCode' in request.params:
                # Root level comment
                discussion = discussionLib.getDiscussion(request.params['discussionCode'])
                parentCommentID = 0
            comment = commentLib.Comment(data, c.authuser, discussion, c.privs, role = None, parent = parentCommentID)
            return redirect(session['return_to'])
                
        except KeyError:
            # Check if the 'submit' variable is in the posted variables.
            return redirect(session['return_to'])
        return redirect(session['return_to'])

    ####################################################
    # 
    # The below functions are currently unused
    # 
    ####################################################
    def permalink(self, workshopCode, workshopURL, revisionCode):
        c.r = revisionLib.getRevisionByCode(revisionCode)
        c.u = userLib.getUserByID(c.r.owner)
        c.comment = commentLib.getComment(c.r['parent_id'])
        
        return render('/derived/permaComment.bootstrap')

    def showThread(self, workshopCode, workshopURL, commentCode):
        c.w = workshopLib.getWorkshop(workshopCode, workshopURL)
        c.rootComment = commentLib.getCommentByCode(commentCode)
        c.discussion = discussionLib.getDiscussionByID(int(c.rootComment['discussion_id']))
        if 'user' in session:
            c.isScoped = workshopLib.isScoped(c.authuser, c.w)
            c.isFacilitator = facilitatorLib.isFacilitator(c.authuser.id, c.w.id)
            c.facilitators = facilitatorLib.getFacilitatorsByWorkshop(c.w.id)
        
        return render('/derived/commentThread.bootstrap')
