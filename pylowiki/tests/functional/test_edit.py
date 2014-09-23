# -*- coding: utf-8 -*-
from pylowiki.tests import *

class TestCreateController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='edit', action='index'))
        # Test response...
