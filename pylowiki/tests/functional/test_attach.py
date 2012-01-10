from pylowiki.tests import *

class TestAttachController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='attach', action='index'))
        # Test response...
