# -*- coding: utf-8 -*-
from pylowiki.tests import *

class TestSearchController(TestController):

    def test_login_form(self):
        response = self.app.get(url(controller='login', action='index' ))
        assert "Login" in response

    def test_correct_login(self):
        response = self.app.post(
            url=url(controller='login', action='index'),
            params={
                'username': 'admin',
                'password': 'pass'
            },
            status=302
        )

    def test_incorrect_login(self):
        response = self.app.post(
            url=url(controller='login', action='index'),
            params={
                'username': 'admin',
                'password': '!pass'
            }
        )
        assert "incorrect username or password" in response
