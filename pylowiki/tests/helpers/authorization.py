# -*- coding: utf-8 -*-
from pylowiki.tests import *
from routes import url_for
from urlparse import urlparse

from pylowiki.tests.helpers.registration import login_user


def login_and_set_user_auth_level(self, adminEmail, adminPass, adminController, adminAction, firstName, lastName, authLevel):

    displayActiveUsers = 'Show Active Users'
    usersName = firstName + ' ' + lastName
    adminButton = str.lower(firstName) + '-' + str.lower(lastName) + '/admin'
    accessPrivsForm = 'userPrivs'

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
    # rAdmin = login_and_set_user_auth_level(self, TestSurveyController.adminEmail, TestSurveyController.adminPass, TestSurveyController.adminController, TestSurveyController.adminAction, TestSurveyController.userName1, TestSurveyController.facilitatorButton)
    login = login_user(self, adminEmail, adminPass)
    # go to the desired admin page (workshops here)
    adminPage = self.app.get(url=url_for(controller=adminController, action=adminAction))
    # click the tab for displaying active users
    listActiveUsers = adminPage.click(description=displayActiveUsers, verbose=True)
    # click the name of the new user
    profilePage = listActiveUsers.click(description=usersName, index=0, verbose=True)
    # click the admin button on this user's page
    # adminUser = rProfilePage.click(description=TestSurveyController.adminButton, verbose=True)
    adminUser = profilePage.click(href=adminButton, verbose=True)
    
    #assert adminUser.status == '404'
    # get the form we went, there are multiple forms so this gets all forms
    adminForms = adminUser.forms
    adminPrivsForm = adminForms[accessPrivsForm]
     #adminPrivsForm.select('setPrivsAdmin', '200')
    adminPrivsForm.select(authNameDict[authLevel], authValDict[authLevel])
    adminPrivsForm['changeAccessReason'] = 'testing'
    # submit
    adminPrivsRes = adminPrivsForm.submit().follow()

    return adminPrivsRes

def logout(self):
    response = self.app.get(
        url=url(controller='login', action='logout'),
        status=302
    )
