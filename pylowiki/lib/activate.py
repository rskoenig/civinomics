# -*- coding: utf-8 -*-
import logging

from pylons.controllers.util import redirect
from pylons import session, config, request, tmpl_context as c
from decorator import decorator #easy_install decorator   http://pypi.python.org/pypi/decorator
import helpers as h

from pylowiki.model import get_user_by_email, commit
from pylowiki.lib.mail import send

log = logging.getLogger(__name__)

"""Sets the activation state for an account, sends out an email"""
def activateCreate():
    email = request.params["email"]
    user = get_user_by_email(email)
    if user:
        activateHash = user.generateActivationHash()
        user.activationHash = activateHash
        commit(user)

        toEmail = user.email;
        frEmail = c.conf['activation.email']
        url = 'http://www.greenocracy.org:2718/activate/%s__%s'% (activateHash, email)
        #myURL = "%s/%s_%s" % (h.url('/', _qualified = True), activateHash, email)
        subject = "Account Activation"
        message = 'Please click on the following link to activate your account:\n\n%s' % url
        send(toEmail, frEmail, subject, message)
        log.info("Successful account creation (deactivated) for %s" %email)

