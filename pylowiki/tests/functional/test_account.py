# -*- coding: utf-8 -*-
from pylowiki.tests import *

from pylowiki.tests.helpers.authorization import login_and_set_user_auth_level, login_and_view_user_admin_page, logout
from pylowiki.tests.helpers.registration import create_and_activate_user, login_user

# need to parse a url
import re

class TestAccountController(TestController): 

    user1 = 'test1@civinomics.org'
    pass1 = 'test1'
    zip1 = '94122'
    member1 = 'individual'
    first1 = 'Testing1'
    last1 = 'Home1'
    userName1 = first1 + ' ' + last1
    userName1AdminButton = str.lower(first1) + '-' + str.lower(last1) + '/admin'
    user1AccessLevel = 'user'

    user2 = 'test2@civinomics.org'
    pass2 = 'test2'
    zip2 = '94122'
    member2 = 'individual'
    first2 = 'Testing2'
    last2 = 'Home2'
    userName2 = first2 + ' ' + last2
    userName2AdminButton = str.lower(first2) + '-' + str.lower(last2) + '/admin'
    user2AccessLevel = 'facilitator'

    adminEmail = 'username@civinomics.com'
    adminPass = 'password'
    adminController = 'systemAdmin'
    adminAction = 'index'
    displayActiveUsers = 'Show Active Users'
    accessControls = 'Access Controls'

    find_account_info_form = 'userAccount'
    select_num_objects_name = 'numHost'
    num_objects_to_host = '3'

    def test_change_hosted_accounts_admin(self):
        # create a user
        create_and_activate_user(self, TestAccountController.user1, TestAccountController.pass1, TestAccountController.zip1, TestAccountController.member1,TestAccountController.first1, TestAccountController.last1)
        # login as an admin, find this new user and look at their admin page
        user_admin_page = login_and_view_user_admin_page(self, TestAccountController.adminEmail, TestAccountController.adminPass, TestAccountController.adminController, TestAccountController.adminAction, TestAccountController.first1, TestAccountController.last1)
        # obtain the form for changing # of hosted accounts for the user
        admin_page_forms = user_admin_page.forms
        admin_page_account_form = admin_page_forms[TestAccountController.find_account_info_form]
        # change this number and submit the form
        admin_page_account_form.set(TestAccountController.select_num_objects_name, TestAccountController.num_objects_to_host)
        hosted_accounts_updated = admin_page_account_form.submit().follow()
        # we should see success by noting the page now states this many hosted accounts are now hosted.
        assert "Total hosting for account: " + TestAccountController.num_objects_to_host in hosted_accounts_updated
    
    def test_change_hosted_accounts_facilitator(self):
        # create a user
        create_and_activate_user(self, TestAccountController.user2, TestAccountController.pass2, TestAccountController.zip2, TestAccountController.member2,TestAccountController.first2, TestAccountController.last2)
        # set this user's access level to facilitator
        adminPrivsRes = login_and_set_user_auth_level(self, TestAccountController.adminEmail, TestAccountController.adminPass, TestAccountController.adminController, TestAccountController.adminAction, TestAccountController.first2, TestAccountController.last2, TestAccountController.user2AccessLevel)
        # logout
        logout(self)
        # login as this new user
        login = login_user(self, TestAccountController.user2, TestAccountController.pass2)
        # visit my profile page and obtain code/name
        landing_page = self.app.get(url=url(controller='actionlist', action='index', id='sitemapIssues'))
        profile_page = landing_page.click("Profile")
        # profile_page.request.url == http://localhost/profile/4ICk/testing2-home2
        profile_url = profile_page.request.url
        pile = profile_url.split('/')
        name_index = len(pile)-1
        code_index = len(pile)-2
        this_name = pile[name_index]
        this_code = pile[code_index]
        # use this along with spoofed form data and send at the handler 
        response = self.app.post(
            url=url(controller='account', action='accountAdminHandler', id1=this_code, id2=this_name), 
            params={
                'numHost' : '3'
            }
        )
        landing = response.follow()
        assert "Total hosting for account: " + TestAccountController.num_objects_to_host not in landing
        assert landing.status_int == 302