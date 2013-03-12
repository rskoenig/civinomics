import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import pylowiki.lib.helpers as h
from pylowiki.lib.base import BaseController, render
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import simplejson as json

log = logging.getLogger(__name__)

class FollowController(BaseController):
    
    @h.login_required
    def followHandler(self, code):
        try:
            thing = generic.getThing(code)
        except:
            abort(404)
        f = followLib.FollowOrUnfollow(c.authuser, thing)
        return "ok"
        
    @h.login_required
    def followerNotificationHandler(self, workshopCode, url, userCode):
        user = userLib.getUserByCode(userCode)
        workshop = workshopLib.getWorkshopByCode(workshopCode)
        follower = followLib.getFollow(user, workshop)
        # initialize to current value if any, '0' if not set in object
        iAlerts = '0'
        eAction = ''
        if 'itemAlerts' in follower:
            iAlerts = follower['itemAlerts']
        
        payload = json.loads(request.body)
        if 'alert' not in payload:
            return "Error"
        alert = payload['alert']
        if alert == 'items':
            if 'itemAlerts' in follower.keys(): # Not needed after DB reset
                if follower['itemAlerts'] == u'1':
                    follower['itemAlerts'] = u'0'
                    eAction = 'Turned off'
                else:
                    follower['itemAlerts'] = u'1'
                    eAction = 'Turned on'
            else:
                follower['itemAlerts'] = u'1'
                eAction = 'Turned on'
        else:
            return "Error"   
        dbHelpers.commit(follower)
        if eAction != '':
            eventLib.Event('Follower item notifications set', eAction, follower, c.authuser)
        return eAction