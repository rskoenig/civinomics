# -*- coding: utf-8 -*-
from pylowiki.tests import *
from routes import url_for
from urlparse import urlparse

from pylowiki.tests.helpers.registration import login_user

def find_active_users():
    return 'Show Active Users'

def make_user_full_name(firstName, lastName):
    return firstName + ' ' + lastName

def find_user_admin_button(firstName, lastName):
    return str.lower(firstName) + '-' + str.lower(lastName) + '/admin'

def find_access_privelages_form():
    return 'userPrivs'

def login_and_set_user_auth_level(self, adminEmail, adminPass, adminController, adminAction, firstName, lastName, authLevel):

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
    adminPage = self.app.get(url=url_for(controller=adminController, action=adminAction))
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

def login_and_view_user_admin_page(self, adminEmail, adminPass, adminController, adminAction, firstName, lastName):
    
    displayActiveUsers = find_active_users()
    usersName = make_user_full_name(firstName, lastName)
    adminButton = find_user_admin_button(firstName, lastName)

    # login as an admin
    login = login_user(self, adminEmail, adminPass)
    # go to the desired admin page (workshops here)
    adminPage = self.app.get(url=url_for(controller=adminController, action=adminAction))
    # click the tab for displaying active users
    listActiveUsers = adminPage.click(description=displayActiveUsers, verbose=True)
    # click the name of the new user
    profilePage = listActiveUsers.click(description=usersName, index=0, verbose=True)
    # click the admin button on this user's page
    adminUser = profilePage.click(href=adminButton, verbose=True)

    # return a view of this user's admin page
    return adminUser

def logout(self):
    response = self.app.get(
        url=url(controller='login', action='logout'),
        status=302
    )
