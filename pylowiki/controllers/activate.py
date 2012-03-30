import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.model import get_user_by_email, commit
from pylowiki.lib.mail import send

import time

log = logging.getLogger(__name__)

class ActivateController(BaseController):

    def index(self, id):
        hash, sep, email = id.partition('__')
        user = get_user_by_email(email)
        if user:
            log.info('user exists')
            if user.activated == 0:
                log.info('user inactive')
                if user.activationHash == hash:
                    log.info('hashes match')
                    user.activated = 1
                    user.laston = time.time()
                    if commit(user):
                        toEmail = user.email;
                        frEmail = c.conf['contact.email']
                        subject = 'Account Activation - Password'
                        message = 'We have activated your account and set your temporary password to: %s' % user.password
                        #send(toEmail, frEmail, subject, message)
                        return 'Congratulations %s, you are now registered!' % email
                        #session['user'] = user.name
                        #return redirect('/')
                    else:
                        return 'Unknown error in activating %s.' % email
                else:
                    return 'Error: Incorrect activation string given.  Please check link and try again.'
            else:
                return 'Error: %s is already marked as active!' %email
        else:
            return ('User not found!')

