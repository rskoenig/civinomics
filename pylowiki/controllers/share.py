import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers         as h
import pylowiki.lib.db.share        as shareLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.mail            as mailLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic

import simplejson as json

log = logging.getLogger(__name__)

class ShareController(BaseController):
    @h.login_required
    def __before__(self, action, userCode = None, workshopCode = None):
        if userCode is not None and workshopCode is not None:
                c.user = userLib.getUserByCode(userCode)
                c.w = workshopLib.getWorkshopByCode(workshopCode)
        else:
            abort(404)

    @h.login_required
    def shareEmailHandler(self):
        payload = json.loads(request.body)
        if 'itemURL' not in payload or 'itemCode' not in payload or 'memberMessage' not in payload or 'recipientName' not in payload or 'recipientEmail' not in payload:
            return "Please enter all requested information."
        itemURL = payload['itemURL']
        if not itemURL or itemURL == '':
            return "Need URL to item"
        itemCode = payload['itemCode']
        if not itemCode or itemCode == '':
            return "Need urlCode to item"
        memberMessage = payload['memberMessage']
        recipientName = payload['recipientName']
        if not recipientName or recipientName == '':
            return "Need name of recipient"
        recipientEmail = payload['recipientEmail']
        if not recipientEmail or recipientEmail == '':
            return "Need email address of recipient"
            
        # create the share object
        share = shareLib.Share(c.user, itemCode, itemURL, recipientEmail, recipientName, memberMessage)
        item = generic.getThing(itemCode)
        mailLib.sendShareMail(recipientName, recipientEmail, memberMessage, c.user, c.w, item, itemURL)
        
        returnMsg =  "Email sent, thanks for sharing!"
        return returnMsg
  
    @h.login_required
    def shareFacebookHandler(self, itemCode, itemURL, postId):
        # create the share object
        # we can't directly see what message the user posted with this share, but we
        # might be able to look it up with a facebook graph api call using the postId,
        # so for now it's best to store the postId as the message. 
        # see https://developers.facebook.com/docs/reference/api/post/
        # NOTE - should we add a field to the share object to account for facebook shares?
        # itemCode, itemURL, postId = id1.split("&")
        if itemCode and itemURL and postId:
            if 'user' in session:
                share = shareLib.Share(c.authuser, itemCode, itemURL, 'facebook', '', postId)
                return 'share stored'
        else:
            return None