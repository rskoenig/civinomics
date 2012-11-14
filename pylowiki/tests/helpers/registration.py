from pylowiki.tests import *
from routes import url_for
from urlparse import urlparse


def create_user(self, usern, passw, zipc, membert, firstn, lastn):
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
            'firstName': firstn,
            'lastName': lastn,
            'chkTOS': 'true'
        }
    )

    return rReg

def activate_user(self, hash_and_email):
    # Next: activate this user, then visit the home page. 
    # To do this, must make the hash and email available form within lib/user 
    # in lib/user: request.environ['paste.testing_variables']['hash_and_email'] = '%s__%s'%(hash, toEmail)
    rAct = self.app.get(
        url=url_for(controller='activate', action='index', id=hash_and_email)
    )

    return rAct

def create_and_activate_user(self, usern, passw, zipc, membert, firstn, lastn):
    user_created = create_user(self, usern, passw, zipc, membert, firstn, lastn)    
    return activate_user(self, user_created.hash_and_email)

def login_user(self, usern, passw):
    # Now that we've created a user and activated the account, let's login and visit the homepage.
    # get the login form, fill it out and submit
    rLog = self.app.get(url=url_for(controller='login', action='loginDisplay'))
    logForm = rLog.form
    logForm['email'] = usern
    logForm['password'] = passw
    rLogin = logForm.submit()
    return rLogin
