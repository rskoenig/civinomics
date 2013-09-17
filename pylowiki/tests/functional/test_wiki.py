# -*- coding: utf-8 -*-
from pylowiki.tests import *

class TestSearchController(TestController):

    

    def test_index(self):
        #pass
        response = self.app.get(url(controller='wiki', action='index', id = 'home'))
        assert "home" in response 
