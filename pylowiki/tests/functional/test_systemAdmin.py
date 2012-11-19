# -*- coding: utf-8 -*-
from pylowiki.tests import *
from routes import url_for
from urlparse import urlparse

from pylowiki.tests.helpers.authorization import login_and_set_user_auth_level, logout
from pylowiki.tests.helpers.registration import create_and_activate_user, create_user, activate_user, login_user

class TestSystemAdminController(TestController):

    user1 = 'test1@civinomics.org'
    pass1 = 'test1'
    zip1 = '94122'
    member1 = 'individual'
    first1 = 'Testing1'
    last1 = 'Home1'
    userName1 = first1 + ' ' + last1
    userName1AdminButton = str.lower(first1) + '-' + str.lower(last1) + '/admin'
    user1AccessLevel = 'admin'

    user2 = 'test2@civinomics.org'
    pass2 = 'test2'
    zip2 = '94122'
    member2 = 'individual'
    first2 = 'Testing2'
    last2 = 'Home2'
    userName2 = first2 + ' ' + last2
    userName2AdminButton = str.lower(first2) + '-' + str.lower(last2) + '/admin'
    user2AccessLevel = 'facilitator'

    user3 = 'test3@civinomics.org'
    pass3 = 'test3'
    zip3 = '94122'
    member3 = 'individual'
    first3 = 'Testing3'
    last3 = 'Home3'
    userName3 = first3 + ' ' + last3
    userName3AdminButton = str.lower(first3) + '-' + str.lower(last3) + '/admin'
    user3AccessLevel = 'user'

    adminEmail = 'username@civinomics.com'
    adminPass = 'password'
    

    def test_view_admin(self):
        # create a user
        create_and_activate_user(
            self, 
            TestSystemAdminController.user1, 
            TestSystemAdminController.pass1, 
            TestSystemAdminController.zip1, 
            TestSystemAdminController.member1,
            TestSystemAdminController.first1, 
            TestSystemAdminController.last1
        )
        # login as an admin, find this new user and set the desired access level 
        adminPrivsRes = login_and_set_user_auth_level(
            self, 
            TestSystemAdminController.adminEmail, 
            TestSystemAdminController.adminPass, 
            TestSystemAdminController.first1, 
            TestSystemAdminController.last1, 
            TestSystemAdminController.user1AccessLevel
        )
        # logout
        logout(self)
        # login as this new user
        login_user(
            self, 
            TestSystemAdminController.user1, 
            TestSystemAdminController.pass1
        )
        # try and view the system admin page as a new admin
        response = self.app.get(
            url=url(controller='systemAdmin', action='index'),
            status=200
        )

        #assert adminPrivsRes.status == '404'
        assert response.status_int == 200

    def test_view_facilitator(self):
        # create a user
        create_and_activate_user(
            self, 
            TestSystemAdminController.user2, 
            TestSystemAdminController.pass2, 
            TestSystemAdminController.zip2, 
            TestSystemAdminController.member2,
            TestSystemAdminController.first2, 
            TestSystemAdminController.last2
        )
        # login as an admin, find this new user and set the desired access level 
        adminPrivsRes = login_and_set_user_auth_level(
            self, 
            TestSystemAdminController.adminEmail, 
            TestSystemAdminController.adminPass, 
            TestSystemAdminController.first2, 
            TestSystemAdminController.last2, 
            TestSystemAdminController.user2AccessLevel
        )
        # logout
        logout(self)
        # login as this new user
        login_user(
            self, 
            TestSystemAdminController.user2, 
            TestSystemAdminController.pass2
        )
        # try and view the system admin page as a new admin, expect a redirect
        response = self.app.get(
           url=url(controller='systemAdmin', action='index'),
           status=302
        )
        assert response.status_int == 302

    def test_view_user(self):
        # create a user
        create_and_activate_user(
            self, 
            TestSystemAdminController.user3, 
            TestSystemAdminController.pass3, 
            TestSystemAdminController.zip3, 
            TestSystemAdminController.member3,
            TestSystemAdminController.first3, 
            TestSystemAdminController.last3
        )
        # login as this new user
        login_user(
            self, 
            TestSystemAdminController.user3, 
            TestSystemAdminController.pass3
        )
        # try and view the system admin page as a new admin, expect a redirect
        response = self.app.get(
           url=url(controller='systemAdmin', action='index'),
           status=302
        )
        assert response.status_int == 302

    def test_view_public(self):
        # make sure no one is logged in
        logout(self)
        # try and view the system admin page as a new admin, expect a redirect
        response = self.app.get(
           url=url(controller='systemAdmin', action='index'),
           status=302
        )
        assert response.status_int == 302