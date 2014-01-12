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
import pylowiki.lib.utils           as utils
import simplejson as json

log = logging.getLogger(__name__)

class FollowController(BaseController):
    
    @h.login_required
    def followHandler(self, code):
        iPhoneApp = utils.iPhoneRequestTest(request)
        try:
            thing = generic.getThing(code)
        except:
            if iPhoneApp:
                statusCode = 2
                response.headers['Content-type'] = 'application/json'
                result = "404"
                return json.dumps({'statusCode':statusCode, 'result':result})
            else:
                abort(404)
        f = followLib.FollowOrUnfollow(c.authuser, thing)
        if iPhoneApp:
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            result = "ok"
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return "ok"
        
    @h.login_required
    def followerNotificationHandler(self, parentCode, url, userCode):
        # check to see if this is a request from the iphone app
        iPhoneApp = utils.iPhoneRequestTest(request)

        user = generic.getThing(userCode)
        parent = generic.getThing(parentCode)
        follower = followLib.getFollow(user, parent)
        # initialize to current value if any, '0' if not set in object
        iAlerts = '0'
        eAction = ''
        if 'itemAlerts' in follower:
            iAlerts = follower['itemAlerts']
        
        if iPhoneApp:
            try:
                alert = request.params['alert']
            except:
                statusCode = 2
                response.headers['Content-type'] = 'application/json'
                #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
                return json.dumps({'statusCode':statusCode, 'result':'error'})
        else:
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
        elif alert == 'digest':
            if 'digest' in follower.keys(): # Not needed after DB reset
                if follower['digest'] == u'1':
                    follower['digest'] = u'0'
                    eAction = 'Turned off'
                else:
                    follower['digest'] = u'1'
                    eAction = 'Turned on'
            else:
                follower['digest'] = u'1'
                eAction = 'Turned on'
        else:
            if iPhoneApp:
                statusCode = 2
                response.headers['Content-type'] = 'application/json'
                #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
                return json.dumps({'statusCode':statusCode, 'result':'error'})
            else:
                return "Error"

        dbHelpers.commit(follower)
        if eAction != '':
            eventLib.Event('Follower item notifications set', eAction, follower, c.authuser)
        
        if iPhoneApp:
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            result = eAction
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return eAction