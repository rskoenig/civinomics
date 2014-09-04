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
import pylowiki.lib.fuzzyTime           as fuzzyTime    
import misaka as m
import simplejson as json

from pylowiki.lib.facebook          import FacebookShareObject
import pylowiki.lib.utils           as  utils
import pylowiki.lib.alerts          as  alertsLib
import pylowiki.lib.mail            as  mailLib

log = logging.getLogger(__name__)
import pylowiki.lib.helpers as h

class CommentController(BaseController):
    
    def __before__(self, action, workshopCode = None, workshopURL = None, urlCode = None):
        log.info(c.privs)
        shareOk = False
        shareUrl = None
        if workshopURL is None:
            userLib.setUserPrivs()
        if action in ['permalink', 'showThread']:
            if workshopCode is not None:
                c.w = workshopLib.getWorkshop(workshopCode, workshopURL)
                c.mainImage = mainImageLib.getMainImage(c.w)
                if not c.w:
                    abort(404)
                workshopLib.setWorkshopPrivs(c.w)
                if c.w['public_private'] != 'public':
                    if not c.privs['guest'] and not c.privs['participant'] and not c.privs['facilitator'] and not c.privs['admin']:
                        abort(404)
                shareUrl = utils.workshopURL(c.w)
                shareOk = workshopLib.isPublic(c.w)
            elif urlCode is not None:
                thing = genericLib.getThing(urlCode)
                if not thing:
                    abort(404)
                if thing.objType == 'initiative':
                    c.initiative = thing
                    shareOk = initiativeLib.isPublic(c.initiative)
                    shareUrl = utils.initiativeURL(c.initiative)
                elif thing.objType == 'profile':
                    # note: should we be assigning this something?
                    c.user
                    shareOk = True
                
        ################## FB SHARE ###############################
        # these values are needed for facebook sharing of a workshop
        # - details for sharing a specific idea are modified in the view idea function
        c.facebookShare = FacebookShareObject(
            itemType='comment',
            url=shareUrl,
            shareOk = shareOk
        )
        # add this line to tabs in the workshop in order to link to them on a share:
        # c.facebookShare.url = c.facebookShare.url + '/activity'
        #################################################
    
    @h.login_required
    def commentAddHandler(self):
        # check throughout function if add comment was submited via traditional form or json
        # if through json, it's coming from an activity feed and we do NOT want to return redirect
        # return redirect breaks the success function on https
        if request.params:
            payload = request.params  
        elif json.loads(request.body):
            payload = json.loads(request.body)
        
        try:
            payload['submit']
            parentCommentCode = payload['parentCode']
            thingCode = payload['thingCode']
            thing = genericLib.getThing(thingCode)
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

            elif thing.objType == 'discussion' and (thing['discType'] == 'organization_general' or thing['discType'] == 'organization_position'):
                userLib.setUserPrivs()
            elif thing.objType == 'photo' or thing.objType == 'initiative' or thing.objType == 'agendaitem' or 'initiativeCode' in thing:
                
                userLib.setUserPrivs()
                if 'initiativeCode' in thing:
                    initiative = genericLib.getThing(thing['initiativeCode'])

            data = payload['comment-textarea']
            data = data.strip()
            if data == '':
                alert = {'type':'error'}
                alert['title'] = 'Add Comment failed.'
                alert['content'] = 'No comment text entered.'
                session['alert'] = alert
                session.save()
                if request.params:
                    return redirect(session['return_to'])
                elif json.loads(request.body):
                    return json.dumps({'statusCode':1})
            
            if parentCommentCode and parentCommentCode != '0' and parentCommentCode != '':
                log.info("1")
                # Reply to an existing comment
                parentComment = commentLib.getCommentByCode(parentCommentCode)
                parentCommentID = parentComment.id
                discussion = discussionLib.getDiscussion(parentComment['discussionCode'])
                parentAuthor = userLib.getUserByID(parentComment.owner)
            elif 'discussionCode' in payload:
                log.info("2")
                # Root level comment
                discussion = discussionLib.getDiscussion(payload['discussionCode'])
                parentCommentID = 0
                parentAuthor = userLib.getUserByID(discussion.owner)
            log.info(c.privs)
            comment = commentLib.Comment(data, c.authuser, discussion, c.privs, role = None, parent = parentCommentID)
            if thing.objType == 'idea' or thing.objType == 'initiative' or thing.objType == 'agendaitem':
                if 'commentRole' in payload:
                    commentRole = payload['commentRole']
                    comment['commentRole'] = commentRole
                    dbHelpers.commit(comment)

            # Notifications that the comment was made via message and email
            # don't send message if the object owner is the commenter
            if parentAuthor != c.authuser and thing.objType != 'agendaitem':
                title = ' replied to a post you made'
                text = '(This is an automated message)'
                extraInfo = 'commentResponse'
                
                if thing.objType.replace("Unpublished", "") == 'photo':
                    title = ' commented on one of your pictures'
                    message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, sender = c.authuser, extraInfo = "commentOnPhoto")
                elif thing.objType.replace("Unpublished", "") == 'initiative':
                    title = ' commented on one of your initiatives'
                    message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, sender = c.authuser, extraInfo = "commentOnInitiative")
                elif thing.objType.replace("Unpublished", "") == 'resource':
                    title = ' commented on a post you made'
                    message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, sender = c.authuser, extraInfo = "commentOnResource")
                elif 'workshopCode' in thing:
                    title = ' replied to a post you made'
                    message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, workshop = workshop, extraInfo = extraInfo, sender = c.authuser)
                elif thing.objType.replace("Unpublished", "") == 'discussion':
                    if thing['discType'] == 'update':
                        title = ' commented on an initiative update you made'
                        message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, sender = c.authuser, extraInfo = "commentOnUpdate")
                    elif thing['discType'] == 'organization_general':
                        title = ' commented on an organization forum discussion you started'
                        message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, sender = c.authuser, extraInfo = "commentOnOrgGeneral")
                    elif thing['discType'] == 'organization_position':
                        title = ' commented on one of your organization positions'
                        message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, sender = c.authuser, extraInfo = "commentOnOrgPosition")
                    elif 'workshopCode' in thing:
                        title = ' replied to a post you made'
                        message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, workshop = workshop, extraInfo = extraInfo, sender = c.authuser)
                elif 'workshopCode' in thing:
                        title = ' replied to a post you made'
                        message = messageLib.Message(owner = parentAuthor, title = title, text = text, privs = c.privs, workshop = workshop, extraInfo = extraInfo, sender = c.authuser)
                        
                message = genericLib.linkChildToParent(message, comment)
                dbHelpers.commit(message)
                alertsLib.emailAlerts(comment)

            if 'commentAlerts' in parentAuthor and parentAuthor['commentAlerts'] == '1' and (parentAuthor['email'] != c.authuser['email']):
                if 'workshopCode' in thing:
                    mailLib.sendCommentMail(parentAuthor['email'], thing, workshop, data)
                elif thing.objType.replace("Unpublished", "") == 'photo' or 'photoCode' in thing:
                    mailLib.sendCommentMail(parentAuthor['email'], thing, thing, data)
                elif thing.objType.replace("Unpublished", "") == 'initiative' or 'initiativeCode' in thing:
                    mailLib.sendCommentMail(parentAuthor['email'], thing, thing, data)
            
            if request.params:
                log.info("commentCCN where oh where")
                if 'workshopCode' in thing:   
                    return redirect(utils.thingURL(workshop, thing))
                elif thing.objType == 'photo' or 'photoCode' in thing:
                    return redirect(utils.profilePhotoURL(thing))
                elif thing.objType == 'initiative' or 'initiativeCode' in thing and thing.objType != 'discussion':
                    return redirect(utils.initiativeURL(thing))
                elif thing.objType == 'discussion':
                    return redirect(utils.profileDiscussionURL(thing))
            elif json.loads(request.body):
                return json.dumps({'statusCode':0})
        except KeyError:
            # Check if the 'submit' variable is in the posted variables.
            log.info("commentCCN got error")
            if request.params:
                return redirect(session['return_to'])
            elif json.loads(request.body):
                return json.dumps({'statusCode':1})

        if request.params:
            return redirect(utils.thingURL(workshop, thing))
        elif json.loads(request.body):
            return json.dumps({'statusCode':2})
    
    def permalink(self, workshopCode, workshopURL, revisionCode):
        c.revision = revisionLib.getRevisionByCode(revisionCode)
        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)
            c.facebookShare.url = request.url
        return render('/derived/6_permaComment.bootstrap')
        
    def permalinkPhoto(self, urlCode, revisionCode):
        c.revision = revisionLib.getRevisionByCode(revisionCode)
        c.user = userLib.getUserByCode(urlCode)
        c.facebookShare.url = request.url
        return render('/derived/6_permaPhotoComment.bootstrap')
        
    def permalinkInitiative(self, urlCode, revisionCode):
        c.revision = revisionLib.getRevisionByCode(revisionCode)
        c.initiative = genericLib.getThing(urlCode)
        c.facebookShare.url = request.url
        return render('/derived/6_permaInitiativeComment.bootstrap')

    def jsonCommentsForItem(self, urlCode):
        result = []
        myRatings = []
        if 'ratings' in session:
		    myRatings = session['ratings']
        comments = commentLib.getCommentsInDiscussionByCode(urlCode)
        for comment in comments:
            entry = {}
            entry['text'] = comment['data']
            entry['html'] = m.html(entry['text'], render_flags=m.HTML_SKIP_HTML)
            entry['urlCode'] = comment['urlCode']
            entry['voteCount'] = int(comment['ups']) + int(comment['downs'])
            entry['ups'] = int(comment['ups'])
            entry['downs'] = int(comment['downs'])
            entry['netVotes'] = int(comment['ups']) - int(comment['downs'])
            if entry['urlCode'] in myRatings:
                entry['rated'] = myRatings[entry['urlCode']]
            else:
                entry['rated'] = 0

            entry['commentRole'] = ''
            if 'commentRole' in comment:
                entry['commentRole'] = comment['commentRole']
                    
            if 'ideaCode' in comment or 'initiativeCode' in comment or 'meetingCode' in comment:
                entry['doCommentRole'] = 'yes'
            else:
                entry['doCommentRole'] = 'no'

            entry['date'] = fuzzyTime.timeSince(comment.date)

            # comment author
            author = userLib.getUserByID(comment.owner)
            entry['authorName'] = author['name']
            entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']
            entry['authorPhoto'] = utils._userImageSource(author)
            if 'user' in session and (c.authuser.id == comment.owner or userLib.isAdmin(c.authuser.id)):
                entry['canEdit'] = 'yes'
            else:
                entry['canEdit'] = 'no'
                
            # get revisions
            revisions = revisionLib.getRevisionsForThing(comment)
            if revisions:
                entry['revisions'] = 'yes'
            else:
                entry['revisions'] = 'no'
            entry['revisionList'] = []
            if revisions:
                for rev in revisions:
                    revision = {}
                    code = rev['urlCode'] 
                    date = str(rev.date)
                    text = rev['data']
                    html = m.html(rev['data'], render_flags=m.HTML_SKIP_HTML)
                    if 'commentRole' in rev:
                        role = rev['commentRole']
                    else:
                        role = 'Neutral'
                        
                    if role == 'yes':
                        role = 'Pro'
                    elif role == 'no':
                        role = 'Con'
                    else:
                        role = 'Neutral'
                        
                    revision['date'] = date
                    revision['urlCode'] = code
                    revision['text'] = text
                    revision['html'] = html
                    revision['role'] = role
                    entry['revisionList'].append(revision)
                
            result.append(entry)

        if len(result) == 0:
            return json.dumps({'statusCode':1})
        return json.dumps({'statusCode':0, 'result':result})
        
    def jsonEditCommentHandler(self):
        payload = json.loads(request.body)
        if 'commentCode' in payload:
            commentCode = payload['commentCode']
            comment = commentLib.getCommentByCode(commentCode)
            # save a revision first
            revision = revisionLib.Revision(c.authuser, comment)
            if not comment:
                return json.dumps({'statusCode':1})
            
            if 'commentText' in payload and payload['commentText'] != '':
                comment['data'] = payload['commentText']
                comment['commentRole'] = payload['commentRole']
                dbHelpers.commit(comment)
                return json.dumps({'statusCode':0})

        return json.dumps({'statusCode':1})

        
        
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
