from pylowiki.tests import *
from routes import url_for
from urlparse import urlparse

from pylowiki.tests.helpers.people import make_user
import pylowiki.tests.helpers.content as content

import logging
log = logging.getLogger(__name__)

def create_user(self, usern, passw, postal, membert, name):
    # create a user with normal privs
    rReg = self.app.post(
        url=url_for(controller='register', action='signupHandler'),
        params={
            'email': usern,
            'password': passw,
            'password2': passw,
            'postalCode': postal,
            'country': 'United States',
            'memberType': membert,
            'name': name,
            'chkTOS': 'true'
        }
    ).follow()
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
    # rACt is a 302 redirect from the home page
    rNext = rAct.follow()
    # rNext is a 302 redirect from the workshops page
    rThen = rNext.follow()
    # rThen is the workshop listing page
    assert content.activation_success() in rThen
    return rNext

def create_and_activate_a_user(self, **who):
    """Creates a user and sets access level. kwargs is used for any desired settings 
    otherwise basic defaults are assumed"""
    #: create a user object
    if not who:
        thisUser = make_user()
    else:
        thisUser = make_user(**who)
    #: use the site's signup page to register this user
    user_created = create_user(self, thisUser['email'], thisUser['password'], thisUser['postal'], thisUser['memberType'], thisUser['name'])
    #user_activated = activate_user(self, user_created.hash_and_email)
    from pylowiki.lib.db.user import getUserByEmail
    u = getUserByEmail(thisUser['email'])
    #: activate the user
    u['accessLevel'] = thisUser['accessLevel']
    u['activated'] = '1'
    u['disabled'] = '0'
    from pylowiki.lib.db.dbHelpers import commit
    commit(u)
    #: return user object for use by test function
    return thisUser

def create_and_activate_user(self, usern, passw, postal, membert, name):
    user_created = create_user(self, usern, passw, postal, membert, name)
    return activate_user(self, user_created.hash_and_email)
