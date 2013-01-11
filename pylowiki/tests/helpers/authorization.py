# -*- coding: utf-8 -*-
from pylowiki.tests import *
from routes import url_for
from urlparse import urlparse

from pylowiki.lib.db.user import getUserByEmail

from pylowiki.tests.helpers.people import get_test_admin


##############################################
# CONSTANTS 
##############################################

def get_adminAction():
    return 'index'

def get_adminController():
    return 'systemAdmin'

def find_active_users():
    return 'Show Active Users'

def hosted_account_info_form():
    return 'userAccount'

def make_user_full_name(thisUser):
    return thisUser['name']

def find_access_privelages_form():
    return 'userPrivs'

def select_num_objects_name():
    return 'numHost'


##############################################
# FUNCTIONS 
##############################################

####################################
# login
#   login as this user
####################################
def login(self, thisUser):
    # get the login form, fill it out and submit
    rLog = self.app.get(url=url_for(controller='login', action='loginDisplay'))
    logForm = rLog.form
    logForm['email'] = thisUser['email']
    logForm['password'] = thisUser['password']
    #logForm['password'] = 'badpassword'
    rLogin = logForm.submit()
    assert 'error' not in rLogin
    assert rLogin.status_int == 302
    return rLogin.follow()

####################################
# logout
#   logout of the current session
####################################
def logout(self):
    response = self.app.get(
        url=url(controller='login', action='logout'),
        status=302
    )

# login, visit this user's page, set to desired authentication level
def login_and_set_user_auth_level(self, adminEmail, adminPass, firstName, lastName, authLevel):

    displayActiveUsers = find_active_users()
    usersName = make_user_full_name(firstName, lastName)
    adminButton = find_user_admin_button(firstName, lastName)

    authNameDict = {
        'user' : 'setPrivsUser',
        'facilitator' : 'setPrivsFacil',
        'admin' : 'setPrivsAdmin'
    }
    authValDict = {
        'user' : '0',
        'facilitator' : '100',
        'admin' : '200'
    }

    # login as an admin
    login = login_user(self, adminEmail, adminPass)
    # go to the desired admin page (workshops here)
    adminPage = self.app.get(url=url_for(controller=get_adminController(), action=get_adminAction()))
    # click the tab for displaying active users
    listActiveUsers = adminPage.click(description=displayActiveUsers, verbose=True)
    # click the name of the new user
    profilePage = listActiveUsers.click(description=usersName, index=0, verbose=True)
    # click the admin button on this user's page
    adminUser = profilePage.click(href=adminButton, verbose=True)
    
    # get the form we went, there are multiple forms so this gets all forms
    adminForms = adminUser.forms
    adminPrivsForm = adminForms[find_access_privelages_form()]
    adminPrivsForm.select(authNameDict[authLevel], authValDict[authLevel])
    adminPrivsForm['changeAccessReason'] = 'testing'
    # submit
    adminPrivsRes = adminPrivsForm.submit().follow()

    return adminPrivsRes

def login_and_view_user_admin_page(self, loginAs, viewUser):
    
    displayActiveUsers = find_active_users()
    usersName = make_user_full_name(viewUser)
    
    # user administration button not currently available in the ui
    # adminButton = find_user_admin_button(viewUser)

    # login as an admin
    login(self, loginAs)
    # go to the desired admin page (workshops here)
    adminPage = self.app.get(url=url_for(controller=get_adminController(), action=get_adminAction()))
    # click the tab for displaying active users
    listActiveUsers = adminPage.click(description=displayActiveUsers, verbose=True)
     #assert listActiveUsers == '404'
    # click the name of the new user
    profilePage = listActiveUsers.click(description=usersName, index=0, verbose=True)
    # click the admin button on this user's page
    # doesn't work like this for now:
    #adminUser = profilePage.click(href=adminButton, verbose=True)
    # so instead we add /admin to the request url
    userAdminView = self.app.get(url=profilePage.request.url + profile_admin_url())

    # return a view of this user's admin page
    return userAdminView

####################################
# update_hosted_accounts
#   - login as an admin
#   - view user's administration page
#   - load the forms, load the hosted accounts info form
#   - set the number of hosted accounts for the user
#   - submit, follow, confirm success
#   - logout as admin
####################################
def update_hosted_accounts(self, thisUser, howMany=3):
    testAdmin = get_test_admin()
    user_admin_page = login_and_view_user_admin_page(
            self, 
            testAdmin, 
            thisUser
        )
        
    # obtain the form for changing # of hosted accounts for the user
    admin_page_forms = user_admin_page.forms
    admin_page_account_form = admin_page_forms[hosted_account_info_form()]
    
    # change this number and submit the form
    admin_page_account_form.set(
        select_num_objects_name(), 
        howMany
    )
        
    hosted_accounts_updated = admin_page_account_form.submit().follow()
        
    # we should see success by noting the page now states this many hosted accounts are now hosted.
    assert "Total hosting for account: " + str(howMany) in hosted_accounts_updated
    assert "Number of objects which may be hosted:" not in hosted_accounts_updated
    logout(self)