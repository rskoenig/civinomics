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
    user1AccessLevel = 'user'

    user2 = 'test2@civinomics.org'
    pass2 = 'test2'
    zip2 = '94122'
    member2 = 'individual'
    first2 = 'Testing2'
    last2 = 'Home2'
    user2AccessLevel = 'facilitator'

    user3 = 'test3@civinomics.org'
    pass3 = 'test3'
    zip3 = '94122'
    member3 = 'individual'
    first3 = 'Testing3'
    last3 = 'Home3'
    user3AccessLevel = 'admin'

    user4 = 'test4@civinomics.org'
    pass4 = 'test4'
    zip4 = '94122'
    member4 = 'individual'
    first4 = 'Testing4'
    last4 = 'Home4'

    user5 = 'test5@civinomics.org'
    pass5 = 'test5'
    zip5 = '94122'
    member5 = 'individual'
    first5 = 'Testing5'
    last5 = 'Home5'

    adminEmail = 'username@civinomics.com'
    adminPass = 'password'

    find_account_info_form = 'userAccount'
    select_num_objects_name = 'numHost'
    num_objects_to_host = '3'

    # This test will create a user then log in as an admin and view this user's account admin page. Then we will 
    # use the hosted accounts form to update their hosted account number and confirm that it worked on the resulting page.
    def test_change_hosted_accounts_admin(self):
        # create a user
        create_and_activate_user(
            self, 
            TestAccountController.user1, 
            TestAccountController.pass1, 
            TestAccountController.zip1, 
            TestAccountController.member1, 
            TestAccountController.first1, 
            TestAccountController.last1
        )
        # login as an admin, find this new user and look at their admin page
        user_admin_page = login_and_view_user_admin_page(
            self, 
            TestAccountController.adminEmail, 
            TestAccountController.adminPass, 
            TestAccountController.first1, 
            TestAccountController.last1
        )
        # obtain the form for changing # of hosted accounts for the user
        admin_page_forms = user_admin_page.forms
        admin_page_account_form = admin_page_forms[TestAccountController.find_account_info_form]
        # change this number and submit the form
        admin_page_account_form.set(
            TestAccountController.select_num_objects_name, 
            TestAccountController.num_objects_to_host
        )
        hosted_accounts_updated = admin_page_account_form.submit().follow()
        # we should see success by noting the page now states this many hosted accounts are now hosted.
        assert "Total hosting for account: " + TestAccountController.num_objects_to_host in hosted_accounts_updated
        assert "Number of objects which may be hosted:" not in hosted_accounts_updated
    
    # This test will have a facilitator try to spoof the hosted account handler, telling it to update 
    # the hosted accounts object. After doing this, we log in as an admin and take a look at this user's account
    # admin page. The assertions at the end of this function explain what we should and should not see.
    def test_change_hosted_accounts_facilitator(self):
        # clear session
        logout(self)
        # create a user
        create_and_activate_user(self, 
            TestAccountController.user2, 
            TestAccountController.pass2, 
            TestAccountController.zip2, 
            TestAccountController.member2, 
            TestAccountController.first2, 
            TestAccountController.last2
        )
        # set this user's access level to facilitator
        adminPrivsRes = login_and_set_user_auth_level(
            self, 
            TestAccountController.adminEmail, 
            TestAccountController.adminPass, 
            TestAccountController.first2, 
            TestAccountController.last2, 
            TestAccountController.user2AccessLevel
        )
        # logout
        logout(self)
        # login as this new user
        login = login_user(
            self, 
            TestAccountController.user2, 
            TestAccountController.pass2
        )
        # visit the profile page and obtain code/name
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
                TestAccountController.select_num_objects_name : TestAccountController.num_objects_to_host
            }
        )
        landing = response.follow()
        # if it works, the database will reflect this new numHost value. login as admin and take a look
        logout(self)
        user_admin_page = login_and_view_user_admin_page(
            self, 
            TestAccountController.adminEmail, 
            TestAccountController.adminPass, 
            TestAccountController.first2, 
            TestAccountController.last2
        )
        # since this was a facilitator trying to set hosting accounts, this should not have gone through.
        # Therefore, the previous test string will not be there and instead the one that prints when no 
        # hosted accounts are set will be:

        assert "Number of objects which may be hosted:" in user_admin_page
        assert "Total hosting for account: " + TestAccountController.num_objects_to_host not in user_admin_page
        assert user_admin_page.status_int == 200

    # This test will confirm the previous one would have worked if the user would have been set as an admin. This user 
    # sends the same post at the hosted account handler, telling it to update the hosted accounts object.
    # After doing this, we log in as an admin and take a look at this user's account
    # admin page. The assertions at the end of this function are opposite of the previous test.
    def test_change_hosted_accounts_new_admin(self):
        # clear session
        logout(self)
        # create a user
        create_and_activate_user(self, 
            TestAccountController.user3, 
            TestAccountController.pass3, 
            TestAccountController.zip3, 
            TestAccountController.member3, 
            TestAccountController.first3, 
            TestAccountController.last3
        )
        # set this user's access level to facilitator
        adminPrivsRes = login_and_set_user_auth_level(
            self, 
            TestAccountController.adminEmail, 
            TestAccountController.adminPass, 
            TestAccountController.first3, 
            TestAccountController.last3, 
            TestAccountController.user3AccessLevel
        )
        # logout
        logout(self)
        # login as this new user
        login = login_user(
            self, 
            TestAccountController.user3, 
            TestAccountController.pass3
        )
        # visit the profile page and obtain code/name
        landing_page = self.app.get(url=url(controller='actionlist', action='index', id='sitemapIssues'))
        profile_page = landing_page.click("Profile")
        # profile_page.request.url == http://localhost/profile/4ICk/testing3-home3
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
                TestAccountController.select_num_objects_name : TestAccountController.num_objects_to_host
            }
        )
        landing = response.follow()
        # if it works, the database will reflect this new numHost value. login as admin and take a look
        logout(self)
        user_admin_page = login_and_view_user_admin_page(
            self, 
            TestAccountController.adminEmail, 
            TestAccountController.adminPass, 
            TestAccountController.first3, 
            TestAccountController.last3
        )
        # since this was a facilitator trying to set hosting accounts, this should not have gone through.
        # Therefore, the previous test string will not be there and instead the one that prints when no 
        # hosted accounts are set will be:

        assert "Number of objects which may be hosted:" not in user_admin_page
        assert "Total hosting for account: " + TestAccountController.num_objects_to_host in user_admin_page
        assert user_admin_page.status_int == 200

    # This test will have a user try to spoof the hosted account handler, telling it to update 
    # the hosted accounts object. After doing this, we log in as an admin and take a look at this user's account
    # admin page. The assertions at the end of this function explain what we should and should not see.
    def test_change_hosted_accounts_user(self):
        # clear session
        logout(self)
        # create a user
        create_and_activate_user(self, 
            TestAccountController.user4, 
            TestAccountController.pass4, 
            TestAccountController.zip4, 
            TestAccountController.member4, 
            TestAccountController.first4, 
            TestAccountController.last4
        )
        # login as this new user
        login = login_user(
            self, 
            TestAccountController.user4, 
            TestAccountController.pass4
        )
        # visit the profile page and obtain code/name
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
                TestAccountController.select_num_objects_name : TestAccountController.num_objects_to_host
            }
        )
        landing = response.follow()
        # if it works, the database will reflect this new numHost value. login as admin and take a look
        logout(self)
        user_admin_page = login_and_view_user_admin_page(
            self, 
            TestAccountController.adminEmail, 
            TestAccountController.adminPass, 
            TestAccountController.first4, 
            TestAccountController.last4
        )
        # since this was a facilitator trying to set hosting accounts, this should not have gone through.
        # Therefore, the previous test string will not be there and instead the one that prints when no 
        # hosted accounts are set will be:

        assert "Number of objects which may be hosted:" in user_admin_page
        assert "Total hosting for account: " + TestAccountController.num_objects_to_host not in user_admin_page
        assert user_admin_page.status_int == 200

    # This test will have a public visitor try to spoof the hosted account handler, telling it to update 
    # a user's hosted accounts object. After doing this, we log in as an admin and take a look at this user's account
    # admin page. The assertions at the end of this function explain what we should and should not see.
    def test_change_hosted_accounts_public(self):
        # clear session
        logout(self)
        # create a user
        create_and_activate_user(self, 
            TestAccountController.user5, 
            TestAccountController.pass5, 
            TestAccountController.zip5, 
            TestAccountController.member5, 
            TestAccountController.first5, 
            TestAccountController.last5
        )
        # login as this new user
        login = login_user(
            self, 
            TestAccountController.user5, 
            TestAccountController.pass5
        )
        # visit the profile page and obtain code/name
        landing_page = self.app.get(url=url(controller='actionlist', action='index', id='sitemapIssues'))
        profile_page = landing_page.click("Profile")
        # profile_page.request.url == http://localhost/profile/4ICk/testing5-home5
        profile_url = profile_page.request.url
        pile = profile_url.split('/')
        name_index = len(pile)-1
        code_index = len(pile)-2
        this_name = pile[name_index]
        this_code = pile[code_index]
        # clear session - public test
        logout(self)
        # use this along with spoofed form data and send at the handler 
        response = self.app.post(
            url=url(controller='account', action='accountAdminHandler', id1=this_code, id2=this_name), 
            params={
                TestAccountController.select_num_objects_name : TestAccountController.num_objects_to_host
            }
        )
        landing = response.follow()
        # login as admin and take a look at the user's page to see if the post worked
        user_admin_page = login_and_view_user_admin_page(
            self, 
            TestAccountController.adminEmail, 
            TestAccountController.adminPass, 
            TestAccountController.first5, 
            TestAccountController.last5
        )
        # since this was a facilitator trying to set hosting accounts, this should not have gone through.
        # Therefore, the previous test string will not be there and instead the one that prints when no 
        # hosted accounts are set will be:

        assert "Number of objects which may be hosted:" in user_admin_page
        assert "Total hosting for account: " + TestAccountController.num_objects_to_host not in user_admin_page
        assert user_admin_page.status_int == 200