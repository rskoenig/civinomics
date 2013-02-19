import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.mail import send
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.demo         as demoLib
import pylowiki.lib.db.workshop     as workshopLib

import time

log = logging.getLogger(__name__)

class ActivateController(BaseController):

    def index(self, id):
        hash, sep, email = id.partition('__')
        user = userLib.getUserByEmail(email)
        message = {}
        if user:
            if user['activated'] == '0':
                if user['activationHash'] == hash:
                    user['activated'] = '1'
                    user['laston'] = time.time()
                    if commit(user):
                        session["user"] = user['name']
                        session["userCode"] = user['urlCode']
                        session["userURL"] = user['url']
                        session.save()
                        c.authuser = user
                        userLib.sendWelcomeMail(user)
                        if 'afterLoginURL' in session:
                            returnURL = session['afterLoginURL']
                            session.pop('afterLoginURL')
                            session.save()
                        else:
                            # Send to the demo workshop
                            demo = demoLib.getDemo()
                            if not demo:
                                log.info('not demo')
                                returnURL = '/'
                            else:
                                workshop = workshopLib.getWorkshopByCode(demo['workshopCode'])
                                returnURL = '/workshop/%s/%s' %(workshop['urlCode'], workshop['url'])
                        return redirect(returnURL)
                    else:
                        message['type'] = 'error'
                        message['title'] = 'Error: '
                        message['content'] = 'Unknown error in activating %s.' % email
                        log.debug('Commit error on activating %s' % email)
                else:
                    message['type'] = 'error'
                    message['title'] = 'Error: '
                    message['content'] = 'Incorrect activation string given.  Please check link and try again.'
            else:
                message['type'] = ''
                message['title'] = 'Warning: '
                message['content'] = '%s is already marked as active!' % email
        else:
            message['type'] = ''
            message['title'] = 'Error: '
            message['content'] = 'Specified user not found!'
        c.splashMsg = message
        return render('/derived/login.bootstrap')