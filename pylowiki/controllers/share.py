import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.share        as shareLib
import pylowiki.lib.mail            as mailLib
import pylowiki.lib.db.dbHelpers    as dbHelpers

log = logging.getLogger(__name__)

class ShareController(BaseController):

    def emailShare(self):
        payload = json.loads(request.body)
        if 'urlCode' not in payload or 'memberMessage' not in payload:
            return "Error no urlCode or memberMessage"
        urlCode = payload['urlCode']
        memberMessage = payload['memberMessage']
        # make sure not already a listener for this workshop
        listener = listenerLib.getListenerByCode(urlCode)
        if listener['invites'] != '':
            inviteList = listener['invites'].split(",")
            numInvites = str(len(inviteList))
        else:
            inviteList = []
            numInvites = '0'
        if c.user['urlCode'] in inviteList:
            return "You have already sent an invitiation to this person for this workshop!"
        mailLib.sendListenerInviteMail(listener['email'], c.authuser, c.w, memberMessage, numInvites)
        inviteList.append(c.user['urlCode'])
        listener['invites'] = ",".join(inviteList)
        dbHelpers.commit(listener)
        eventLib.Event('Listener invitation sent', 'Listener invitation sent by %s: %s'%(c.authuser['name'], memberMessage), listener, user = c.authuser)
        return "Invitation sent. Thanks!"
        
