from pylowiki.tests import *

class TestContactController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='contact', action='index'))
        # Test response...
