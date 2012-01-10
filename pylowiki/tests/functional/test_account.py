# -*- coding: utf-8 -*-
from pylowiki.tests import *

class TestAccountController(TestController): 

    def test_account(self):
        response = self.app.post(
            url=url(controller='login', action='index'),
            params={
                'username': 'admin',
                'password': 'pass'
            }
        )
        
        response = self.app.get(url(controller='account', action='index' ))
        assert "Accounts" in response

    def test_user_account_(self):
        response = self.app.post(
            url=url(controller='login', action='index'),
            params={
                'username': 'admin',
                'password': 'pass'
            }
        )

        response = self.app.get(url( controller='account', action='user', id='admin' ))
        assert "stats" in response
        assert "events" in response
