import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

#from pylowiki.model import get_user_by_email, commit
from pylowiki.lib.db.user import getUserByEmail as get_user_by_email
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.mail import send

import time

log = logging.getLogger(__name__)

class ActivateController(BaseController):

    def index(self, id):
        hash, sep, email = id.partition('__')
        user = get_user_by_email(email)
        message = {}
        if user:
            log.info('user exists')
            if user['activated'] == '0':
                log.info('user inactive')
                if user['activationHash'] == hash:
                    log.info('hashes match')
                    user['activated'] = '1'
                    user['laston'] = time.time()
                    if commit(user):
                        session["user"] = user['name']
                        session["userCode"] = user['urlCode']
                        session["userURL"] = user['url']
                        alert = {'type':'success'}
                        alert['title'] = 'Welcome to Civinomics! Please feel free to explore!'
                        session['alert'] = alert
                        session.save()
                        c.authuser = user
                        returnURL = "/"
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