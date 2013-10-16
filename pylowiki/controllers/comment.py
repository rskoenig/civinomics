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
import pylowiki.lib.alerts          as  alertsLib
import pylowiki.lib.mail            as  mailLib

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
            log.info('thingCode is %s'%thingCode)
            if not thing:
                return False
            if thing['disabled'] == '1':
                return False
            if 'workshopCode' in thing:
                workshop = workshopLib.getWorkshopByCode(thing['workshopCode'])
                if not workshop:
                    return False
                else:
                    workshopLib.setWorkshopPrivs(workshop)
            elif thing.objType == 'photo' or thing.objType == 'initiative':
                userLib.setUserPrivs()
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
            log.info('before comment')
            comment = commentLib.Comment(data, c.authuser, discussion, c.privs, role = None, parent = parentCommentID)
            title = ' replied to a post you made'
            text = '(This is an automated message)'
            extraInfo = 'commentResponse'
            log.info('after comment')
            if 'workshopCode' in thing:
                title = ' replied to a post you made'
                message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, workshop = workshop, extraInfo = extraInfo, sender = c.authuser)
            elif thing.objType.replace("Unpublished", "") == 'photo':
                title = ' commented on one of your pictures'
                message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, sender = c.authuser, extraInfo = "commentOnPhoto")
            elif thing.objType.replace("Unpublished", "") == 'initiative':
                title = ' commented on one of your initiatives'
                message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, sender = c.authuser, extraInfo = "commentOnInitiative")
            message = genericLib.linkChildToParent(message, comment.c)
            dbHelpers.commit(message)
            alertsLib.emailAlerts(comment)
            if 'commentAlerts' in parentAuthor and parentAuthor['commentAlerts'] == '1' and (parentAuthor['email'] != c.authuser['email']):
                if 'workshopCode' in thing:
                    mailLib.sendCommentMail(parentAuthor['email'], thing, workshop, data)
                elif thing.objType.replace("Unpublished", "") == 'photo' or 'photoCode' in thing:
                    mailLib.sendCommentMail(parentAuthor['email'], thing, thing, data)
                elif thing.objType.replace("Unpublished", "") == 'initiative' or 'initiativeCode' in thing:
                    mailLib.sendCommentMail(parentAuthor['email'], thing, thing, data)
            
            if 'workshopCode' in thing:   
                return redirect(utils.thingURL(workshop, thing))
            elif thing.objType == 'photo' or 'photoCode' in thing:
                return redirect(utils.profilePhotoURL(thing))
            elif thing.objType == 'initiative' or 'initiativeCode' in thing:
                return redirect(utils.initiativeURL(thing))
        except KeyError:
            # Check if the 'submit' variable is in the posted variables.
            return redirect(utils.thingURL(workshop, thing))
        return redirect(utils.thingURL(workshop, thing))
    
    def permalink(self, workshopCode, workshopURL, revisionCode):
        c.revision = revisionLib.getRevisionByCode(revisionCode)
        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)
        return render('/derived/6_permaComment.bootstrap')
        
    def permalinkPhoto(self, userCode, userURL, revisionCode):
        c.revision = revisionLib.getRevisionByCode(revisionCode)
        c.user = userLib.getUserByCode(userCode)
        return render('/derived/6_permaPhotoComment.bootstrap')
        
    def permalinkInitiative(self, urlCode, url, revisionCode):
        c.revision = revisionLib.getRevisionByCode(revisionCode)
        c.initiative = genericLib.getThing(urlCode)
        return render('/derived/6_permaInitiativeComment.bootstrap')
        
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
