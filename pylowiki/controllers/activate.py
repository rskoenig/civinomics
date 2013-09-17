import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.mail import send
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.demo         as demoLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.mail            as mailLib

import time

log = logging.getLogger(__name__)

class ActivateController(BaseController):

    def index(self, id):
        hash, sep, email = id.partition('__')
        user = userLib.getUserByEmail(email)
        splashMsg = {}
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
                        mailLib.sendWelcomeMail(user)
                        if 'afterLoginURL' in session:
                            returnURL = session['afterLoginURL']
                            session.pop('afterLoginURL')
                            session.save()
                        else:
                            # Send to the demo workshop
                            #demo = demoLib.getDemo()
                            #if not demo:
                                #log.info('not demo')
                                #returnURL = '/'
                            #else:
                                #returnURL = '/workshop/%s/%s#guider=tour_welcome' %(demo['urlCode'], demo['url'])
                            returnURL = '/'
                        return redirect(returnURL)
                    else:
                        splashMsg['type'] = 'error'
                        splashMsg['title'] = 'Error: '
                        splashMsg['content'] = 'Unknown error in activating %s.' % email
                        log.debug('Commit error on activating %s' % email)
                else:
                    splashMsg['type'] = 'error'
                    splashMsg['title'] = 'Error: '
                    splashMsg['content'] = 'Incorrect activation string given.  Please check link and try again.'
                    log.debug('User %s provided an incorrect activation string.' % email)
            else:
                splashMsg['type'] = ''
                splashMsg['title'] = 'Warning: '
                splashMsg['content'] = '%s is already marked as active! Please use the form to login.' % email
                log.debug('User %s attempted to activate an active account.' % email)
        else:
            splashMsg['type'] = ''
            splashMsg['title'] = 'Error: '
            splashMsg['content'] = 'Specified user not found!'
            log.debug('User %s not found' % email)
        session['splashMsg'] = splashMsg
        session.save()
        return redirect('/login')