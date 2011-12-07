# -*- coding: utf-8 -*-
from pylowiki.tests import *

class TestActionlistController(TestController):

    def test_index_edit(self):
        response = self.app.get(url(controller='actionlist', action='index', id = "edit" ))
        assert "Which edit?" in response
        # Test response...

    def test_index_delete(self):
        response = self.app.get(url(controller='actionlist', action='index', id = "delete" ))
        assert "Which delete?" in response 
        # Test response...
