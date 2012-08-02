import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config

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
        c.site_base_url = config['app_conf']['site_base_url']
        c.site_secure_url = config['app_conf']['site_secure_url']
        message = {}
        if user:
            log.info('user exists')
            if int(user['activated']) == 0:
                log.info('user inactive')
                if user['activationHash'] == hash:
                    log.info('hashes match')
                    user['activated'] = 1
                    user['laston'] = time.time()
                    if commit(user):
                        message['type'] = 'success'
                        message['title'] = 'Congratulations!  '
                        message['content'] = '%s, you are now registered!  Please login below.' % email
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
        return render('/derived/splash.bootstrap')