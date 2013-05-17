# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.db.user         as  userLib
import pylowiki.lib.db.facilitator  as  facilitatorLib
import pylowiki.lib.db.workshop     as  workshopLib
import pylowiki.lib.db.comment      as  commentLib 
import pylowiki.lib.db.message      as  messageLib
import pylowiki.lib.db.discussion   as  discussionLib 
import pylowiki.lib.db.revision     as  revisionLib
import pylowiki.lib.db.geoInfo      as  geoInfoLib
import pylowiki.lib.db.generic      as  genericLib
import pylowiki.lib.db.mainImage    as  mainImageLib
import pylowiki.lib.db.dbHelpers    as  dbHelpers
import pylowiki.lib.utils           as  utils

log = logging.getLogger(__name__)
import pylowiki.lib.helpers as h

class CommentController(BaseController):
    
    def __before__(self, action, workshopCode = None, workshopURL = None):
        if action in ['permalink', 'showThread']:
            c.w = workshopLib.getWorkshop(workshopCode, workshopURL)
            c.mainImage = mainImageLib.getMainImage(c.w)
            if not c.w:
                abort(404)
            workshopLib.setWorkshopPrivs(c.w)
            if c.w['public_private'] != 'public':
                if not c.privs['guest'] and not c.privs['participant'] and not c.privs['facilitator'] and not c.privs['admin']:
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
                parentAuthor = userLib.getUserByID(parentComment.owner)
            elif 'discussionCode' in request.params:
                # Root level comment
                discussion = discussionLib.getDiscussion(request.params['discussionCode'])
                parentCommentID = 0
                parentAuthor = userLib.getUserByID(discussion.owner)
            comment = commentLib.Comment(data, c.authuser, discussion, c.privs, role = None, parent = parentCommentID)
            title = 'Someone replied to a post you made'
            text = '(This is an automated message)'
            extraInfo = 'commentResponse'
            message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, workshop = workshop, extraInfo = extraInfo, sender = c.authuser)
            message = genericLib.linkChildToParent(message, comment.c)
            dbHelpers.commit(message)
            return redirect(utils.thingURL(workshop, thing))
                
        except KeyError:
            # Check if the 'submit' variable is in the posted variables.
            return redirect(utils.thingURL(workshop, thing))
        return redirect(utils.thingURL(workshop, thing))
    
    def permalink(self, workshopCode, workshopURL, revisionCode):
        c.revision = revisionLib.getRevisionByCode(revisionCode)
        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)
        return render('/derived/6_permaComment.bootstrap')
        
    ####################################################
    # 
    # The below functions are currently unused
    # 
    ####################################################

    def showThread(self, workshopCode, workshopURL, commentCode):
        c.w = workshopLib.getWorkshop(workshopCode, workshopURL)
        c.rootComment = commentLib.getCommentByCode(commentCode)
        c.discussion = discussionLib.getDiscussionByID(int(c.rootComment['discussion_id']))
        if 'user' in session:
            c.isScoped = workshopLib.isScoped(c.authuser, c.w)
            c.isFacilitator = facilitatorLib.isFacilitator(c.authuser.id, c.w.id)
            c.facilitators = facilitatorLib.getFacilitatorsByWorkshop(c.w.id)
        
        return render('/derived/commentThread.bootstrap')
