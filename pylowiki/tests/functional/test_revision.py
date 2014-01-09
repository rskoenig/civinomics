# -*- coding: utf-8 -*-
from pylowiki.tests import *

class TestSearchController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='revision', action='index'))
        # Test response...
