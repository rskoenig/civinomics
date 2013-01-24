from pylowiki.tests import *
from routes import url_for
from urlparse import urlparse

from pylowiki.tests.helpers.people import make_user, createActivatedUser

import logging
log = logging.getLogger(__name__)

def activation_success():
    return 'registration complete'

def create_user(self, usern, passw, zipc, membert, name):
    # create a user with normal privs
    rReg = self.app.post(
        url=url_for(controller='register', action='register_handler'),
        params={
            'email': usern,
            'password': passw,
            'password2': passw,
            'postalCode': zipc,
            'country': 'United States',
            'memberType': membert,
            'name': name,
            'chkTOS': 'true'
        }
    )
    assert 'alert-error' not in rReg
    assert 'success' in rReg
    return rReg

# NOTE: check that user is actually activated
# what if you know the hashes for two people, and you switch the hashes?
# what if the hash and email is separated by two underscores?
#  | if the hash is cerated by a hex digest it should only be 0-9 and a-z
# what if two people have the same hash but two different emails?
# takes time as part of seed and rounds to nearest second.. with samename and time, its possible
# for a collision. 
def activate_user(self, hash_and_email):
    # Next: activate this user, then visit the home page. 
    # To do this, must make the hash and email available form within lib/user 
    # in lib/user: request.environ['paste.testing_variables']['hash_and_email'] = '%s__%s'%(hash, toEmail)
    rAct = self.app.get(
        url=url_for(controller='activate', action='index', id=hash_and_email)
    )
    rNext = rAct.follow()
    assert activation_success() in rNext
    return rNext

# is there a need
def create_and_activate_a_user(self, **who):
    if not who:
        thisUser = make_user()
         #thisUser = createActivatedUser()
    else:
        thisUser = make_user(**who)
         #thisUser = createActivatedUser(**who)
    user_created = create_user(self, thisUser['email'], thisUser['password'], thisUser['zip'], thisUser['memberType'], thisUser['name'])
    log.info('created ' + thisUser['email'])
    user_activated = activate_user(self, user_created.hash_and_email)

    return thisUser

def create_and_activate_user(self, usern, passw, zipc, membert, name):
    user_created = create_user(self, usern, passw, zipc, membert, name)
    return activate_user(self, user_created.hash_and_email)
